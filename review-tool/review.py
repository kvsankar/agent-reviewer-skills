#!/usr/bin/env python3
"""
Agentic Code Review Tool

Uses Claude AI with Claude Code skills to review GitHub repositories
and generate detailed markdown reports.

Usage:
    uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --use-claude-cli
    uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --model claude-opus-4-20250514
"""

import argparse
import os
import sys
import tempfile
import shutil
import subprocess
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Protocol, Tuple
from abc import ABC, abstractmethod
from importlib.metadata import version, PackageNotFoundError

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required, can use system env vars


def get_package_version(package_name: str) -> str:
    """Get installed package version"""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "not installed"


def parse_github_url(repo_url: str) -> Tuple[str, str]:
    """
    Parse GitHub URL to extract user/org and repo name.

    Examples:
        https://github.com/django/django -> ('django', 'django')
        https://github.com/psf/requests.git -> ('psf', 'requests')
        git@github.com:user/repo.git -> ('user', 'repo')
    """
    # Remove .git suffix if present
    url = repo_url.rstrip('/').replace('.git', '')

    # Try HTTPS format: https://github.com/user/repo
    match = re.search(r'github\.com[:/]([^/]+)/([^/]+)', url)
    if match:
        return match.group(1), match.group(2)

    # Fallback: extract last two path components
    parts = url.rstrip('/').split('/')
    if len(parts) >= 2:
        return parts[-2], parts[-1]

    # If parsing fails, return repo URL as-is
    return 'unknown', repo_url.split('/')[-1]


# Available reviewers and their file patterns
REVIEWERS = {
    # Python reviewers (7)
    'python-refactoring-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for refactoring opportunities',
    },
    'python-functional-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for functional programming patterns',
    },
    'python-zen-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code against Zen of Python',
    },
    'python-format-refactoring-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for style/format refactoring',
    },
    'python-test-reviewer': {
        'patterns': ['test_*.py', '*_test.py', 'tests/*.py', 'tests/**/*.py'],
        'description': 'Reviews Python tests for quality',
    },
    'python-security-privacy-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for security and privacy issues',
    },
    'python-performance-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for performance optimization',
    },
    # JavaScript/TypeScript reviewers (7)
    'javascript-test-reviewer': {
        'patterns': ['*.test.js', '*.test.ts', '*.test.jsx', '*.test.tsx', '*.spec.js', '*.spec.ts', '**/__tests__/*.js', '**/__tests__/*.ts'],
        'description': 'Reviews JavaScript/TypeScript tests for quality',
    },
    'javascript-refactoring-reviewer': {
        'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx'],
        'description': 'Reviews JavaScript/TypeScript for refactoring opportunities',
    },
    'javascript-format-refactoring-reviewer': {
        'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx'],
        'description': 'Reviews JavaScript/TypeScript for style/format refactoring',
    },
    'javascript-functional-reviewer': {
        'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx'],
        'description': 'Reviews JavaScript/TypeScript for functional patterns',
    },
    'javascript-security-privacy-reviewer': {
        'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx'],
        'description': 'Reviews JavaScript/TypeScript for security and privacy issues',
    },
    'javascript-performance-reviewer': {
        'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx'],
        'description': 'Reviews JavaScript/TypeScript for performance optimization',
    },
    'react-reviewer': {
        'patterns': ['*.jsx', '*.tsx', '*.js', '*.ts'],
        'description': 'Reviews React code for best practices and patterns',
    },
    # Other reviewers (4)
    'agile-requirements-reviewer': {
        'patterns': ['*.md', 'requirements.txt', 'REQUIREMENTS.md', 'stories/*.md', 'docs/*.md'],
        'description': 'Reviews requirements, user stories, and specifications',
    },
    'django-reviewer': {
        'patterns': ['*.py', 'settings/*.py', 'manage.py', '**/models.py', '**/views.py', '**/serializers.py', '**/urls.py', '**/forms.py', '**/admin.py'],
        'description': 'Reviews Django projects for production readiness',
    },
    'openapi-reviewer': {
        'patterns': ['*.yaml', '*.yml', '*.json', 'openapi.*', 'swagger.*'],
        'description': 'Reviews OpenAPI/Swagger specifications',
    },
    'database-schema-reviewer': {
        'patterns': ['*.sql', 'schema.sql', 'migrations/*.sql', '**/migrations/*.py'],
        'description': 'Reviews database schemas for normalization and performance',
    },
}


def load_reviewer_tags(tags_file: Path = None) -> Dict[str, List[str]]:
    """
    Load reviewer tags from YAML configuration file.

    Args:
        tags_file: Path to tags.yaml file. If None, uses default location.

    Returns:
        Dictionary mapping tag names to lists of reviewer names.
    """
    if tags_file is None:
        # Default location: same directory as this script
        tags_file = Path(__file__).parent / 'tags.yaml'

    if not tags_file.exists():
        print(f"[!] Warning: Tags file not found: {tags_file}")
        print(f"[!] Tag expansion will not work. Using individual reviewers only.")
        return {}

    try:
        with open(tags_file, 'r', encoding='utf-8') as f:
            tags_data = yaml.safe_load(f)

        # Convert YAML structure to simple dict of tag -> list of reviewers
        tags_dict = {}
        for tag_name, tag_config in tags_data.items():
            if isinstance(tag_config, dict) and 'reviewers' in tag_config:
                tags_dict[tag_name.lower()] = tag_config['reviewers']
            else:
                print(f"[!] Warning: Invalid tag format for '{tag_name}' in {tags_file}")

        return tags_dict

    except yaml.YAMLError as e:
        print(f"[-] Error parsing tags file {tags_file}: {e}")
        return {}
    except Exception as e:
        print(f"[-] Error loading tags file {tags_file}: {e}")
        return {}


def expand_reviewer_tags(reviewer_inputs: List[str], tags_dict: Dict[str, List[str]]) -> List[str]:
    """
    Expand reviewer tags to their constituent reviewers using provided tags dictionary.

    If a tag is found in tags_dict, expand it to multiple reviewers.
    If not a tag, treat as individual reviewer name.
    Removes duplicates while preserving order.

    Args:
        reviewer_inputs: List of reviewer names or tags from command line
        tags_dict: Dictionary mapping tag names to lists of reviewers

    Returns:
        List of expanded reviewer names

    Examples:
        ['python'], tags_dict -> ['refactoring-reviewer', 'functional-python-reviewer', ...]
        ['django', 'security'], tags_dict -> ['django-reviewer', 'security-privacy-reviewer']
        ['refactoring-reviewer'], tags_dict -> ['refactoring-reviewer']
    """
    expanded = []
    seen = set()

    for item in reviewer_inputs:
        item_lower = item.lower()

        # Check if it's a tag in the loaded tags dictionary
        if item_lower in tags_dict:
            # Expand tag to reviewers
            for reviewer in tags_dict[item_lower]:
                if reviewer not in seen:
                    expanded.append(reviewer)
                    seen.add(reviewer)
        else:
            # Treat as individual reviewer name
            if item not in seen:
                expanded.append(item)
                seen.add(item)

    return expanded


def list_reviewers_and_tags(tags_file: Optional[Path] = None, skills_dir: Optional[Path] = None) -> None:
    """
    List all available reviewers and tags with descriptions.

    Args:
        tags_file: Path to tags.yaml file. If None, uses default location.
        skills_dir: Path to skills directory. If None, uses parent of script directory.
    """
    if tags_file is None:
        tags_file = Path(__file__).parent / 'tags.yaml'

    if skills_dir is None:
        # Check /skills (Docker) or parent directory (local)
        if Path('/skills').exists():
            skills_dir = Path('/skills')
        else:
            skills_dir = Path(__file__).parent.parent

    print("=" * 70)
    print("AVAILABLE REVIEWERS AND TAGS")
    print("=" * 70)

    # Load tags
    tags_data = {}
    if tags_file.exists():
        try:
            with open(tags_file, 'r', encoding='utf-8') as f:
                tags_data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load tags file: {e}\n")

    # Discover individual reviewers
    print("\nINDIVIDUAL REVIEWERS:")
    print("-" * 70)

    reviewers = []
    if skills_dir.exists():
        for item in sorted(skills_dir.iterdir()):
            if item.is_dir() and (item / 'SKILL.md').exists():
                reviewers.append(item.name)

    if reviewers:
        for reviewer in reviewers:
            print(f"  • {reviewer}")
        print(f"\nTotal: {len(reviewers)} reviewer(s)")
    else:
        print("  No reviewers found")

    # Display tags
    if tags_data:
        print("\n" + "=" * 70)
        print("TAGS (shortcuts for multiple reviewers):")
        print("-" * 70)

        for tag_name in sorted(tags_data.keys()):
            tag_config = tags_data[tag_name]
            if isinstance(tag_config, dict):
                description = tag_config.get('description', 'No description')
                reviewers_list = tag_config.get('reviewers', [])

                print(f"\n  {tag_name}")
                print(f"    Description: {description}")
                print(f"    Reviewers ({len(reviewers_list)}):")
                for rev in reviewers_list:
                    print(f"      - {rev}")

        print(f"\n{'-' * 70}")
        print(f"Total: {len(tags_data)} tag(s)")
    else:
        print("\n" + "=" * 70)
        print("No tags file found or tags file is empty")

    print("\n" + "=" * 70)
    print("\nUSAGE:")
    print("  --reviewer REVIEWER    Use individual reviewer")
    print("  --reviewer TAG         Use tag (expands to multiple reviewers)")
    print("  --reviewer TAG1 --reviewer TAG2   Combine multiple tags/reviewers")
    print("\nEXAMPLES:")
    print("  --reviewer python                    # All Python reviewers (tag)")
    print("  --reviewer django                    # Django-specific reviewers (tag)")
    print("  --reviewer refactoring-reviewer      # Single reviewer")
    print("  --reviewer security --reviewer tests # Combine tags")
    print("=" * 70)


class AIProvider(ABC):
    """Base class for AI providers"""

    @abstractmethod
    def review(self, skill_prompt: str, code_context: str, repo_url: str) -> str:
        """Perform review using the AI provider"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name"""
        pass


class ClaudeProvider(AIProvider):
    """Anthropic Claude provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514", agentic: bool = False, repo_path: Path = None, use_cli: bool = False):
        self.model = model
        self.repo_path = repo_path
        self.use_cli = use_cli
        self.agentic = agentic
        self.package_version = get_package_version('anthropic')

        if use_cli:
            # CLI mode - uses ~/.claude/.credentials.json
            # Check if claude CLI is available
            try:
                result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode != 0:
                    raise RuntimeError(f"Claude CLI not found or not working. Return code: {result.returncode}, stderr: {result.stderr}")
                print(f"[+] Using Claude CLI (version: {result.stdout.strip()})")
            except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                raise RuntimeError(
                    f"Claude CLI not found: {e}\n"
                    "Install with: npm install -g @anthropic-ai/claude-code\n"
                    "Or use API key mode instead."
                )

            # Check if credentials file exists
            creds_file = Path.home() / '.claude' / '.credentials.json'
            if not creds_file.exists():
                raise ValueError(
                    f"Claude credentials not found at {creds_file}\n"
                    "Please authenticate with: claude login"
                )

            self.client = None  # No SDK client in CLI mode
        else:
            # API key mode - uses Anthropic Python SDK
            try:
                import anthropic
            except ImportError:
                raise ImportError("anthropic package not installed. Run: uv pip install anthropic")

            self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")

            self.client = anthropic.Anthropic(api_key=self.api_key)

    @property
    def name(self) -> str:
        mode = " [AGENTIC]" if self.agentic else ""
        auth = " [CLI]" if self.use_cli else ""
        return f"Claude ({self.model}) [anthropic v{self.package_version}]{mode}{auth}"

    def review_agentic(self, skill_prompt: str, repo_url: str) -> str:
        """
        Agentic review mode - Claude explores repo with bash tools.

        WARNING: Uses dangerouslyDisableSandbox=True (SDK) or --dangerously-skip-permissions (CLI)
        Only safe in container environment!
        """
        print("  [AGENTIC] Claude will explore the repository with bash tools")
        print(f"  [AGENTIC] Repository location: {self.repo_path}")

        # Change to repo directory for bash commands
        original_cwd = Path.cwd()
        os.chdir(self.repo_path)

        try:
            # Create agentic prompt
            agentic_prompt = f"""
{skill_prompt}

---

You are reviewing the repository: {repo_url}

Repository is located at: {self.repo_path}

You have access to bash commands to explore this repository. Use commands like:
- `ls` / `find` - List and find files
- `cat` / `head` / `tail` - Read file contents
- `grep` / `rg` - Search for patterns
- `wc` - Count lines/files
- `tree` (if available) - View directory structure

IMPORTANT:
1. Start by exploring the repository structure
2. Identify files relevant to this review
3. Read and analyze the relevant files
4. Generate a comprehensive review following the skill guidelines

Work methodically:
- First understand the project structure
- Then focus on files matching the review scope
- Finally, write the detailed review in markdown format

Current working directory is the repository root. All bash commands will execute there.

Begin your review now.
"""

            # CLI mode or SDK mode?
            if self.use_cli:
                return self._review_agentic_cli(agentic_prompt)
            else:
                return self._review_agentic_sdk(agentic_prompt)

        except Exception as e:
            return f"Error during agentic review: {str(e)}"
        finally:
            # Always return to original directory
            os.chdir(original_cwd)

    def _review_agentic_sdk(self, agentic_prompt: str) -> str:
        """Agentic mode using Python SDK"""
        # Call Claude with bash tool access - DANGEROUS MODE
        print("  [AGENTIC/SDK] Calling Claude with bash tool access (dangerous mode enabled)")

        message = self.client.messages.create(
            model=self.model,
            max_tokens=16000,
            temperature=0,
            tools=[{
                "type": "bash_20241022",
                "name": "bash"
            }],
            messages=[{
                "role": "user",
                "content": agentic_prompt
            }],
            # DANGEROUS: Disable sandbox - only safe in container!
            betas=["pdfs-2024-09-25", "prompt-caching-2024-07-31", "computer-use-2024-10-22"],
            dangerouslyDisableSandbox=True
        )

        # Process response and tool use
        response_text = []
        tool_uses = 0

        for block in message.content:
            if hasattr(block, 'type'):
                if block.type == 'text':
                    response_text.append(block.text)
                elif block.type == 'tool_use':
                    tool_uses += 1
                    print(f"  [AGENTIC/SDK] Tool use #{tool_uses}: {block.name}")

        print(f"  [AGENTIC/SDK] Review complete - {tool_uses} tool uses")

        return '\n\n'.join(response_text) if response_text else "No review text generated"

    def _review_agentic_cli(self, agentic_prompt: str) -> str:
        """Agentic mode using Claude CLI with --dangerously-skip-permissions"""
        print("  [AGENTIC/CLI] Calling Claude CLI with bash tools (dangerous permissions)")

        # Call claude CLI with --print mode, --tools for bash access, --dangerously-skip-permissions
        # This allows Claude to use bash tools without approval prompts
        result = subprocess.run(
            ['claude', '--print', '--model', self.model, '--tools', 'Bash', '--dangerously-skip-permissions'],
            input=agentic_prompt,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout for exploration
        )

        if result.returncode != 0:
            error_msg = f"Error calling Claude CLI (exit code {result.returncode}):\n"
            if result.stderr:
                error_msg += f"STDERR: {result.stderr}\n"
            if result.stdout:
                error_msg += f"STDOUT: {result.stdout}\n"
            return error_msg

        print("  [AGENTIC/CLI] Review complete")
        return result.stdout

    def review_cli(self, skill_prompt: str, code_context: str, repo_url: str) -> str:
        """
        Review using Claude CLI (uses ~/.claude/.credentials.json).
        This allows Claude Code subscription users to review without API keys.
        """
        review_prompt = f"""
{skill_prompt}

---

You are reviewing the repository: {repo_url}

Please perform a comprehensive review of the following code files using the guidelines from the skill above.

{code_context}

Provide a detailed review following the structured markdown format specified in the skill.
Focus on the most critical issues first.
"""

        try:
            print("  [CLI] Calling Claude via CLI...")

            # Call claude CLI with --print mode (non-interactive) and pass prompt via stdin
            # Use --dangerously-skip-permissions since we're in a safe container environment
            # Disable tools (empty string = no tools)
            result = subprocess.run(
                ['claude', '--print', '--model', self.model, '--tools', '', '--dangerously-skip-permissions'],
                input=review_prompt,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                error_msg = f"Error calling Claude CLI (exit code {result.returncode}):\n"
                if result.stderr:
                    error_msg += f"STDERR: {result.stderr}\n"
                if result.stdout:
                    error_msg += f"STDOUT: {result.stdout}\n"
                if not result.stderr and not result.stdout:
                    error_msg += "No error output captured. This usually means:\n"
                    error_msg += "  - Claude CLI authentication issue (try: claude login)\n"
                    error_msg += "  - Token expired (open Claude Code to refresh)\n"
                    error_msg += "  - Network connectivity issue\n"
                    error_msg += f"  - Command: claude --print --model {self.model} --tools '' --dangerously-skip-permissions\n"
                return error_msg

            return result.stdout

        except subprocess.TimeoutExpired:
            return "Error: Claude CLI call timed out after 5 minutes"
        except Exception as e:
            return f"Error during Claude CLI review: {str(e)}"

    def review(self, skill_prompt: str, code_context: str, repo_url: str) -> str:
        # Use CLI mode if enabled
        if self.use_cli:
            return self.review_cli(skill_prompt, code_context, repo_url)

        # Otherwise use API key mode (SDK)
        review_prompt = f"""
{skill_prompt}

---

You are reviewing the repository: {repo_url}

Please perform a comprehensive review of the following code files using the guidelines from the skill above.

{code_context}

Provide a detailed review following the structured markdown format specified in the skill.
Focus on the most critical issues first.
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": review_prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error during Claude review: {str(e)}"


def create_provider(model: Optional[str] = None, agentic: bool = False, repo_path: Path = None, use_cli: bool = False) -> AIProvider:
    """Factory function to create Claude provider"""
    provider_class = ClaudeProvider

    try:
        if model:
            return provider_class(model=model, agentic=agentic, repo_path=repo_path, use_cli=use_cli)
        else:
            return provider_class(agentic=agentic, repo_path=repo_path, use_cli=use_cli)
    except (ImportError, ValueError, RuntimeError) as e:
        print(f"\n[-] Error initializing Claude provider: {e}")
        sys.exit(1)


class ReviewAgent:
    """Agent that performs code reviews using AI providers with skills"""

    def __init__(self, provider: AIProvider):
        self.provider = provider
        # Skills directory: check /skills (Docker volume) or parent directory (local)
        if Path('/skills').exists():
            self.skills_dir = Path('/skills')
        else:
            self.skills_dir = Path(__file__).parent.parent

    def load_skill(self, reviewer_name: str) -> str:
        """Load skill prompt from SKILL.md"""
        skill_path = self.skills_dir / reviewer_name / 'SKILL.md'

        if not skill_path.exists():
            raise FileNotFoundError(f"Skill not found: {skill_path}")

        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract content after the frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()

        return content

    def discover_files(self, repo_path: Path, patterns: List[str], max_files: int = 50) -> List[Path]:
        """Discover files matching patterns in repository"""
        files = []

        for pattern in patterns:
            # Handle glob patterns
            if '**' in pattern:
                found = list(repo_path.glob(pattern))
            else:
                found = list(repo_path.rglob(pattern))

            files.extend(found)

        # Filter out common directories to ignore
        ignore_dirs = {'.git', 'node_modules', 'venv', 'env', '.venv', '__pycache__',
                      'build', 'dist', '.eggs', '*.egg-info', '.tox', 'htmlcov'}

        filtered_files = []
        for f in files:
            if f.is_file() and not any(ignored in f.parts for ignored in ignore_dirs):
                filtered_files.append(f)

        # Sort by modification time (most recent first) and limit
        filtered_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return filtered_files[:max_files]

    def read_file_content(self, file_path: Path, max_lines: int = 500) -> str:
        """Read file content with line limit"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[:max_lines]
                content = ''.join(lines)

                if len(lines) == max_lines:
                    content += f"\n\n... (truncated, total lines: {len(lines)})"

                return content
        except Exception as e:
            return f"Error reading file: {e}"

    def prepare_code_context(self, repo_path: Path, files: List[Path]) -> str:
        """Prepare code context for review"""
        context = "# Code Files for Review\n\n"

        for file_path in files:
            rel_path = file_path.relative_to(repo_path)
            content = self.read_file_content(file_path)

            context += f"## File: {rel_path}\n\n"
            context += f"```{file_path.suffix[1:]}\n"
            context += content
            context += "\n```\n\n"

        return context

    def review(self, repo_path: Path, reviewer_name: str, repo_url: str) -> str:
        """Perform review using AI provider with skill"""
        print(f"  Loading skill: {reviewer_name}")
        skill_prompt = self.load_skill(reviewer_name)

        # Check if provider supports and is in agentic mode
        if hasattr(self.provider, 'agentic') and self.provider.agentic:
            print(f"  [AGENTIC MODE] Skipping file discovery - AI will explore")
            print(f"  Calling {self.provider.name} for agentic review...")
            return self.provider.review_agentic(skill_prompt, repo_url)

        # Standard batch review mode
        print(f"  Discovering files...")
        reviewer_config = REVIEWERS[reviewer_name]
        files = self.discover_files(repo_path, reviewer_config['patterns'])

        if not files:
            return f"# {reviewer_name} Review\n\nNo files found matching patterns: {reviewer_config['patterns']}"

        print(f"  Found {len(files)} files to review")
        print(f"  Preparing code context...")
        code_context = self.prepare_code_context(repo_path, files)

        print(f"  Calling {self.provider.name} for review...")
        return self.provider.review(skill_prompt, code_context, repo_url)


def clone_repository(repo_url: str, target_dir: Path) -> bool:
    """Clone git repository to target directory"""
    try:
        print(f"Cloning repository: {repo_url}")
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, str(target_dir)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[+] Repository cloned successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Failed to clone repository: {e.stderr}")
        return False
    except FileNotFoundError:
        print("[-] Git is not installed or not in PATH")
        return False


def generate_report(reviewer_name: str, review_content: str, repo_url: str,
                   output_dir: Path, provider_name: str) -> Path:
    """Generate markdown report with format: {user}-{repo}-{reviewer}-{provider}-{timestamp}.md"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Parse GitHub URL to get user/org and repo name
    user, repo = parse_github_url(repo_url)

    # Create filename: user-repo-reviewer-provider-timestamp.md
    filename = f"{user}-{repo}-{reviewer_name}-{provider_name}-{timestamp}.md"
    output_path = output_dir / filename

    report = f"""# {reviewer_name} Review

**Repository:** {repo_url}
**Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Reviewer:** {reviewer_name}
**AI Provider:** {provider_name}

---

{review_content}

---

*Generated by Claude Code Skills Review Tool using {provider_name}*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Agentic code review tool using AI providers with Claude Code skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available models:
  - claude-sonnet-4-20250514 (default): Fast, intelligent model for daily use
  - claude-opus-4-20250514: Most capable model for complex tasks

Available reviewers (18 total):

  Python (7):
    python-refactoring-reviewer, python-functional-reviewer, python-zen-reviewer,
    python-format-refactoring-reviewer, python-test-reviewer,
    python-security-privacy-reviewer, python-performance-reviewer

  JavaScript/TypeScript (7):
    javascript-test-reviewer, javascript-refactoring-reviewer,
    javascript-format-refactoring-reviewer, javascript-functional-reviewer,
    javascript-security-privacy-reviewer, javascript-performance-reviewer,
    react-reviewer

  Other (4):
    agile-requirements-reviewer, django-reviewer, openapi-reviewer,
    database-schema-reviewer

Available tags:
  python, javascript/js, react, django, security, testing/tests, functional/fp,
  quality, complete/all

Examples:
  # Review Python project (7 reviewers)
  uv run review.py --repo https://github.com/pallets/flask --reviewer python --use-claude-cli

  # Review React/JS project (7 reviewers)
  uv run review.py --repo https://github.com/user/react-app --reviewer javascript --use-claude-cli

  # Single reviewer
  uv run review.py --repo https://github.com/user/repo --reviewer python-security-privacy-reviewer

  # Multiple reviewers
  uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --reviewer security-privacy-reviewer --use-claude-cli
        """
    )

    parser.add_argument(
        '--repo',
        help='GitHub repository URL to review'
    )

    parser.add_argument(
        '--reviewer',
        action='append',
        help='Reviewer(s) or tag(s) to use (can specify multiple times). '
             'Tags are defined in tags.yaml and can be customized. '
             'Use --list-reviewers to see all available options.'
    )


    parser.add_argument(
        '--model',
        help='Claude model to use (e.g., claude-sonnet-4-20250514, claude-opus-4-20250514)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('reviews'),
        help='Output directory for review reports (default: reviews)'
    )

    parser.add_argument(
        '--keep-repo',
        action='store_true',
        help='Keep cloned repository after review'
    )

    parser.add_argument(
        '--auth',
        choices=['oauth', 'apikey'],
        default='oauth',
        help='Authentication method: "oauth" (uses ~/.claude credentials, default) or "apikey" (uses ANTHROPIC_API_KEY)'
    )

    parser.add_argument(
        '--mode',
        choices=['agentic', 'batch'],
        default='agentic',
        help='Review mode: "agentic" (AI explores repo with tools, default) or "batch" (sends all files at once)'
    )

    # Legacy support for old flags (hidden, will be converted)
    parser.add_argument('--use-claude-cli', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--no-agentic', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--agentic', action='store_true', help=argparse.SUPPRESS)

    parser.add_argument(
        '--list-reviewers',
        action='store_true',
        help='List all available reviewers and tags, then exit'
    )

    args = parser.parse_args()

    # Handle legacy flags (convert to new format)
    if args.use_claude_cli:
        args.auth = 'oauth'
    if args.no_agentic:
        args.mode = 'batch'

    # Handle --list-reviewers flag
    if args.list_reviewers:
        list_reviewers_and_tags()
        sys.exit(0)

    # Validate required arguments (only needed when not listing)
    if not args.repo:
        parser.error('--repo is required (use --list-reviewers to see available reviewers)')
    if not args.reviewer:
        parser.error('--reviewer is required (use --list-reviewers to see available reviewers)')

    # Check OAuth mode requirements
    if args.auth == 'oauth':
        # Check if credentials file exists (will be mounted in container)
        creds_file = Path.home() / '.claude' / '.credentials.json'
        if not creds_file.exists():
            print("[-] Error: OAuth credentials not found")
            print(f"    Expected at: {creds_file}")
            print("")
            print("In Docker, make sure credentials are mounted:")
            print("  - ~/.claude/.credentials.json:/home/appuser/.claude/.credentials.json:ro")
            print("")
            print("Or authenticate locally: claude login")
            print("")
            print("To use API key mode instead:")
            print("  ./review-cli.py --repo URL --reviewer TAG --auth apikey")
            sys.exit(1)

        print(f"[+] Authentication: OAuth (Claude CLI)")

    # Check API key mode requirements
    if args.auth == 'apikey':
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            print("[-] Error: ANTHROPIC_API_KEY not found")
            print("")
            print("Set your API key:")
            print("  export ANTHROPIC_API_KEY=sk-ant-your-key-here")
            print("Or add to .env file")
            print("")
            print("Get your API key from: https://console.anthropic.com/")
            print("")
            print("To use OAuth mode instead:")
            print("  ./review-cli.py --repo URL --reviewer TAG --auth oauth --mode batch")
            sys.exit(1)

        print(f"[+] Authentication: API Key")

    # Set review mode
    use_agentic = (args.mode == 'agentic')
    print(f"[+] Review mode: {args.mode.capitalize()}")

    # Check agentic mode requirements
    if use_agentic:
        # Check if in container
        in_container = os.environ.get('IN_CONTAINER', '').lower() == 'true'

        if not in_container:
            print("=" * 60)
            print("[!] ERROR: Agentic Mode Requires Container")
            print("=" * 60)
            print("Agentic mode enables Claude to run bash commands.")
            print("This is potentially dangerous outside a container.")
            print("")
            print("Please run in Docker:")
            print("  ./review-cli.py --repo URL --reviewer TAG --auth apikey --mode agentic")
            print("")
            print("Or disable agentic mode:")
            print("  ./review-cli.py --repo URL --reviewer TAG --mode batch")
            print("=" * 60)
            sys.exit(1)

    # Load reviewer tags from YAML configuration
    tags_dict = load_reviewer_tags()

    # Expand reviewer tags to actual reviewers
    original_inputs = args.reviewer.copy()
    expanded_reviewers = expand_reviewer_tags(args.reviewer, tags_dict)

    # Validate all reviewers exist
    invalid_reviewers = [r for r in expanded_reviewers if r not in REVIEWERS]
    if invalid_reviewers:
        print(f"[-] Error: Invalid reviewer(s): {', '.join(invalid_reviewers)}")
        print(f"\nAvailable reviewers: {', '.join(sorted(REVIEWERS.keys()))}")
        if tags_dict:
            print(f"\nAvailable tags: {', '.join(sorted(tags_dict.keys()))}")
        else:
            print(f"\n[!] No tags loaded. Check tags.yaml file.")
        sys.exit(1)

    # Update args with expanded reviewers
    args.reviewer = expanded_reviewers

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Claude Code Skills Review Tool")
    print("=" * 60)
    print(f"Repository: {args.repo}")

    # Show tag expansion if tags were used
    if original_inputs != expanded_reviewers:
        print(f"Input: {', '.join(original_inputs)}")
        print(f"Expanded to {len(expanded_reviewers)} reviewer(s): {', '.join(expanded_reviewers)}")
    else:
        print(f"Reviewers: {', '.join(args.reviewer)}")
    print(f"AI Provider: claude")
    if args.model:
        print(f"Model: {args.model}")
    print(f"Output: {args.output_dir}")
    print("=" * 60)

    # Create temp directory for cloning
    temp_dir = None
    try:
        temp_dir = Path(tempfile.mkdtemp(prefix='code_review_'))
        print(f"\nWorking directory: {temp_dir}")

        # Clone repository
        if not clone_repository(args.repo, temp_dir):
            sys.exit(1)

        # Create provider (after cloning, so we have repo_path for agentic mode)
        use_cli = (args.auth == 'oauth')
        provider = create_provider(args.model, use_agentic, temp_dir, use_cli)
        print(f"\n[+] Using {provider.name}")

        # Initialize review agent with provider
        agent = ReviewAgent(provider)

        # Perform reviews
        reports = []
        for reviewer in args.reviewer:
            print(f"\n{'=' * 60}")
            print(f"Running {reviewer}")
            print(f"{'=' * 60}")

            review_content = agent.review(temp_dir, reviewer, args.repo)
            report_path = generate_report(
                reviewer,
                review_content,
                args.repo,
                args.output_dir,
                'claude'
            )

            print(f"[+] Review complete: {report_path}")
            reports.append(report_path)

        # Summary
        print(f"\n{'=' * 60}")
        print("Review Summary")
        print(f"{'=' * 60}")
        print(f"[+] Completed {len(reports)} review(s) using {provider.name}")
        print(f"\nReports generated:")
        for report in reports:
            print(f"  - {report}")

        print(f"\n[*] All reviews complete!")

    except KeyboardInterrupt:
        print("\n\n[-] Review interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        # Cleanup
        if temp_dir and temp_dir.exists() and not args.keep_repo:
            print(f"\nCleaning up temporary directory...")
            shutil.rmtree(temp_dir, ignore_errors=True)
        elif args.keep_repo and temp_dir:
            print(f"\nRepository kept at: {temp_dir}")


if __name__ == '__main__':
    main()
