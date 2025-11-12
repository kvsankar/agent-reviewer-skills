# Claude Code Skills Review Tool

AI-powered code review using Claude with specialized review skills. No API keys needed - uses your Claude Code subscription.

## Quick Start

```bash
# One command to review any repository
./review-cli.py \
  --repo https://github.com/simonw/datasette \
  --reviewer python \
  --use-claude-cli
```

## Features

- ✅ **No API Keys Needed** - Uses Claude Code subscription via OAuth
- ✅ **Zero Setup** - Python wrapper handles everything automatically
- ✅ **Multiple Reviewers** - Run 6+ specialized reviewers in parallel
- ✅ **Fresh Context** - Each reviewer gets independent analysis
- ✅ **Agentic Mode** - Claude explores repositories with bash tools
- ✅ **Containerized** - Safe Docker environment for all operations
- ✅ **Volume Mounts** - No rebuilds needed for code changes

## Installation

### Prerequisites

- Docker and Docker Compose
- Claude Code (for CLI mode - recommended)

### Setup

```bash
git clone <repository-url>
cd claude-skills/review-tool

# That's it! The wrapper handles the rest
./review-cli.py --repo <URL> --reviewer python --use-claude-cli
```

## Usage

### Basic Review

```bash
./review-cli.py \
  --repo https://github.com/django/django \
  --reviewer django-reviewer \
  --use-claude-cli
```

### Multiple Reviewers with Tags

```bash
# 'python' expands to 6 reviewers
./review-cli.py \
  --repo https://github.com/pallets/flask \
  --reviewer python \
  --use-claude-cli
```

### Agentic Mode (Deep Analysis)

```bash
./review-cli.py \
  --repo https://github.com/user/repo \
  --reviewer python \
  --agentic \
  --use-claude-cli
```

### Specific Model

```bash
./review-cli.py \
  --repo https://github.com/user/repo \
  --reviewer django \
  --model claude-opus-4-20250514 \
  --use-claude-cli
```

## Available Reviewers

### Individual Reviewers

| Reviewer | Focus Area |
|----------|------------|
| `agile-requirements-reviewer` | Requirements, user stories, specifications |
| `django-reviewer` | Django production readiness |
| `format-refactoring-reviewer` | Python code style and formatting |
| `functional-javascript-reviewer` | JavaScript functional patterns |
| `functional-python-reviewer` | Python functional programming |
| `python-test-reviewer` | Test quality and coverage |
| `refactoring-reviewer` | General Python refactoring |
| `security-privacy-reviewer` | Security and privacy issues |
| `zen-of-python-reviewer` | Zen of Python principles |

### Tags (Multiple Reviewers)

| Tag | Expands To |
|-----|------------|
| `python` | All 6 Python reviewers |
| `javascript` | All JavaScript reviewers |
| `security` | Security-focused reviewers |
| `django` | Django-specific reviewers |

**Customize tags:** Edit `tags.yaml` to create your own combinations.

## Authentication

### Option 1: Claude CLI (Recommended)

Uses your Claude Code subscription - no API keys needed.

```bash
# Authenticate once
claude login

# Use with --use-claude-cli flag
./review-cli.py --repo URL --reviewer NAME --use-claude-cli
```

### Option 2: API Key

```bash
# Set environment variable
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Run without --use-claude-cli flag
./review-cli.py --repo URL --reviewer NAME
```

## What Gets Reviewed

- **Files:** 50 most recently modified files matching reviewer patterns
- **Analysis:** Full file contents (up to 500 lines per file)
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
--model MODEL            Claude model (sonnet-4 or opus-4)
--output-dir DIR         Output directory (default: reviews)
--keep-repo              Keep cloned repository
--agentic                Enable agentic mode
--use-claude-cli         Use Claude CLI auth (recommended)
--skip-checks            Skip prerequisite checks
```

### Docker Direct (`docker-compose`)

```bash
docker-compose run --rm reviewer \
  --repo URL \
  --reviewer NAME \
  --use-claude-cli
```

## Advanced Usage

### Agentic Mode

Agentic mode allows Claude to explore the repository with bash tools for deeper analysis:

```bash
./review-cli.py \
  --repo https://github.com/large/codebase \
  --reviewer python \
  --agentic \
  --use-claude-cli
```

**Features:**
- Claude explores repository structure autonomously
- Searches for patterns across unlimited files
- More thorough analysis for complex codebases
- Costs more (~$1-5 per review)

**Requirements:**
- Must run in container (safety)
- Only supports batch mode (50 files per reviewer)

**Comparison:**

| Feature | Batch Mode | Agentic Mode |
|---------|------------|--------------|
| Speed | ~30 seconds | ~2-5 minutes |
| Cost | $0.15-0.50 | $1-5 |
| Files | 50 max | Unlimited |
| Thoroughness | Good | Excellent |
| Container | Optional | Required |

### Custom Tags

Create custom reviewer combinations in `tags.yaml`:

```yaml
backend:
  description: "Backend-focused reviews"
  reviewers:
    - django-reviewer
    - security-privacy-reviewer
    - python-test-reviewer

frontend:
  description: "Frontend-focused reviews"
  reviewers:
    - functional-javascript-reviewer
```

Then use:

```bash
./review-cli.py --repo URL --reviewer backend --use-claude-cli
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
        run: |
          cd review-tool
          ./review-cli.py \
            --repo ${{ github.repository }} \
            --reviewer security \
            --use-claude-cli
```

### Batch Reviews

```bash
# Review multiple repositories
for repo in django flask fastapi; do
  ./review-cli.py \
    --repo https://github.com/user/$repo \
    --reviewer python \
    --use-claude-cli
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
│  │  - Discovers matching files                    │    │
│  │  - Calls Claude for each reviewer              │    │
│  │  - Generates markdown reports                  │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Mounted Volumes:                                       │
│  - ~/.claude → /home/appuser/.claude (credentials)     │
│  - ../skills → /skills (reviewer templates)             │
│  - ./reviews → /app/reviews (output)                   │
│  - ./review.py → /app/review.py (live code)           │
└──────────────────────────────────────────────────────────┘
```

### Permission Handling

The container runs as your user (not root) to avoid permission issues:

1. `test-setup.sh` creates `.env` with `USER_ID` and `GROUP_ID`
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

### "Agentic mode requires container"

Agentic mode must run in Docker for safety. Use the Python wrapper:

```bash
./review-cli.py --repo URL --reviewer NAME --agentic --use-claude-cli
```

## Examples

### Review Django Project

```bash
./review-cli.py \
  --repo https://github.com/django/django \
  --reviewer django \
  --use-claude-cli
```

**Output:** 1 comprehensive Django production readiness review

### Review Simon Willison's Datasette

```bash
./review-cli.py \
  --repo https://github.com/simonw/datasette \
  --reviewer python \
  --use-claude-cli
```

**Output:** 6 independent reviews covering:
- Refactoring opportunities
- Functional programming patterns
- Zen of Python alignment
- Code formatting
- Test quality
- Security & privacy

### Security Audit

```bash
./review-cli.py \
  --repo https://github.com/your-org/app \
  --reviewer security-privacy-reviewer \
  --use-claude-cli
```

**Output:** Security-focused review with vulnerability analysis

## Cost Estimates

Using Claude CLI (your Claude Code subscription):

| Review Type | Estimated Cost |
|-------------|----------------|
| Single reviewer | $0.15 - $0.50 |
| Python tag (6 reviewers) | $1.00 - $3.00 |
| Agentic mode | $1.00 - $5.00 |

Costs vary by:
- Repository size
- Number of files
- Model choice (Sonnet vs Opus)

## Development

### Project Structure

```
review-tool/
├── review-cli.py          # Python wrapper (user-facing)
├── review.py              # Core review logic (runs in container)
├── test-setup.sh          # Setup verification script
├── Dockerfile             # Container definition
├── docker-compose.yml     # Docker orchestration
├── tags.yaml              # Reviewer tag definitions
├── reviews/               # Output directory
└── README.md              # This file
```

### Adding Custom Reviewers

1. Create a new skill directory in parent:
   ```bash
   mkdir ../my-custom-reviewer
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
   ./review-cli.py --repo URL --reviewer my-custom-reviewer --use-claude-cli
   ```

### Volume-Based Development

No rebuilds needed! Code is mounted as volumes:

```yaml
volumes:
  - ./review.py:/app/review.py:ro     # Edit locally, runs in container
  - ./tags.yaml:/app/tags.yaml:ro     # Edit tag definitions
  - ..:/skills:ro                      # All reviewer skills
```

Just edit files and run - changes take effect immediately.

## FAQ

**Q: Do I need an API key?**
A: No! Use `--use-claude-cli` with your Claude Code subscription (recommended).

**Q: How many files are reviewed?**
A: 50 most recently modified files matching the reviewer's patterns.

**Q: Can I review private repositories?**
A: Yes, if you can clone them (SSH keys, credentials, etc.).

**Q: What's the difference between reviewers and tags?**
A: Reviewers are individual (e.g., `django-reviewer`). Tags expand to multiple reviewers (e.g., `python` → 6 reviewers).

**Q: Can I run multiple reviews in parallel?**
A: Yes! Each reviewer runs sequentially with fresh context, preventing cross-contamination.

**Q: What models are supported?**
A: Claude Sonnet 4 (default, fast) and Claude Opus 4 (most capable).

**Q: Is my code sent to the cloud?**
A: Yes, to Claude's API for review. Use appropriate repositories.

**Q: Can I customize the output format?**
A: Yes, edit the skill templates in `../*/SKILL.md` files.

## Support

- **Test setup:** `./test-setup.sh`
- **Documentation:** This README
- **Implementation notes:** `STATUS.md`
- **Help:** `./review-cli.py --help`

## License

See parent repository for license information.

## Credits

Built with:
- [Claude](https://claude.ai) - AI code review
- [Docker](https://docker.com) - Containerization
- [Python](https://python.org) - Scripting
- [Claude Code](https://claude.com/claude-code) - CLI authentication

---

**Ready to review!**

```bash
./review-cli.py --repo <YOUR_REPO_URL> --reviewer python --use-claude-cli
```
