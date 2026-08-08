#!/usr/bin/env python3
"""Run Rhodes skill experiment on real-world code (doit repo).

No ground truth - qualitative comparison + judge assessment of flagged issues.
"""

import json
import subprocess
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

ZERO_SHOT = """Review the following Python code for quality, style, and design issues.
For each issue found:
1. Give it a short identifier
2. Show the problematic code
3. Show the improved code
4. Explain why the change matters

Output your review in markdown format."""

GENERIC = """You are an expert Python code reviewer.
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

RHODES_PRIORITY_IDS = [
    "NO-MOCK", "NO-CALL", "TOP-DOWN", "COPERNICAN",
    "BREAK-TEST", "PASS-FUNC", "PREBOUND-METHOD", "NO-SCATTERED-IFS",
]


def build_code_context(code_files: dict) -> str:
    parts = []
    for filename, content in code_files.items():
        parts.append(f"\n### File: {filename}\n\n```python\n{content}\n```\n\n")
    return "".join(parts)


def run_claude_conditions(code_context: str, output_dir: Path, skill_path: Path):
    """Run all 4 Claude conditions."""
    conditions = {
        "zero-shot": ZERO_SHOT,
        "generic-prompt": GENERIC,
        "full-skill": generate_variant(skill_path, "full"),
        "hybrid": generate_variant(skill_path, "hybrid", priority_ids=RHODES_PRIORITY_IDS),
    }

    results = {}
    for cond_name, prompt in conditions.items():
        print(f"\n  [{cond_name}] ({len(prompt)} chars prompt)")
        cond_dir = output_dir / cond_name
        cond_dir.mkdir(parents=True, exist_ok=True)
        (cond_dir / "prompt.md").write_text(prompt, encoding="utf-8")

        print(f"    Run 1/1...", end=" ", flush=True)
        result = run_review(prompt, code_context)

        if result["success"]:
            result["findings"] = extract_findings(result["output"])
            result["findings_count"] = len(result["findings"])
        else:
            result["findings"] = []
            result["findings_count"] = 0

        (cond_dir / "run-1.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        (cond_dir / "run-1-review.md").write_text(result["output"], encoding="utf-8")

        status = "OK" if result["success"] else "FAILED"
        print(f"{status} ({result['duration_seconds']:.1f}s, {result['findings_count']} findings)")

        results[cond_name] = {
            "findings": result["findings_count"],
            "duration": result["duration_seconds"],
            "finding_ids": [f["id"] for f in result["findings"]],
        }
        time.sleep(3)

    return results


def run_codex_condition(code_context: str, output_dir: Path):
    """Run Codex zero-shot review."""
    cond_dir = output_dir / "codex-zero-shot"
    cond_dir.mkdir(parents=True, exist_ok=True)

    prompt = f"""{ZERO_SHOT}

{code_context}"""

    (cond_dir / "prompt.md").write_text(ZERO_SHOT, encoding="utf-8")

    print(f"\n  [codex-zero-shot]")
    print(f"    Run 1/1...", end=" ", flush=True)

    start = time.time()
    try:
        env = {k: v for k, v in __import__("os").environ.items() if k != "CLAUDECODE"}
        result = subprocess.run(
            ["codex", "exec", "--full-auto", "--ephemeral",
             "-o", str(cond_dir / "run-1-review.md"),
             prompt],
            capture_output=True,
            text=True,
            timeout=300,
            env=env,
        )
        duration = time.time() - start

        # The review is in the -o file, but also extract from stdout
        review_file = cond_dir / "run-1-review.md"
        if review_file.exists():
            review_text = review_file.read_text(encoding="utf-8")
        else:
            # Extract from stdout - find the review content
            import re
            output = result.stdout + result.stderr
            start_idx = output.find("# ")
            if start_idx == -1:
                start_idx = output.find("## ")
            if start_idx == -1:
                start_idx = output.find("### ")
            if start_idx > 0:
                review_text = output[start_idx:]
            else:
                review_text = output
            review_file.write_text(review_text, encoding="utf-8")

        findings = extract_findings(review_text)
        print(f"OK ({duration:.1f}s, {len(findings)} findings)")

        # Save metadata
        meta = {
            "output": review_text[:500] + "...",
            "duration_seconds": duration,
            "model": "gpt-5.3-codex",
            "findings": findings,
            "findings_count": len(findings),
            "condition": "codex-zero-shot",
            "run": 1,
            "success": True,
        }
        (cond_dir / "run-1.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        return {
            "findings": len(findings),
            "duration": duration,
            "finding_ids": [f["id"] for f in findings],
        }

    except Exception as e:
        duration = time.time() - start
        print(f"FAILED ({duration:.1f}s): {e}")
        return {"findings": 0, "duration": duration, "finding_ids": []}


def main():
    print("=" * 70)
    print("RHODES REAL-WORLD EXPERIMENT (doit repo)")
    print(f"Started at {datetime.now().isoformat()}")
    print("=" * 70)

    skill_path = SKILLS / "python-rhodes-reviewer" / "SKILL.md"
    code_files = load_code_files([
        REPOS / "doit-repo" / "doit" / "action.py",
        REPOS / "doit-repo" / "doit" / "runner.py",
    ])
    total_lines = sum(c.count("\n") for c in code_files.values())
    print(f"Files: {len(code_files)}, Lines: {total_lines}")

    code_context = build_code_context(code_files)
    output_dir = RESULTS / "exp-rhodes-realworld" / "doit"

    # Run Claude conditions
    claude_results = run_claude_conditions(code_context, output_dir, skill_path)

    # Run Codex
    codex_result = run_codex_condition(code_context, output_dir)
    claude_results["codex-zero-shot"] = codex_result

    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"\n{'Condition':<20} {'Findings':>8} {'Duration':>10} {'Finding IDs'}")
    print("-" * 90)
    for cond, data in sorted(claude_results.items()):
        ids = ", ".join(data["finding_ids"][:10])
        if len(data["finding_ids"]) > 10:
            ids += f" (+{len(data['finding_ids']) - 10} more)"
        print(f"  {cond:<18} {data['findings']:>8} {data['duration']:>8.1f}s  {ids}")

    # Save
    results_file = output_dir / "review_results.json"
    results_file.write_text(
        json.dumps({"timestamp": datetime.now().isoformat(), **claude_results}, indent=2),
        encoding="utf-8",
    )
    print(f"\nResults saved to {results_file}")


if __name__ == "__main__":
    main()
