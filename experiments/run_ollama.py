#!/usr/bin/env python3
"""Run the Rhodes review benchmark against Ollama on a remote host.

The runner sends prompts to Ollama's local HTTP API over SSH. Model weights and
review inference stay on the remote machine; only prompts and JSON responses
cross the SSH connection.
"""

import argparse
import hashlib
import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

from experiment_runner import extract_findings
from generate_variants import generate_variant


BASE = Path(__file__).parent
DEFAULT_SKILL = BASE.parent / "reviewers" / "python-rhodes-reviewer" / "SKILL.md"

ZERO_SHOT_PROMPT = """Review the following Python code for quality, style, and design issues.
For each issue found:
1. Give it a short mnemonic identifier
2. Show the problematic code
3. Show the improved code
4. Explain why the change matters

Output your review in structured markdown format."""

RHODES_PRIORITY_IDS = [
    "NO-MOCK",
    "NO-CALL",
    "TOP-DOWN",
    "COPERNICAN",
    "BREAK-TEST",
    "PASS-FUNC",
    "PREBOUND-METHOD",
    "NO-SCATTERED-IFS",
]


def git_source_metadata(source: Path) -> dict[str, str]:
    """Validate that the input comes from a clean, identifiable Git revision."""
    location = source.parent

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
                f"Evaluation code must be in a Git checkout: {source} "
                f"({completed.stderr.strip()})"
            )
        return completed.stdout.strip()

    root = git("rev-parse", "--show-toplevel")
    commit = git("rev-parse", "HEAD")
    remote = git("remote", "get-url", "origin")
    dirty = git("status", "--porcelain")
    if dirty:
        raise ValueError(
            f"Evaluation code must come from an immutable clean revision: {root}\n{dirty}"
        )
    return {
        "repository_root": root,
        "upstream": remote,
        "commit": commit,
        "file_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }


def build_condition_prompt(condition: str, skill_path: Path) -> str:
    """Build one of the controlled benchmark prompts."""
    if condition == "regular":
        return ""
    if condition == "lean-skill":
        return skill_path.read_text(encoding="utf-8")
    if condition == "zero-shot":
        return ZERO_SHOT_PROMPT
    if condition == "ids-only":
        return generate_variant(skill_path, "ids-only")
    if condition == "hybrid":
        return generate_variant(
            skill_path,
            "hybrid",
            priority_ids=RHODES_PRIORITY_IDS,
        )
    if condition == "full-skill":
        return generate_variant(skill_path, "full")
    raise ValueError(f"Unknown condition: {condition}")


def build_review_prompt(instructions: str, code_path: Path) -> str:
    """Combine review instructions and a selected file from a real repository."""
    code = code_path.read_text(encoding="utf-8")
    return f"""{instructions}

---

## Code to Review

### File: {code_path.name}

```python
{code}
```

Provide a detailed review following the requested format. Focus on the most
important issues first. Do not execute the code.
"""


def safe_model_name(model: str) -> str:
    """Convert an Ollama model tag to a portable directory name."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model)


def run_ollama(
    *,
    host: str,
    ssh_config: Path,
    model: str,
    prompt: str,
    temperature: float,
    seed: int,
    num_ctx: int,
    num_predict: int,
    think: bool | str,
    timeout: int,
) -> dict:
    """Call Ollama's non-streaming generate API over SSH."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": think,
        "keep_alive": "10m",
        "options": {
            "temperature": temperature,
            "seed": seed,
            "num_ctx": num_ctx,
            "num_predict": num_predict,
        },
    }
    command = [
        "ssh",
        "-F",
        str(ssh_config),
        "-o",
        "BatchMode=yes",
        host,
        "/usr/bin/curl",
        "-sS",
        "http://127.0.0.1:11434/api/generate",
        "--json",
        "@-",
    ]

    started = time.monotonic()
    completed = subprocess.run(
        command,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    wall_seconds = time.monotonic() - started

    if completed.returncode != 0:
        raise RuntimeError(
            f"SSH/Ollama request failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )

    response = json.loads(completed.stdout)
    if response.get("error"):
        raise RuntimeError(f"Ollama error: {response['error']}")

    output = response.get("response", "")
    findings = extract_findings(output)
    eval_count = response.get("eval_count", 0)
    eval_duration = response.get("eval_duration", 0)
    prompt_eval_count = response.get("prompt_eval_count", 0)
    prompt_eval_duration = response.get("prompt_eval_duration", 0)

    return {
        "output": output,
        "thinking": response.get("thinking", ""),
        "duration_seconds": wall_seconds,
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "success": response.get("done", False),
        "done_reason": response.get("done_reason"),
        "findings": findings,
        "findings_count": len(findings),
        "prompt_eval_count": prompt_eval_count,
        "eval_count": eval_count,
        "prompt_tokens_per_second": (
            prompt_eval_count / (prompt_eval_duration / 1_000_000_000)
            if prompt_eval_duration
            else 0
        ),
        "output_tokens_per_second": (
            eval_count / (eval_duration / 1_000_000_000)
            if eval_duration
            else 0
        ),
        "ollama_total_duration_seconds": response.get("total_duration", 0)
        / 1_000_000_000,
        "ollama_load_duration_seconds": response.get("load_duration", 0)
        / 1_000_000_000,
    }


def write_run(
    output_dir: Path,
    model: str,
    condition: str,
    run_number: int,
    instructions: str,
    result: dict,
) -> None:
    """Persist machine-readable metrics and readable model output."""
    condition_dir = output_dir / safe_model_name(model) / condition
    condition_dir.mkdir(parents=True, exist_ok=True)
    (condition_dir / "prompt.md").write_text(instructions, encoding="utf-8")
    (condition_dir / f"run-{run_number}.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )
    (condition_dir / f"run-{run_number}-review.md").write_text(
        result["output"],
        encoding="utf-8",
    )
    if result.get("thinking"):
        (condition_dir / f"run-{run_number}-thinking.md").write_text(
            result["thinking"],
            encoding="utf-8",
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark review prompts against Ollama over SSH"
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["gpt-oss:20b", "devstral-small-2:latest", "qwen3-coder:30b"],
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
    parser.add_argument(
        "--ssh-config",
        type=Path,
        default=Path.home() / ".ssh" / "config",
    )
    parser.add_argument("--skill", type=Path, default=DEFAULT_SKILL)
    parser.add_argument(
        "--code",
        type=Path,
        required=True,
        help="File from an immutable real-repository revision",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-ctx", type=int, default=32768)
    parser.add_argument("--num-predict", type=int, default=4096)
    parser.add_argument(
        "--think",
        choices=["false", "true", "low", "medium", "high"],
        default="false",
        help="Ollama thinking mode; disabled by default for equal output budgets",
    )
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    source = git_source_metadata(args.code)
    think: bool | str
    if args.think in {"true", "false"}:
        think = args.think == "true"
    else:
        think = args.think

    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "host": args.host,
        "models": args.models,
        "conditions": args.conditions,
        "runs": args.runs,
        "temperature": args.temperature,
        "seed": args.seed,
        "num_ctx": args.num_ctx,
        "num_predict": args.num_predict,
        "think": think,
        "skill": str(args.skill),
        "code": str(args.code),
        "source": source,
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    summary = []
    for model in args.models:
        for condition in args.conditions:
            instructions = build_condition_prompt(condition, args.skill)
            prompt = build_review_prompt(instructions, args.code)
            for run_number in range(1, args.runs + 1):
                print(
                    f"[{model}] {condition} run {run_number}/{args.runs} "
                    f"({len(prompt):,} chars)",
                    flush=True,
                )
                try:
                    result = run_ollama(
                        host=args.host,
                        ssh_config=args.ssh_config,
                        model=model,
                        prompt=prompt,
                        temperature=args.temperature,
                        seed=args.seed,
                        num_ctx=args.num_ctx,
                        num_predict=args.num_predict,
                        think=think,
                        timeout=args.timeout,
                    )
                except Exception as exc:
                    result = {
                        "output": f"ERROR: {exc}",
                        "thinking": "",
                        "duration_seconds": 0,
                        "model": model,
                        "timestamp": datetime.now().isoformat(),
                        "success": False,
                        "findings": [],
                        "findings_count": 0,
                    }

                result["condition"] = condition
                result["run"] = run_number
                result["prompt_characters"] = len(prompt)
                write_run(
                    args.output,
                    model,
                    condition,
                    run_number,
                    instructions,
                    result,
                )
                summary.append(
                    {
                        key: result.get(key)
                        for key in (
                            "model",
                            "condition",
                            "run",
                            "success",
                            "findings_count",
                            "duration_seconds",
                            "prompt_eval_count",
                            "eval_count",
                            "output_tokens_per_second",
                            "done_reason",
                        )
                    }
                )
                print(
                    f"  success={result['success']} "
                    f"findings={result['findings_count']} "
                    f"duration={result.get('duration_seconds', 0):.1f}s "
                    f"output_tps={result.get('output_tokens_per_second', 0):.1f}",
                    flush=True,
                )

    (args.output / "summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(f"Results written to {args.output}", flush=True)


if __name__ == "__main__":
    main()
