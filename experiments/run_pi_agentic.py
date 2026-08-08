#!/usr/bin/env python3
"""Run read-only agentic code reviews with Pi backed by remote Ollama."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
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
    parse_pi_jsonl,
    snapshot_delta,
    write_agent_run,
)


def free_local_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_port(port: int, process: subprocess.Popen, timeout: float = 10.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            stderr = process.stderr.read() if process.stderr else ""
            raise RuntimeError(f"SSH tunnel exited early: {stderr.strip()}")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.25):
                return
        except OSError:
            time.sleep(0.1)
    raise TimeoutError(f"SSH tunnel did not open local port {port}")


def start_tunnel(host: str, ssh_config: Path, local_port: int) -> subprocess.Popen:
    command = [
        "ssh",
        "-F",
        str(ssh_config),
        "-o",
        "BatchMode=yes",
        "-o",
        "ExitOnForwardFailure=yes",
        "-N",
        "-L",
        f"127.0.0.1:{local_port}:127.0.0.1:11434",
        host,
    ]
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    wait_for_port(local_port, process)
    return process


def write_pi_config(config_dir: Path, port: int, models: list[str], max_tokens: int) -> None:
    config_dir.mkdir(parents=True, exist_ok=True)
    model_entries = [
        {
            "id": model,
            "name": f"{model} via tsmac Ollama",
            "reasoning": model.startswith("gpt-oss"),
            "input": ["text"],
            "contextWindow": 32768,
            "maxTokens": max_tokens,
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
        }
        for model in models
    ]
    config = {
        "providers": {
            "ollama": {
                "baseUrl": f"http://127.0.0.1:{port}/v1",
                "api": "openai-completions",
                "apiKey": "ollama",
                "compat": {
                    "supportsDeveloperRole": False,
                    "supportsReasoningEffort": False,
                    "maxTokensField": "max_tokens",
                },
                "models": model_entries,
            }
        }
    }
    (config_dir / "models.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    (config_dir / "settings.json").write_text(
        json.dumps({"telemetry": False, "defaultProjectTrust": "never"}, indent=2),
        encoding="utf-8",
    )


def run_pi(
    *,
    pi_binary: str,
    work_dir: Path,
    config_dir: Path,
    model: str,
    instructions_file: Path,
    task: str,
    timeout: int,
) -> tuple[subprocess.CompletedProcess, float]:
    command = [
        pi_binary,
        "--print",
        "--mode",
        "json",
        "--no-session",
        "--no-context-files",
        "--no-extensions",
        "--no-skills",
        "--no-prompt-templates",
        "--no-approve",
        "--offline",
        "--provider",
        "ollama",
        "--model",
        model,
        "--api-key",
        "ollama",
        "--tools",
        "read,bash,grep,find,ls",
        "--append-system-prompt",
        str(instructions_file),
        task,
    ]
    env = os.environ.copy()
    env.update(
        {
            "PI_CODING_AGENT_DIR": str(config_dir),
            "PI_CODING_AGENT_SESSION_DIR": str(config_dir / "sessions"),
            "PI_OFFLINE": "1",
            "PI_TELEMETRY": "0",
        }
    )
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=work_dir,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return completed, time.monotonic() - started


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Pi agentic reviews against Ollama on a remote host"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["devstral-small-2:latest", "qwen3-coder:30b"],
    )
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
    parser.add_argument("--host", default="tsmac")
    parser.add_argument("--ssh-config", type=Path, default=Path.home() / ".ssh" / "config")
    parser.add_argument(
        "--repo",
        type=Path,
        required=True,
        help="Checkout of an immutable real upstream revision",
    )
    parser.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--task", default=AGENT_TASK)
    parser.add_argument("--pi", default=shutil.which("pi") or "pi")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    source = git_source_metadata(args.repo)
    args.output.mkdir(parents=True, exist_ok=True)
    port = free_local_port()
    tunnel = start_tunnel(args.host, args.ssh_config, port)
    try:
        with tempfile.TemporaryDirectory(prefix="pi-eval-config-") as config_name:
            config_dir = Path(config_name)
            write_pi_config(config_dir, port, args.models, args.max_tokens)
            manifest = {
                "timestamp": datetime.now().isoformat(),
                "subject": "pi-ollama",
                "host": args.host,
                "models": args.models,
                "conditions": args.conditions,
                "runs": args.runs,
                "repo": str(args.repo.resolve()),
                "source": source,
                "skill": str(args.skill.resolve()),
                "tools": ["read", "bash", "grep", "find", "ls"],
                "permissions": "Pi has no approval prompts; each run uses a disposable copy",
                "pi_version": command_version(args.pi),
            }
            (args.output / "pi-ollama-manifest.json").write_text(
                json.dumps(manifest, indent=2), encoding="utf-8"
            )

            for model in args.models:
                for condition in args.conditions:
                    instructions = condition_instructions(condition, args.skill)
                    for run_number in range(1, args.runs + 1):
                        print(f"[pi/{model}] {condition} run {run_number}/{args.runs}", flush=True)
                        with tempfile.TemporaryDirectory(prefix="pi-eval-repo-") as repo_name:
                            work_dir = Path(repo_name) / "repo"
                            copy_repo(args.repo, work_dir)
                            before = file_snapshot(work_dir)
                            instructions_file = config_dir / "condition.md"
                            instructions_file.write_text(instructions, encoding="utf-8")
                            completed, elapsed = run_pi(
                                pi_binary=args.pi,
                                work_dir=work_dir,
                                config_dir=config_dir,
                                model=model,
                                instructions_file=instructions_file,
                                task=args.task,
                                timeout=args.timeout,
                            )
                            parsed = parse_pi_jsonl(completed.stdout)
                            parsed.update(
                                {
                                    "subject": "pi-ollama",
                                    "model": model,
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
                                subject="pi-ollama",
                                model=model,
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
    finally:
        tunnel.terminate()
        try:
            tunnel.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tunnel.kill()
            tunnel.wait()


if __name__ == "__main__":
    main()
