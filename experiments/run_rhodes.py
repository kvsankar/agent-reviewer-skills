#!/usr/bin/env python3
"""Run Rhodes skill experiments with LLM-as-judge evaluation.

Experiment: zero-shot vs generic-prompt vs full-skill vs hybrid
Target: synthetic order_processor.py with 15 planted Rhodes violations
Evaluation: LLM-as-judge (semantic matching)

Usage:
    python3 run_rhodes.py              # Run all 4 conditions, 3 runs each
    python3 run_rhodes.py --runs 1     # Quick single-run test
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from experiment_runner import run_review, extract_findings, load_code_files
from generate_variants import generate_variant

BASE = Path(__file__).parent
REPOS = BASE / "repos"
RESULTS = BASE / "results"
SKILLS = BASE.parent / "reviewers"

# Rhodes-specific prompts for non-skill conditions
RHODES_ZERO_SHOT = """Review the following Python code for quality, style, and design issues.
For each issue found:
1. Give it a short identifier
2. Show the problematic code
3. Show the improved code
4. Explain why the change matters

Output your review in markdown format."""

RHODES_GENERIC = """You are an expert Python code reviewer.
Review the following code for:

1. **Pythonic idioms** - Is the code idiomatic Python?
2. **SOLID principles** - Single responsibility, dependency inversion, etc.
3. **Testability** - Can this code be easily unit tested?
4. **Separation of concerns** - Are I/O, logic, and presentation separated?
5. **Naming** - Are names clear and descriptive?
6. **Code smells** - Deep nesting, mutable globals, tight coupling?

For each issue:
1. Provide a short mnemonic ID
2. Show the current code
3. Show the improved version
4. Explain the principle behind the improvement

Output your review in structured markdown format."""

# Guidelines the model consistently misses - need full detail in hybrid
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


def build_prompt(condition: str, skill_path: Path) -> str:
    """Build the prompt for a given condition."""
    if condition == "zero-shot":
        return RHODES_ZERO_SHOT
    elif condition == "generic-prompt":
        return RHODES_GENERIC
    elif condition == "full-skill":
        return generate_variant(skill_path, "full")
    elif condition == "hybrid":
        return generate_variant(skill_path, "hybrid", priority_ids=RHODES_PRIORITY_IDS)
    else:
        raise ValueError(f"Unknown condition: {condition}")


def run_condition(condition: str, prompt: str, code_context: str, output_dir: Path, runs: int):
    """Run a single condition for N runs."""
    cond_dir = output_dir / condition
    cond_dir.mkdir(parents=True, exist_ok=True)
    (cond_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    results = []
    for run_num in range(1, runs + 1):
        print(f"    Run {run_num}/{runs}...", end=" ", flush=True)
        result = run_review(prompt, code_context)

        if result["success"]:
            result["findings"] = extract_findings(result["output"])
            result["findings_count"] = len(result["findings"])
        else:
            result["findings"] = []
            result["findings_count"] = 0

        result["condition"] = condition
        result["run"] = run_num

        (cond_dir / f"run-{run_num}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        (cond_dir / f"run-{run_num}-review.md").write_text(
            result["output"], encoding="utf-8"
        )

        status = "OK" if result["success"] else "FAILED"
        print(f"{status} ({result['duration_seconds']:.1f}s, {result['findings_count']} findings)")
        results.append(result)

        if run_num < runs:
            time.sleep(3)

    return results


def run_rhodes_experiment(runs: int = 3):
    """Run the Rhodes skill experiment."""
    print("=" * 70)
    print(f"RHODES SKILL EXPERIMENT ({runs} runs per condition)")
    print(f"Started at {datetime.now().isoformat()}")
    print("=" * 70)

    skill_path = SKILLS / "python-rhodes-reviewer" / "SKILL.md"
    code_files = load_code_files([REPOS / "rhodes-synthetic" / "order_processor.py"])
    total_lines = sum(c.count("\n") for c in code_files.values())
    print(f"Files: {len(code_files)}, Lines: {total_lines}")

    # Build code context once
    code_context = ""
    for filename, content in code_files.items():
        code_context += f"\n### File: {filename}\n\n```\n{content}\n```\n\n"

    output_dir = RESULTS / "exp-rhodes-v3" / "rhodes-synthetic"
    conditions = ["zero-shot", "generic-prompt", "full-skill", "hybrid"]

    all_results = {}
    for condition in conditions:
        print(f"\n  [{condition}]")
        prompt = build_prompt(condition, skill_path)
        print(f"    Prompt size: {len(prompt)} chars")
        results = run_condition(condition, prompt, code_context, output_dir, runs)

        all_results[condition] = {
            "runs": [
                {
                    "findings": r["findings_count"],
                    "duration": r["duration_seconds"],
                    "finding_ids": [f["id"] for f in r["findings"]],
                }
                for r in results
            ],
            "avg_findings": sum(r["findings_count"] for r in results) / len(results),
            "avg_duration": sum(r["duration_seconds"] for r in results) / len(results),
        }
        time.sleep(5)  # longer pause between conditions

    # Print summary
    print("\n" + "=" * 70)
    print("REVIEW RESULTS SUMMARY")
    print("=" * 70)
    print(f"\n{'Condition':<20} {'Avg Findings':>12} {'Avg Duration':>12} {'Per-Run Findings'}")
    print("-" * 80)
    for cond, data in all_results.items():
        per_run = " | ".join(str(r["findings"]) for r in data["runs"])
        print(f"  {cond:<18} {data['avg_findings']:>12.1f} {data['avg_duration']:>10.1f}s  [{per_run}]")

    # Save results
    results_file = output_dir / "review_results.json"
    results_file.write_text(
        json.dumps({"timestamp": datetime.now().isoformat(), **all_results}, indent=2),
        encoding="utf-8",
    )
    print(f"\nResults saved to {results_file}")
    print(f"\nNext: Run LLM-as-judge evaluation:")
    print(f"  python3 evaluate_judge.py --gt ground-truth/rhodes-synthetic.yaml \\")
    print(f"    --results-dir results/exp-rhodes-v2/rhodes-synthetic/")

    return all_results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=3, help="Runs per condition")
    args = parser.parse_args()
    run_rhodes_experiment(runs=args.runs)
