#!/usr/bin/env python3
"""Blind, deduplicate, and source-adjudicate novel findings from frozen-reference scoring."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from agent_eval_common import command_version, git_source_metadata
from build_review_pool import adjudicate_groups, cluster_candidates


def collect_candidates(evaluation: dict) -> tuple[list[dict], dict[str, dict]]:
    """Assign anonymous IDs while retaining origins in a private map."""
    blinded: list[dict] = []
    private: dict[str, dict] = {}
    for run in evaluation.get("runs", []):
        for finding in run.get("novel_findings", []):
            candidate_id = f"N-{len(blinded) + 1:03d}"
            blinded.append(
                {
                    "candidate_id": candidate_id,
                    "title": finding["claim"],
                    "claim": finding["claim"],
                    "file": finding["file"],
                    "symbol": finding["symbol"],
                    "evidence": finding["evidence"],
                }
            )
            private[candidate_id] = {
                "label": run["label"],
                "condition": run["condition"],
                "run": run["run"],
            }
    return blinded, private


def score_novel(
    evaluation: dict, adjudications: list[dict], private: dict[str, dict]
) -> dict:
    """Count source-validated novel groups per run and condition."""
    by_run: dict[tuple[str, int], dict] = {}
    for run in evaluation.get("runs", []):
        key = (run["label"], run["run"])
        by_run[key] = {
            "label": run["label"],
            "condition": run["condition"],
            "run": run["run"],
            "reference_matches": run["detected"],
            "frozen_reference_ids": [
                item["issue_id"]
                for item in run["judgments"]
                if item["detected"]
            ],
            "frozen_reference_recall": run["recall"],
            "unsupported_findings": run["unsupported_count"],
            "novel_submitted": 0,
            "novel_validated": 0,
            "novel_invalid": 0,
            "novel_uncertain": 0,
            "novel_ids": [],
        }

    for index, item in enumerate(adjudications, start=1):
        novel_id = f"NV-{index:03d}"
        item["novel_reference_id"] = novel_id
        touched = {
            (private[member]["label"], private[member]["run"])
            for member in item["member_ids"]
        }
        for key in touched:
            score = by_run[key]
            score["novel_submitted"] += 1
            verdict_counter = {
                "valid": "novel_validated",
                "invalid": "novel_invalid",
                "uncertain": "novel_uncertain",
            }[item["verdict"]]
            score[verdict_counter] += 1
            if item["verdict"] == "valid":
                score["novel_ids"].append(novel_id)

    conditions: dict[str, dict] = {}
    grouped: dict[str, list[dict]] = defaultdict(list)
    for score in by_run.values():
        grouped[score["condition"]].append(score)
    for condition, runs in sorted(grouped.items()):
        frozen_union = {
            reference_id
            for run in runs
            for reference_id in run["frozen_reference_ids"]
        }
        valid_union = {
            novel_id for run in runs for novel_id in run["novel_ids"]
        }
        reference_matches = sum(run["reference_matches"] for run in runs)
        novel_validated = sum(run["novel_validated"] for run in runs)
        conditions[condition] = {
            "runs": len(runs),
            "avg_frozen_reference_recall": round(
                sum(run["frozen_reference_recall"] for run in runs) / len(runs), 3
            ),
            "total_reference_matches": reference_matches,
            "distinct_frozen_reference_matches": len(frozen_union),
            "total_novel_validated_run_hits": novel_validated,
            "distinct_novel_validated": len(valid_union),
            "total_validated_run_hits": reference_matches + novel_validated,
            "avg_validated_per_run": round(
                (reference_matches + novel_validated) / len(runs), 2
            ),
            "total_distinct_validated": len(frozen_union) + len(valid_union),
            "total_novel_invalid_run_hits": sum(run["novel_invalid"] for run in runs),
            "total_unsupported": sum(run["unsupported_findings"] for run in runs),
        }
    return {"runs": list(by_run.values()), "conditions": conditions}


def render_summary(scores: dict, adjudications: list[dict]) -> str:
    lines = [
        "# Codex regular vs lean-skill evaluation",
        "",
        "## Condition summary",
        "",
        "| Condition | Runs | Frozen recall | Validated/run | Total valid hits | Distinct valid | Novel invalid | Evidence flags |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for condition, score in scores["conditions"].items():
        lines.append(
            f"| {condition} | {score['runs']} | "
            f"{score['avg_frozen_reference_recall']:.1%} | "
            f"{score['avg_validated_per_run']:.2f} | "
            f"{score['total_validated_run_hits']} | "
            f"{score['total_distinct_validated']} | "
            f"{score['total_novel_invalid_run_hits']} | "
            f"{score['total_unsupported']} |"
        )
    lines.extend(["", "## Novel adjudications", ""])
    for item in adjudications:
        lines.extend(
            [
                f"### {item['novel_reference_id']}: {item['title']}",
                "",
                f"- Verdict: {item['verdict']}",
                f"- Severity: {item['severity']}",
                f"- Location: `{item['file']}:{item['line_start']}-{item['line_end']}`",
                f"- Candidates: {', '.join(item['member_ids'])}",
                "",
                item["reasoning"],
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluation", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--claude", default="claude")
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    evaluation = json.loads(args.evaluation.read_text(encoding="utf-8"))
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    source = git_source_metadata(args.repo)
    if source["commit"] != reference["source"]["commit"]:
        raise SystemExit("Repository revision does not match the frozen reference")

    blinded, private = collect_candidates(evaluation)
    if not blinded:
        raise SystemExit("No novel findings to adjudicate")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "novel-candidates.blind.json").write_text(
        json.dumps(blinded, indent=2), encoding="utf-8"
    )
    (args.output_dir / "novel-candidate-map.private.json").write_text(
        json.dumps(private, indent=2), encoding="utf-8"
    )

    groups_path = args.output_dir / "novel-groups.blind.json"
    if groups_path.exists():
        print(f"Reusing blinded groups from {groups_path}...", flush=True)
        groups = json.loads(groups_path.read_text(encoding="utf-8"))
        cluster_meta = {"duration_seconds": 0, "reused": True}
    else:
        print(f"Clustering {len(blinded)} anonymous novel candidates...", flush=True)
        groups, cluster_meta = cluster_candidates(
            blinded, args.claude, args.model, args.timeout
        )
        groups_path.write_text(json.dumps(groups, indent=2), encoding="utf-8")
    adjudication_path = args.output_dir / "novel-adjudication.json"
    if adjudication_path.exists():
        adjudication = json.loads(adjudication_path.read_text(encoding="utf-8"))
        expected = {item["candidate_id"] for item in blinded}
        actual = {
            member
            for item in adjudication["adjudications"]
            for member in item["member_ids"]
        }
        if actual != expected:
            raise SystemExit("Persisted novel adjudication does not match candidates")
        print(f"Reusing source adjudication from {adjudication_path}...", flush=True)
        previous_manifest_path = args.output_dir / "manifest.json"
        previous_manifest = (
            json.loads(previous_manifest_path.read_text(encoding="utf-8"))
            if previous_manifest_path.exists()
            else {}
        )
        adjudication_meta = {
            "duration_seconds": previous_manifest.get("phase_seconds", {}).get(
                "adjudication", 0
            ),
            "reused": True,
        }
        delta = previous_manifest.get(
            "workspace_delta", {"created": [], "removed": [], "changed": []}
        )
    else:
        print(f"Source-adjudicating {len(groups)} novel groups...", flush=True)
        adjudication, adjudication_meta, delta = adjudicate_groups(
            repo=args.repo,
            groups=groups,
            claude_binary=args.claude,
            model=args.model,
            timeout=args.timeout,
        )
        adjudication_path.write_text(
            json.dumps(adjudication, indent=2), encoding="utf-8"
        )
    scores = score_novel(evaluation, adjudication["adjudications"], private)
    (args.output_dir / "scores.json").write_text(
        json.dumps(scores, indent=2), encoding="utf-8"
    )
    (args.output_dir / "summary.md").write_text(
        render_summary(scores, adjudication["adjudications"]), encoding="utf-8"
    )
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "frozen_reference": str(args.reference),
        "judge": {
            "cli": args.claude,
            "version": command_version(args.claude),
            "model": args.model,
        },
        "candidate_count": len(blinded),
        "group_count": len(groups),
        "workspace_delta": delta,
        "phase_seconds": {
            "clustering": cluster_meta["duration_seconds"],
            "adjudication": adjudication_meta["duration_seconds"],
        },
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(f"Wrote final A/B scores to {args.output_dir}", flush=True)


if __name__ == "__main__":
    main()
