# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of 23 Claude Code skills for code review, requirements analysis, and software quality. Each skill is a specialized reviewer that provides detailed analysis with concrete examples, mnemonic IDs, and actionable recommendations.

The repository consists of:
- **23 skill directories** (`*-reviewer/`) containing SKILL.md, README.md, and SOURCES.md
- **Installation script** (`install_skills.py`) for automated deployment to Windows/WSL
- **Review tool** (`review-tool/`) for automated GitHub repository reviews using the Claude Agent SDK

## Repository Structure

```
claude-skills/
├── *-reviewer/              # 23 skill directories
│   ├── SKILL.md            # Skill definition and review guidelines
│   ├── README.md           # User documentation
│   └── SOURCES.md          # Attribution and references
├── review-tool/            # Agentic review tool
│   ├── review-cli.py       # Python wrapper
│   ├── review.py           # Core review logic
│   ├── tags.yaml           # Reviewer tag definitions
│   ├── Dockerfile
│   └── docker-compose.yml
└── install_skills.py       # Cross-platform installer
```

## Available Skills

### Python Skills (8)
- `python-refactoring-reviewer` - Code smells, SOLID, design patterns
- `python-functional-reviewer` - Functional programming patterns
- `python-zen-reviewer` - PEP 20 principles
- `python-format-refactoring-reviewer` - Style through refactoring
- `python-test-reviewer` - Test quality and strategies
- `python-security-privacy-reviewer` - Security, OWASP, GDPR
- `python-performance-reviewer` - Performance optimization
- `python-rhodes-reviewer` - Brandon Rhodes' Pythonic patterns

### JavaScript/TypeScript Skills (8)
- `javascript-test-reviewer` - Jest, Vitest, Testing Library
- `javascript-refactoring-reviewer` - SOLID, modern patterns
- `javascript-format-refactoring-reviewer` - ESLint/Prettier fixes
- `javascript-functional-reviewer` - FP patterns
- `javascript-security-privacy-reviewer` - XSS, CSRF, OWASP
- `javascript-performance-reviewer` - Performance optimization
- `react-reviewer` - React best practices, hooks
- `javascript-react-native-expo-reviewer` - React Native with Expo

### Mobile Testing Skills (1)
- `appium-test-reviewer` - Appium mobile automation tests

### Other Skills (6)
- `agile-requirements-reviewer` - Requirements, user stories
- `django-reviewer` - Django production readiness
- `openapi-reviewer` - OpenAPI/Swagger specs
- `database-schema-reviewer` - Normalization, indexing
- `code-authenticity-reviewer` - AI/LLM fabrication detection
- `playwright-test-reviewer` - E2E tests, flaky patterns

## Common Commands

### Installation

```bash
# Install all skills to Windows and WSL
python install_skills.py

# Manual installation (Linux/Mac)
cp -r *-reviewer ~/.claude/skills/

# Manual installation (Windows PowerShell)
Copy-Item -Recurse "*-reviewer" "$env:USERPROFILE\.claude\skills\"
```

### Review Tool

```bash
# Navigate to review tool
cd review-tool

# Basic review (OAuth + Agentic - default)
./review-cli.py --repo <URL> --reviewer python

# Multiple reviewers using tags
./review-cli.py --repo <URL> --reviewer python    # All 8 Python reviewers
./review-cli.py --repo <URL> --reviewer javascript # All 8 JS reviewers
./review-cli.py --repo <URL> --reviewer mobile     # React Native + Appium
./review-cli.py --repo <URL> --reviewer complete   # All 23 reviewers

# Batch mode (small repos only)
./review-cli.py --repo <URL> --reviewer python --mode batch

# API key mode
export ANTHROPIC_API_KEY='sk-ant-...'
./review-cli.py --repo <URL> --reviewer python --auth apikey

# List available reviewers
./review-cli.py --list-reviewers
```

### Quality Tools

```bash
# Run markdownlint (pre-commit hook)
pre-commit run markdownlint --all-files

# Check markdown manually
markdownlint --config .markdownlint.json **/*.md
```

## Architecture Notes

### Skill Structure

Each skill directory must contain:
1. **SKILL.md** - The main skill prompt that Claude executes
2. **README.md** - User-facing documentation
3. **SOURCES.md** - Attribution and authoritative references

Skills are self-contained with no external dependencies. All guidelines are embedded in SKILL.md.

### Installation Script (`install_skills.py`)

**Key implementation details:**

- Detects WSL vs Windows via `/proc/version`
- WSL mode: Installs to local `~/.claude/skills/` + Windows path via `/mnt/c/`
- Windows mode: Installs to local `%USERPROFILE%\.claude\skills\` + WSL via `wsl.exe`
- Uses `shutil.copytree()` to copy entire skill directories
- Removes existing directories before copying (always latest version)

**Windows home discovery logic:**
1. Primary: Query `%USERPROFILE%` via `cmd.exe`, convert with `wslpath`
2. Fallback: Scan `/mnt/` drives for `.claude` directory

### Review Tool Architecture

**Two-tier design:**

1. **review-cli.py** (Python wrapper)
   - Validates arguments and prerequisites
   - Sets up `.env` with `USER_ID` and `GROUP_ID` for permission handling
   - Launches Docker container with proper volume mounts

2. **review.py** (Container script)
   - Clones repository
   - Loads skill definitions from `/skills` mount
   - Two modes:
     - **Agentic** (default): Claude explores repo with bash tools (ls, cat, grep)
     - **Batch**: Discovers 50 most recent files matching patterns
   - Uses Claude Agent SDK for API calls
   - Generates markdown reports in `/app/reviews`

**Volume mounts:**
- `~/.claude` → `/home/appuser/.claude` (OAuth credentials)
- `../` → `/skills` (all skill SKILL.md files)
- `./reviews` → `/app/reviews` (output)
- `./review.py` → `/app/review.py` (live code - no rebuild needed)

**Authentication:**
- OAuth (default): Uses `~/.claude/.credentials.json` from Claude Code
- API Key: Uses `ANTHROPIC_API_KEY` environment variable

**Reviewer tags** (tags.yaml):
- Tags expand to multiple reviewers (e.g., `python` → 8 reviewers)
- Each reviewer runs independently with fresh context
- Prevents cross-contamination between reviews
- Mobile tags: `mobile`, `react-native`, `expo`, `appium`

### Key Files

- `.markdownlint.json` - Markdown linting rules (used by pre-commit)
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `.claude/settings.json` - Claude Code project settings
- `review-tool/tags.yaml` - Reviewer tag-to-reviewer mappings

## Claude Code Token Limits

**IMPORTANT:** Understanding these limits is critical when working with SKILL.md files.

### Per-File Token Limit (Read Tool)
- **Maximum: 25,000 tokens per file**
- Files exceeding this limit cannot be read directly with the Read tool
- Example: `playwright-test-reviewer/SKILL.md` has 29,294 tokens (exceeds limit)

**Workarounds for large files:**
```bash
# Use offset and limit parameters
Read(file_path="path/to/large.md", offset=0, limit=500)
Read(file_path="path/to/large.md", offset=500, limit=500)

# Use Grep to search for specific content
Grep(pattern="specific-section", path="path/to/large.md")

# Use Task tool with an agent to process the file
Task(subagent_type="Explore", prompt="Analyze the playwright reviewer skill")
```

### Context Window Limits
- **Standard session:** 200,000 tokens total (all input + output)
- **Extended (beta):** 1,000,000 tokens (Claude Sonnet 4/4.5 only)
- The entire conversation (files read, messages, tool results) counts toward this limit

### SKILL.md File Size Guidelines

When creating or modifying SKILL.md files:

1. **Keep under 25,000 tokens** for direct Read tool access
2. **Current status of skills:**
   - Most skills: Under 25K tokens ✓
   - `playwright-test-reviewer/SKILL.md`: 29,294 tokens (exceeds limit)
3. **If a SKILL.md must be larger:**
   - Structure with clear section headers for Grep searching
   - Document sections in README.md for easy navigation
   - Consider splitting very large guidelines into focused subsections

### File Size Checking

```bash
# Check token count of a file before reading
# Claude Code will warn if file exceeds 25,000 tokens
```

## Development Workflow

### Adding a New Skill

1. Create skill directory: `mkdir new-reviewer`
2. Add required files:
   - `SKILL.md` - Review prompt and guidelines
   - `README.md` - User documentation
   - `SOURCES.md` - Attribution
3. Update `review-tool/review.py`:
   - Add to `REVIEWERS` dict with patterns and description
4. Optionally update `review-tool/tags.yaml` to include in tags
5. Run `python install_skills.py` to install

### Modifying Skills

- **SKILL.md changes:** Take effect immediately (skills are read at runtime)
- **Review tool changes:** Take effect immediately (mounted as volume)
- **Dockerfile changes:** Require rebuild: `docker-compose build --no-cache`

### Testing Skills

```bash
# Test individual skill via review tool
cd review-tool
./review-cli.py --repo <test-repo-url> --reviewer <skill-name>

# Check output in reviews/ directory
ls -l reviews/
```

## Important Conventions

### Skill Design Principles

1. **Self-contained:** All guidelines in SKILL.md, no external files
2. **Mnemonic IDs:** Each finding has memorable ID (e.g., SQL-INJECT, USE-CONST)
3. **Concrete examples:** Before/after code snippets
4. **Attribution:** All sources documented in SOURCES.md
5. **Educational:** Explain "why" not just "what"

### Code Quality Standards

- Skills focus on **quality over quantity** - detailed analysis beats surface-level pattern matching
- Multiple testing strategies with trade-offs (not just one "right way")
- Industry best practices from authoritative sources (OWASP, PEP 8, Jest docs, etc.)
- Severity ratings for all findings (CRITICAL, HIGH, MEDIUM, LOW)

### Review Tool Design

- **Agentic mode is default:** Handles repos of any size, more thorough
- **Batch mode:** Faster but may fail on large repos with "prompt too long"
- **Fresh context per reviewer:** Each review is independent
- **No rebuild workflow:** Code changes via volume mounts
- **User-owned files:** Container runs as user's UID/GID

## Troubleshooting

### Installation Issues

**Windows home not found:**
- Ensure Claude Code is installed on Windows
- Verify `.claude` directory exists in `%USERPROFILE%`
- Check `/mnt/c/Users/<username>/.claude` exists from WSL

**WSL not detected:**
- Verify WSL 2 is installed: `wsl --list --verbose`
- Check `/proc/version` contains "microsoft" or "wsl"

### Review Tool Issues

**"Docker not found":**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**"Claude credentials not found":**
```bash
claude login
ls ~/.claude/.credentials.json  # Should exist
```

**Permission errors on reviews:**
```bash
sudo chown -R $(id -u):$(id -g) reviews/
```

**"Prompt too long" in batch mode:**
- Switch to agentic mode (default): `./review-cli.py --repo URL --reviewer NAME`
- Or reduce repo size

## Repository Maintenance

This repository is designed for minimal maintenance:

- Skills are independent - updates don't affect others
- Review tool uses volume mounts - no rebuild for code changes
- Installation script is cross-platform - works on Windows and WSL
- All dependencies in container - no host setup needed

When updating skills, focus on:
1. Accuracy of guidelines (match authoritative sources)
2. Quality of examples (complete, runnable code)
3. Attribution (SOURCES.md must be current)
4. User documentation (README.md clarity)
