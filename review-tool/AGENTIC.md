# Agentic Review Mode

Agentic mode enables AI to dynamically explore repositories using bash tools. Instead of receiving a fixed set of files, the AI can:
- List and find files
- Read file contents selectively
- Search for patterns
- Navigate the codebase intelligently

This results in more thorough reviews, especially for large repositories.

## 🔒 Safety First

**Agentic mode requires running in a Docker container for safety.**

The AI runs bash commands with full access (`dangerouslyDisableSandbox`). This is only safe in an isolated container environment where:
- Container is destroyed after review
- No persistent data on host
- Network can be restricted (optional)
- No access to host system

**Never run agentic mode directly on your host machine!**

## Quick Start

### Build Container

```bash
# From the claude-skills-public directory
cd claude-skills-public
docker build -f review-tool/Dockerfile -t claude-reviewer .
```

### Run Agentic Review

```bash
docker run --rm \
  -v $(pwd)/review-tool/reviews:/app/reviews \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  claude-reviewer \
  --repo https://github.com/psf/requests \
  --reviewer python \
  --agentic
```

### Using Docker Compose (Easier)

```bash
cd review-tool

# Build
docker-compose build

# Run
docker-compose run --rm reviewer \
  --repo https://github.com/psf/requests \
  --reviewer python \
  --agentic
```

## How It Works

### Standard (Batch) Mode
```
1. Clone repo
2. Python script discovers matching files (max 50)
3. Python script reads files (max 500 lines each)
4. Send all content to AI in one prompt (~50K tokens)
5. AI generates review
6. Done
```

**Pros:** Fast, predictable cost, works with all providers
**Cons:** Limited to 50 files, misses context, wastes tokens on irrelevant files

### Agentic Mode
```
1. Clone repo
2. Give AI bash tool access
3. AI explores: ls, find, cat, grep, etc.
4. AI decides what's important
5. AI reads only relevant files
6. AI generates review
7. Done
```

**Pros:** Thorough, scales to large repos, intelligent exploration
**Cons:** Slower, more expensive, Claude-only (for now), requires container

## Comparison

| Feature | Standard Mode | Agentic Mode |
|---------|---------------|--------------|
| **Speed** | ~30 seconds | ~2-5 minutes |
| **Cost** | $0.33 per review | $1-5 per review |
| **Files** | Max 50 files | Unlimited (AI decides) |
| **Providers** | Claude, OpenAI, Gemini | Claude only (for now) |
| **Environment** | Any | Container required |
| **Thoroughness** | Good | Excellent |
| **Large repos** | Struggles | Excels |

## When to Use Agentic Mode

### ✅ Use Agentic Mode When:
- Reviewing large repositories (>100 files)
- Deep analysis needed
- Complex codebases with many directories
- Want AI to discover issues dynamically
- Cost isn't primary concern
- Have time for thorough review

### ❌ Use Standard Mode When:
- Small repositories (<50 files)
- Quick feedback needed
- Cost-sensitive
- Using OpenAI or Gemini
- Simple review sufficient

## Examples

### Basic Agentic Review

```bash
docker-compose run --rm reviewer \
  --repo https://github.com/django/django \
  --reviewer python \
  --agentic
```

### Multiple Reviewers (Agentic)

```bash
docker-compose run --rm reviewer \
  --repo https://github.com/pallets/flask \
  --reviewer python \
  --reviewer security \
  --agentic
```

### With Custom Model

```bash
docker-compose run --rm reviewer \
  --repo https://github.com/user/repo \
  --reviewer django \
  --provider claude \
  --model claude-opus-4-20250514 \
  --agentic
```

### With Custom Output Directory

```bash
docker run --rm \
  -v $(pwd)/my-reviews:/app/reviews \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  claude-reviewer \
  --repo https://github.com/user/repo \
  --reviewer refactoring-reviewer \
  --agentic
```

## What the AI Can Do

In agentic mode, Claude has access to bash commands:

### File Discovery
```bash
# List files
ls -la

# Find Python files
find . -name "*.py" -type f

# Find test files
find . -path "*/tests/*.py"

# Show directory structure
tree -L 3
```

### File Reading
```bash
# Read entire file
cat src/main.py

# Read first 50 lines
head -n 50 README.md

# Read last 20 lines
tail -n 20 app.py
```

### Search and Analysis
```bash
# Search for pattern
grep -r "TODO" --include="*.py"

# Count Python files
find . -name "*.py" | wc -l

# Find large files
find . -type f -size +100k

# Search for security issues
grep -r "eval(" --include="*.py"
```

### Repository Info
```bash
# Git info
git log --oneline -10
git branch
git status

# File stats
wc -l src/*.py
```

## Cost Analysis

### Example: Django Repository

**Standard Mode:**
- Discovers 50 files (limit)
- Reads ~25K lines
- ~40K input tokens
- ~10K output tokens
- **Cost: ~$0.33**

**Agentic Mode:**
- AI explores structure (10 bash commands)
- AI identifies 15 key files
- AI reads selectively (~30 commands)
- ~60K input tokens (with tool use overhead)
- ~15K output tokens (more detailed)
- **Cost: ~$2.50**

### Cost Factors

Agentic mode costs more due to:
1. **Multiple API calls** - Each bash command is a round trip
2. **Tool use overhead** - Extra tokens for tool descriptions
3. **More thorough** - AI reads more context when needed

**Cost optimization tips:**
- Use for important reviews
- Combine with standard mode (quick check → deep dive)
- Use Opus only when critical
- Batch multiple small repos in one container run

## Security

### Container Isolation

The container provides multiple layers of security:

1. **Filesystem isolation** - Only review-tool code and cloned repo
2. **No host access** - Can't access your files
3. **Ephemeral** - Destroyed after review
4. **No persistence** - Nothing saved except mounted reviews directory
5. **Optional network isolation** - Can disable network except API calls

### What AI Can't Do

Even with bash access, the AI:
- ❌ Can't access your host system
- ❌ Can't access other containers
- ❌ Can't persist data outside mounted volume
- ❌ Can't install system packages (container is immutable during run)
- ❌ Can't access your SSH keys or credentials

### Bash Command Safety

The AI runs in the cloned repository directory:
- Commands execute in `/tmp/code_review_XXXXX/`
- Only affects cloned code (destroyed after)
- Can't `rm -rf /` the host
- Can't access `~/.ssh/` or other host directories

## Advanced Usage

### Custom Tags with Agentic Mode

```bash
# Create custom tag in tags.yaml
production-audit:
  description: Production readiness audit
  reviewers:
    - django-reviewer
    - security-privacy-reviewer
    - python-test-reviewer

# Run with agentic mode
docker-compose run --rm reviewer \
  --repo https://github.com/myorg/prod-app \
  --reviewer production-audit \
  --agentic
```

### Batch Reviews

Review multiple repos:

```bash
#!/bin/bash
REPOS=(
  "https://github.com/user/repo1"
  "https://github.com/user/repo2"
  "https://github.com/user/repo3"
)

for repo in "${REPOS[@]}"; do
  echo "Reviewing: $repo"
  docker-compose run --rm reviewer \
    --repo "$repo" \
    --reviewer python \
    --agentic
done
```

### Resource Limits

Add resource limits in docker-compose.yml:

```yaml
services:
  reviewer:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Network Isolation

For extra security, disable network except for API:

```yaml
services:
  reviewer:
    network_mode: none  # No network access
    # Or use custom network with egress rules
```

**Note:** You'll need to set up a proxy or allow only Anthropic API endpoints.

## Troubleshooting

### "Agentic mode requires container"

**Problem:** Tried to run --agentic outside container

**Solution:** Run in Docker:
```bash
docker-compose run --rm reviewer --repo URL --reviewer TAG --agentic
```

### "Only supports Claude provider"

**Problem:** Tried --agentic with OpenAI or Gemini

**Solution:** Agentic mode currently supports Claude only:
```bash
docker-compose run --rm reviewer --repo URL --reviewer TAG --provider claude --agentic
```

OpenAI and Gemini support coming in future versions.

### "API key not set"

**Problem:** ANTHROPIC_API_KEY not passed to container

**Solution:** Set environment variable:
```bash
# Option 1: Export before running
export ANTHROPIC_API_KEY='sk-ant-...'
docker-compose run --rm reviewer ...

# Option 2: Pass directly
docker-compose run --rm -e ANTHROPIC_API_KEY='sk-ant-...' reviewer ...

# Option 3: Use .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
docker-compose run --rm reviewer ...
```

### Review taking too long

**Problem:** Agentic review stuck or taking >10 minutes

**Possible causes:**
1. Very large repository
2. AI exploring too many files
3. Network issues

**Solutions:**
- Check logs: `docker-compose logs`
- Kill and retry: `docker-compose down`
- Use standard mode for initial review
- Try smaller tag (e.g., `security` instead of `complete`)

### Out of memory

**Problem:** Container crashes during review

**Solution:** Increase memory limit in docker-compose.yml:
```yaml
deploy:
  resources:
    limits:
      memory: 8G  # Increase from 4G
```

## Future Enhancements

### Coming Soon:
- ✅ Claude agentic mode (implemented)
- 🔄 OpenAI function calling support
- 🔄 Gemini tool use support
- 🔄 Multi-turn conversations for deeper analysis
- 🔄 Caching for repeated reviews
- 🔄 Incremental reviews (only changed files)

### Planned Features:
- Local model support (Ollama, LM Studio)
- Custom tool definitions
- Review result caching
- Diff-based reviews
- PR integration
- CI/CD workflows

## Summary

**Agentic mode gives AI the ability to explore code dynamically, resulting in more thorough reviews.**

**Key Points:**
- 🔒 **Requires container** for safety
- 🤖 **Claude only** (for now)
- 💰 **More expensive** but more thorough
- ⏱️ **Slower** but better for large repos
- 🎯 **Best for production-critical code**

**Get Started:**
```bash
cd review-tool
docker-compose build
docker-compose run --rm reviewer \
  --repo https://github.com/user/repo \
  --reviewer python \
  --agentic
```

---

For more information:
- [README.md](./README.md) - Main documentation
- [QUICKSTART.md](./QUICKSTART.md) - Quick start guide
- [PROVIDERS.md](./PROVIDERS.md) - Provider comparison
- [TAGS.md](./TAGS.md) - Reviewer tags guide
