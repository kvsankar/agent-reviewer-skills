#!/usr/bin/env python3
"""
Test script to verify the review tool structure without requiring API key
"""

from pathlib import Path
import sys

def test_structure():
    """Test that the review tool can find skills"""
    print("Testing review-tool structure...")
    print("=" * 60)

    # Get skills directory (parent of review-tool/)
    review_tool_dir = Path(__file__).parent
    skills_dir = review_tool_dir.parent

    print(f"[+] Review tool directory: {review_tool_dir}")
    print(f"[+] Skills directory: {skills_dir}")

    # Test skill discovery
    reviewers = [
        'agile-requirements-reviewer',
        'django-reviewer',
        'format-refactoring-reviewer',
        'functional-javascript-reviewer',
        'functional-python-reviewer',
        'python-test-reviewer',
        'refactoring-reviewer',
        'security-privacy-reviewer',
        'zen-of-python-reviewer',
    ]

    print(f"\nChecking {len(reviewers)} skills...")
    print("-" * 60)

    found = 0
    missing = []

    for reviewer in reviewers:
        skill_path = skills_dir / reviewer / 'SKILL.md'
        if skill_path.exists():
            print(f"  [+] {reviewer}")
            found += 1
        else:
            print(f"  [-] {reviewer} - NOT FOUND")
            missing.append(reviewer)

    print("=" * 60)
    print(f"Results: {found}/{len(reviewers)} skills found")

    if missing:
        print(f"\nMissing skills:")
        for skill in missing:
            print(f"  - {skill}")
        return False

    print("\n[*] All skills accessible!")
    return True

if __name__ == '__main__':
    success = test_structure()
    sys.exit(0 if success else 1)
