#!/usr/bin/env python3
"""Generate SKILL.md variants for experiments.

Variants:
  full          - Original SKILL.md unchanged
  principles    - Code blocks stripped, principles/why/risk preserved
  ids-only      - Just the Key Guidelines section + output format
  trimmed-N     - Only first N guidelines
  selected      - Only guidelines matching given IDs
"""

import re
import sys
from pathlib import Path


DETAILED_GUIDELINES_HEADING = re.compile(
    r"^#\s+(?:Complete\b.*Guidelines|Python Coding Guidelines\b)"
)


def starts_detailed_guidelines(line: str) -> bool:
    """Return whether a top-level heading starts full guideline detail."""
    return bool(DETAILED_GUIDELINES_HEADING.match(line))


def strip_code_blocks(content: str) -> str:
    """Remove code blocks that follow Vulnerable/Secure/Bad/Good labels.

    Preserves all other content: frontmatter, mission, process,
    guideline headers, risk descriptions, why explanations, compliance refs.
    """
    lines = content.split("\n")
    result = []
    skip_until_fence_close = False
    skip_label = False

    # Labels that precede code blocks we want to strip
    label_pattern = re.compile(
        r"^\*\*(Vulnerable|Secure|Bad|Good|Before|After|"
        r"Anti-pattern|Preferred|Wrong|Correct|"
        r"Problematic|Suggested|Code Smell|Current|Improved|"
        r"Problematic code|Improved code|Slow|Fast|"
        r"Bad Example|Good Example|Secure implementation|"
        r"Vulnerable code)[^*]*\*\*",
        re.IGNORECASE,
    )

    i = 0
    while i < len(lines):
        line = lines[i]

        # If we're inside a code fence we're skipping
        if skip_until_fence_close:
            if line.strip().startswith("```"):
                skip_until_fence_close = False
                skip_label = False
            i += 1
            continue

        # Check if this line is a label preceding a code block
        if label_pattern.match(line.strip()):
            # Look ahead for a code fence
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and lines[j].strip().startswith("```"):
                # Skip the label line, blank lines, and code fence
                skip_until_fence_close = True
                skip_label = True
                i = j + 1  # skip past the opening ```
                continue

        result.append(line)
        i += 1

    return "\n".join(result)


def extract_ids_only(content: str) -> str:
    """Extract only frontmatter + mission + Key Guidelines + output format.

    This gives the LLM the mnemonic IDs and one-line descriptions
    without any detailed guidelines or code examples.
    """
    lines = content.split("\n")
    result = []
    section = "start"

    # Sections to keep: frontmatter, mission/review process, key guidelines, output format
    # Section to skip: "# Complete ... Guidelines" and everything under it
    keep_sections = True

    for line in lines:
        # Stop keeping when we hit the complete guidelines section
        if starts_detailed_guidelines(line):
            keep_sections = False
            continue

        # Also stop at "## 1." which starts detailed guidelines in some skills
        if not keep_sections:
            # But resume if we hit Expected Good Patterns or similar end sections
            if re.match(r"^##\s+(Expected Good Patterns|Quick Reference|Performance Wisdom|React Wisdom)", line):
                keep_sections = True

        if keep_sections:
            result.append(line)

    return "\n".join(result)


def trim_guidelines(content: str, n: int) -> str:
    """Keep only the first N guidelines from the complete guidelines section."""
    lines = content.split("\n")
    result = []
    guideline_count = 0
    in_guidelines = False
    done_trimming = False

    for line in lines:
        if done_trimming:
            # After trimming, look for end sections to include
            if re.match(r"^##\s+(Expected Good Patterns|Quick Reference)", line):
                done_trimming = False
                result.append(line)
            continue

        # Detect start of complete guidelines
        if starts_detailed_guidelines(line):
            in_guidelines = True
            result.append(line)
            continue

        if in_guidelines:
            # Count guideline headers
            if re.match(r"^###\s+[A-Z][A-Z0-9-]+:", line):
                guideline_count += 1
                if guideline_count > n:
                    done_trimming = True
                    result.append("")
                    result.append(f"> *{n} of the most relevant guidelines shown. Remaining guidelines omitted.*")
                    result.append("")
                    continue

        if not done_trimming:
            result.append(line)

    return "\n".join(result)


def select_guidelines(content: str, ids: list[str]) -> str:
    """Keep only guidelines matching the given mnemonic IDs."""
    lines = content.split("\n")
    result = []
    in_guidelines = False
    current_guideline_lines = []
    current_id = None
    ids_set = set(ids)

    def flush_guideline():
        nonlocal current_guideline_lines, current_id
        if current_id and current_id in ids_set:
            result.extend(current_guideline_lines)
        current_guideline_lines = []
        current_id = None

    for line in lines:
        if starts_detailed_guidelines(line):
            in_guidelines = True
            result.append(line)
            continue

        if not in_guidelines:
            result.append(line)
            continue

        # Category headers (## N. Category)
        if re.match(r"^##\s+", line) and not re.match(r"^###", line):
            flush_guideline()
            result.append(line)
            continue

        # Guideline header
        match = re.match(r"^###\s+([A-Z][A-Z0-9-]+):", line)
        if match:
            flush_guideline()
            current_id = match.group(1)
            current_guideline_lines = [line]
            continue

        if current_id:
            current_guideline_lines.append(line)
        else:
            result.append(line)

    flush_guideline()
    return "\n".join(result)


def hybrid_variant(content: str, priority_ids: list[str]) -> str:
    """Create a hybrid variant: ids-only checklist + full detail for priority guidelines.

    The ids-only checklist focuses the model on what to look for, while
    detailed examples for hard-to-detect categories provide the depth needed
    for subtle issues (authorization, session, token predictability).
    """
    ids_section = extract_ids_only(content)
    selected = select_guidelines(content, priority_ids)

    # Extract just the detailed guidelines from the selected output
    # (skip the duplicated frontmatter/mission which is already in ids_section)
    lines = selected.split("\n")
    detail_lines = []
    in_guidelines = False
    for line in lines:
        if starts_detailed_guidelines(line):
            in_guidelines = True
        if in_guidelines:
            detail_lines.append(line)

    detail_section = "\n".join(detail_lines)

    return f"""{ids_section}

---

# Detailed Guidelines for Hard-to-Detect Issues

The following guidelines require extra attention. These vulnerability classes are
frequently missed because they require understanding application logic and trust
boundaries, not just recognizing dangerous API calls.

{detail_section}
"""


# Default priority IDs: categories that models consistently miss
SECURITY_PRIORITY_IDS = [
    "AUTHZ-CHECK",
    "SESSION-SECURE",
    "TOKEN-EXPIRE",
    "TOKEN-PREDICT",
    "VALIDATE-INPUT",
    "COOKIE-SECURE",
    "CSRF-TOKEN",
    "CSRF-PROTECT",
]


def generate_variant(skill_path: Path, variant: str, **kwargs) -> str:
    """Generate a skill variant.

    Args:
        skill_path: Path to the original SKILL.md
        variant: One of 'full', 'principles', 'ids-only', 'trimmed-N', 'selected', 'hybrid'
        **kwargs: Extra args (ids for 'selected', priority_ids for 'hybrid')

    Returns:
        Modified SKILL.md content
    """
    content = skill_path.read_text(encoding="utf-8")

    if variant == "full":
        return content
    elif variant == "principles":
        return strip_code_blocks(content)
    elif variant == "ids-only":
        return extract_ids_only(content)
    elif variant.startswith("trimmed-"):
        n = int(variant.split("-")[1])
        return trim_guidelines(content, n)
    elif variant == "selected":
        ids = kwargs.get("ids", [])
        if not ids:
            raise ValueError("'selected' variant requires 'ids' kwarg")
        return select_guidelines(content, ids)
    elif variant == "hybrid":
        priority_ids = kwargs.get("priority_ids", SECURITY_PRIORITY_IDS)
        return hybrid_variant(content, priority_ids)
    else:
        raise ValueError(f"Unknown variant: {variant}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate SKILL.md variants")
    parser.add_argument("skill_path", type=Path, help="Path to SKILL.md")
    parser.add_argument(
        "variant",
        choices=["full", "principles", "ids-only", "trimmed-20", "trimmed-40", "selected", "hybrid"],
        help="Variant type",
    )
    parser.add_argument("--ids", nargs="+", help="Guideline IDs for 'selected' variant")
    parser.add_argument("--output", "-o", type=Path, help="Output file (default: stdout)")

    args = parser.parse_args()
    result = generate_variant(args.skill_path, args.variant, ids=args.ids or [])

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
        # Count guidelines in output
        count = len(re.findall(r"^### [A-Z][A-Z0-9-]+:", result, re.MULTILINE))
        print(f"Written to {args.output} ({count} guidelines, {len(result)} chars)")
    else:
        print(result)


if __name__ == "__main__":
    main()
