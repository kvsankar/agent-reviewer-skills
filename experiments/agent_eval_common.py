#!/usr/bin/env python3
"""Shared helpers for disposable, non-interactive agent evaluations."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

from experiment_runner import extract_findings
from run_ollama import build_condition_prompt, safe_model_name


DEFAULT_SKILL = Path(__file__).parent.parent / "python-rhodes-reviewer" / "SKILL.md"

AGENT_TASK = """Review the repository in your current working directory.

Explore it with the available read-only tools before answering. Focus on concrete
quality, design, maintainability, and correctness problems in the code. Do not
modify files. For every finding, include a short mnemonic, the file and relevant
line or symbol, the problematic code, a suggested improvement, and why it
matters. Return only the final review in structured Markdown.
"""


def copy_repo(source: Path, destination: Path) -> None:
    """Copy an evaluation repository without VCS or benchmark answer files."""
    if not source.is_dir():
        raise ValueError(f"Repository does not exist: {source}")
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(
            ".git",
            ".hg",
            ".svn",
            "__pycache__",
            ".pytest_cache",
            "ground-truth*",
        ),
    )


def file_snapshot(root: Path) -> dict[str, str]:
    """Hash regular files so a supposedly read-only run can be audited."""
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            result[str(path.relative_to(root))] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    return result


def snapshot_delta(before: dict[str, str], after: dict[str, str]) -> dict[str, list[str]]:
    """Describe created, removed, and changed files between two snapshots."""
    return {
        "created": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "changed": sorted(
            path for path in before.keys() & after.keys() if before[path] != after[path]
        ),
    }


def extract_text(content: object) -> str:
    """Extract text from common agent message content representations."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for block in content:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict) and block.get("type") in {"text", "output_text"}:
            text = block.get("text")
            if isinstance(text, str):
                parts.append(text)
    return "\n".join(parts)


def parse_pi_jsonl(raw: str) -> dict:
    """Summarize Pi's JSON event stream and recover the final assistant text."""
    events: list[dict] = []
    malformed: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            malformed.append(line[:500])
            continue
        if isinstance(event, dict):
            events.append(event)

    assistant_messages: list[str] = []
    tool_calls: list[dict] = []
    tool_errors = 0
    for event in events:
        if event.get("type") == "message_end":
            message = event.get("message", {})
            if message.get("role") == "assistant":
                text = extract_text(message.get("content"))
                if text:
                    assistant_messages.append(text)
        elif event.get("type") == "tool_execution_start":
            tool_calls.append(
                {
                    "id": event.get("toolCallId"),
                    "name": event.get("toolName"),
                    "args": event.get("args"),
                }
            )
        elif event.get("type") == "tool_execution_end" and event.get("isError"):
            tool_errors += 1

    output = assistant_messages[-1] if assistant_messages else ""
    return {
        "output": output,
        "events": events,
        "event_count": len(events),
        "malformed_lines": malformed,
        "tool_calls": tool_calls,
        "tool_call_count": len(tool_calls),
        "tool_error_count": tool_errors,
        "findings": extract_findings(output),
        "findings_count": len(extract_findings(output)),
    }


def parse_codex_jsonl(raw: str) -> dict:
    """Summarize Codex exec JSONL without depending on one CLI event version."""
    events: list[dict] = []
    malformed: list[str] = []
    final_candidates: list[str] = []
    tool_calls_by_id: dict[str, dict] = {}
    tool_errors = 0

    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            malformed.append(line[:500])
            continue
        if not isinstance(event, dict):
            continue
        events.append(event)
        item = event.get("item")
        if isinstance(item, dict):
            item_type = str(item.get("type", ""))
            if item_type in {"agent_message", "message"}:
                text = item.get("text") or extract_text(item.get("content"))
                if isinstance(text, str) and text:
                    final_candidates.append(text)
            if item_type in {
                "command_execution",
                "mcp_tool_call",
                "web_search",
                "file_change",
            }:
                item_id = str(item.get("id") or f"event-{len(events)}")
                tool_calls_by_id[item_id] = item
                if item.get("status") == "failed":
                    tool_errors += 1
        message = event.get("message")
        if isinstance(message, dict) and message.get("role") == "assistant":
            text = extract_text(message.get("content"))
            if text:
                final_candidates.append(text)

    output = final_candidates[-1] if final_candidates else ""
    findings = extract_findings(output)
    tool_calls = list(tool_calls_by_id.values())
    return {
        "output": output,
        "events": events,
        "event_count": len(events),
        "malformed_lines": malformed,
        "tool_calls": tool_calls,
        "tool_call_count": len(tool_calls),
        "tool_error_count": tool_errors,
        "findings": findings,
        "findings_count": len(findings),
    }


def compact_jsonl(raw: str) -> str:
    """Drop high-volume incremental events while retaining replayable outcomes."""
    omitted = {"message_update", "tool_execution_update"}
    lines: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            lines.append(line)
            continue
        if isinstance(event, dict) and event.get("type") in omitted:
            continue
        lines.append(json.dumps(event, separators=(",", ":")))
    return "\n".join(lines) + ("\n" if lines else "")


def command_version(binary: str) -> str:
    """Return a CLI version string without making runner startup fragile."""
    import subprocess

    try:
        completed = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except OSError as exc:
        return f"unavailable: {exc}"
    return (completed.stdout or completed.stderr).strip()


def git_source_metadata(source: Path) -> dict[str, str]:
    """Validate a clean Git source and return its immutable identity."""
    import subprocess

    location = source if source.is_dir() else source.parent

    def git(*args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(location), *args],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if completed.returncode != 0:
            raise ValueError(
                f"Evaluation source must be in a Git checkout: {source} "
                f"({completed.stderr.strip()})"
            )
        return completed.stdout.strip()

    root = git("rev-parse", "--show-toplevel")
    commit = git("rev-parse", "HEAD")
    remote = git("remote", "get-url", "origin")
    dirty = git("status", "--porcelain")
    if dirty:
        raise ValueError(
            f"Evaluation source must be an immutable clean revision: {root}\n{dirty}"
        )
    return {"repository_root": root, "upstream": remote, "commit": commit}


def write_agent_run(
    *,
    output_root: Path,
    subject: str,
    model: str,
    condition: str,
    run_number: int,
    instructions: str,
    result: dict,
    transcript: str,
) -> Path:
    """Persist one agent run in the same review layout as direct-model runs."""
    run_dir = output_root / subject / safe_model_name(model) / condition
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "prompt.md").write_text(instructions, encoding="utf-8")
    (run_dir / f"run-{run_number}-review.md").write_text(
        result.get("output", ""), encoding="utf-8"
    )
    (run_dir / f"run-{run_number}-events.jsonl").write_text(
        compact_jsonl(transcript), encoding="utf-8"
    )
    serializable = {key: value for key, value in result.items() if key != "events"}
    (run_dir / f"run-{run_number}.json").write_text(
        json.dumps(serializable, indent=2), encoding="utf-8"
    )
    return run_dir


def condition_instructions(condition: str, skill: Path) -> str:
    """Expose the shared controlled prompt generator under a clearer name."""
    return build_condition_prompt(condition, skill)


def safe_condition(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9-]+", value):
        raise ValueError(f"Unsafe condition name: {value}")
    return value
