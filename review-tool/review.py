#!/usr/bin/env python3
"""
Agentic Code Review Tool

Uses AI coding agents (Claude, OpenAI, Gemini) with Claude Code skills to review
GitHub repositories and generate detailed markdown reports.

Usage:
    uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --provider claude
    uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --provider openai --model gpt-4
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
    'agile-requirements-reviewer': {
        'patterns': ['*.md', 'requirements.txt', 'REQUIREMENTS.md', 'stories/*.md', 'docs/*.md'],
        'description': 'Reviews requirements, user stories, and specifications',
    },
    'django-reviewer': {
        'patterns': ['*.py', 'settings/*.py', 'manage.py', '**/models.py', '**/views.py', '**/serializers.py', '**/urls.py', '**/forms.py', '**/admin.py'],
        'description': 'Reviews Django projects for production readiness',
    },
    'format-refactoring-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for style/format refactoring',
    },
    'functional-javascript-reviewer': {
        'patterns': ['*.js', '*.jsx', '*.ts', '*.tsx'],
        'description': 'Reviews JavaScript/TypeScript for functional patterns',
    },
    'functional-python-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for functional programming patterns',
    },
    'python-test-reviewer': {
        'patterns': ['test_*.py', '*_test.py', 'tests/*.py', 'tests/**/*.py'],
        'description': 'Reviews Python tests for quality',
    },
    'refactoring-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code for refactoring opportunities',
    },
    'security-privacy-reviewer': {
        'patterns': ['*.py', '*.js', '*.ts', '*.java', '*.go', '*.rb'],
        'description': 'Reviews code for security and privacy issues',
    },
    'zen-of-python-reviewer': {
        'patterns': ['*.py'],
        'description': 'Reviews Python code against Zen of Python',
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
        self.agentic = agentic
        self.repo_path = repo_path
        self.use_cli = use_cli
        self.package_version = get_package_version('anthropic')

        if use_cli:
            # CLI mode - uses ~/.claude/.credentials.json
            # Check if claude CLI is available
            try:
                result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode != 0:
                    raise RuntimeError("Claude CLI not found or not working")
                print(f"[+] Using Claude CLI (version: {result.stdout.strip()})")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                raise RuntimeError(
                    "Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-cli\n"
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

        WARNING: Uses dangerouslyDisableSandbox=True
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

            # Call Claude with bash tool access - DANGEROUS MODE
            print("  [AGENTIC] Calling Claude with bash tool access (dangerous mode enabled)")

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
                betas=["pdfs-2024-09-25", "prompt-caching-2024-07-31", "computer-use-2024-10-22"]
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
                        print(f"  [AGENTIC] Tool use #{tool_uses}: {block.name}")

            print(f"  [AGENTIC] Review complete - {tool_uses} tool uses")

            return '\n\n'.join(response_text) if response_text else "No review text generated"

        except Exception as e:
            return f"Error during agentic review: {str(e)}"
        finally:
            # Always return to original directory
            os.chdir(original_cwd)

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

            # Write prompt to temp file (CLI reads from file or stdin)
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(review_prompt)
                prompt_file = f.name

            try:
                # Call claude CLI
                result = subprocess.run(
                    ['claude', 'chat', '--file', prompt_file, '--model', self.model],
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )

                if result.returncode != 0:
                    return f"Error calling Claude CLI: {result.stderr}"

                return result.stdout

            finally:
                # Cleanup temp file
                import os
                try:
                    os.unlink(prompt_file)
                except:
                    pass

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


class OpenAIProvider(AIProvider):
    """OpenAI provider (GPT-4, GPT-4 Turbo, etc.)"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: uv pip install openai")

        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")

        self.model = model
        self.package_version = get_package_version('openai')
        self.client = OpenAI(api_key=self.api_key)

    @property
    def name(self) -> str:
        return f"OpenAI ({self.model}) [openai v{self.package_version}]"

    def review(self, skill_prompt: str, code_context: str, repo_url: str) -> str:
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer using established best practices and security guidelines."
                    },
                    {
                        "role": "user",
                        "content": review_prompt
                    }
                ],
                max_tokens=16000,
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during OpenAI review: {str(e)}"


class GeminiProvider(AIProvider):
    """Google Gemini provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("google-generativeai package not installed. Run: uv pip install google-generativeai")

        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not set")

        self.model_name = model
        self.package_version = get_package_version('google-generativeai')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)

    @property
    def name(self) -> str:
        return f"Gemini ({self.model_name}) [google-generativeai v{self.package_version}]"

    def review(self, skill_prompt: str, code_context: str, repo_url: str) -> str:
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
            response = self.model.generate_content(
                review_prompt,
                generation_config={
                    'temperature': 0,
                    'max_output_tokens': 16000,
                }
            )
            return response.text
        except Exception as e:
            return f"Error during Gemini review: {str(e)}"


def create_provider(provider_name: str, model: Optional[str] = None, agentic: bool = False, repo_path: Path = None, use_cli: bool = False) -> AIProvider:
    """Factory function to create AI provider"""
    providers = {
        'claude': ClaudeProvider,
        'openai': OpenAIProvider,
        'gemini': GeminiProvider,
    }

    if provider_name not in providers:
        raise ValueError(f"Unknown provider: {provider_name}. Choose from: {', '.join(providers.keys())}")

    provider_class = providers[provider_name]

    try:
        # Claude supports agentic mode and CLI authentication
        if provider_name == 'claude':
            if model:
                return provider_class(model=model, agentic=agentic, repo_path=repo_path, use_cli=use_cli)
            else:
                return provider_class(agentic=agentic, repo_path=repo_path, use_cli=use_cli)
        else:
            # Other providers don't support agentic mode or CLI yet
            if model:
                return provider_class(model=model)
            else:
                return provider_class()
    except (ImportError, ValueError, RuntimeError) as e:
        print(f"\n[-] Error initializing {provider_name} provider: {e}")
        sys.exit(1)


class ReviewAgent:
    """Agent that performs code reviews using AI providers with skills"""

    def __init__(self, provider: AIProvider):
        self.provider = provider
        # Skills are in parent directory
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
Available providers:
  - claude: Anthropic Claude (claude-sonnet-4, claude-opus-4)
  - openai: OpenAI GPT models (gpt-4, gpt-4-turbo-preview, gpt-3.5-turbo)
  - gemini: Google Gemini (gemini-pro, gemini-pro-vision)

Available reviewers:
  - agile-requirements-reviewer: Requirements and user stories
  - django-reviewer: Django production readiness
  - format-refactoring-reviewer: Python style refactoring
  - functional-javascript-reviewer: JavaScript functional patterns
  - functional-python-reviewer: Python functional patterns
  - python-test-reviewer: Python test quality
  - refactoring-reviewer: Python refactoring opportunities
  - security-privacy-reviewer: Security and privacy issues
  - zen-of-python-reviewer: Zen of Python principles

Examples:
  # Using Claude
  uv run review.py --repo https://github.com/django/django --reviewer django-reviewer --provider claude

  # Using OpenAI
  uv run review.py --repo https://github.com/user/repo --reviewer security-privacy-reviewer --provider openai --model gpt-4

  # Using Gemini
  uv run review.py --repo https://github.com/user/repo --reviewer refactoring-reviewer --provider gemini

  # Multiple reviewers
  uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --reviewer security-privacy-reviewer --provider claude
        """
    )

    parser.add_argument(
        '--repo',
        required=True,
        help='GitHub repository URL to review'
    )

    parser.add_argument(
        '--reviewer',
        action='append',
        required=True,
        help='Reviewer(s) or tag(s) to use (can specify multiple times). '
             'Tags are defined in tags.yaml and can be customized. '
             'See TAGS.md for details.'
    )

    parser.add_argument(
        '--provider',
        default='claude',
        choices=['claude', 'openai', 'gemini'],
        help='AI provider to use (default: claude)'
    )

    parser.add_argument(
        '--model',
        help='Specific model to use (provider-dependent)'
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
        '--agentic',
        action='store_true',
        help='Enable agentic mode (AI explores repo with tools). '
             'Requires container environment for safety. '
             'Currently supports Claude only. More expensive but thorough.'
    )

    parser.add_argument(
        '--use-claude-cli',
        action='store_true',
        help='Use Claude CLI with ~/.claude credentials instead of API key. '
             'Allows Claude Code subscription users to review without API keys. '
             'Requires Claude CLI installed and credentials mounted in container.'
    )

    args = parser.parse_args()

    # Check CLI mode requirements
    if args.use_claude_cli:
        if args.provider != 'claude':
            print(f"[-] Error: --use-claude-cli only works with Claude provider")
            print(f"    You specified: {args.provider}")
            sys.exit(1)

        # Check if credentials file exists (will be mounted in container)
        creds_file = Path.home() / '.claude' / '.credentials.json'
        if not creds_file.exists():
            print("[-] Error: Claude credentials not found")
            print(f"    Expected at: {creds_file}")
            print("")
            print("In Docker, make sure credentials are mounted:")
            print("  - ~/.claude/.credentials.json:/root/.claude/.credentials.json:ro")
            print("")
            print("Or authenticate locally: claude login")
            sys.exit(1)

        print("[+] Claude CLI mode enabled")

    # Check agentic mode requirements
    if args.agentic:
        # Check if in container
        in_container = os.environ.get('IN_CONTAINER', '').lower() == 'true'

        if not in_container:
            print("=" * 60)
            print("[!] WARNING: Agentic Mode Requires Container")
            print("=" * 60)
            print("Agentic mode enables AI to run bash commands with full access.")
            print("This is potentially dangerous outside a container.")
            print("")
            print("Please run in Docker:")
            print("  docker-compose run --rm reviewer --repo URL --reviewer TAG --agentic")
            print("")
            print("Or build and run manually:")
            print("  docker build -f review-tool/Dockerfile -t claude-reviewer .")
            print("  docker run --rm -v $(pwd)/reviews:/app/reviews \\")
            print("    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \\")
            print("    claude-reviewer --repo URL --reviewer TAG --agentic")
            print("=" * 60)
            sys.exit(1)

        # Check provider is Claude (only supported for now)
        if args.provider != 'claude':
            print(f"[-] Error: Agentic mode currently only supports Claude provider")
            print(f"    You specified: {args.provider}")
            print(f"    Future versions will support OpenAI and Gemini")
            sys.exit(1)

        print("[+] Agentic mode enabled (containerized environment detected)")

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
    print(f"AI Provider: {args.provider}")
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
        provider = create_provider(args.provider, args.model, args.agentic, temp_dir, args.use_claude_cli)
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
                args.provider
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
