#!/usr/bin/env python3
"""Pool, blind, deduplicate, adjudicate, and score real-repository reviews."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from agent_eval_common import (
    command_version,
    copy_repo,
    file_snapshot,
    git_source_metadata,
    snapshot_delta,
)


EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "origin_id": {"type": "string"},
                    "source_finding_id": {"type": "string"},
                    "title": {"type": "string"},
                    "claim": {"type": "string"},
                    "file": {"type": "string"},
                    "line_or_symbol": {"type": "string"},
                    "quoted_evidence": {"type": "string"},
                    "suggested_fix": {"type": "string"},
                },
                "required": [
                    "origin_id",
                    "source_finding_id",
                    "title",
                    "claim",
                    "file",
                    "line_or_symbol",
                    "quoted_evidence",
                    "suggested_fix",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["candidates"],
    "additionalProperties": False,
}


CLUSTER_SCHEMA = {
    "type": "object",
    "properties": {
        "groups": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "group_id": {"type": "string"},
                    "title": {"type": "string"},
                    "claim": {"type": "string"},
                    "file": {"type": "string"},
                    "symbol": {"type": "string"},
                    "member_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": [
                    "group_id",
                    "title",
                    "claim",
                    "file",
                    "symbol",
                    "member_ids",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["groups"],
    "additionalProperties": False,
}


ADJUDICATION_SCHEMA = {
    "type": "object",
    "properties": {
        "adjudications": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "reference_id": {"type": "string"},
                    "verdict": {
                        "type": "string",
                        "enum": ["valid", "invalid", "uncertain"],
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                    },
                    "title": {"type": "string"},
                    "file": {"type": "string"},
                    "line_start": {"type": "integer", "minimum": 1},
                    "line_end": {"type": "integer", "minimum": 1},
                    "symbol": {"type": "string"},
                    "member_ids": {"type": "array", "items": {"type": "string"}},
                    "source_evidence": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
                "required": [
                    "reference_id",
                    "verdict",
                    "severity",
                    "title",
                    "file",
                    "line_start",
                    "line_end",
                    "symbol",
                    "member_ids",
                    "source_evidence",
                    "reasoning",
                ],
                "additionalProperties": False,
            },
        },
        "scope_notes": {"type": "string"},
    },
    "required": ["adjudications", "scope_notes"],
    "additionalProperties": False,
}


def discover_origins(pool_dir: Path) -> list[dict]:
    baseline = sorted(pool_dir.glob("claude/*/baseline-*/review.md"))
    subjects = sorted(pool_dir.glob("*/**/run-*-review.md"))
    subjects = [path for path in subjects if "claude" not in path.parts]
    if len(baseline) != 1:
        raise ValueError(f"Expected exactly one Claude baseline, found {len(baseline)}")
    origins = [
        {
            "origin_id": "B1",
            "kind": "baseline",
            "path": baseline[0],
            "label": str(baseline[0].parent.relative_to(pool_dir)),
        }
    ]
    for index, path in enumerate(subjects, start=1):
        origins.append(
            {
                "origin_id": f"X{index}",
                "kind": "subject",
                "path": path,
                "label": str(path.parent.relative_to(pool_dir)),
            }
        )
    return origins


def claude_structured(
    *,
    claude_binary: str,
    model: str,
    effort: str,
    prompt: str,
    schema: dict,
    timeout: int,
    cwd: Path | None = None,
    tools: str = "",
) -> tuple[dict, dict]:
    command = [
        claude_binary,
        "--print",
        "--safe-mode",
        "--model",
        model,
        "--effort",
        effort,
        "--tools",
        tools,
        "--dangerously-skip-permissions",
        "--no-session-persistence",
        "--no-chrome",
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(schema, separators=(",", ":")),
    ]
    env = {key: value for key, value in os.environ.items() if key != "CLAUDECODE"}
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=cwd,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Claude structured call failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    envelope = json.loads(completed.stdout)
    structured = envelope.get("structured_output")
    if not isinstance(structured, dict):
        result = envelope.get("result")
        if isinstance(result, str):
            structured = json.loads(result)
    if not isinstance(structured, dict):
        raise ValueError("Claude response did not contain structured output")
    metadata = {
        "duration_seconds": time.monotonic() - started,
        "stderr": completed.stderr,
        "envelope": envelope,
    }
    return structured, metadata


def extract_candidates(
    origins: list[dict], claude_binary: str, model: str, timeout: int
) -> tuple[list[dict], dict]:
    review_sections = []
    for origin in origins:
        review_sections.append(
            f"## REVIEW {origin['origin_id']}\n\n"
            f"{origin['path'].read_text(encoding='utf-8')}"
        )
    prompt = """Atomize the supplied code reviews into individual candidate findings.

This is transcription, not judging. Preserve every concrete issue claim, even
if it looks wrong, weak, duplicated, or contradicted. Do not merge findings from
different reviews. Split a review item only when it makes genuinely independent
claims that could receive different validity verdicts. Ignore strengths,
summaries, and generic advice without a concrete source claim. Preserve the
REVIEW origin ID exactly. Use the review's own finding ID when present; otherwise
assign a stable local ID such as ITEM-01. Do not inspect or infer repository code.

""" + "\n\n---\n\n".join(review_sections)
    result, metadata = claude_structured(
        claude_binary=claude_binary,
        model=model,
        effort="high",
        prompt=prompt,
        schema=EXTRACTION_SCHEMA,
        timeout=timeout,
        tools="",
    )
    known_origins = {origin["origin_id"] for origin in origins}
    candidates = result["candidates"]
    for candidate in candidates:
        if candidate["origin_id"] not in known_origins:
            raise ValueError(f"Unknown extracted origin: {candidate['origin_id']}")
    return candidates, metadata


def blind_candidates(candidates: list[dict]) -> tuple[list[dict], dict[str, dict]]:
    blinded: list[dict] = []
    private_map: dict[str, dict] = {}
    for index, candidate in enumerate(candidates, start=1):
        blind_id = f"C-{index:03d}"
        public = {
            key: value
            for key, value in candidate.items()
            if key not in {"origin_id", "source_finding_id"}
        }
        public["candidate_id"] = blind_id
        blinded.append(public)
        private_map[blind_id] = {
            "origin_id": candidate["origin_id"],
            "source_finding_id": candidate["source_finding_id"],
        }
    return blinded, private_map


def require_exact_members(items: list[dict], expected: set[str], field: str) -> None:
    seen = [member for item in items for member in item[field]]
    duplicates = sorted({member for member in seen if seen.count(member) > 1})
    missing = sorted(expected - set(seen))
    extras = sorted(set(seen) - expected)
    if duplicates or missing or extras:
        raise ValueError(
            f"Invalid member partition: duplicates={duplicates}, missing={missing}, "
            f"extras={extras}"
        )


def cluster_candidates(
    blinded: list[dict], claude_binary: str, model: str, timeout: int
) -> tuple[list[dict], dict]:
    prompt = f"""Group semantically duplicate code-review candidates.

Candidates belong together only when they identify the same underlying problem
in the same code. Similar principles applied to different symbols are separate.
Do not judge validity. Every candidate_id must occur exactly once across the
groups. Use group IDs G-001, G-002, and so on.

## Anonymous candidates

{json.dumps(blinded, indent=2)}
"""
    result, metadata = claude_structured(
        claude_binary=claude_binary,
        model=model,
        effort="high",
        prompt=prompt,
        schema=CLUSTER_SCHEMA,
        timeout=timeout,
        tools="",
    )
    groups = result["groups"]
    require_exact_members(groups, {item["candidate_id"] for item in blinded}, "member_ids")
    return groups, metadata


def adjudicate_groups(
    *,
    repo: Path,
    groups: list[dict],
    claude_binary: str,
    model: str,
    timeout: int,
) -> tuple[dict, dict, dict]:
    prompt = f"""Adjudicate anonymous candidate findings against the exact source
repository in the current working directory.

Explore and read the source before deciding. A valid finding must describe a
concrete, actionable defect or meaningful maintainability risk actually supported
by this revision. Intended behavior, speculative concurrency scenarios,
subjective preferences, already-safe code, and negligible observations are
invalid. Use uncertain only when source inspection cannot resolve the claim.

The preliminary groups are suggestions, not truth. Split a group when its member
claims need different verdicts; keep duplicates together otherwise. Every
candidate member_id must occur exactly once in the adjudications. Assign R-001,
R-002, and so on, without knowing or guessing candidate origins. Cite exact source
evidence and corrected line ranges. Do not modify files.

## Anonymous candidate groups

{json.dumps(groups, indent=2)}
"""
    with tempfile.TemporaryDirectory(prefix="review-pool-judge-") as name:
        work_dir = Path(name) / "repo"
        copy_repo(repo, work_dir)
        before = file_snapshot(work_dir)
        result, metadata = claude_structured(
            claude_binary=claude_binary,
            model=model,
            effort="high",
            prompt=prompt,
            schema=ADJUDICATION_SCHEMA,
            timeout=timeout,
            cwd=work_dir,
            tools="Read,Grep,Glob,Bash",
        )
        delta = snapshot_delta(before, file_snapshot(work_dir))
    expected = {member for group in groups for member in group["member_ids"]}
    require_exact_members(result["adjudications"], expected, "member_ids")
    return result, metadata, delta


def score_origins(
    origins: list[dict], adjudications: list[dict], private_map: dict[str, dict]
) -> dict:
    valid = [item for item in adjudications if item["verdict"] == "valid"]
    scores: dict[str, dict] = {}
    for origin in origins:
        origin_id = origin["origin_id"]
        touched = [
            item
            for item in adjudications
            if any(private_map[member]["origin_id"] == origin_id for member in item["member_ids"])
        ]
        valid_touched = [item for item in touched if item["verdict"] == "valid"]
        submitted = len(touched)
        scores[origin_id] = {
            "label": origin["label"],
            "kind": origin["kind"],
            "submitted_canonical_candidates": submitted,
            "validated_findings": len(valid_touched),
            "invalid_findings": sum(item["verdict"] == "invalid" for item in touched),
            "uncertain_findings": sum(item["verdict"] == "uncertain" for item in touched),
            "precision": round(len(valid_touched) / submitted, 3) if submitted else 0,
            "coverage": round(len(valid_touched) / len(valid), 3) if valid else 0,
            "reference_ids": [item["reference_id"] for item in valid_touched],
        }

    for item in valid:
        contributing = {
            private_map[member]["origin_id"] for member in item["member_ids"]
        }
        if len(contributing) == 1:
            origin_id = next(iter(contributing))
            scores[origin_id].setdefault("unique_reference_ids", []).append(
                item["reference_id"]
            )
    for score in scores.values():
        score.setdefault("unique_reference_ids", [])
        score["unique_validated_discoveries"] = len(score["unique_reference_ids"])
    return scores


def render_summary(source: dict, adjudication: dict, scores: dict) -> str:
    valid = [item for item in adjudication["adjudications"] if item["verdict"] == "valid"]
    invalid = [item for item in adjudication["adjudications"] if item["verdict"] == "invalid"]
    uncertain = [item for item in adjudication["adjudications"] if item["verdict"] == "uncertain"]
    lines = [
        "# Review Pool v1",
        "",
        f"- Upstream: `{source['upstream']}`",
        f"- Commit: `{source['commit']}`",
        f"- Valid reference findings: {len(valid)}",
        f"- Invalid candidates: {len(invalid)}",
        f"- Uncertain candidates: {len(uncertain)}",
        "",
        "## Scores",
        "",
        "| Origin | Review | Valid | Precision | Coverage | Unique |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for origin_id, score in scores.items():
        lines.append(
            f"| {origin_id} | `{score['label']}` | {score['validated_findings']} | "
            f"{score['precision']:.1%} | {score['coverage']:.1%} | "
            f"{score['unique_validated_discoveries']} |"
        )
    lines.extend(["", "## Validated Reference Inventory", ""])
    for item in valid:
        lines.extend(
            [
                f"### {item['reference_id']}: {item['title']}",
                "",
                f"- Severity: {item['severity']}",
                f"- Location: `{item['file']}:{item['line_start']}-{item['line_end']}`",
                f"- Symbol: `{item['symbol']}`",
                f"- Anonymous candidates: {', '.join(item['member_ids'])}",
                "",
                item["reasoning"],
                "",
                "```text",
                item["source_evidence"],
                "```",
                "",
            ]
        )
    lines.extend(["## Adjudication Scope Notes", "", adjudication["scope_notes"], ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an adjudicated review pool")
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--pool-dir", type=Path, required=True)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--claude", default=shutil.which("claude") or "claude")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    source = git_source_metadata(args.repo)
    origins = discover_origins(args.pool_dir)
    output_dir = args.pool_dir / "reference-v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    public_origins = [
        {key: str(value) if key == "path" else value for key, value in origin.items()}
        for origin in origins
    ]
    (output_dir / "origins.json").write_text(
        json.dumps(public_origins, indent=2), encoding="utf-8"
    )

    print(f"Extracting candidates from {len(origins)} reviews...", flush=True)
    candidates, extraction_meta = extract_candidates(
        origins, args.claude, args.model, args.timeout
    )
    blinded, private_map = blind_candidates(candidates)
    (output_dir / "candidate-map.private.json").write_text(
        json.dumps(private_map, indent=2), encoding="utf-8"
    )
    (output_dir / "candidates.blind.json").write_text(
        json.dumps(blinded, indent=2), encoding="utf-8"
    )
    print(f"Extracted {len(blinded)} anonymous candidates; clustering...", flush=True)

    groups, cluster_meta = cluster_candidates(
        blinded, args.claude, args.model, args.timeout
    )
    (output_dir / "candidate-groups.blind.json").write_text(
        json.dumps(groups, indent=2), encoding="utf-8"
    )
    print(f"Created {len(groups)} anonymous groups; adjudicating source...", flush=True)

    adjudication, adjudication_meta, delta = adjudicate_groups(
        repo=args.repo,
        groups=groups,
        claude_binary=args.claude,
        model=args.model,
        timeout=args.timeout,
    )
    scores = score_origins(origins, adjudication["adjudications"], private_map)
    valid_reference = {
        "version": 1,
        "source": source,
        "findings": [
            item for item in adjudication["adjudications"] if item["verdict"] == "valid"
        ],
    }
    (output_dir / "adjudication.json").write_text(
        json.dumps(adjudication, indent=2), encoding="utf-8"
    )
    (output_dir / "reference.json").write_text(
        json.dumps(valid_reference, indent=2), encoding="utf-8"
    )
    (output_dir / "scores.json").write_text(
        json.dumps(scores, indent=2), encoding="utf-8"
    )
    (output_dir / "summary.md").write_text(
        render_summary(source, adjudication, scores), encoding="utf-8"
    )
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "judge": {
            "cli": args.claude,
            "version": command_version(args.claude),
            "model": args.model,
            "effort": "high",
        },
        "origin_count": len(origins),
        "candidate_count": len(blinded),
        "group_count": len(groups),
        "reference_count": len(valid_reference["findings"]),
        "workspace_delta": delta,
        "phase_seconds": {
            "extraction": extraction_meta["duration_seconds"],
            "clustering": cluster_meta["duration_seconds"],
            "adjudication": adjudication_meta["duration_seconds"],
        },
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print(
        f"Reference v1: {len(valid_reference['findings'])} valid findings; "
        f"written to {output_dir}",
        flush=True,
    )


if __name__ == "__main__":
    main()
