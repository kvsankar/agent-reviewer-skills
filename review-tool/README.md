# Claude Code Skills Review Tool

> [!WARNING]
> **Deprecated:** this Docker and Claude Agent SDK harness is retained for
> reproducibility of historical reviews only. New evaluations use direct Ollama
> calls for non-agentic tests, Pi for local-model agentic tests, Codex as the
> hosted agentic baseline, and separate tool-free matching and source-aware
> Claude adjudication passes. See the
> [Experiment Conclusion](../docs/experiment-conclusion.md) and
> [Evaluation Harness](../docs/evaluation-harness.md).

AI-powered code review using Claude with specialized review skills. No API keys needed - uses your Claude Code subscription.

## Quick Start

```bash
# One command to review any repository (uses OAuth + Agentic mode by default)
./review-cli.py \
  --repo https://github.com/simonw/datasette \
  --reviewer python
```

## Features

- ✅ **No API Keys Needed** - Uses Claude Code subscription via OAuth (default)
- ✅ **Zero Setup** - Python wrapper handles everything automatically
- ✅ **Agentic Mode** - Claude explores repositories with bash tools (default)
- ✅ **Multiple Reviewers** - Run 20 specialized reviewers in parallel
- ✅ **Fresh Context** - Each reviewer gets independent analysis
- ✅ **Containerized** - Safe Docker environment for all operations
- ✅ **Volume Mounts** - No rebuilds needed for code changes

## Installation

### Prerequisites

- Docker and Docker Compose
- Claude Code (for OAuth mode - recommended, default)
- OR: Anthropic API key (for API key mode)

### Setup

```bash
git clone <repository-url>
cd agent-reviewer-skills/review-tool

# Authenticate with Claude (one-time)
claude login

# That's it! Run your first review
./review-cli.py --repo <URL> --reviewer python
```

## Usage

### Basic Review

```bash
# Default: OAuth + Agentic (best for most repos)
./review-cli.py \
  --repo https://github.com/django/django \
  --reviewer django-reviewer
```

### Multiple Reviewers with Tags

```bash
# 'python' expands to 7 reviewers
./review-cli.py \
  --repo https://github.com/pallets/flask \
  --reviewer python

# 'javascript' expands to 7 reviewers (including react-reviewer)
./review-cli.py \
  --repo https://github.com/maciekt07/TodoApp \
  --reviewer javascript
```

### Batch Mode (Small Repos)

```bash
# Sends all files at once (faster but may fail on large repos)
./review-cli.py \
  --repo https://github.com/user/small-repo \
  --reviewer python \
  --mode batch
```

### API Key Mode

```bash
# Use API key instead of OAuth
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

./review-cli.py \
  --repo https://github.com/user/repo \
  --reviewer python \
  --auth apikey
```

### Specific Model

```bash
./review-cli.py \
  --repo https://github.com/user/repo \
  --reviewer django \
  --model claude-opus-4-20250514
```

## Available Reviewers

### Python Reviewers (7)

| Reviewer | Focus Area |
|----------|------------|
| `python-refactoring-reviewer` | Code smells, SOLID principles, design patterns |
| `python-functional-reviewer` | Functional programming patterns |
| `python-zen-reviewer` | Zen of Python (PEP 20) principles |
| `python-format-refactoring-reviewer` | Style issues through refactoring |
| `python-test-reviewer` | Test quality and coverage |
| `python-security-privacy-reviewer` | Security vulnerabilities, OWASP, GDPR |
| `python-performance-reviewer` | Performance optimization |

### JavaScript/TypeScript Reviewers (7)

| Reviewer | Focus Area |
|----------|------------|
| `javascript-test-reviewer` | Jest, Vitest, Testing Library |
| `javascript-refactoring-reviewer` | Code smells, SOLID, modern patterns |
| `javascript-format-refactoring-reviewer` | ESLint/Prettier through refactoring |
| `javascript-functional-reviewer` | Functional programming patterns |
| `javascript-security-privacy-reviewer` | XSS, CSRF, OWASP, GDPR |
| `javascript-performance-reviewer` | Performance optimization |
| `react-reviewer` | React best practices, hooks, patterns |

### Other Reviewers (6)

| Reviewer | Focus Area |
|----------|------------|
| `agile-requirements-reviewer` | Requirements, user stories, specifications |
| `django-reviewer` | Django production readiness |
| `openapi-reviewer` | OpenAPI/Swagger specifications |
| `database-schema-reviewer` | Database normalization, indexing |
| `code-authenticity-reviewer` | Detect fabricated/hallucinated code assertions |
| `playwright-test-reviewer` | Playwright E2E tests, flaky patterns, React testing |

### Tags (Multiple Reviewers)

| Tag | Expands To |
|-----|------------|
| `python` | All 7 Python reviewers |
| `javascript` / `js` | All 7 JavaScript reviewers |
| `react` | React + JS refactoring, security, test reviewers |
| `django` | Django + Python refactoring, security, test reviewers |
| `security` | Python + JavaScript security reviewers |
| `testing` / `tests` | Python + JavaScript + Playwright test reviewers |
| `functional` / `fp` | Python + JavaScript functional reviewers |
| `quality` | All refactoring and format reviewers |
| `playwright` / `e2e` | Playwright E2E test reviewer |
| `authenticity` | Code authenticity reviewer (AI/LLM fabrication detection) |
| `complete` / `all` | All 20 reviewers |

**Customize tags:** Edit `tags.yaml` to create your own combinations.

## Authentication & Modes

### Authentication (--auth)

**OAuth (default, recommended):**
```bash
# Uses ~/.claude credentials - no API key needed
claude login  # One-time setup
./review-cli.py --repo URL --reviewer NAME
# or explicitly: --auth oauth
```

**API Key:**
```bash
# Uses ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
./review-cli.py --repo URL --reviewer NAME --auth apikey
```

### Review Modes (--mode)

**Agentic (default, recommended):**
- Claude explores repo with bash tools (ls, cat, grep)
- Handles large repos well
- More thorough analysis

```bash
# Default mode
./review-cli.py --repo URL --reviewer NAME
# or explicitly: --mode agentic
```

**Batch:**
- Sends all files at once
- Faster (~30 seconds)
- May fail with "prompt too long" on large repos

```bash
./review-cli.py --repo URL --reviewer NAME --mode batch
```

### Supported Combinations

| Auth | Mode | Use Case |
|------|------|----------|
| **oauth** | **agentic** | ✅ **Default** - Best for most repos, no API key needed |
| oauth | batch | Small repos, no API key needed |
| apikey | agentic | Large repos with API key |
| apikey | batch | Small repos with API key |

## What Gets Reviewed

- **Agentic Mode:** Claude explores and reads relevant files autonomously
- **Batch Mode:** 50 most recently modified files matching reviewer patterns
- **Analysis:** Full file contents (up to 500 lines per file in batch mode)
- **Output:** Structured markdown with examples and recommendations

## Output Format

Reviews are saved to `reviews/` directory:

```
reviews/
├── simonw-datasette-refactoring-reviewer-claude-20251112_084305.md
├── simonw-datasette-security-privacy-reviewer-claude-20251112_084815.md
└── ...
```

Each review includes:
- Executive summary
- Strengths identified
- Issues with severity levels
- Code examples (before/after)
- Specific recommendations

## Command-Line Options

### Python Wrapper (`review-cli.py`)

```
--repo REPO              Repository URL (required)
--reviewer REVIEWER      Reviewer or tag (can specify multiple)
--auth MODE              Authentication: oauth|apikey (default: oauth)
--mode MODE              Review mode: agentic|batch (default: agentic)
--model MODEL            Claude model (sonnet-4 or opus-4)
--output-dir DIR         Output directory (default: reviews)
--keep-repo              Keep cloned repository
--skip-checks            Skip prerequisite checks
--list-reviewers         List all available reviewers and tags
```

### Docker Direct (`docker-compose`)

```bash
docker-compose run --rm reviewer \
  --repo URL \
  --reviewer NAME \
  --auth oauth \
  --mode agentic
```

## Advanced Usage

### Agentic Mode Details

Agentic mode (default) allows Claude to explore the repository with bash tools:

```bash
./review-cli.py \
  --repo https://github.com/large/codebase \
  --reviewer python
```

**How it works:**
- Claude uses `ls`, `find` to discover files
- Uses `cat`, `head`, `tail` to read code
- Uses `grep` to search patterns
- Explores incrementally based on findings

**Features:**
- Handles repositories of any size
- More thorough analysis
- Discovers patterns across entire codebase
- Adapts exploration based on what it finds

**Comparison:**

| Feature | Batch Mode | Agentic Mode (Default) |
|---------|------------|------------------------|
| Speed | ~30 seconds | ~2-5 minutes |
| Files | 50 max | Unlimited |
| Large repos | May fail | ✅ Works |
| Thoroughness | Good | Excellent |
| Container | Required | Required |
| Auth | Both | Both |

### Custom Tags

Create custom reviewer combinations in `tags.yaml`:

```yaml
backend:
  description: "Backend-focused reviews"
  reviewers:
    - django-reviewer
    - python-security-privacy-reviewer
    - python-test-reviewer

frontend:
  description: "Frontend-focused reviews"
  reviewers:
    - react-reviewer
    - javascript-security-privacy-reviewer
    - javascript-test-reviewer
```

Then use:

```bash
./review-cli.py --repo URL --reviewer backend
```

### CI/CD Integration

```yaml
# GitHub Actions
name: Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cd review-tool
          ./review-cli.py \
            --repo ${{ github.repository }} \
            --reviewer security \
            --auth apikey
```

### Batch Reviews

```bash
# Review multiple repositories
for repo in django flask fastapi; do
  ./review-cli.py \
    --repo https://github.com/user/$repo \
    --reviewer python
done
```

## Architecture

### How It Works

```
┌─────────────────────────────────────────────────────────┐
│  Python Wrapper (review-cli.py)                         │
│  - Validates arguments                                  │
│  - Checks prerequisites                                 │
│  - Sets up .env with UID/GID                           │
│  - Runs Docker container                                │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│  Docker Container                                        │
│  ┌────────────────────────────────────────────────┐    │
│  │  review.py (Main Script)                       │    │
│  │  - Clones repository                           │    │
│  │  - Loads reviewer skills from /skills          │    │
│  │  - Agentic: Claude explores with bash tools    │    │
│  │  - Batch: Discovers matching files             │    │
│  │  - Calls Claude for each reviewer              │    │
│  │  - Generates markdown reports                  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Mounted Volumes:                                       │
│  - ~/.claude → /home/appuser/.claude (OAuth creds)     │
│  - ../reviewers → /skills (reviewer templates)          │
│  - ./reviews → /app/reviews (output)                   │
│  - ./review.py → /app/review.py (live code)           │
└──────────────────────────────────────────────────────────┘
```

### Permission Handling

The container runs as your user (not root) to avoid permission issues:

1. Wrapper creates `.env` with `USER_ID` and `GROUP_ID`
2. Docker uses these values: `user: "${USER_ID}:${GROUP_ID}"`
3. Files created in container are owned by you on the host

## Troubleshooting

### "Docker not found"

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### "Claude credentials not found"

```bash
claude login
ls ~/.claude/.credentials.json  # Should exist
```

### "Permission denied" on reviews

```bash
# Fix ownership
sudo chown -R $(id -u):$(id -g) reviews

# Or delete and recreate
sudo rm -rf reviews
```

### Build fails

```bash
# Rebuild from scratch
docker-compose build --no-cache
```

### "Prompt too long" error

Use agentic mode (default) instead of batch mode:

```bash
./review-cli.py --repo URL --reviewer NAME
# Agentic mode is already the default!
```

## Examples

### Review Django Project

```bash
./review-cli.py \
  --repo https://github.com/django/django \
  --reviewer django
```

**Output:** 1 comprehensive Django production readiness review

### Review Simon Willison's Datasette

```bash
./review-cli.py \
  --repo https://github.com/simonw/datasette \
  --reviewer python
```

**Output:** 7 independent reviews covering:
- Refactoring opportunities
- Functional programming patterns
- Zen of Python alignment
- Code formatting
- Test quality
- Security & privacy
- Performance optimization

### Security Audit

```bash
./review-cli.py \
  --repo https://github.com/your-org/app \
  --reviewer security
```

**Output:** Security-focused reviews (Python + JavaScript) with vulnerability analysis

### React Application Review

```bash
./review-cli.py \
  --repo https://github.com/maciekt07/TodoApp \
  --reviewer react
```

**Output:** 4 reviews covering React patterns, refactoring, security, and testing

## Sample Reviews

The `sample_reviews/` directory contains real review examples from popular open-source projects:

**HTTPie** (8 Python reviewers):
- [httpie/httpie](https://github.com/httpie/httpie) - Modern command-line HTTP client
- Reviews: refactoring, functional patterns, tests, Zen of Python, formatting, security, performance, and Rhodes-inspired code quality
- Total: 119KiB of analysis

**Datasette** (8 Python reviewers):
- [simonw/datasette](https://github.com/simonw/datasette) - Data exploration tool
- Reviews: refactoring, functional patterns, tests, Zen of Python, formatting, security, performance, and Rhodes-inspired code quality
- Total: 108KiB of analysis

**TodoApp** (7 JavaScript/React reviewers):
- [maciekt07/TodoApp](https://github.com/maciekt07/TodoApp) - React and TypeScript task application
- Reviews: refactoring, functional patterns, tests, formatting, security, performance, and React
- Total: 135KiB of analysis

**Chandrayaan3** (JavaScript reviewer):
- [kvsankar/chandrayaan3](https://github.com/kvsankar/chandrayaan3) - ISRO mission visualization
- Review: functional JavaScript patterns
- Total: 11KiB of analysis

All samples generated using default OAuth + Agentic mode. Each review demonstrates:
- Mnemonic IDs for findings (e.g., USE-CONST, IMMUT-COPY)
- Concrete code examples with before/after
- Severity ratings and impact analysis
- Specific, actionable recommendations

Browse `sample_reviews/` to see what reviews look like before running your own.

## Development

### Project Structure

```
review-tool/
├── review-cli.py          # Python wrapper (user-facing)
├── review.py              # Core review logic (runs in container)
├── Dockerfile             # Container definition
├── docker-compose.yml     # Docker orchestration
├── tags.yaml              # Reviewer tag definitions
├── reviews/               # Output directory
├── sample_reviews/        # Example reviews from real projects
└── README.md              # This file
```

### Adding Custom Reviewers

1. Create a new skill directory under `reviewers/`:
   ```bash
   mkdir ../reviewers/my-custom-reviewer
   ```

2. Add `SKILL.md` with review template:
   ```markdown
   ---
   name: My Custom Reviewer
   description: Reviews for X, Y, Z
   ---

   You are an expert code reviewer focusing on...
   ```

3. Add to `review.py` REVIEWERS dict:
   ```python
   'my-custom-reviewer': {
       'patterns': ['*.py', '*.js'],
       'description': 'Custom review focus',
   }
   ```

4. Use it:
   ```bash
   ./review-cli.py --repo URL --reviewer my-custom-reviewer
   ```

### Volume-Based Development

No rebuilds needed! Code is mounted as volumes:

```yaml
volumes:
  - ./review.py:/app/review.py:ro     # Edit locally, runs in container
  - ./tags.yaml:/app/tags.yaml:ro     # Edit tag definitions
  - ../reviewers:/skills:ro            # All reviewer skills
```

Just edit files and run - changes take effect immediately.

## FAQ

**Q: Do I need an API key?**
A: No! Use the default OAuth mode with your Claude Code subscription (recommended).

**Q: How many files are reviewed?**
A: Agentic mode (default) explores as many files as needed. Batch mode reviews 50 most recent files.

**Q: Can I review private repositories?**
A: Yes, if you can clone them (SSH keys, credentials, etc.).

**Q: What's the difference between reviewers and tags?**
A: Reviewers are individual (e.g., `django-reviewer`). Tags expand to multiple reviewers (e.g., `python` → 7 reviewers).

**Q: Can I run multiple reviews in parallel?**
A: Yes! Each reviewer runs sequentially with fresh context, preventing cross-contamination.

**Q: What models are supported?**
A: Claude Sonnet 4 (default, fast) and Claude Opus 4 (most capable).

**Q: Is my code sent to the cloud?**
A: Yes, to Claude's API for review. Use appropriate repositories.

**Q: Can I customize the output format?**
A: Yes, edit the skill templates in `../*/SKILL.md` files.

**Q: Why use agentic mode?**
A: It's the default because it handles repos of any size and provides thorough analysis. Batch mode may fail with "prompt too long" on larger repos.

## Support

- **List reviewers:** `./review-cli.py --list-reviewers`
- **Documentation:** This README
- **Help:** `./review-cli.py --help`

## License

See parent repository for license information.

## Credits

Built with:
- [Claude](https://claude.ai) - AI code review
- [Docker](https://docker.com) - Containerization
- [Python](https://python.org) - Scripting
- [Claude Code](https://claude.com/claude-code) - OAuth authentication

---

**Ready to review!**

```bash
./review-cli.py --repo <YOUR_REPO_URL> --reviewer python
```
