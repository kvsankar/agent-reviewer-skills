#!/usr/bin/env python3
"""
Token counter for Claude Code SKILL.md files.

Uses the Anthropic API's count_tokens method to accurately count tokens
using the same tokenization that Claude uses.

Usage:
    # Count all SKILL.md files
    python count_tokens.py

    # Count specific file
    python count_tokens.py path/to/file.md

    # Show verbose output
    python count_tokens.py --verbose

    # Export to CSV
    python count_tokens.py --csv tokens.csv
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional
import argparse

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# Try to import tiktoken for local tokenization
try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


class TokenCounter:
    """Count tokens in files using Anthropic's tokenization."""

    # Claude Code Read tool limit (actual: 25000)
    # Using 20000 as threshold since tiktoken reports ~80% of Claude's count
    MAX_TOKENS_PER_FILE = 20000

    def __init__(self, api_key: Optional[str] = None, use_local: bool = False):
        """Initialize with API key from environment or parameter."""
        self.use_local = use_local
        self.client = None
        self.encoding = None

        if not use_local and HAS_ANTHROPIC:
            # Try to get API key from multiple sources
            self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

            # If no API key, try Claude Code OAuth credentials
            if not self.api_key:
                self.api_key = self._get_claude_oauth_token()

            if self.api_key:
                try:
                    self.client = anthropic.Anthropic(api_key=self.api_key)
                except Exception as e:
                    print(f"Warning: Could not create Anthropic client: {e}")
                    print("Falling back to local token counting")
                    self.use_local = True
            else:
                print("Warning: No authentication method found")
                print("Falling back to local token counting")
                self.use_local = True

        # Set up local tokenization if needed
        if self.use_local or not self.client:
            if HAS_TIKTOKEN:
                # Use cl100k_base encoding (closest to Claude's tokenization)
                self.encoding = tiktoken.get_encoding("cl100k_base")
                print("Using local tiktoken for token counting (approximate)")
            else:
                print("Warning: Neither anthropic nor tiktoken available")
                print("Using simple estimation (4 chars ≈ 1 token)")
                print("Install for accurate counts: uv pip install anthropic tiktoken")

    def _get_claude_oauth_token(self) -> Optional[str]:
        """Get OAuth access token from Claude Code credentials."""
        creds_path = Path.home() / ".claude" / ".credentials.json"
        if not creds_path.exists():
            return None

        try:
            with open(creds_path, 'r') as f:
                creds = json.load(f)

            oauth = creds.get("claudeAiOauth", {})
            access_token = oauth.get("accessToken")

            if access_token:
                print("Using Claude Code OAuth credentials")
                return access_token
        except Exception as e:
            print(f"Warning: Could not read Claude OAuth credentials: {e}")

        return None

    def count_tokens(self, text: str, model: str = "claude-sonnet-4-20250514") -> int:
        """
        Count tokens in text using Anthropic's tokenization.

        Args:
            text: Text to count tokens for
            model: Claude model to use for tokenization

        Returns:
            Number of tokens
        """
        # Method 1: Use Anthropic API (most accurate)
        if self.client:
            try:
                response = self.client.messages.count_tokens(
                    model=model,
                    messages=[{"role": "user", "content": text}]
                )
                return response.input_tokens
            except Exception as e:
                print(f"Warning: API token counting failed: {e}")
                print("Falling back to local counting")
                # Fall through to local methods

        # Method 2: Use tiktoken (close approximation)
        if self.encoding:
            try:
                tokens = self.encoding.encode(text)
                return len(tokens)
            except Exception as e:
                print(f"Warning: tiktoken failed: {e}")
                # Fall through to estimation

        # Method 3: Simple estimation (rough approximation)
        # Claude tokens are roughly 4 characters per token on average
        return len(text) // 4

    def count_file_tokens(self, file_path: Path, model: str = "claude-sonnet-4-20250514") -> dict:
        """
        Count tokens in a file.

        Args:
            file_path: Path to file
            model: Claude model to use for tokenization

        Returns:
            Dictionary with file info and token count
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tokens = self.count_tokens(content, model)
            file_size = os.path.getsize(file_path)

            return {
                'file': str(file_path),
                'tokens': tokens,
                'size_bytes': file_size,
                'size_kb': round(file_size / 1024, 2),
                'exceeds_limit': tokens > self.MAX_TOKENS_PER_FILE,
                'percentage': round((tokens / self.MAX_TOKENS_PER_FILE) * 100, 1)
            }
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def scan_skill_files(self, base_dir: Path = None) -> list[dict]:
        """
        Scan all SKILL.md files in reviewer directories.

        Args:
            base_dir: Base directory to scan (default: current directory)

        Returns:
            List of file info dictionaries
        """
        if base_dir is None:
            base_dir = Path(__file__).parent

        results = []
        skill_files = list(base_dir.glob("reviewers/*-reviewer/SKILL.md"))

        print(f"Found {len(skill_files)} SKILL.md files")
        print()

        for skill_file in sorted(skill_files):
            print(f"Counting tokens: {skill_file.parent.name}/SKILL.md ... ", end='', flush=True)
            result = self.count_file_tokens(skill_file)
            if result:
                results.append(result)
                status = "❌ EXCEEDS LIMIT" if result['exceeds_limit'] else "✓"
                print(f"{result['tokens']:,} tokens ({result['percentage']}%) {status}")
            else:
                print("ERROR")

        return results


def print_summary(results: list[dict]):
    """Print summary of token counts."""
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total_files = len(results)
    exceeds_limit = [r for r in results if r['exceeds_limit']]
    total_tokens = sum(r['tokens'] for r in results)

    print(f"Total files scanned: {total_files}")
    print(f"Files exceeding limit: {len(exceeds_limit)}")
    print(f"Total tokens across all files: {total_tokens:,}")
    print(f"Average tokens per file: {total_tokens // total_files:,}")

    if exceeds_limit:
        print("\n" + "-" * 80)
        print("FILES EXCEEDING 25,000 TOKEN LIMIT:")
        print("-" * 80)
        for result in sorted(exceeds_limit, key=lambda x: x['tokens'], reverse=True):
            skill_name = Path(result['file']).parent.name
            excess = result['tokens'] - TokenCounter.MAX_TOKENS_PER_FILE
            print(f"  {skill_name}")
            print(f"    Tokens: {result['tokens']:,} (exceeds by {excess:,})")
            print(f"    Percentage: {result['percentage']}%")
            print()

    # Top 5 largest files
    print("-" * 80)
    print("TOP 5 LARGEST FILES:")
    print("-" * 80)
    sorted_results = sorted(results, key=lambda x: x['tokens'], reverse=True)[:5]
    for i, result in enumerate(sorted_results, 1):
        skill_name = Path(result['file']).parent.name
        status = "❌" if result['exceeds_limit'] else "✓"
        print(f"{i}. {skill_name}: {result['tokens']:,} tokens ({result['percentage']}%) {status}")


def export_csv(results: list[dict], output_file: str):
    """Export results to CSV."""
    import csv

    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'file', 'tokens', 'percentage', 'exceeds_limit', 'size_kb'
        ])
        writer.writeheader()
        for result in sorted(results, key=lambda x: x['tokens'], reverse=True):
            writer.writerow({
                'file': Path(result['file']).parent.name,
                'tokens': result['tokens'],
                'percentage': result['percentage'],
                'exceeds_limit': result['exceeds_limit'],
                'size_kb': result['size_kb']
            })

    print(f"\nExported to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Count tokens in SKILL.md files using Anthropic's tokenization"
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='Specific file to count tokens for (default: scan all SKILL.md files)'
    )
    parser.add_argument(
        '--model',
        default='claude-sonnet-4-20250514',
        help='Claude model to use for tokenization (default: claude-sonnet-4-20250514)'
    )
    parser.add_argument(
        '--csv',
        metavar='FILE',
        help='Export results to CSV file'
    )
    parser.add_argument(
        '--local',
        action='store_true',
        help='Use local token counting (tiktoken) instead of API'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show verbose output'
    )

    args = parser.parse_args()

    counter = TokenCounter(use_local=args.local)

    if args.file:
        # Count specific file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}")
            sys.exit(1)

        result = counter.count_file_tokens(file_path, args.model)
        if result:
            print(f"File: {result['file']}")
            print(f"Tokens: {result['tokens']:,}")
            print(f"Size: {result['size_kb']} KB")
            print(f"Percentage of limit: {result['percentage']}%")
            if result['exceeds_limit']:
                excess = result['tokens'] - TokenCounter.MAX_TOKENS_PER_FILE
                print(f"❌ EXCEEDS LIMIT by {excess:,} tokens")
            else:
                remaining = TokenCounter.MAX_TOKENS_PER_FILE - result['tokens']
                print(f"✓ Within limit ({remaining:,} tokens remaining)")
    else:
        # Scan all SKILL.md files
        results = counter.scan_skill_files()

        if results:
            print_summary(results)

            if args.csv:
                export_csv(results, args.csv)


if __name__ == "__main__":
    main()
