#!/usr/bin/env python3
"""Run Codex exec as the hosted agentic baseline for review evaluations."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path

from agent_eval_common import (
    AGENT_TASK,
    DEFAULT_SKILL,
    command_version,
    condition_instructions,
    copy_repo,
    file_snapshot,
    git_source_metadata,
    parse_codex_jsonl,
    snapshot_delta,
    write_agent_run,
)


def run_codex(
    *,
    codex_binary: str,
    work_dir: Path,
    model: str | None,
    prompt: str,
    timeout: int,
) -> tuple[subprocess.CompletedProcess, float]:
    command = [
        codex_binary,
        "exec",
        "--ephemeral",
        "--json",
        "--dangerously-bypass-approvals-and-sandbox",
        "--skip-git-repo-check",
        "--ignore-user-config",
        "--ignore-rules",
        "-C",
        str(work_dir),
    ]
    if model:
        command.extend(["--model", model])
    command.append("-")
    started = time.monotonic()
    completed = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return completed, time.monotonic() - started


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Codex exec agentic review baselines")
    parser.add_argument(
        "--conditions",
        nargs="+",
        choices=[
            "regular",
            "lean-skill",
            "zero-shot",
            "ids-only",
            "hybrid",
            "full-skill",
        ],
        default=["zero-shot", "ids-only", "hybrid"],
    )
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--model", help="Codex model; omit to use the configured default")
    parser.add_argument(
        "--repo",
        type=Path,
        required=True,
        help="Checkout of an immutable real upstream revision",
    )
    parser.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task", default=AGENT_TASK)
    parser.add_argument("--codex", default=shutil.which("codex") or "codex")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    source = git_source_metadata(args.repo)
    args.output.mkdir(parents=True, exist_ok=True)
    display_model = args.model or "configured-default"
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "subject": "codex",
        "model": display_model,
        "conditions": args.conditions,
        "runs": args.runs,
        "repo": str(args.repo.resolve()),
        "source": source,
        "skill": str(args.skill.resolve()),
        "permissions": "Codex yolo mode in a disposable copy; this is not an OS security boundary",
        "codex_version": command_version(args.codex),
    }
    (args.output / "codex-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    for condition in args.conditions:
        instructions = condition_instructions(condition, args.skill)
        prompt = args.task
        if instructions:
            prompt += f"\n\n## Review guidance\n\n{instructions}"
        for run_number in range(1, args.runs + 1):
            print(f"[codex/{display_model}] {condition} run {run_number}/{args.runs}", flush=True)
            with tempfile.TemporaryDirectory(prefix="codex-eval-repo-") as repo_name:
                work_dir = Path(repo_name) / "repo"
                copy_repo(args.repo, work_dir)
                before = file_snapshot(work_dir)
                completed, elapsed = run_codex(
                    codex_binary=args.codex,
                    work_dir=work_dir,
                    model=args.model,
                    prompt=prompt,
                    timeout=args.timeout,
                )
                parsed = parse_codex_jsonl(completed.stdout)
                parsed.update(
                    {
                        "subject": "codex",
                        "model": display_model,
                        "condition": condition,
                        "run": run_number,
                        "success": completed.returncode == 0 and bool(parsed["output"]),
                        "returncode": completed.returncode,
                        "stderr": completed.stderr,
                        "duration_seconds": elapsed,
                        "timestamp": datetime.now().isoformat(),
                        "workspace_delta": snapshot_delta(before, file_snapshot(work_dir)),
                    }
                )
                write_agent_run(
                    output_root=args.output,
                    subject="codex",
                    model=display_model,
                    condition=condition,
                    run_number=run_number,
                    instructions=instructions,
                    result=parsed,
                    transcript=completed.stdout,
                )
                print(
                    f"  success={parsed['success']} tools={parsed['tool_call_count']} "
                    f"findings={parsed['findings_count']} duration={elapsed:.1f}s",
                    flush=True,
                )


if __name__ == "__main__":
    main()
