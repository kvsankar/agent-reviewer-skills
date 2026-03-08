#!/usr/bin/env python3
"""Run all experiments and produce a summary report.

Experiments:
  1. Baseline: zero-shot vs generic-prompt vs full-skill (3 repos)
  2. Ablation: full vs principles-only vs ids-only vs trimmed-20 (3 repos)

Repos:
  - pygoat (Python/Django, 19 known vulnerabilities)
  - dvna (Node.js, 13 known vulnerabilities)
  - auth (real codebase, no ground truth)
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Add experiments dir to path
sys.path.insert(0, str(Path(__file__).parent))

from experiment_runner import run_experiment_condition, load_code_files

BASE = Path(__file__).parent
REPOS = BASE / "repos"
RESULTS = BASE / "results"
SKILLS = BASE.parent  # claude-skills root


def run_exp1_baseline():
    """Experiment 1: With skill vs without skill."""
    print("=" * 70)
    print("EXPERIMENT 1: BASELINE (zero-shot vs generic vs full-skill)")
    print("=" * 70)

    targets = [
        {
            "name": "pygoat",
            "skill": SKILLS / "python-security-privacy-reviewer" / "SKILL.md",
            "files": [REPOS / "pygoat" / "introduction" / "views.py"],
            "ground_truth": 19,
        },
        {
            "name": "dvna",
            "skill": SKILLS / "javascript-security-privacy-reviewer" / "SKILL.md",
            "files": [
                REPOS / "dvna" / "core" / "appHandler.js",
                REPOS / "dvna" / "core" / "authHandler.js",
                REPOS / "dvna" / "server.js",
            ],
            "ground_truth": 13,
        },
        {
            "name": "auth",
            "skill": SKILLS / "python-security-privacy-reviewer" / "SKILL.md",
            "files": [
                Path("/home/sankar/sankar/projects/auth/backend/authentication/services.py"),
            ],
            "ground_truth": None,  # no ground truth
        },
    ]

    conditions = [
        ("zero-shot", None, None),
        ("generic-prompt", None, None),
        ("full-skill", "SKILL_PATH", "full"),
    ]

    all_results = {}

    for target in targets:
        print(f"\n--- {target['name'].upper()} ---")
        code_files = load_code_files(target["files"])
        total_lines = sum(c.count("\n") for c in code_files.values())
        print(f"  Files: {len(code_files)}, Lines: {total_lines}")

        output_dir = RESULTS / "exp1-baseline" / target["name"]

        for cond_name, skill_placeholder, variant in conditions:
            skill = target["skill"] if skill_placeholder else None
            print(f"\n  [{cond_name}]")
            results = run_experiment_condition(
                condition_name=cond_name,
                skill_path=skill,
                variant=variant,
                code_files=code_files,
                output_dir=output_dir,
            )
            key = f"{target['name']}/{cond_name}"
            all_results[key] = {
                "findings": results[0]["findings_count"],
                "duration": results[0]["duration_seconds"],
                "finding_ids": [f["id"] for f in results[0]["findings"]],
                "ground_truth": target["ground_truth"],
            }
            time.sleep(3)  # rate limit buffer

    return all_results


def run_exp3_improved():
    """Experiment 3: Test improved guidelines + hybrid prompt structure."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: IMPROVED (full-v2 vs hybrid vs ids-only)")
    print("=" * 70)

    targets = [
        {
            "name": "pygoat",
            "skill": SKILLS / "python-security-privacy-reviewer" / "SKILL.md",
            "files": [REPOS / "pygoat" / "introduction" / "views.py"],
            "ground_truth": 19,
        },
        {
            "name": "dvna",
            "skill": SKILLS / "javascript-security-privacy-reviewer" / "SKILL.md",
            "files": [
                REPOS / "dvna" / "core" / "appHandler.js",
                REPOS / "dvna" / "core" / "authHandler.js",
                REPOS / "dvna" / "server.js",
            ],
            "ground_truth": 13,
        },
    ]

    conditions = [
        ("full-v2", "full"),
        ("hybrid", "hybrid"),
        ("ids-only", "ids-only"),
    ]

    all_results = {}

    for target in targets:
        print(f"\n--- {target['name'].upper()} ---")
        code_files = load_code_files(target["files"])

        output_dir = RESULTS / "exp3-improved" / target["name"]

        for cond_name, variant in conditions:
            print(f"\n  [{cond_name}]")
            results = run_experiment_condition(
                condition_name=cond_name,
                skill_path=target["skill"],
                variant=variant,
                code_files=code_files,
                output_dir=output_dir,
            )
            key = f"{target['name']}/{cond_name}"
            all_results[key] = {
                "findings": results[0]["findings_count"],
                "duration": results[0]["duration_seconds"],
                "finding_ids": [f["id"] for f in results[0]["findings"]],
                "ground_truth": target["ground_truth"],
            }
            time.sleep(3)

    return all_results


def run_exp2_ablation():
    """Experiment 2: Full skill vs principles-only vs ids-only vs trimmed-20."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: ABLATION (full vs principles vs ids-only vs trimmed-20)")
    print("=" * 70)

    targets = [
        {
            "name": "pygoat",
            "skill": SKILLS / "python-security-privacy-reviewer" / "SKILL.md",
            "files": [REPOS / "pygoat" / "introduction" / "views.py"],
            "ground_truth": 19,
        },
        {
            "name": "dvna",
            "skill": SKILLS / "javascript-security-privacy-reviewer" / "SKILL.md",
            "files": [
                REPOS / "dvna" / "core" / "appHandler.js",
                REPOS / "dvna" / "core" / "authHandler.js",
                REPOS / "dvna" / "server.js",
            ],
            "ground_truth": 13,
        },
        {
            "name": "auth",
            "skill": SKILLS / "python-security-privacy-reviewer" / "SKILL.md",
            "files": [
                Path("/home/sankar/sankar/projects/auth/backend/authentication/services.py"),
            ],
            "ground_truth": None,
        },
    ]

    conditions = [
        ("full-skill", "full"),
        ("principles-only", "principles"),
        ("ids-only", "ids-only"),
        ("trimmed-20", "trimmed-20"),
    ]

    all_results = {}

    for target in targets:
        print(f"\n--- {target['name'].upper()} ---")
        code_files = load_code_files(target["files"])

        output_dir = RESULTS / "exp2-ablation" / target["name"]

        for cond_name, variant in conditions:
            print(f"\n  [{cond_name}]")
            results = run_experiment_condition(
                condition_name=cond_name,
                skill_path=target["skill"],
                variant=variant,
                code_files=code_files,
                output_dir=output_dir,
            )
            key = f"{target['name']}/{cond_name}"
            all_results[key] = {
                "findings": results[0]["findings_count"],
                "duration": results[0]["duration_seconds"],
                "finding_ids": [f["id"] for f in results[0]["findings"]],
                "ground_truth": target["ground_truth"],
            }
            time.sleep(3)

    return all_results


def print_summary(exp1_results, exp2_results):
    """Print combined summary report."""
    print("\n" + "=" * 70)
    print("EXPERIMENT RESULTS SUMMARY")
    print("=" * 70)

    print("\n## Experiment 1: Baseline (With Skill vs Without)")
    print(f"\n{'Repo/Condition':<30} {'Findings':>8} {'Duration':>10} {'Finding IDs'}")
    print("-" * 90)
    for key, data in sorted(exp1_results.items()):
        ids = ", ".join(data["finding_ids"][:8])
        if len(data["finding_ids"]) > 8:
            ids += f" (+{len(data['finding_ids']) - 8} more)"
        gt = f" (GT: {data['ground_truth']})" if data["ground_truth"] else ""
        print(f"  {key:<28} {data['findings']:>8} {data['duration']:>8.1f}s  {ids}{gt}")

    print("\n## Experiment 2: Ablation (Skill Variants)")
    print(f"\n{'Repo/Condition':<30} {'Findings':>8} {'Duration':>10} {'Finding IDs'}")
    print("-" * 90)
    for key, data in sorted(exp2_results.items()):
        ids = ", ".join(data["finding_ids"][:8])
        if len(data["finding_ids"]) > 8:
            ids += f" (+{len(data['finding_ids']) - 8} more)"
        gt = f" (GT: {data['ground_truth']})" if data["ground_truth"] else ""
        print(f"  {key:<28} {data['findings']:>8} {data['duration']:>8.1f}s  {ids}{gt}")

    # Save full results
    all_data = {
        "timestamp": datetime.now().isoformat(),
        "experiment_1_baseline": exp1_results,
        "experiment_2_ablation": exp2_results,
    }
    results_file = RESULTS / "all_results.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    results_file.write_text(json.dumps(all_data, indent=2))
    print(f"\nFull results saved to {results_file}")


def main():
    print(f"Starting experiments at {datetime.now().isoformat()}")
    print(f"Model: claude-sonnet-4-20250514")
    print()

    exp1_results = run_exp1_baseline()
    exp2_results = run_exp2_ablation()
    print_summary(exp1_results, exp2_results)

    print(f"\nCompleted at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
