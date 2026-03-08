#!/usr/bin/env python3
"""LLM-as-judge evaluation for non-security skills.

For skills like Rhodes Python reviewer where ground truth matching is
subjective (e.g., did the review catch "vague naming" even if it used
different terminology?), we use an LLM to semantically assess whether
each planted violation was detected in the review output.

Usage:
    python3 evaluate_judge.py --gt ground-truth/rhodes-synthetic.yaml \
        --results-dir results/exp-rhodes/rhodes-synthetic/
"""

import json
import re
import subprocess
import sys
import time
import yaml
from pathlib import Path


def load_ground_truth(gt_path: Path) -> list[dict]:
    """Load ground truth issues from YAML."""
    with open(gt_path) as f:
        gt = yaml.safe_load(f)
    issues = []
    for file_entry in gt.get("files", []):
        for issue in file_entry.get("issues", []):
            issue["file"] = file_entry["path"]
            issues.append(issue)
    return issues


def load_review(results_dir: Path, condition: str, run: int = 1) -> str | None:
    """Load review markdown from a condition directory."""
    review_file = results_dir / condition / f"run-{run}-review.md"
    if review_file.exists():
        return review_file.read_text(encoding="utf-8")
    return None


def discover_runs(results_dir: Path, condition: str) -> list[int]:
    """Find all run numbers for a condition."""
    cond_dir = results_dir / condition
    if not cond_dir.is_dir():
        return []
    runs = []
    for f in sorted(cond_dir.glob("run-*-review.md")):
        match = re.match(r"run-(\d+)-review\.md", f.name)
        if match:
            runs.append(int(match.group(1)))
    return runs


def judge_single_issue(
    issue: dict,
    review_text: str,
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    """Ask LLM judge whether a specific issue was detected in the review.

    Returns dict with: detected (bool), confidence (high/medium/low),
    evidence (str), reasoning (str)
    """
    prompt = f"""You are an impartial judge evaluating whether a code review caught a specific issue.

## Ground Truth Issue

- **ID**: {issue['id']}
- **Type**: {issue['type']}
- **Guideline**: {issue.get('guideline', 'N/A')}
- **Description**: {issue['description']}
- **Function**: {issue.get('function', 'N/A')}
- **Lines**: {issue.get('line_range', 'N/A')}

## Review Output

{review_text}

## Your Task

Determine whether the review **detected this specific issue**. The review does NOT need to use the exact same terminology or mnemonic ID. It counts as detected if the review:
1. Identifies the same problematic code or function, AND
2. Describes the same underlying problem (even in different words)

For example, if the ground truth says "HOIST-IO: I/O mixed in business logic" and the review says "database queries should be separated from calculation logic", that counts as detected.

Respond in this exact JSON format:
```json
{{
  "detected": true/false,
  "confidence": "high" | "medium" | "low",
  "evidence": "Quote the specific part of the review that addresses this issue, or 'none' if not detected",
  "reasoning": "Brief explanation of why you judged it as detected or not"
}}
```

Respond ONLY with the JSON block, no other text."""

    try:
        env = {k: v for k, v in __import__("os").environ.items() if k != "CLAUDECODE"}
        result = subprocess.run(
            ["claude", "--print", "--model", model, "--tools", "", "--dangerously-skip-permissions"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
        if result.returncode != 0:
            return {
                "detected": False,
                "confidence": "low",
                "evidence": "none",
                "reasoning": f"Judge call failed: {result.stderr[:200]}",
            }

        # Extract JSON from response - try multiple patterns
        output = result.stdout.strip()

        # Try code-fenced JSON first
        fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", output, re.DOTALL)
        if fenced:
            try:
                return json.loads(fenced.group(1))
            except json.JSONDecodeError:
                pass

        # Try any JSON object (greedy to handle nested quotes)
        json_match = re.search(r"\{.*\"detected\".*\}", output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # Fallback: look for detected true/false in text
        detected = bool(re.search(r'"detected"\s*:\s*true', output, re.IGNORECASE))
        return {
            "detected": detected,
            "confidence": "low",
            "evidence": "none",
            "reasoning": f"Parsed from raw text: {output[:200]}",
        }

    except Exception as e:
        return {
            "detected": False,
            "confidence": "low",
            "evidence": "none",
            "reasoning": f"Error: {e}",
        }


def evaluate_condition(
    condition: str,
    review_text: str,
    gt_issues: list[dict],
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    """Evaluate all ground truth issues for a single condition."""
    results = []
    detected_count = 0

    for i, issue in enumerate(gt_issues):
        print(f"    Judging {issue['id']} ({issue['type']})...", end=" ", flush=True)
        judgment = judge_single_issue(issue, review_text, model=model)
        judgment["issue_id"] = issue["id"]
        judgment["issue_type"] = issue["type"]
        results.append(judgment)

        if judgment["detected"]:
            detected_count += 1
            print(f"DETECTED ({judgment['confidence']})")
        else:
            print(f"MISSED ({judgment['confidence']})")

        time.sleep(1)  # rate limit

    total = len(gt_issues)
    recall = detected_count / total if total > 0 else 0

    return {
        "condition": condition,
        "total_issues": total,
        "detected": detected_count,
        "missed": total - detected_count,
        "recall": round(recall, 3),
        "judgments": results,
    }


def count_review_findings(review_text: str) -> int:
    """Count the number of distinct findings/suggestions in a review."""
    # Count mnemonic IDs (Rhodes style: #### MNEMONIC-ID: or **MNEMONIC-ID**)
    pattern = re.compile(r"(?:#{2,4})\s+(?:\*\*)?([A-Z][A-Z0-9-]+)(?:\*\*)?[:\s]+")
    ids = set()
    for match in pattern.finditer(review_text):
        mid = match.group(1)
        if mid not in ("MNEMONIC", "ID", "NEXT"):  # skip template text
            ids.add(mid)
    return len(ids) if ids else review_text.count("####")


def evaluate_all(
    gt_path: Path,
    results_dir: Path,
    conditions: list[str] | None = None,
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    """Evaluate all conditions against ground truth.

    Handles multiple runs per condition and aggregates results.
    """
    gt_issues = load_ground_truth(gt_path)
    print(f"Ground truth: {len(gt_issues)} issues from {gt_path.name}")

    if conditions is None:
        conditions = sorted(
            d.name for d in results_dir.iterdir()
            if d.is_dir() and (d / "run-1-review.md").exists()
        )

    print(f"Conditions: {', '.join(conditions)}")

    all_results = {}
    for condition in conditions:
        runs = discover_runs(results_dir, condition)
        if not runs:
            print(f"\n  [{condition}] No reviews found, skipping")
            continue

        print(f"\n  [{condition}] ({len(runs)} run(s))")
        run_results = []

        for run_num in runs:
            review_text = load_review(results_dir, condition, run=run_num)
            if not review_text:
                continue

            print(f"    --- Run {run_num} ---")
            finding_count = count_review_findings(review_text)
            result = evaluate_condition(condition, review_text, gt_issues, model=model)
            result["run"] = run_num
            result["total_findings_in_review"] = finding_count
            run_results.append(result)

        if not run_results:
            continue

        # Aggregate across runs
        avg_recall = sum(r["recall"] for r in run_results) / len(run_results)
        avg_detected = sum(r["detected"] for r in run_results) / len(run_results)

        # Per-issue: count how many runs detected each issue
        issue_detection_rates = {}
        for issue in gt_issues:
            count = 0
            for r in run_results:
                j = next((j for j in r["judgments"] if j["issue_id"] == issue["id"]), None)
                if j and j["detected"]:
                    count += 1
            issue_detection_rates[issue["id"]] = {
                "detected_in": count,
                "total_runs": len(run_results),
                "rate": count / len(run_results),
            }

        all_results[condition] = {
            "total_issues": len(gt_issues),
            "num_runs": len(run_results),
            "avg_detected": round(avg_detected, 1),
            "avg_recall": round(avg_recall, 3),
            "per_run_recall": [r["recall"] for r in run_results],
            "per_run_detected": [r["detected"] for r in run_results],
            "issue_detection_rates": issue_detection_rates,
            "runs": run_results,
        }

    return all_results


def print_report(all_results: dict, gt_issues: list[dict]):
    """Print a summary report of judge evaluations."""
    print("\n" + "=" * 70)
    print("LLM-AS-JUDGE EVALUATION REPORT")
    print("=" * 70)

    # Summary table
    cond_names = sorted(all_results.keys())
    print(f"\n{'Condition':<20} {'Runs':>5} {'Avg Det':>8} {'Avg Recall':>10} {'Per-Run Recall'}")
    print("-" * 80)
    for cond in cond_names:
        r = all_results[cond]
        per_run = " | ".join(f"{x:.0%}" for x in r["per_run_recall"])
        print(
            f"  {cond:<18} {r['num_runs']:>5} {r['avg_detected']:>8.1f} "
            f"{r['avg_recall']:>9.1%}  [{per_run}]"
        )

    # Per-issue detection matrix (shows rate across runs)
    print(f"\n{'Issue':<12} {'Type':<16}", end="")
    for c in cond_names:
        label = c[:14]
        print(f" {label:>14}", end="")
    print()
    print("-" * (28 + 15 * len(cond_names)))

    for issue in gt_issues:
        print(f"  {issue['id']:<10} {issue['type']:<16}", end="")
        for c in cond_names:
            if c in all_results:
                rates = all_results[c]["issue_detection_rates"]
                info = rates.get(issue["id"], {})
                detected_in = info.get("detected_in", 0)
                total_runs = info.get("total_runs", 0)
                if total_runs == 0:
                    print(f" {'N/A':>14}", end="")
                elif detected_in == total_runs:
                    print(f" {f'{detected_in}/{total_runs} ALL':>14}", end="")
                elif detected_in == 0:
                    print(f" {f'0/{total_runs}  -':>14}", end="")
                else:
                    print(f" {f'{detected_in}/{total_runs}':>14}", end="")
            else:
                print(f" {'N/A':>14}", end="")
        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="LLM-as-judge evaluation")
    parser.add_argument("--gt", type=Path, required=True, help="Ground truth YAML")
    parser.add_argument("--results-dir", type=Path, required=True, help="Results directory")
    parser.add_argument("--conditions", nargs="+", help="Specific conditions to evaluate")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", help="Judge model")
    parser.add_argument("--output", "-o", type=Path, help="Output JSON file")

    args = parser.parse_args()

    all_results = evaluate_all(
        gt_path=args.gt,
        results_dir=args.results_dir,
        conditions=args.conditions,
        model=args.model,
    )

    gt_issues = load_ground_truth(args.gt)
    print_report(all_results, gt_issues)

    # Save results
    output_path = args.output or (args.results_dir / "judge-evaluation.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
    print(f"\nDetailed results saved to {output_path}")


if __name__ == "__main__":
    main()
