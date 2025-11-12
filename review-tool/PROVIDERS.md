# AI Provider Guide

The review tool supports three AI providers: **Claude**, **OpenAI**, and **Gemini**.

## Supported Providers

### 1. Anthropic Claude

**Models:**
- `claude-sonnet-4-20250514` (default) - Latest Sonnet, best balance
- `claude-opus-4-20250514` - Most capable, highest cost
- `claude-3-5-sonnet-20241022` - Previous generation

**Best for:**
- Detailed code analysis
- Security reviews
- Complex refactoring recommendations
- Following detailed guidelines

**Setup:**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
# or add to .env file
```

**Usage:**
```bash
uv run review.py \
  --repo https://github.com/user/repo \
  --reviewer django-reviewer \
  --provider claude \
  --model claude-sonnet-4-20250514
```

**Cost:** $3/$15 per MTok (input/output)

---

### 2. OpenAI (GPT-4)

**Models:**
- `gpt-4-turbo-preview` (default) - Latest GPT-4 Turbo
- `gpt-4` - Standard GPT-4
- `gpt-4-1106-preview` - 128K context window
- `gpt-3.5-turbo` - Faster, cheaper

**Best for:**
- General purpose reviews
- Fast iteration
- Cost-effective analysis
- Good balance of quality and speed

**Setup:**
```bash
export OPENAI_API_KEY='sk-your-openai-key-here'
# or add to .env file
```

**Usage:**
```bash
uv run review.py \
  --repo https://github.com/user/repo \
  --reviewer refactoring-reviewer \
  --provider openai \
  --model gpt-4
```

**Cost:** $10/$30 per MTok (input/output) for GPT-4

---

### 3. Google Gemini

**Models:**
- `gemini-pro` (default) - Standard model
- `gemini-pro-vision` - Multimodal (not used for code review)
- `gemini-1.5-pro` - Larger context window

**Best for:**
- Cost-effective reviews
- High-volume analysis
- Quick assessments
- Budget-conscious projects

**Setup:**
```bash
export GOOGLE_API_KEY='your-google-key-here'
# or GEMINI_API_KEY
# or add to .env file
```

**Usage:**
```bash
uv run review.py \
  --repo https://github.com/user/repo \
  --reviewer security-privacy-reviewer \
  --provider gemini
```

**Cost:** Free tier available, then ~$0.50/$1.50 per MTok

---

## Provider Comparison

| Feature | Claude | OpenAI | Gemini |
|---------|--------|--------|--------|
| **Best Model** | Sonnet 4 | GPT-4 Turbo | Gemini Pro |
| **Context Window** | 200K | 128K | 128K-1M |
| **Code Analysis** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Security Focus** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cost** | $$$ | $$ | $ |
| **Output Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Installation

### Install specific provider

```bash
# Claude only
uv pip install python-dotenv anthropic

# OpenAI only
uv pip install python-dotenv openai

# Gemini only
uv pip install python-dotenv google-generativeai
```

### Install all providers

```bash
uv pip install python-dotenv anthropic openai google-generativeai
```

### Using pyproject.toml extras

```bash
# Install Claude support
uv pip install -e ".[claude]"

# Install OpenAI support
uv pip install -e ".[openai]"

# Install Gemini support
uv pip install -e ".[gemini]"

# Install all providers
uv pip install -e ".[all]"
```

## Authentication

### Method 1: .env File (Recommended)

```bash
# Copy template
cp .env.example .env

# Edit .env and add your keys
# .env file:
ANTHROPIC_API_KEY=sk-ant-your-key
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=your-google-key
```

The tool automatically loads .env via python-dotenv.

### Method 2: Environment Variables

```bash
export ANTHROPIC_API_KEY='sk-ant-your-key'
export OPENAI_API_KEY='sk-your-openai-key'
export GOOGLE_API_KEY='your-google-key'
```

### Method 3: External Auth (CLI tools)

For external authentication setups:
- **gcloud**: `gcloud auth application-default login` (for Gemini)
- **aws**: AWS credentials for Bedrock models (future)
- The tool relies on SDK's default credential chain

## Usage Examples

### Basic Usage

```bash
# Claude (default)
uv run review.py --repo URL --reviewer REVIEWER --provider claude

# OpenAI
uv run review.py --repo URL --reviewer REVIEWER --provider openai

# Gemini
uv run review.py --repo URL --reviewer REVIEWER --provider gemini
```

### With Specific Models

```bash
# Claude Opus (most capable)
uv run review.py --repo URL --reviewer REVIEWER --provider claude --model claude-opus-4-20250514

# GPT-4 Turbo
uv run review.py --repo URL --reviewer REVIEWER --provider openai --model gpt-4-turbo-preview

# Gemini 1.5 Pro
uv run review.py --repo URL --reviewer REVIEWER --provider gemini --model gemini-1.5-pro
```

### Compare Providers

Run same review with different providers:

```bash
REPO="https://github.com/user/project"
REVIEWER="django-reviewer"

# Claude
uv run review.py --repo $REPO --reviewer $REVIEWER --provider claude --output-dir reports

# OpenAI
uv run review.py --repo $REPO --reviewer $REVIEWER --provider openai --model gpt-4 --output-dir reports

# Gemini
uv run review.py --repo $REPO --reviewer $REVIEWER --provider gemini --output-dir reports
```

Compare the three reports to see quality, detail, and focus differences!

## Cost Estimation

Approximate costs per review (with ~50 files, ~500 lines each):

### Input Tokens
- Skill prompt: ~10K tokens
- Code files: ~40K tokens
- **Total input:** ~50K tokens

### Output Tokens
- Review report: ~10-15K tokens

### Per-Review Cost

**Claude Sonnet 4:**
- Input: 50K × $3/1M = $0.15
- Output: 12K × $15/1M = $0.18
- **Total: ~$0.33**

**OpenAI GPT-4:**
- Input: 50K × $10/1M = $0.50
- Output: 12K × $30/1M = $0.36
- **Total: ~$0.86**

**Gemini Pro:**
- Input: 50K × $0.50/1M = $0.025
- Output: 12K × $1.50/1M = $0.018
- **Total: ~$0.04**

💡 *Actual costs vary based on code size and review complexity*

## Best Practices

### 1. Provider Selection

**Use Claude for:**
- Production-critical reviews
- Security audits
- Detailed refactoring
- Django/Python expertise

**Use OpenAI for:**
- General code review
- Fast iteration
- Good balance of quality/cost
- Broad language support

**Use Gemini for:**
- High-volume reviews
- Budget constraints
- Quick assessments
- Experimental analysis

### 2. Model Selection

**Default models are recommended:**
- Claude: `claude-sonnet-4-20250514`
- OpenAI: `gpt-4-turbo-preview`
- Gemini: `gemini-pro`

**Use premium models for:**
- Critical production code
- Security-sensitive reviews
- Complex architectural analysis

**Use cheaper models for:**
- Draft reviews
- Learning/experimentation
- High-volume batch processing

### 3. Cost Optimization

- **Start with Gemini** for initial assessment
- **Use Claude/GPT-4** for final production review
- **Limit file count** with focused patterns
- **Review incrementally** (only changed files)
- **Monitor API usage** via provider dashboards

### 4. Quality Optimization

- **Use Claude** for most detailed analysis
- **Compare providers** on same codebase
- **Specify exact models** for consistency
- **Review smaller chunks** for better focus

## Error Handling

The tool provides clear error messages:

```
[-] Error initializing claude provider: ANTHROPIC_API_KEY not set
[-] Error initializing openai provider: openai package not installed
[-] Error initializing gemini provider: GOOGLE_API_KEY or GEMINI_API_KEY not set
```

**Common fixes:**
1. Check API key is set (env var or .env)
2. Install required package: `uv pip install anthropic/openai/google-generativeai`
3. Verify API key is valid and has credits
4. Check network connectivity

## Rate Limits

### Claude
- Tier 1: 50 requests/min
- Tier 2: 1000 requests/min
- See: https://docs.anthropic.com/claude/reference/rate-limits

### OpenAI
- Free tier: 3 requests/min
- Paid tier: 3500 requests/min (GPT-4)
- See: https://platform.openai.com/docs/guides/rate-limits

### Gemini
- Free tier: 60 requests/min
- Paid tier: Higher limits
- See: https://ai.google.dev/pricing

💡 **Tip:** For batch reviews, add delays between requests or use provider's batch API if available.

## Future Providers

Planned support:
- ✅ Claude (Anthropic)
- ✅ OpenAI (GPT-4)
- ✅ Gemini (Google)
- 🔄 Azure OpenAI
- 🔄 AWS Bedrock (Claude, Titan)
- 🔄 Cohere
- 🔄 Local models (Ollama, LM Studio)

## Troubleshooting

### Provider-Specific Issues

**Claude:**
```bash
# Error: anthropic package not installed
uv pip install anthropic

# Error: API key invalid
# Check key format: sk-ant-api03-...
```

**OpenAI:**
```bash
# Error: openai package not installed
uv pip install openai

# Error: API key invalid
# Check key format: sk-...
```

**Gemini:**
```bash
# Error: google-generativeai package not installed
uv pip install google-generativeai

# Error: API key invalid
# Get key from: https://makersuite.google.com/app/apikey
```

### Getting Help

- Provider docs: See links in respective sections
- Tool docs: [README.md](./README.md)
- Quick start: [QUICKSTART.md](./QUICKSTART.md)
- Examples: [examples/](./examples/)

---

**Choose the right provider for your needs: Quality, Speed, or Cost!**
