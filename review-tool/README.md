# Agentic Code Review Tool

Automated code review tool that uses Claude Code skills to review GitHub repositories and generate comprehensive markdown reports.

**Two modes:**
- **Standard Mode**: Fast, predictable, works with all providers (Claude, OpenAI, Gemini)
- **Agentic Mode**: AI explores repo with bash tools (container required, Claude only)

**Two authentication options for Claude:**
- **API Key**: Use `ANTHROPIC_API_KEY` (get from console.anthropic.com)
- **Claude CLI**: Use your Claude Code subscription (no API key needed) - see [CLAUDE-CLI.md](./CLAUDE-CLI.md)

## 🎯 Quick Start

### Prerequisites

- **Python 3.8+**
- **Git** installed and in PATH
- **uv** package manager ([installation](https://github.com/astral-sh/uv))
- **API Key** for your chosen provider:
  - **Claude**: https://console.anthropic.com/
  - **OpenAI**: https://platform.openai.com/api-keys
  - **Gemini**: https://makersuite.google.com/

### Installation

```bash
# 1. Navigate to review-tool directory
cd review-tool

# 2. Set your API key (choose one)
export ANTHROPIC_API_KEY='your-api-key-here'  # For Claude
export OPENAI_API_KEY='your-api-key-here'     # For OpenAI
export GOOGLE_API_KEY='your-api-key-here'     # For Gemini

# 3. Install dependencies with uv (choose your provider)
uv pip install python-dotenv pyyaml anthropic        # For Claude
uv pip install python-dotenv pyyaml openai           # For OpenAI
uv pip install python-dotenv pyyaml google-generativeai  # For Gemini

# Note: pyyaml is required for tag support

# Done! No virtual environment needed with uv
```

### Basic Usage

The tool displays the provider and version when running:
```
[+] Using Claude (claude-sonnet-4-20250514) [anthropic v0.40.0]
```

```bash
# Review a Django project with Claude (default)
uv run review.py \
  --repo https://github.com/django/django \
  --reviewer django-reviewer \
  --provider claude

# Review with OpenAI GPT-4
uv run review.py \
  --repo https://github.com/django/django \
  --reviewer django-reviewer \
  --provider openai \
  --model gpt-4

# Multiple reviewers at once with Gemini
uv run review.py \
  --repo https://github.com/user/project \
  --reviewer django-reviewer \
  --reviewer security-privacy-reviewer \
  --provider gemini

# Custom output directory and keep the cloned repo
uv run review.py \
  --repo https://github.com/user/project \
  --reviewer refactoring-reviewer \
  --provider claude \
  --output-dir my-reviews \
  --keep-repo
```

## 📋 Available Reviewers

| Reviewer | File Patterns | Best For |
|----------|---------------|----------|
| `agile-requirements-reviewer` | `*.md`, `requirements.txt`, `docs/*.md` | Documentation, requirements |
| `django-reviewer` | `*.py`, `models.py`, `views.py`, `settings/*.py` | Django projects |
| `format-refactoring-reviewer` | `*.py` | Python style issues |
| `functional-javascript-reviewer` | `*.js`, `*.jsx`, `*.ts`, `*.tsx` | JS/TS projects |
| `functional-python-reviewer` | `*.py` | Python FP patterns |
| `python-test-reviewer` | `test_*.py`, `tests/*.py` | Python tests |
| `refactoring-reviewer` | `*.py` | Python refactoring |
| `security-privacy-reviewer` | `*.py`, `*.js`, `*.ts`, `*.java`, `*.go` | Security audits |
| `zen-of-python-reviewer` | `*.py` | Pythonic code style |

## 🏷️ Reviewer Tags

Use tags to run multiple related reviewers at once. Each reviewer runs with fresh context.

**Tags are defined in `tags.yaml` - customize them for your needs!**

| Tag | Reviewers | Use Case |
|-----|-----------|----------|
| `python` | 6 Python reviewers | Complete Python review (refactoring, FP, style, tests, security) |
| `quality` | 3 quality reviewers | Code quality and best practices |
| `django` | 4 reviewers | Django application review (Django, refactoring, security, tests) |
| `security` / `privacy` | 1 reviewer | Security and privacy audit |
| `functional` / `fp` | 2 FP reviewers | Functional programming patterns |
| `testing` / `tests` | 1 reviewer | Test quality review |
| `javascript` / `js` | 1 reviewer | JavaScript/TypeScript functional patterns |
| `requirements` / `docs` | 1 reviewer | Requirements and documentation |
| `complete` / `all` | All 9 reviewers | Exhaustive review |

**Examples:**
```bash
# All Python reviewers
uv run review.py --repo URL --reviewer python --provider claude

# Django + quality checks
uv run review.py --repo URL --reviewer django --reviewer quality --provider claude

# Complete review with all reviewers
uv run review.py --repo URL --reviewer complete --provider claude
```

**Customize tags:** Edit `tags.yaml` to create your own combinations. See [TAGS.md](./TAGS.md) for complete guide.

## 🤖 Agentic Mode (Advanced)

Enable AI to explore repositories dynamically with bash tools - more thorough but requires Docker.

```bash
# Build container
docker build -f review-tool/Dockerfile -t claude-reviewer .

# Run agentic review
docker run --rm \
  -v $(pwd)/review-tool/reviews:/app/reviews \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  claude-reviewer \
  --repo https://github.com/django/django \
  --reviewer python \
  --agentic
```

**Or use docker-compose:**
```bash
cd review-tool
docker-compose build
docker-compose run --rm reviewer --repo URL --reviewer python --agentic
```

**Agentic vs Standard:**
- **Agentic**: AI explores with ls/cat/grep (~2-5 min, $1-5, Claude only, container required)
- **Standard**: Fixed files sent to AI (~30 sec, $0.33, all providers, runs anywhere)

See [AGENTIC.md](./AGENTIC.md) for complete guide.

## 💡 Usage Examples

### Example 1: Django Security & Performance Review

```bash
uv run review.py \
  --repo https://github.com/django/django \
  --reviewer django-reviewer \
  --reviewer security-privacy-reviewer \
  --provider claude
```

### Example 2: Python Code Quality Assessment with OpenAI

```bash
uv run review.py \
  --repo https://github.com/psf/requests \
  --reviewer refactoring-reviewer \
  --reviewer zen-of-python-reviewer \
  --reviewer python-test-reviewer \
  --provider openai \
  --model gpt-4
```

### Example 3: JavaScript Functional Patterns with Gemini

```bash
uv run review.py \
  --repo https://github.com/user/react-app \
  --reviewer functional-javascript-reviewer \
  --provider gemini
```

### Example 4: Requirements Review

```bash
uv run review.py \
  --repo https://github.com/user/specs \
  --reviewer agile-requirements-reviewer \
  --provider claude
```

### Example 5: Complete Python Review with Tags

```bash
# Use the 'python' tag to run all 5 Python reviewers
uv run review.py \
  --repo https://github.com/psf/requests \
  --reviewer python \
  --provider claude

# Generates 5 separate reports with fresh context for each
```

### Example 6: Django Full Stack Review

```bash
# Combine Django and quality tags
uv run review.py \
  --repo https://github.com/user/django-app \
  --reviewer django \
  --reviewer quality \
  --provider claude

# Expands to 5 reviewers: django, security, refactoring, zen-of-python, format-refactoring
```

### Example 7: Compare Providers on Same Repository

```bash
# Run with Claude
uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --provider claude

# Run with OpenAI
uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --provider openai --model gpt-4

# Run with Gemini
uv run review.py --repo https://github.com/user/repo --reviewer django-reviewer --provider gemini

# Compare the three generated reports!
```

## 📊 Output

Reports are generated as markdown files in the `reviews/` directory (default):

```
reviews/
├── django-django-django-reviewer-claude-20250112_143022.md
├── django-django-security-privacy-reviewer-claude-20250112_143525.md
├── psf-requests-refactoring-reviewer-openai-20250112_144018.md
└── user-repo-django-reviewer-gemini-20250112_144530.md
```

**Filename format:** `{user}-{repo}-{reviewer}-{provider}-{timestamp}.md`

Each report includes:
- **Repository metadata** (URL, date, reviewer, provider)
- **Critical issues** with mnemonic IDs (e.g., SEC-SQL, PERF-N+1)
- **Before/after code examples**
- **Explanations** of why issues matter
- **Best practice** recommendations

## ⚙️ Command Line Options

```
usage: review.py [-h] --repo REPO --reviewer REVIEWER
                 [--provider {claude,openai,gemini}] [--model MODEL]
                 [--output-dir OUTPUT_DIR] [--keep-repo]

required arguments:
  --repo REPO           GitHub repository URL to review
  --reviewer REVIEWER   Reviewer(s) or tag(s) to use (can specify multiple times)
                        Tags are defined in tags.yaml and can be customized
                        See TAGS.md for details

optional arguments:
  --provider PROVIDER   AI provider: claude, openai, or gemini (default: claude)
  --model MODEL         Model to use (provider-specific, uses defaults if not specified)
                        - Claude: claude-sonnet-4-20250514 (default), claude-opus-4-20250514
                        - OpenAI: gpt-4-turbo-preview (default), gpt-4, gpt-3.5-turbo
                        - Gemini: gemini-pro (default), gemini-1.5-pro
  --output-dir DIR      Output directory for reports (default: reviews)
  --keep-repo           Keep cloned repository after review
  -h, --help            Show help message
```

## 🔧 How It Works

1. **Clone Repository** - Creates temp dir, clones repo with `--depth 1`
2. **Discover Files** - Finds files matching reviewer patterns
3. **Load Skill** - Loads skill guidelines from `../[reviewer]/SKILL.md`
4. **Prepare Context** - Formats code files (max 50 files, 500 lines each)
5. **Call AI Provider** - Sends skill + code to chosen provider (Claude/OpenAI/Gemini)
6. **Generate Report** - Saves markdown report with provider and timestamp
7. **Cleanup** - Removes temp directory (unless `--keep-repo`)

## 🤖 AI Providers

The tool supports three AI providers with different strengths:

| Provider | Best For | Cost | Models |
|----------|----------|------|--------|
| **Claude** | Code analysis, security, Django | $$$ | Sonnet 4, Opus 4 |
| **OpenAI** | General purpose, fast | $$ | GPT-4, GPT-4 Turbo |
| **Gemini** | Cost-effective, high volume | $ | Gemini Pro, 1.5 Pro |

For detailed provider comparison and setup, see [PROVIDERS.md](./PROVIDERS.md).

## 🎓 Use Cases

### Learning from Popular Projects
```bash
uv run review.py --repo https://github.com/django/django --reviewer django-reviewer --provider claude
```

### Security Audits
```bash
uv run review.py --repo https://github.com/yourorg/api --reviewer security-privacy-reviewer --provider claude --output-dir audits
```

### Pre-Production Review
```bash
uv run review.py --repo https://github.com/yourorg/app \
  --reviewer django-reviewer \
  --reviewer security-privacy-reviewer \
  --provider claude \
  --output-dir pre-prod
```

### Cost-Effective Batch Reviews
```bash
# Use Gemini for high-volume reviews
uv run review.py --repo https://github.com/user/repo --reviewer refactoring-reviewer --provider gemini
```

### CI/CD Integration

**.github/workflows/code-review.yml:**
```yaml
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Run Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cd review-tool
          uv pip install python-dotenv anthropic
          uv run review.py --repo ${{ github.repository }} --reviewer django-reviewer --provider claude

      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: review-reports
          path: review-tool/reviews/
```

## 💰 Cost Considerations

Approximate cost per review varies by provider:

| Provider | Input (50K tokens) | Output (12K tokens) | Total per Review |
|----------|-------------------|---------------------|------------------|
| **Claude Sonnet 4** | $0.15 | $0.18 | **~$0.33** |
| **OpenAI GPT-4** | $0.50 | $0.36 | **~$0.86** |
| **Gemini Pro** | $0.025 | $0.018 | **~$0.04** |

**Tips to reduce costs:**
- Start with Gemini for initial assessment
- Use Claude or GPT-4 for final production review
- Review smaller repositories
- Use fewer reviewers per run
- Focus on specific file patterns
- Review incrementally (only changed files)

## 🔒 Security & Privacy

**API Keys:**
- Store in environment variables (never commit)
- Use `.env` file locally (git-ignored)
- Use secrets management in CI/CD
- Each provider has different API key formats

**Code Privacy:**
- Code sent to chosen AI provider's API for review
- Only review public repos or code you can share
- Check organization policies for sensitive code
- Review provider data retention policies

**Data Retention:**
- Cloned repo deleted after review (unless `--keep-repo`)
- Review reports saved locally only in `reviews/` directory

## 🛠️ Customization

### Adjust File/Line Limits

Edit `review.py`:

```python
# Line 126 - Change max files
files = self.discover_files(repo_path, reviewer_config['patterns'], max_files=100)

# Line 151 - Change max lines per file
def read_file_content(self, file_path: Path, max_lines: int = 1000):
```

### Add Custom Reviewer

1. Create skill in parent directory: `../my-custom-reviewer/SKILL.md`
2. Add to `REVIEWERS` dict in `review.py`:

```python
REVIEWERS = {
    'my-custom-reviewer': {
        'patterns': ['*.py', '*.js'],
        'description': 'My custom focus',
    },
    # ... existing reviewers
}
```

### Change Model

Use the `--model` flag:

```bash
# Claude Opus (most capable)
uv run review.py --repo URL --reviewer REVIEWER --provider claude --model claude-opus-4-20250514

# GPT-4 Turbo
uv run review.py --repo URL --reviewer REVIEWER --provider openai --model gpt-4-turbo-preview

# Gemini 1.5 Pro
uv run review.py --repo URL --reviewer REVIEWER --provider gemini --model gemini-1.5-pro
```

## 🐛 Troubleshooting

### "API key not set"
```bash
# For Claude
export ANTHROPIC_API_KEY='sk-ant-...'

# For OpenAI
export OPENAI_API_KEY='sk-...'

# For Gemini
export GOOGLE_API_KEY='your-key'
```

Or use a `.env` file (copy from `.env.example`).

### "Provider package not installed"
```bash
# Claude
uv pip install anthropic

# OpenAI
uv pip install openai

# Gemini
uv pip install google-generativeai
```

### "Git is not installed"
Install git:
- **Mac**: `brew install git`
- **Ubuntu**: `sudo apt-get install git`
- **Windows**: https://git-scm.com/download/win

### "uv not found"
Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "Skill not found"
Make sure you're running from the `review-tool/` directory and skills exist in parent directory `../[reviewer-name]/`

### "No files found"
Repository may not contain files matching the reviewer's patterns. Try a different reviewer or check repository structure.

## 📚 Project Structure

```
claude-skills-public/
├── agile-requirements-reviewer/
│   └── SKILL.md
├── django-reviewer/
│   └── SKILL.md
├── ... (other skills)
└── review-tool/               ← You are here
    ├── review.py              ← Main script
    ├── pyproject.toml         ← uv project config
    ├── README.md              ← This file
    ├── .env.example           ← API key template
    ├── Dockerfile             ← Container for agentic mode
    ├── docker-compose.yml     ← Docker Compose configuration
    ├── .dockerignore          ← Docker build exclusions
    ├── PROVIDERS.md           ← Provider comparison guide
    ├── QUICKSTART.md          ← Quick start guide
    ├── TAGS.md                ← Reviewer tags reference
    ├── AGENTIC.md             ← Agentic mode guide
    ├── tags.yaml              ← Reviewer tags configuration
    ├── examples/              ← Example reports
    └── reviews/               ← Generated reports (git-ignored)
```

## 🤝 Contributing

Ideas for contributions:
- Add filtering by directory/file patterns
- Add support for private repositories
- Add incremental review (only changed files)
- Add HTML report output
- Add batch review mode (multiple repos)
- Add support for Azure OpenAI, AWS Bedrock
- Add local model support (Ollama, LM Studio)

## 📄 License

Same license as Claude Code Skills Collection (parent directory).

## 📞 Resources

- **Quick Start Guide**: [QUICKSTART.md](./QUICKSTART.md)
- **Provider Guide**: [PROVIDERS.md](./PROVIDERS.md)
- **Reviewer Tags**: [TAGS.md](./TAGS.md)
- **Agentic Mode**: [AGENTIC.md](./AGENTIC.md)
- **Claude CLI Auth**: [CLAUDE-CLI.md](./CLAUDE-CLI.md)
- **Parent README**: [../README.md](../README.md)
- **Skills Documentation**: [../*-reviewer/README.md](../)
- **Claude API Docs**: https://docs.anthropic.com/
- **OpenAI API Docs**: https://platform.openai.com/docs
- **Gemini API Docs**: https://ai.google.dev/docs
- **uv Documentation**: https://github.com/astral-sh/uv

---

**Generate comprehensive AI-powered code reviews with Claude, OpenAI, or Gemini.**
