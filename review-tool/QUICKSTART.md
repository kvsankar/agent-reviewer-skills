# Quick Start Guide

Get started with the multi-provider review tool in 3 steps!

## 1. Setup

### Install uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Navigate to tool directory

```bash
cd review-tool
```

### Set up API keys

**Option A: Using .env file (Recommended)**

```bash
# Copy template
cp .env.example .env

# Edit .env and add your API keys
# (use your preferred editor)
nano .env  # or vim, code, etc.
```

**Option B: Using environment variables**

```bash
# Claude
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# OpenAI
export OPENAI_API_KEY='sk-your-openai-key-here'

# Gemini
export GOOGLE_API_KEY='your-google-key-here'
```

**Option C: Use Claude Code subscription (no API key needed)**

If you have Claude Code installed and authenticated, you can use CLI mode:

```bash
# Uses your ~/.claude/.credentials.json
docker-compose run --rm reviewer \
  --repo URL \
  --reviewer python \
  --use-claude-cli
```

See [CLAUDE-CLI.md](./CLAUDE-CLI.md) for details.

### Install dependencies

**For Claude:**
```bash
uv pip install python-dotenv pyyaml anthropic
```

**For OpenAI:**
```bash
uv pip install python-dotenv pyyaml openai
```

**For Gemini:**
```bash
uv pip install python-dotenv pyyaml google-generativeai
```

**For all providers:**
```bash
uv pip install python-dotenv pyyaml anthropic openai google-generativeai
```

**Note:** `pyyaml` is required for tag configuration support.

## 2. Test Installation

```bash
# Verify structure
python test_structure.py

# Should output:
# [*] All skills accessible!
```

## 3. Run Your First Review

The tool will display the provider and package version when running:
```
[+] Using Claude (claude-sonnet-4-20250514) [anthropic v0.40.0]
```

### Using Claude (Default)

```bash
uv run review.py \
  --repo https://github.com/psf/requests \
  --reviewer refactoring-reviewer \
  --provider claude
  # Output will go to reviews/ by default
```

### Using OpenAI (GPT-4)

```bash
uv run review.py \
  --repo https://github.com/psf/requests \
  --reviewer refactoring-reviewer \
  --provider openai \
  --model gpt-4
  # Output will go to reviews/ by default
```

### Using Gemini

```bash
uv run review.py \
  --repo https://github.com/psf/requests \
  --reviewer refactoring-reviewer \
  --provider gemini
  # Output will go to reviews/ by default
```

### Using Tags for Multiple Reviewers

Tags let you run multiple related reviewers at once. Tags are defined in `tags.yaml` and you can customize them!

```bash
# Review with all Python reviewers (6 reviewers)
uv run review.py \
  --repo https://github.com/psf/requests \
  --reviewer python \
  --provider claude

# Output shows expansion:
# Input: python
# Expanded to 6 reviewer(s): refactoring-reviewer, functional-python-reviewer, zen-of-python-reviewer, format-refactoring-reviewer, python-test-reviewer, security-privacy-reviewer
```

**Available tags** (from `tags.yaml`):
- `python` - Complete Python review (6 reviewers)
- `javascript` / `js` - JavaScript/TypeScript reviewers
- `quality` - Code quality and style (3 reviewers)
- `functional` / `fp` - Functional programming patterns
- `security` / `privacy` - Security and privacy audit
- `django` - Django framework (4 reviewers)
- `testing` / `tests` - Test quality review
- `requirements` / `docs` - Requirements and documentation
- `complete` / `all` - All reviewers (9 reviewers)

**Combine tags and specific reviewers:**
```bash
# Django review + quality checks
uv run review.py \
  --repo https://github.com/user/django-app \
  --reviewer django \
  --reviewer quality \
  --provider claude
```

**Customize tags:**
Edit `tags.yaml` to create your own tag combinations:
```yaml
my-tag:
  description: My custom review combination
  reviewers:
    - refactoring-reviewer
    - security-privacy-reviewer
```

### Agentic Mode (Advanced)

For more thorough reviews, enable agentic mode where AI explores repos with bash tools:

```bash
# Requires Docker
docker-compose build
docker-compose run --rm reviewer \
  --repo https://github.com/django/django \
  --reviewer python \
  --agentic
```

**Agentic mode:**
- ✅ More thorough (AI explores dynamically)
- ✅ Handles large repos better
- ❌ Requires Docker container (for safety)
- ❌ Slower (~2-5 minutes)
- ❌ More expensive ($1-5 per review)
- ❌ Claude only (for now)

See [AGENTIC.md](./AGENTIC.md) for complete guide.

## Provider Comparison

| Provider | Models | Best For | Cost (approx per review) |
|----------|--------|----------|--------------------------|
| **Claude** | Sonnet 4, Opus 4 | Code analysis, detailed reviews | $0.50 - $2.00 |
| **OpenAI** | GPT-4, GPT-4 Turbo | General purpose, fast | $0.30 - $1.50 |
| **Gemini** | Gemini Pro | Cost-effective, good quality | $0.20 - $1.00 |

## Output

Find your generated report in the `reviews/` directory (default):

```
reviews/
└── psf-requests-refactoring-reviewer-claude-20250112_143022.md
```

**Filename format:** `{user}-{repo}-{reviewer}-{provider}-{timestamp}.md`

Example: `django-django-django-reviewer-claude-20250112_143022.md`

## Multiple Reviewers

Run multiple reviewers with one provider:

```bash
uv run review.py \
  --repo https://github.com/django/django \
  --reviewer django-reviewer \
  --reviewer security-privacy-reviewer \
  --provider claude \
  --output-dir reports
```

## Advanced Examples

### Django review with GPT-4

```bash
uv run review.py \
  --repo https://github.com/django/django \
  --reviewer django-reviewer \
  --provider openai \
  --model gpt-4-turbo-preview \
  --output-dir reports/django
```

### Security audit with Gemini

```bash
uv run review.py \
  --repo https://github.com/user/webapp \
  --reviewer security-privacy-reviewer \
  --provider gemini \
  --output-dir reports/security
```

### Compare providers

Run the same review with different providers to compare results:

```bash
# With Claude
uv run review.py --repo https://github.com/user/repo --reviewer refactoring-reviewer --provider claude --output-dir reports

# With OpenAI
uv run review.py --repo https://github.com/user/repo --reviewer refactoring-reviewer --provider openai --model gpt-4 --output-dir reports

# With Gemini
uv run review.py --repo https://github.com/user/repo --reviewer refactoring-reviewer --provider gemini --output-dir reports
```

Then compare the three generated reports!

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
# Option 1: Set in environment
export ANTHROPIC_API_KEY='sk-ant-your-key-here'

# Option 2: Add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env
```

### "openai package not installed"
```bash
uv pip install openai
```

### "google-generativeai package not installed"
```bash
uv pip install google-generativeai
```

### "uv not found"
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Can't load .env file
```bash
# Make sure python-dotenv is installed
uv pip install python-dotenv

# Or use environment variables directly
export ANTHROPIC_API_KEY='your-key'
```

## Next Steps

- See [README.md](./README.md) for full documentation
- Check [.env.example](./.env.example) for all available API keys
- Try different providers and models
- Compare review quality across providers
- Check out examples in the [examples/](./examples/) directory

## Getting API Keys

### Anthropic Claude
1. Visit https://console.anthropic.com/
2. Sign up for an account
3. Generate an API key in the API Keys section

### OpenAI
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Go to API Keys: https://platform.openai.com/api-keys
4. Create new secret key

### Google Gemini
1. Visit https://makersuite.google.com/
2. Sign in with Google account
3. Go to "Get API key"
4. Create API key for your project

---

For complete documentation, see [README.md](./README.md)
