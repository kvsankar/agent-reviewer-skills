#!/usr/bin/env python3
"""Generate one source-aware Claude seed review from a real repository."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path

from agent_eval_common import (
    DEFAULT_SKILL,
    command_version,
    copy_repo,
    file_snapshot,
    git_source_metadata,
    snapshot_delta,
)
from run_ollama import build_condition_prompt, safe_model_name


BASELINE_SCHEMA = {
    "type": "object",
    "properties": {
        "repository_summary": {"type": "string"},
        "scope_notes": {"type": "string"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                    },
                    "confidence": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                    "file": {"type": "string"},
                    "line_start": {"type": "integer", "minimum": 1},
                    "line_end": {"type": "integer", "minimum": 1},
                    "symbol": {"type": "string"},
                    "problem": {"type": "string"},
                    "source_evidence": {"type": "string"},
                    "suggested_fix": {"type": "string"},
                    "why_it_matters": {"type": "string"},
                },
                "required": [
                    "id",
                    "title",
                    "severity",
                    "confidence",
                    "file",
                    "line_start",
                    "line_end",
                    "symbol",
                    "problem",
                    "source_evidence",
                    "suggested_fix",
                    "why_it_matters",
                ],
                "additionalProperties": False,
            },
        },
    },
    "required": ["repository_summary", "scope_notes", "findings"],
    "additionalProperties": False,
}


BASELINE_TASK = """Perform a source-aware review of the entire repository in the
current working directory. This is a discovery pass, not ground truth.

Explore the repository before reporting findings. Inspect architecture, central
execution paths, tests, and error-prone boundaries. Report only concrete,
actionable issues supported by the exact checked-out source. Do not pad the
review to satisfy a checklist, and do not report purely subjective preferences.

For every finding, cite one primary file and the narrowest useful line range,
name the relevant symbol, quote concise source evidence, explain the actual
failure or maintenance risk, and propose a proportionate fix. Use stable IDs
starting B-001, B-002, and so on. If broad coverage was not possible, state that
honestly in scope_notes. Do not modify repository files.
"""


def parse_result(stdout: str) -> tuple[dict, dict]:
    envelope = json.loads(stdout)
    structured = envelope.get("structured_output")
    if not isinstance(structured, dict):
        result = envelope.get("result")
        if isinstance(result, str):
            structured = json.loads(result)
    if not isinstance(structured, dict):
        raise ValueError("Claude response did not contain structured baseline output")
    return structured, envelope


def render_markdown(review: dict, source: dict[str, str]) -> str:
    lines = [
        "# Claude Seed Review",
        "",
        f"- Upstream: `{source['upstream']}`",
        f"- Commit: `{source['commit']}`",
        "- Status: Candidate findings only; not adjudicated ground truth",
        "",
        "## Repository Summary",
        "",
        review["repository_summary"],
        "",
        "## Scope Notes",
        "",
        review["scope_notes"],
        "",
        "## Candidate Findings",
        "",
    ]
    for finding in review["findings"]:
        location = (
            f"{finding['file']}:{finding['line_start']}-{finding['line_end']}"
        )
        lines.extend(
            [
                f"### {finding['id']}: {finding['title']}",
                "",
                f"- Severity: {finding['severity']}",
                f"- Confidence: {finding['confidence']}",
                f"- Location: `{location}`",
                f"- Symbol: `{finding['symbol']}`",
                "",
                finding["problem"],
                "",
                "**Source evidence**",
                "",
                "```text",
                finding["source_evidence"],
                "```",
                "",
                "**Suggested fix**",
                "",
                finding["suggested_fix"],
                "",
                "**Why it matters**",
                "",
                finding["why_it_matters"],
                "",
            ]
        )
    return "\n".join(lines)


def run_claude(
    *,
    claude_binary: str,
    work_dir: Path,
    model: str,
    effort: str,
    prompt: str,
    timeout: int,
) -> tuple[subprocess.CompletedProcess, float]:
    command = [
        claude_binary,
        "--print",
        "--safe-mode",
        "--model",
        model,
        "--effort",
        effort,
        "--tools",
        "Read,Grep,Glob,Bash",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        "--no-chrome",
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(BASELINE_SCHEMA, separators=(",", ":")),
    ]
    env = {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=work_dir,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        check=False,
    )
    return completed, time.monotonic() - started


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one Claude seed review")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    parser.add_argument("--condition", default="full-skill", choices=["full-skill"])
    parser.add_argument("--model", default="sonnet")
    parser.add_argument(
        "--effort",
        default="high",
        choices=["low", "medium", "high", "xhigh", "max"],
    )
    parser.add_argument("--claude", default=shutil.which("claude") or "claude")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    source = git_source_metadata(args.repo)
    guidance = build_condition_prompt(args.condition, args.skill)
    prompt = f"{BASELINE_TASK}\n\n## Review guidance\n\n{guidance}"
    args.output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="claude-baseline-repo-") as name:
        work_dir = Path(name) / "repo"
        copy_repo(args.repo, work_dir)
        before = file_snapshot(work_dir)
        completed, elapsed = run_claude(
            claude_binary=args.claude,
            work_dir=work_dir,
            model=args.model,
            effort=args.effort,
            prompt=prompt,
            timeout=args.timeout,
        )
        delta = snapshot_delta(before, file_snapshot(work_dir))

    if completed.returncode != 0:
        raise SystemExit(
            f"Claude baseline failed ({completed.returncode}): {completed.stderr.strip()}"
        )
    review, envelope = parse_result(completed.stdout)
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "subject": "claude-baseline",
        "model": args.model,
        "effort": args.effort,
        "condition": args.condition,
        "source": source,
        "skill": str(args.skill.resolve()),
        "claude_version": command_version(args.claude),
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "permission_mode": "dangerously-skip-permissions",
        "duration_seconds": elapsed,
        "workspace_delta": delta,
        "finding_count": len(review["findings"]),
    }
    model_dir = args.output / "claude" / safe_model_name(args.model) / "baseline-1"
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    (model_dir / "review.json").write_text(
        json.dumps(review, indent=2), encoding="utf-8"
    )
    (model_dir / "review.md").write_text(
        render_markdown(review, source), encoding="utf-8"
    )
    (model_dir / "claude-response.json").write_text(
        json.dumps(envelope, indent=2), encoding="utf-8"
    )
    (model_dir / "stderr.txt").write_text(completed.stderr, encoding="utf-8")
    print(
        f"Baseline written to {model_dir}: {len(review['findings'])} candidate "
        f"findings in {elapsed:.1f}s"
    )


if __name__ == "__main__":
    main()
