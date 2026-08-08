#!/usr/bin/env python3
"""Judge review outputs semantically with non-interactive Claude Code.

Each review is evaluated in one structured call against all ground-truth issues.
The judge has no tools, no persisted session, and receives only the benchmark
ground truth and the review text. This supports both the legacy
``condition/run-N-review.md`` layout and nested ``subject/model/condition``
layouts produced by the newer agent runners.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
from collections import defaultdict
from pathlib import Path

import yaml

from agent_eval_common import command_version
from experiment_runner import extract_findings


JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "judgments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"},
                    "detected": {"type": "boolean"},
                    "confidence": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                    "evidence": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
                "required": [
                    "issue_id",
                    "detected",
                    "confidence",
                    "evidence",
                    "reasoning",
                ],
                "additionalProperties": False,
            },
        },
        "unsupported_findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim": {"type": "string"},
                    "why_unsupported": {"type": "string"},
                },
                "required": ["claim", "why_unsupported"],
                "additionalProperties": False,
            },
        },
        "novel_findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim": {"type": "string"},
                    "file": {"type": "string"},
                    "symbol": {"type": "string"},
                    "evidence": {"type": "string"},
                },
                "required": ["claim", "file", "symbol", "evidence"],
                "additionalProperties": False,
            },
        },
        "quality": {
            "type": "object",
            "properties": {
                "usefulness": {"type": "integer", "minimum": 1, "maximum": 5},
                "specificity": {"type": "integer", "minimum": 1, "maximum": 5},
                "notes": {"type": "string"},
            },
            "required": ["usefulness", "specificity", "notes"],
            "additionalProperties": False,
        },
    },
    "required": ["judgments", "unsupported_findings", "novel_findings", "quality"],
    "additionalProperties": False,
}


def load_ground_truth(gt_path: Path) -> list[dict]:
    """Load planted YAML issues or a source-adjudicated JSON reference."""
    if gt_path.suffix == ".json":
        payload = json.loads(gt_path.read_text(encoding="utf-8"))
        issues: list[dict] = []
        for original in payload.get("findings", []):
            issues.append(
                {
                    "id": original["reference_id"],
                    "type": "validated-reference",
                    "file": original.get("file"),
                    "function": original.get("symbol"),
                    "line_range": [
                        original.get("line_start"),
                        original.get("line_end"),
                    ],
                    "severity": original.get("severity"),
                    "description": original.get("title"),
                    "guideline": original.get("reasoning"),
                    "source_evidence": original.get("source_evidence"),
                }
            )
        return issues

    with gt_path.open(encoding="utf-8") as stream:
        ground_truth = yaml.safe_load(stream)
    issues: list[dict] = []
    for file_entry in ground_truth.get("files", []):
        for original in file_entry.get("issues", []):
            issue = dict(original)
            issue["file"] = file_entry["path"]
            issues.append(issue)
    return issues


def discover_reviews(results_dir: Path, conditions: set[str] | None = None) -> list[dict]:
    """Find reviews recursively and assign stable subject/model/condition labels."""
    reviews: list[dict] = []
    pattern = re.compile(r"run-(\d+)-review\.md$")
    for review_path in sorted(results_dir.rglob("run-*-review.md")):
        match = pattern.match(review_path.name)
        if not match:
            continue
        relative_parent = review_path.parent.relative_to(results_dir)
        condition = review_path.parent.name
        if conditions and condition not in conditions:
            continue
        reviews.append(
            {
                "path": review_path,
                "label": "/".join(relative_parent.parts),
                "condition": condition,
                "run": int(match.group(1)),
            }
        )
    return reviews


def build_judge_prompt(issues: list[dict], review_text: str) -> str:
    """Build a self-contained, rubric-bound judging prompt."""
    compact_issues = [
        {
            key: issue.get(key)
            for key in (
                "id",
                "type",
                "file",
                "function",
                "line_range",
                "severity",
                "description",
                "guideline",
                "source_evidence",
            )
        }
        for issue in issues
    ]
    return f"""You are an impartial judge of a code-review benchmark.

Evaluate whether the review detected every validated reference issue. A detection requires
both the same code location or symbol and the same underlying problem. Exact
mnemonic wording is unnecessary. Do not award credit for merely repeating a
guideline without connecting it to the relevant code.

Also list concrete findings made by the review that are contradicted by, or
have no support in, the review's own quoted code. Do not call a useful extra
finding unsupported merely because it is absent from the planted ground truth.

List every concrete review finding that does not match a reference issue under
novel_findings. This is a routing decision, not a validity judgment: a later
source-aware pass will inspect those claims. Do not place vague praise, general
advice, or duplicate phrasings of a detected reference issue in novel_findings.

Use short evidence excerpts. Return exactly one judgment for every issue ID and
no invented IDs. Judge only the supplied text; you have no repository tools.

## Ground truth

{json.dumps(compact_issues, indent=2)}

## Review to judge

{review_text}
"""


def parse_claude_result(stdout: str) -> dict:
    """Extract structured output from Claude Code's JSON result envelope."""
    envelope = json.loads(stdout)
    if isinstance(envelope, dict):
        structured = envelope.get("structured_output")
        if isinstance(structured, dict):
            return structured
        result = envelope.get("result")
        if isinstance(result, dict):
            return result
        if isinstance(result, str):
            try:
                parsed = json.loads(result)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", result, re.DOTALL)
                if fenced:
                    return json.loads(fenced.group(1))
        if "judgments" in envelope:
            return envelope
    raise ValueError("Claude output did not contain structured judge data")


def run_claude_judge(
    *,
    issues: list[dict],
    review_text: str,
    model: str,
    timeout: int,
) -> tuple[dict, dict]:
    """Run Claude Code non-interactively with permissions bypassed and no tools."""
    command = [
        "claude",
        "--print",
        "--model",
        model,
        "--tools",
        "",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(JUDGE_SCHEMA, separators=(",", ":")),
    ]
    env = {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}
    started = time.monotonic()
    completed = subprocess.run(
        command,
        input=build_judge_prompt(issues, review_text),
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        check=False,
    )
    metadata = {
        "returncode": completed.returncode,
        "duration_seconds": time.monotonic() - started,
        "stderr": completed.stderr,
    }
    if completed.returncode != 0:
        raise RuntimeError(
            f"Claude judge failed ({completed.returncode}): {completed.stderr.strip()}"
        )
    return parse_claude_result(completed.stdout), metadata


def normalize_judgments(issues: list[dict], result: dict) -> list[dict]:
    """Order judgments by ground truth and mark missing/duplicate judge output."""
    by_id: dict[str, list[dict]] = defaultdict(list)
    for judgment in result.get("judgments", []):
        by_id[str(judgment.get("issue_id"))].append(judgment)

    normalized: list[dict] = []
    for issue in issues:
        candidates = by_id.get(issue["id"], [])
        if len(candidates) == 1:
            judgment = dict(candidates[0])
            judgment["judge_output_valid"] = True
        else:
            reason = "missing" if not candidates else "duplicate"
            judgment = {
                "issue_id": issue["id"],
                "detected": False,
                "confidence": "low",
                "evidence": "none",
                "reasoning": f"Invalid judge output: {reason} judgment",
                "judge_output_valid": False,
            }
        judgment["issue_type"] = issue["type"]
        normalized.append(judgment)
    return normalized


def score_review(
    *,
    review: dict,
    issues: list[dict],
    model: str,
    timeout: int,
) -> dict:
    review_text = review["path"].read_text(encoding="utf-8")
    judged, metadata = run_claude_judge(
        issues=issues,
        review_text=review_text,
        model=model,
        timeout=timeout,
    )
    judgments = normalize_judgments(issues, judged)
    detected = sum(bool(item["detected"]) for item in judgments)
    valid = sum(bool(item["judge_output_valid"]) for item in judgments)
    return {
        "label": review["label"],
        "condition": review["condition"],
        "run": review["run"],
        "review_path": str(review["path"]),
        "total_issues": len(issues),
        "detected": detected,
        "missed": len(issues) - detected,
        "recall": round(detected / len(issues), 3) if issues else 0,
        "valid_judgments": valid,
        "findings_count": len(extract_findings(review_text)),
        "unsupported_findings": judged.get("unsupported_findings", []),
        "unsupported_count": len(judged.get("unsupported_findings", [])),
        "novel_findings": judged.get("novel_findings", []),
        "novel_count": len(judged.get("novel_findings", [])),
        "quality": judged.get("quality", {}),
        "judgments": judgments,
        "judge_metadata": metadata,
    }


def aggregate(scored: list[dict]) -> dict:
    """Aggregate repeated runs by their full nested label."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    for result in scored:
        grouped[result["label"]].append(result)
    summary: dict[str, dict] = {}
    for label, runs in sorted(grouped.items()):
        summary[label] = {
            "num_runs": len(runs),
            "avg_recall": round(sum(run["recall"] for run in runs) / len(runs), 3),
            "per_run_recall": [run["recall"] for run in runs],
            "avg_unsupported": round(
                sum(run["unsupported_count"] for run in runs) / len(runs), 2
            ),
            "avg_novel": round(
                sum(run["novel_count"] for run in runs) / len(runs), 2
            ),
            "avg_usefulness": round(
                sum(run["quality"].get("usefulness", 0) for run in runs) / len(runs),
                2,
            ),
        }
    return summary


def print_report(summary: dict) -> None:
    print("\nCLAUDE JUDGE SUMMARY")
    print(f"{'Subject/model/condition':<62} {'Runs':>4} {'Recall':>8} {'Unsup.':>7} {'Useful':>7}")
    print("-" * 94)
    for label, result in summary.items():
        print(
            f"{label:<62} {result['num_runs']:>4} "
            f"{result['avg_recall']:>7.1%} {result['avg_unsupported']:>7.2f} "
            f"{result['avg_usefulness']:>7.2f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Judge code-review outputs with Claude Code")
    parser.add_argument(
        "--gt",
        type=Path,
        required=True,
        help="Frozen source-adjudicated JSON reference or legacy ground-truth YAML",
    )
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--conditions", nargs="+", help="Filter by final condition directory")
    parser.add_argument("--model", default="sonnet", help="Claude judge model or alias")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--limit", type=int, help="Judge only the first N reviews")
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()

    issues = load_ground_truth(args.gt)
    reviews = discover_reviews(
        args.results_dir,
        set(args.conditions) if args.conditions else None,
    )
    if args.limit is not None:
        reviews = reviews[: args.limit]
    if not reviews:
        raise SystemExit(f"No run-*-review.md files found under {args.results_dir}")

    print(f"Ground truth: {len(issues)} issues; reviews: {len(reviews)}")
    scored: list[dict] = []
    failures: list[dict] = []
    for index, review in enumerate(reviews, start=1):
        print(
            f"[{index}/{len(reviews)}] {review['label']} run {review['run']}...",
            end=" ",
            flush=True,
        )
        try:
            result = score_review(
                review=review,
                issues=issues,
                model=args.model,
                timeout=args.timeout,
            )
        except Exception as exc:
            print(f"FAILED: {exc}")
            failures.append({"review": str(review["path"]), "error": str(exc)})
            continue
        scored.append(result)
        print(
            f"recall={result['recall']:.1%} unsupported={result['unsupported_count']} "
            f"usefulness={result['quality'].get('usefulness', 'N/A')}"
        )

    summary = aggregate(scored)
    print_report(summary)
    output = {
        "judge": {
            "cli": "claude",
            "cli_version": command_version("claude"),
            "model": args.model,
            "tools": [],
        },
        "ground_truth": str(args.gt),
        "results_dir": str(args.results_dir),
        "summary": summary,
        "runs": scored,
        "failures": failures,
    }
    output_path = args.output or (args.results_dir / "judge-evaluation.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nDetailed results written to {output_path}")


if __name__ == "__main__":
    main()
