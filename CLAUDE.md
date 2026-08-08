# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a concluded experiment containing 23 Claude Code skills for code review,
requirements analysis, and software quality. The final real-code evaluation did
not show a material advantage over ordinary Codex review. Preserve the skills
and harness for reproducibility; do not expand the collection as an active
product. See `docs/experiment-conclusion-2026-08-08.md`.

The repository consists of:
- **23 skill directories** (`*-reviewer/`) containing SKILL.md, README.md, and SOURCES.md
- **Installation script** (`install_skills.py`) for automated deployment to Windows/WSL
- **Evaluation harness** (`experiments/`) for direct Ollama, Pi agentic, Codex
  baseline, and Claude judge runs
- **Deprecated review tool** (`review-tool/`) retained for historical
  reproducibility

## Repository Structure

```
claude-skills/
├── *-reviewer/              # 23 skill directories
│   ├── SKILL.md            # Skill definition and review guidelines
│   ├── README.md           # User documentation
│   └── SOURCES.md          # Attribution and references
├── experiments/            # Current two-track evaluation harness
│   ├── run_ollama.py       # Direct, non-agentic Ollama runner
│   ├── run_pi_agentic.py   # Pi + Ollama agentic runner
│   ├── run_codex_agentic.py # Codex agentic baseline
│   ├── evaluate_judge.py   # Tool-free frozen-reference matcher
│   └── adjudicate_novel_findings.py # Source-aware novel finding judge
├── review-tool/            # Deprecated Docker/Agent SDK harness
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

### Evaluation Harness

```bash
# One source-aware Claude seed review (candidate findings, not ground truth)
python3 experiments/run_claude_baseline.py \
  --repo experiments/repos/doit-repo \
  --output experiments/results/real-pool/doit

# Direct non-agentic benchmark on tsmac Ollama
python3 experiments/run_ollama.py --models qwen3-coder:30b \
  --code experiments/repos/doit-repo/doit/action.py \
  --output experiments/results/direct-real/doit

# Agentic local-model benchmark through Pi
python3 experiments/run_pi_agentic.py --models qwen3-coder:30b \
  --repo experiments/repos/doit-repo \
  --output experiments/results/agentic-real/doit

# Codex agentic baseline
python3 experiments/run_codex_agentic.py \
  --repo experiments/repos/doit-repo \
  --output experiments/results/agentic-real/doit

# Claude Code semantic judge
python3 experiments/evaluate_judge.py \
  --gt experiments/results/real-pool/doit/reference-v1/reference.json \
  --results-dir experiments/results/agentic-real/doit

# Harness regression tests
PYTHONPATH=experiments python3 -m unittest discover \
  -s experiments -p 'test_*.py' -v
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

### Evaluation Harness Architecture

The current harness uses matched prompt conditions across two tracks:

1. `run_ollama.py` sends the complete code fixture directly to Ollama. This
   isolates instruction-following and review quality without tools.
2. `run_pi_agentic.py` lets the same local models explore a disposable repository
   through Pi in non-interactive mode. It records JSONL events and tool use.
3. `run_codex_agentic.py` runs the same task with `codex exec --yolo` as the
   hosted agentic baseline.
4. `evaluate_judge.py` runs Claude Code non-interactively with no tools and a
   JSON schema to match each review against a frozen reference.
5. `adjudicate_novel_findings.py` anonymizes unmatched findings and uses a
   separate source-aware Claude pass before recalculating the overall findings.

The Docker and Claude Agent SDK implementation in `review-tool/` is deprecated.
Do not add new evaluation features there. See `docs/evaluation-harness.md`.

### Key Files

- `.markdownlint.json` - Markdown linting rules (used by pre-commit)
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `.claude/settings.json` - Claude Code project settings
- `docs/evaluation-harness.md` - Current benchmark design and operating guide
- `review-tool/` - Deprecated historical harness

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
3. Add or update an evaluation fixture and ground-truth YAML when measurable
   coverage is required
4. Run `python install_skills.py` to install

### Modifying Skills

- **SKILL.md changes:** Take effect immediately (skills are read at runtime)
- **Evaluation harness changes:** Run the regression tests before a benchmark
- **Deprecated review tool changes:** Avoid unless reproducing a historical run

### Testing Skills

```bash
# Test evaluation plumbing without model calls
PYTHONPATH=experiments python3 -m unittest discover \
  -s experiments -p 'test_*.py' -v

# Run a one-model, one-condition smoke before a matrix
python3 experiments/run_ollama.py \
  --models qwen3-coder:30b --conditions zero-shot --runs 1 \
  --code experiments/repos/doit-repo/doit/action.py \
  --output experiments/results/smoke-real/doit
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

### Evaluation Design

- Keep non-agentic and agentic results separate; they answer different questions.
- Use only code from immutable revisions of real production repositories. Do not
  use benchmark-authored, synthetic, or planted-defect fixtures.
- Do not use deliberately vulnerable training applications as primary evidence;
  their issue distributions are intentionally contrived.
- Use matched models, prompt conditions, fixtures, and run counts where possible.
- Treat deterministic ground truth as primary and the Claude judge as semantic
  interpretation, not truth by fiat.
- Agentic runs use fresh disposable repository copies and ephemeral sessions.
- Yolo permission bypass is not a security boundary; use only trusted fixtures
  and prompts unless an external sandbox is added.

## Troubleshooting

### Installation Issues

**Windows home not found:**
- Ensure Claude Code is installed on Windows
- Verify `.claude` directory exists in `%USERPROFILE%`
- Check `/mnt/c/Users/<username>/.claude` exists from WSL

**WSL not detected:**
- Verify WSL 2 is installed: `wsl --list --verbose`
- Check `/proc/version` contains "microsoft" or "wsl"

### Evaluation Harness Issues

- If `tsmac` is unreachable, verify the SSH host alias and that Ollama is running.
- If Pi cannot find a model, verify the model tag with `ollama list` on `tsmac`.
- If agent output is empty, inspect the saved JSONL events and stderr in the run
  JSON before retrying.
- If the Claude judge fails, verify `claude --print` works outside a Claude Code
  parent session.

## Repository Maintenance

This repository is an experimental archive requiring minimal maintenance:

- Skills are independent - updates don't affect others
- Evaluation runners are plain Python scripts and need no container rebuild
- Installation script is cross-platform - works on Windows and WSL
- The deprecated Docker harness remains only for historical reproduction

If correcting an existing skill, focus on:
1. Accuracy of guidelines (match authoritative sources)
2. Quality of examples (complete, runnable code)
3. Attribution (SOURCES.md must be current)
4. User documentation (README.md clarity)

<!-- claude-insights:start -->
## Working with Claude

These working agreements come from a `/insights` analysis of past sessions. Keep them in mind on every task in this repo.

- When pre-commit or pre-push hooks fail, fix the underlying issues (line length, trailing whitespace, lint errors) properly. Do NOT skip hooks, amend silently, or work around them. Never run `git init`, rewrite history (rebase, force push), or skip flaky tests without explicit permission.
- When asked to fix a problem, diagnose the root cause before proposing a fix. Do not jump to surface-level changes (e.g., flipping a port without understanding the networking, attributing a CSS bug to line-height without investigating).
- If two approaches have failed for the same problem, stop and present options to the user instead of trying a third. Don't thrash.
- Never fabricate documentation content. If you don't know what a doc actually says, read the file first.
<!-- claude-insights:end -->
