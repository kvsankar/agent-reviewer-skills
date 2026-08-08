#!/usr/bin/env python3
"""Run code review experiments to measure skill effectiveness.

Uses Claude CLI with OAuth (Pro Max subscription).
Each run gets fresh context via --print mode.

Usage:
    # Run a single experiment condition
    python experiment_runner.py run \
        --skill ../reviewers/python-security-privacy-reviewer/SKILL.md \
        --variant full --repo-path ../auth/backend/authentication/services.py

    # Run a full experiment
    python experiment_runner.py experiment --config experiment.yaml

    # List available skills
    python experiment_runner.py list-skills
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from generate_variants import generate_variant

# Prompts for non-skill conditions
ZERO_SHOT_PROMPT = """Review the following code for security issues and code quality problems.
For each issue found:
1. Give it a short identifier
2. Show the problematic code
3. Show the improved code
4. Explain the severity and impact

Output your review in markdown format."""

GENERIC_SECURITY_PROMPT = """You are an expert security code reviewer.
Review the following code for security vulnerabilities following OWASP Top 10 and CWE Top 25.

For each issue found:
1. Provide a mnemonic ID (e.g., SQL-INJECT, XSS)
2. State the CWE number
3. Rate severity: Critical, High, Medium, Low
4. Show the vulnerable code
5. Show the secure alternative
6. Explain the attack scenario

Also check for:
- Input validation and sanitization
- Authentication and authorization flaws
- Cryptographic issues
- Information disclosure
- Dependency vulnerabilities

Output your review in structured markdown format."""


def run_review(
    prompt: str,
    code: str,
    model: str = "claude-sonnet-4-20250514",
    timeout: int = 300,
) -> dict:
    """Run a single review via Claude CLI.

    Returns dict with: output, duration_seconds, model, timestamp, success
    """
    full_prompt = f"""{prompt}

---

## Code to Review

```
{code}
```

Provide a detailed review following the format specified above.
Focus on the most critical issues first."""

    start = time.time()
    timestamp = datetime.now().isoformat()

    try:
        # Unset CLAUDECODE env var to allow nested invocation
        env = {k: v for k, v in __import__("os").environ.items() if k != "CLAUDECODE"}
        result = subprocess.run(
            ["claude", "--print", "--model", model, "--tools", "", "--dangerously-skip-permissions"],
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        duration = time.time() - start

        if result.returncode != 0:
            return {
                "output": f"ERROR: exit code {result.returncode}\n{result.stderr}",
                "duration_seconds": duration,
                "model": model,
                "timestamp": timestamp,
                "success": False,
            }

        return {
            "output": result.stdout,
            "duration_seconds": duration,
            "model": model,
            "timestamp": timestamp,
            "success": True,
        }

    except subprocess.TimeoutExpired:
        return {
            "output": f"ERROR: timed out after {timeout}s",
            "duration_seconds": timeout,
            "model": model,
            "timestamp": timestamp,
            "success": False,
        }
    except Exception as e:
        return {
            "output": f"ERROR: {e}",
            "duration_seconds": time.time() - start,
            "model": model,
            "timestamp": timestamp,
            "success": False,
        }


def extract_findings(review_text: str) -> list[dict]:
    """Extract structured findings from a review output.

    Looks for mnemonic IDs like SQL-INJECT, XSS-PREVENT, etc.
    """
    findings = []
    # Match headings with an optional list number/emoji before the mnemonic.
    # Local models commonly use underscores or headings such as
    # "## 1️⃣ LOG_CFG – Logging configuration at import time".
    pattern = re.compile(
        r"(?:#{2,4})\s+"
        r"(?:[Ii]ssue\s+\d+\s*:\s*)?"
        r"(?:\d+\S*\s+)?"
        r"(?:\*\*|`)?([A-Z][A-Z0-9_-]{2,})(?:\*\*|`)?"
        r"(?:\s*[:–—-]\s*|\s+)"
        r"(.+?)(?:\n|$)"
    )

    for match in pattern.finditer(review_text):
        findings.append({
            "id": match.group(1),
            "title": match.group(2).strip(),
        })

    # Also catch **MNEMONIC-ID** inline references
    inline_pattern = re.compile(r"\*\*([A-Z][A-Z0-9_-]{2,})\*\*")
    inline_ids = set(f["id"] for f in findings)
    for match in inline_pattern.finditer(review_text):
        mid = match.group(1)
        if mid not in inline_ids and len(mid) > 3:
            findings.append({"id": mid, "title": ""})
            inline_ids.add(mid)

    return findings


def run_experiment_condition(
    condition_name: str,
    skill_path: Path | None,
    variant: str,
    code_files: dict[str, str],
    output_dir: Path,
    model: str = "claude-sonnet-4-20250514",
    runs: int = 1,
    delay: float = 2.0,
):
    """Run all reviews for a single experiment condition.

    Args:
        condition_name: e.g. "zero-shot", "full-skill", "principles-only"
        skill_path: Path to SKILL.md (None for zero-shot/generic)
        variant: Variant type for generate_variants
        code_files: Dict of {filename: code_content}
        output_dir: Where to save results
        model: Claude model to use
        runs: Number of repetitions
        delay: Seconds between API calls
    """
    # Build the prompt
    if skill_path and variant:
        prompt = generate_variant(skill_path, variant)
    elif condition_name == "zero-shot":
        prompt = ZERO_SHOT_PROMPT
    elif condition_name == "generic-prompt":
        prompt = GENERIC_SECURITY_PROMPT
    else:
        raise ValueError(f"Unknown condition: {condition_name}")

    # Combine code files into context
    code_context = ""
    for filename, content in code_files.items():
        code_context += f"\n### File: {filename}\n\n```\n{content}\n```\n\n"

    condition_dir = output_dir / condition_name
    condition_dir.mkdir(parents=True, exist_ok=True)

    # Save the prompt used
    (condition_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    results = []
    for run_num in range(1, runs + 1):
        print(f"  Run {run_num}/{runs}...", end=" ", flush=True)
        result = run_review(prompt, code_context, model=model)

        # Extract findings
        if result["success"]:
            result["findings"] = extract_findings(result["output"])
            result["findings_count"] = len(result["findings"])
        else:
            result["findings"] = []
            result["findings_count"] = 0

        result["condition"] = condition_name
        result["variant"] = variant
        result["run"] = run_num

        # Save individual run
        run_file = condition_dir / f"run-{run_num}.json"
        run_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

        # Save review output as readable markdown
        review_file = condition_dir / f"run-{run_num}-review.md"
        review_file.write_text(result["output"], encoding="utf-8")

        status = "OK" if result["success"] else "FAILED"
        print(f"{status} ({result['duration_seconds']:.1f}s, {result['findings_count']} findings)")

        results.append(result)

        if run_num < runs:
            time.sleep(delay)

    return results


def load_code_files(paths: list[Path]) -> dict[str, str]:
    """Load code files into a dict."""
    files = {}
    for p in paths:
        p = Path(p)
        if p.is_file():
            files[p.name] = p.read_text(encoding="utf-8")
        elif p.is_dir():
            for f in sorted(p.rglob("*.py")):
                rel = f.relative_to(p)
                files[str(rel)] = f.read_text(encoding="utf-8")
    return files


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run code review experiments")
    subparsers = parser.add_subparsers(dest="command")

    # Single run
    run_parser = subparsers.add_parser("run", help="Run a single condition")
    run_parser.add_argument("--skill", type=Path, help="Path to SKILL.md")
    run_parser.add_argument(
        "--variant",
        default="full",
        choices=["full", "principles", "ids-only", "trimmed-20", "trimmed-40"],
    )
    run_parser.add_argument("--condition", default=None, help="Condition name (default: variant name)")
    run_parser.add_argument("--code", type=Path, nargs="+", required=True, help="Code files/dirs to review")
    run_parser.add_argument("--output", "-o", type=Path, default=Path("results"), help="Output directory")
    run_parser.add_argument("--model", default="claude-sonnet-4-20250514")
    run_parser.add_argument("--runs", type=int, default=1)

    # Baseline experiment (Exp 1)
    baseline_parser = subparsers.add_parser("baseline", help="Run Experiment 1: with vs without skill")
    baseline_parser.add_argument("--skill", type=Path, required=True, help="Path to SKILL.md")
    baseline_parser.add_argument("--code", type=Path, nargs="+", required=True)
    baseline_parser.add_argument("--output", "-o", type=Path, default=Path("results/baseline"))
    baseline_parser.add_argument("--model", default="claude-sonnet-4-20250514")
    baseline_parser.add_argument("--runs", type=int, default=1)

    # Ablation experiment (Exp 2)
    ablation_parser = subparsers.add_parser("ablation", help="Run Experiment 2: full vs principles vs ids-only")
    ablation_parser.add_argument("--skill", type=Path, required=True)
    ablation_parser.add_argument("--code", type=Path, nargs="+", required=True)
    ablation_parser.add_argument("--output", "-o", type=Path, default=Path("results/ablation"))
    ablation_parser.add_argument("--model", default="claude-sonnet-4-20250514")
    ablation_parser.add_argument("--runs", type=int, default=1)

    # List skills
    subparsers.add_parser("list-skills", help="List available skills")

    args = parser.parse_args()

    if args.command == "list-skills":
        skills_dir = Path(__file__).parent.parent / "reviewers"
        for d in sorted(skills_dir.iterdir()):
            skill_file = d / "SKILL.md"
            if skill_file.exists():
                print(f"  {d.name}/SKILL.md")
        return

    if args.command == "run":
        code_files = load_code_files(args.code)
        if not code_files:
            print("No code files found")
            sys.exit(1)

        print(f"Loaded {len(code_files)} files")
        condition = args.condition or args.variant
        run_experiment_condition(
            condition_name=condition,
            skill_path=args.skill,
            variant=args.variant,
            code_files=code_files,
            output_dir=args.output,
            model=args.model,
            runs=args.runs,
        )

    elif args.command == "baseline":
        code_files = load_code_files(args.code)
        if not code_files:
            print("No code files found")
            sys.exit(1)

        total_lines = sum(c.count("\n") for c in code_files.values())
        print(f"Loaded {len(code_files)} files ({total_lines} lines)")
        print(f"Skill: {args.skill}")
        print(f"Model: {args.model}")
        print(f"Runs per condition: {args.runs}")
        print()

        conditions = [
            ("zero-shot", None, None),
            ("generic-prompt", None, None),
            ("full-skill", args.skill, "full"),
        ]

        all_results = {}
        for cond_name, skill, variant in conditions:
            print(f"[{cond_name}]")
            results = run_experiment_condition(
                condition_name=cond_name,
                skill_path=skill,
                variant=variant,
                code_files=code_files,
                output_dir=args.output,
                model=args.model,
                runs=args.runs,
            )
            all_results[cond_name] = results
            print()

        # Summary
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for cond_name, results in all_results.items():
            avg_findings = sum(r["findings_count"] for r in results) / len(results)
            avg_duration = sum(r["duration_seconds"] for r in results) / len(results)
            print(f"  {cond_name:20s}: {avg_findings:.1f} findings (avg), {avg_duration:.1f}s")

    elif args.command == "ablation":
        code_files = load_code_files(args.code)
        if not code_files:
            print("No code files found")
            sys.exit(1)

        total_lines = sum(c.count("\n") for c in code_files.values())
        print(f"Loaded {len(code_files)} files ({total_lines} lines)")
        print()

        conditions = [
            ("full-skill", args.skill, "full"),
            ("principles-only", args.skill, "principles"),
            ("ids-only", args.skill, "ids-only"),
            ("trimmed-20", args.skill, "trimmed-20"),
        ]

        all_results = {}
        for cond_name, skill, variant in conditions:
            print(f"[{cond_name}]")
            results = run_experiment_condition(
                condition_name=cond_name,
                skill_path=skill,
                variant=variant,
                code_files=code_files,
                output_dir=args.output,
                model=args.model,
                runs=args.runs,
            )
            all_results[cond_name] = results
            print()

        # Summary
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for cond_name, results in all_results.items():
            avg_findings = sum(r["findings_count"] for r in results) / len(results)
            avg_duration = sum(r["duration_seconds"] for r in results) / len(results)
            print(f"  {cond_name:20s}: {avg_findings:.1f} findings (avg), {avg_duration:.1f}s")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
