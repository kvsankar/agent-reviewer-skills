#!/usr/bin/env python3
"""Evaluate experiment results against ground truth.

Matches review findings to ground truth vulnerabilities using:
1. Mnemonic ID type matching (e.g., SQL-INJECT -> GT-PG-01 type SQL-INJECT)
2. Function name detection in review text (e.g., "sql_lab" -> GT-PG-01)
3. CWE number matching (e.g., CWE-89 -> SQL injection items)

Computes precision, recall, F1 per condition and produces a summary table.
"""

import json
import re
import sys
from pathlib import Path

import yaml

BASE = Path(__file__).parent
RESULTS = BASE / "results"
GT_DIR = BASE / "ground-truth"


# Mapping from ground truth type to patterns that match finding IDs in reviews
GT_TYPE_PATTERNS = {
    "SQL-INJECT": [r"SQL[-_]?INJECT", r"SQLI"],
    "CMD-INJECT": [r"CMD[-_]?INJECT", r"COMMAND[-_]?INJECT"],
    "CODE-INJECT": [
        r"CODE[-_]?INJECT",
        r"EVAL[-_]",
        r"PICKLE",
        r"DESERIAL",
        r"INSEC[-_]?DES",
        r"YAML[-_]?INJECT",
        r"SSTI",
        r"IMAGEMATH",
    ],
    "XML-INJECT": [r"XML[-_]?INJECT", r"XXE", r"XML[-_]?EXTERNAL"],
    "XSS-PREVENT": [r"XSS", r"CROSS[-_]?SITE[-_]?SCRIPT"],
    "AUTHZ-CHECK": [r"AUTHZ", r"IDOR", r"BROKEN[-_]?ACCESS", r"MISSING[-_]?AUTHZ"],
    "WEAK-HASH": [r"WEAK[-_]?HASH", r"WEAK[-_]?CRYPTO", r"MD5[-_]?HASH"],
    "PATH-TRAVERSE": [r"PATH[-_]?TRAVERS", r"DIRECTORY[-_]?TRAVERS"],
    "VALIDATE-INPUT": [r"SSRF", r"OPEN[-_]?REDIRECT", r"VALIDATE[-_]?INPUT", r"REDIRECT"],
    "CSRF-PROTECT": [r"CSRF", r"MISSING[-_]?CSRF"],
    "NO-HARDCODE": [r"HARDCODE", r"NO[-_]?HARDCODE", r"JWT[-_]?WEAK", r"HARDCODED"],
    "SESSION-SECURE": [r"SESSION[-_]?SECURE", r"COOKIE[-_]?SECURE", r"INSECURE[-_]?COOKIE"],
    "PII-LOG": [r"PII[-_]?LOG", r"PII[-_]?EXPOSURE", r"LOG[-_]?INJECT"],
    "PII-ACCESS": [r"PII[-_]?ACCESS", r"PASSWORD[-_]?HASH", r"SENSITIVE[-_]?DATA"],
    "TOKEN-EXPIRE": [r"TOKEN[-_]?EXPIRE", r"WEAK[-_]?RESET", r"RESET[-_]?TOKEN", r"PREDICTABLE"],
    "COOKIE-SECURE": [r"COOKIE[-_]?SECURE", r"INSECURE[-_]?COOKIE"],
    "ERROR-SAFE": [r"ERROR[-_]?SAFE", r"ERROR[-_]?DISCLOSE", r"STACK[-_]?TRACE", r"INFO[-_]?DISCLOS"],
}

# Function names from ground truth, used to disambiguate multiple GT items of same type
GT_FUNCTIONS = {
    "pygoat": {
        "GT-PG-01": ["sql_lab"],
        "GT-PG-02": ["injection_sql_lab"],
        "GT-PG-03": ["cmd_lab"],
        "GT-PG-04": ["cmd_lab2", "eval("],
        "GT-PG-05": ["xxe_parse", "make_parser", "feature_external"],
        "GT-PG-06": ["insec_des_lab", "pickle.loads", "pickle"],
        "GT-PG-07": ["a9_lab", "yaml.load", "yaml.Loader"],
        "GT-PG-08": ["a9_lab2", "ImageMath"],
        "GT-PG-09": ["xss_lab"],
        "GT-PG-10": ["xss_lab2"],
        "GT-PG-11": ["ba_lab", "admin.*cookie"],
        "GT-PG-12": ["crypto_failure_lab", "md5("],
        "GT-PG-13": ["ssrf_lab", "path", "traversal", "open(filename"],
        "GT-PG-14": ["ssrf_lab2", "requests.get(url)"],
        "GT-PG-15": ["ssti_lab", "template injection"],
        "GT-PG-16": ["auth_failure_lab3", "csrf_exempt"],
        "GT-PG-17": ["sec_misconfig_lab3", "jwt", "SECRET_COOKIE_KEY"],
        "GT-PG-18": ["auth_lab_login", "set_cookie.*userid"],
        "GT-PG-19": ["a10_lab2", "logging.info"],
    },
    "dvna": {
        "GT-DV-01": ["userSearch", "SELECT.*FROM.*Users"],
        "GT-DV-02": ["ping", "exec(", "child_process"],
        "GT-DV-03": ["listUsersAPI", "password"],
        "GT-DV-04": ["bulkProducts", "libxmljs", "noent"],
        "GT-DV-05": ["userEditSubmit", "IDOR", "ownership"],
        "GT-DV-06": ["bulkProductsLegacy", "serialize", "unserialize"],
        "GT-DV-07": ["redirect", "req.query.url"],
        "GT-DV-08": ["calc", "mathjs", "stack trace"],
        "GT-DV-09": ["resetPw", "md5.*login", "reset.*token"],
        "GT-DV-10": ["keyboard cat", "session.*secret"],
        "GT-DV-11": ["secure: false", "cookie.*secure"],
        "GT-DV-12": ["<%- ", "products.ejs", "reflected"],
        "GT-DV-13": ["stored XSS", "<%- ", "product data"],
    },
}


def load_ground_truth(repo_name: str) -> list[dict]:
    """Load ground truth YAML for a repo."""
    gt_file = GT_DIR / f"{repo_name}.yaml"
    if not gt_file.exists():
        return []
    with open(gt_file) as f:
        data = yaml.safe_load(f)
    issues = []
    for file_entry in data.get("files", []):
        for issue in file_entry.get("issues", []):
            issue["file"] = file_entry["path"]
            issues.append(issue)
    return issues


def match_finding_to_gt_type(finding_id: str, gt_type: str) -> bool:
    """Check if a finding ID matches a ground truth type."""
    patterns = GT_TYPE_PATTERNS.get(gt_type, [])
    for pattern in patterns:
        if re.search(pattern, finding_id, re.IGNORECASE):
            return True
    return False


def find_gt_matches_in_text(review_text: str, gt_item: dict, repo_name: str) -> bool:
    """Check if a ground truth item is discussed in the review text."""
    gt_id = gt_item["id"]
    functions = GT_FUNCTIONS.get(repo_name, {}).get(gt_id, [])
    for func_pattern in functions:
        if re.search(re.escape(func_pattern), review_text, re.IGNORECASE):
            return True
    return False


def check_gt_detected(review_text: str, gt_item: dict, repo_name: str,
                      finding_ids: list[str]) -> str | None:
    """Check if a GT item is detected in the review, return matching evidence.

    Uses three methods in order:
    1. Finding ID matches GT type AND review text mentions specific instance
    2. Review text mentions function name / code pattern for this GT item
    3. CWE number match in review text

    Returns the matching evidence string, or None if not detected.
    """
    gt_id = gt_item["id"]
    gt_type = gt_item["type"]

    # Method 1: Finding ID matches GT type
    for fid in finding_ids:
        if match_finding_to_gt_type(fid, gt_type):
            # If there are function markers, verify this specific instance
            functions = GT_FUNCTIONS.get(repo_name, {}).get(gt_id, [])
            if functions:
                for func_pattern in functions:
                    if re.search(re.escape(func_pattern), review_text, re.IGNORECASE):
                        return f"ID:{fid}+TEXT:{func_pattern}"
            else:
                return f"ID:{fid}"

    # Method 2: Review text mentions function/code patterns
    functions = GT_FUNCTIONS.get(repo_name, {}).get(gt_id, [])
    for func_pattern in functions:
        if re.search(re.escape(func_pattern), review_text, re.IGNORECASE):
            return f"TEXT:{func_pattern}"

    # Method 3: CWE number match
    cwe = gt_item.get("cwe", "")
    if cwe and re.search(re.escape(cwe), review_text):
        return f"CWE:{cwe}"

    return None


def classify_finding(finding_id: str) -> str:
    """Classify a finding as 'vulnerability', 'recommendation', or 'noise'."""
    noise_ids = {
        "OWASP", "AUTHENTICATION-PRESENT", "ARGON2-USAGE", "STRUCTURED-VIEWS",
        "FRAMEWORK-CHOICE", "AUTH-DECORATOR",
    }
    recommendation_patterns = [
        r"^MISSING[-_]",  # MISSING-VALIDATION, MISSING-HEADERS, etc.
    ]
    if finding_id in noise_ids:
        return "noise"
    for pat in recommendation_patterns:
        if re.match(pat, finding_id):
            return "recommendation"
    # Check if it matches any known vulnerability type
    for gt_type, patterns in GT_TYPE_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, finding_id, re.IGNORECASE):
                return "vulnerability"
    return "other"


def evaluate_run(run_file: Path, gt_issues: list[dict], repo_name: str) -> dict:
    """Evaluate a single run against ground truth.

    Strategy: For each GT item, check if ANY evidence exists in the review
    (finding IDs, function names, CWE numbers). This avoids the problem of
    one finding "consuming" a GT item and leaving related findings as FP.

    For FP: count findings that don't match any GT vulnerability type at all,
    excluding noise/recommendation IDs.
    """
    with open(run_file) as f:
        run_data = json.load(f)

    review_text = run_data.get("output", "")
    findings = run_data.get("findings", [])
    finding_ids = [f["id"] for f in findings]

    # Phase 1: For each GT item, check if the review covers it
    detected_gt = {}
    for gt in gt_issues:
        evidence = check_gt_detected(review_text, gt, repo_name, finding_ids)
        if evidence:
            detected_gt[gt["id"]] = evidence

    tp = len(detected_gt)
    fn = len(gt_issues) - tp

    # Phase 2: Count FP — findings that are actual vulnerability claims
    # but don't correspond to any GT type present in this repo
    gt_types_present = {gt["type"] for gt in gt_issues}
    fp_findings = []
    matched_types = set()
    for fid in finding_ids:
        fclass = classify_finding(fid)
        if fclass in ("noise", "recommendation"):
            continue
        # Check if this finding matches ANY GT type in this repo
        matches_any_gt = False
        for gt_type in gt_types_present:
            if match_finding_to_gt_type(fid, gt_type):
                matches_any_gt = True
                break
        if not matches_any_gt:
            fp_findings.append(fid)

    fp = len(fp_findings)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "total_findings": len(findings),
        "total_gt": len(gt_issues),
        "detected": {k: v for k, v in detected_gt.items()},
        "missed": [
            {"id": gt["id"], "type": gt["type"], "description": gt["description"]}
            for gt in gt_issues if gt["id"] not in detected_gt
        ],
        "false_positives": fp_findings,
        "duration": run_data.get("duration_seconds", 0),
    }


def evaluate_all():
    """Evaluate all experiment results against ground truth."""
    repos_with_gt = ["pygoat", "dvna"]
    experiments = ["exp1-baseline", "exp2-ablation", "exp3-improved"]

    all_results = {}

    for exp in experiments:
        for repo in repos_with_gt:
            gt_issues = load_ground_truth(repo)
            if not gt_issues:
                print(f"  No ground truth for {repo}, skipping")
                continue

            exp_dir = RESULTS / exp / repo
            if not exp_dir.exists():
                continue

            for condition_dir in sorted(exp_dir.iterdir()):
                if not condition_dir.is_dir():
                    continue
                run_file = condition_dir / "run-1.json"
                if not run_file.exists():
                    continue

                condition = condition_dir.name
                result = evaluate_run(run_file, gt_issues, repo)
                key = f"{exp}/{repo}/{condition}"
                all_results[key] = result

    return all_results


def print_report(results: dict):
    """Print evaluation report."""
    print("=" * 100)
    print("EVALUATION REPORT: Ground Truth Matching")
    print("=" * 100)

    # Group by experiment
    for exp_name in ["exp1-baseline", "exp2-ablation", "exp3-improved"]:
        exp_results = {k: v for k, v in results.items() if k.startswith(exp_name)}
        if not exp_results:
            continue

        print(f"\n## {exp_name.upper()}")
        print(f"\n{'Condition':<45} {'TP':>4} {'FP':>4} {'FN':>4} {'Prec':>6} {'Rec':>6} {'F1':>6} {'Time':>7}")
        print("-" * 90)

        for key in sorted(exp_results.keys()):
            r = exp_results[key]
            # Shorten key for display
            parts = key.split("/")
            label = f"{parts[1]}/{parts[2]}"
            print(
                f"  {label:<43} {r['tp']:>4} {r['fp']:>4} {r['fn']:>4} "
                f"{r['precision']:>5.1%} {r['recall']:>5.1%} {r['f1']:>5.1%} "
                f"{r['duration']:>6.1f}s"
            )

    # Aggregate by condition across repos
    print("\n\n## AGGREGATE BY CONDITION (across repos)")
    print(f"\n{'Condition':<25} {'TP':>4} {'FP':>4} {'FN':>4} {'Prec':>6} {'Rec':>6} {'F1':>6}")
    print("-" * 65)

    conditions = {}
    for key, r in results.items():
        parts = key.split("/")
        cond = parts[2]
        if cond not in conditions:
            conditions[cond] = {"tp": 0, "fp": 0, "fn": 0}
        conditions[cond]["tp"] += r["tp"]
        conditions[cond]["fp"] += r["fp"]
        conditions[cond]["fn"] += r["fn"]

    for cond in ["zero-shot", "generic-prompt", "full-skill", "principles-only", "ids-only", "trimmed-20", "full-v2", "hybrid"]:
        if cond not in conditions:
            continue
        c = conditions[cond]
        tp, fp, fn = c["tp"], c["fp"], c["fn"]
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        print(f"  {cond:<23} {tp:>4} {fp:>4} {fn:>4} {prec:>5.1%} {rec:>5.1%} {f1:>5.1%}")

    # Per-experiment aggregates (fair comparison - same # runs per condition)
    for exp_name in ["exp1-baseline", "exp2-ablation", "exp3-improved"]:
        print(f"\n\n## AGGREGATE: {exp_name.upper()} only")
        print(f"\n{'Condition':<25} {'TP':>4} {'FP':>4} {'FN':>4} {'Prec':>6} {'Rec':>6} {'F1':>6}")
        print("-" * 65)
        exp_conds = {}
        for key, r in results.items():
            if not key.startswith(exp_name):
                continue
            cond = key.split("/")[2]
            if cond not in exp_conds:
                exp_conds[cond] = {"tp": 0, "fp": 0, "fn": 0}
            exp_conds[cond]["tp"] += r["tp"]
            exp_conds[cond]["fp"] += r["fp"]
            exp_conds[cond]["fn"] += r["fn"]

        order = ["zero-shot", "generic-prompt", "full-skill", "principles-only", "ids-only", "trimmed-20", "full-v2", "hybrid"]
        for cond in order:
            if cond not in exp_conds:
                continue
            c = exp_conds[cond]
            tp, fp, fn = c["tp"], c["fp"], c["fn"]
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
            print(f"  {cond:<23} {tp:>4} {fp:>4} {fn:>4} {prec:>5.1%} {rec:>5.1%} {f1:>5.1%}")

    # Detailed missed/FP analysis for full-skill
    print("\n\n## MISSED VULNERABILITIES (full-skill condition)")
    print("-" * 65)
    for key, r in sorted(results.items()):
        if "full-skill" not in key:
            continue
        if r["missed"]:
            parts = key.split("/")
            print(f"\n  {parts[0]}/{parts[1]}:")
            for m in r["missed"]:
                print(f"    MISSED: {m['id']} ({m['type']}) - {m['description']}")
        if r["false_positives"]:
            print(f"    FP: {', '.join(r['false_positives'])}")


def main():
    print("Loading ground truth and evaluating results...\n")
    results = evaluate_all()

    if not results:
        print("No results found. Run experiments first.")
        sys.exit(1)

    print_report(results)

    # Save detailed results
    output_file = RESULTS / "evaluation.json"
    output_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nDetailed results saved to {output_file}")


if __name__ == "__main__":
    main()
