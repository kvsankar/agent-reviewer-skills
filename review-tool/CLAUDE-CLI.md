# Claude CLI Authentication

Use your Claude Code subscription without API keys by using the Claude CLI.

## Overview

If you have a Claude Code subscription but don't have (or don't want to use) an API key, you can use the Claude CLI which authenticates via your `~/.claude/.credentials.json` file.

**Key difference:**
- **API Key Mode**: Uses `ANTHROPIC_API_KEY` environment variable
- **CLI Mode**: Uses `~/.claude/.credentials.json` OAuth tokens from Claude Code

## Quick Start

### Step 1: Build Container with CLI Support

```bash
cd claude-skills-public
docker build -f review-tool/Dockerfile -t claude-reviewer .
```

The Docker image includes:
- Claude CLI (`@anthropic-ai/claude-cli` npm package)
- Node.js and npm
- Ready to mount your credentials

### Step 2: Run with CLI Authentication

```bash
docker run --rm \
  -v $(pwd)/review-tool/reviews:/app/reviews \
  -v ~/.claude/.credentials.json:/root/.claude/.credentials.json:ro \
  claude-reviewer \
  --repo https://github.com/psf/requests \
  --reviewer python \
  --use-claude-cli
```

**Or with docker-compose** (credentials already mounted):

```bash
cd review-tool
docker-compose build
docker-compose run --rm reviewer \
  --repo https://github.com/psf/requests \
  --reviewer python \
  --use-claude-cli
```

## How It Works

```
1. Mount ~/.claude/.credentials.json into container (read-only)
2. Container has Claude CLI installed
3. Script calls: claude chat --file prompt.txt
4. CLI reads OAuth token from mounted credentials
5. CLI authenticates to Anthropic and returns response
6. Script formats response as review report
```

## Authentication Comparison

| Method | Requires | Good For | Setup |
|--------|----------|----------|-------|
| **API Key** | `ANTHROPIC_API_KEY` | Production, CI/CD | Get key from console.anthropic.com |
| **CLI Mode** | Claude Code subscription | Personal use, existing Claude Code users | Already authenticated if using Claude Code |

## Usage Examples

### Standard Mode with CLI

```bash
docker-compose run --rm reviewer \
  --repo https://github.com/django/django \
  --reviewer python \
  --provider claude \
  --use-claude-cli
```

### Agentic Mode with CLI

```bash
docker-compose run --rm reviewer \
  --repo https://github.com/django/django \
  --reviewer python \
  --agentic \
  --use-claude-cli
```

**Note:** Agentic mode with CLI gives Claude bash tool access. Safe in container but powerful!

### Multiple Reviewers

```bash
docker-compose run --rm reviewer \
  --repo https://github.com/pallets/flask \
  --reviewer django \
  --reviewer security \
  --use-claude-cli
```

### Custom Model

```bash
docker-compose run --rm reviewer \
  --repo https://github.com/user/repo \
  --reviewer refactoring-reviewer \
  --model claude-opus-4-20250514 \
  --use-claude-cli
```

## Credentials File Format

Your `~/.claude/.credentials.json` contains:

```json
{
  "claudeAiOauth": {
    "accessToken": "sk-ant-oat01-...",
    "refreshToken": "sk-ant-ort01-...",
    "expiresAt": 1762937224961,
    "subscriptionType": "max"
  }
}
```

**Security:**
- File is mounted **read-only** (`:ro` flag)
- Container can't modify your credentials
- Container is destroyed after review
- No credentials leave your machine

## Token Expiration

OAuth tokens expire periodically. If you get authentication errors:

```bash
# Check token expiration
python << 'EOF'
import json
from pathlib import Path
from datetime import datetime

creds = json.load(open(Path.home() / '.claude' / '.credentials.json'))
expires = datetime.fromtimestamp(creds['claudeAiOauth']['expiresAt'] / 1000)
print(f"Token expires: {expires}")
EOF

# If expired, refresh by using Claude Code
# Just open Claude Code - it will auto-refresh tokens
```

## Advantages of CLI Mode

**✅ No API key needed**
- Use your existing Claude Code subscription
- No need to generate/manage API keys
- Already authenticated

**✅ Same subscription limits**
- Uses your Claude Code subscription tier
- No separate billing
- Same rate limits as Claude Code

**✅ Secure**
- Credentials mounted read-only
- No API keys in environment variables
- Token stays on your machine

## Disadvantages

**❌ Requires container**
- Must run in Docker (can't run directly on host easily)
- Slightly more setup than API key mode

**❌ Slower**
- CLI adds overhead vs direct SDK calls
- Each request shells out to claude CLI

**❌ Less flexibility**
- Can't easily pass to CI/CD
- Harder to share with team

## When to Use Each Mode

### Use CLI Mode When:
- You have Claude Code subscription
- Personal development machine
- Don't want to manage API keys
- Already using Claude Code regularly

### Use API Key Mode When:
- Running in CI/CD
- Team shared environment
- Need fastest performance
- Want simpler Docker setup

## Troubleshooting

### "Claude CLI not found"

**Problem:** Container can't find `claude` command

**Solution:** Rebuild container:
```bash
docker-compose build --no-cache
```

The Dockerfile installs Claude CLI automatically.

### "Claude credentials not found"

**Problem:** `.credentials.json` not mounted

**Solution:** Check docker-compose.yml has:
```yaml
volumes:
  - ~/.claude/.credentials.json:/root/.claude/.credentials.json:ro
```

Or when using `docker run`:
```bash
-v ~/.claude/.credentials.json:/root/.claude/.credentials.json:ro
```

### "Authentication failed"

**Problem:** OAuth token expired

**Solution:**
1. Open Claude Code on your machine
2. It will auto-refresh the token
3. Try review again

### "Permission denied"

**Problem:** Credentials file not readable

**Solution:** Check file permissions:
```bash
ls -la ~/.claude/.credentials.json
chmod 600 ~/.claude/.credentials.json
```

### CLI hangs or times out

**Problem:** CLI call taking too long

**Current timeout:** 5 minutes

**Solutions:**
- Reduce prompt size (fewer files)
- Use standard mode instead of agentic
- Check network connection
- Try API key mode for better performance

## Mixed Mode (Advanced)

You can run some reviews with CLI, others with API key:

```bash
# Review 1: Use CLI (your subscription)
docker-compose run --rm reviewer \
  --repo https://github.com/user/personal-project \
  --reviewer python \
  --use-claude-cli

# Review 2: Use API key (company account)
docker-compose run --rm \
  -e ANTHROPIC_API_KEY=$COMPANY_API_KEY \
  reviewer \
  --repo https://github.com/company/project \
  --reviewer python
```

## Cost Considerations

**CLI Mode uses your Claude Code subscription:**
- Max tier: More generous limits
- Same as using Claude Code directly
- No per-token billing (flat subscription)

**API Key Mode:**
- Pay-per-token
- $3/$15 per MTok (Sonnet 4)
- Better for occasional use

## Security Best Practices

### 1. Always Mount Read-Only

```yaml
volumes:
  - ~/.claude/.credentials.json:/root/.claude/.credentials.json:ro
#                                                                ^^^ read-only
```

### 2. Don't Commit Credentials

Already in `.gitignore`:
```
.env
*.json
```

### 3. Use Container Isolation

Don't run with `--use-claude-cli` outside container:
```bash
# ❌ DON'T DO THIS (on host)
python review.py --repo URL --reviewer python --use-claude-cli

# ✅ DO THIS (in container)
docker-compose run --rm reviewer --repo URL --reviewer python --use-claude-cli
```

### 4. Limit Container Resources

In docker-compose.yml:
```yaml
deploy:
  resources:
    limits:
      memory: 4G
      cpus: '2'
```

## Summary

**Claude CLI mode lets Claude Code subscription users run reviews without API keys.**

**Key points:**
- 🔑 Uses `~/.claude/.credentials.json` OAuth tokens
- 🐳 Requires Docker container
- 🔒 Credentials mounted read-only
- 📦 Claude CLI included in container
- ⚡ Slightly slower than API key mode
- 💰 Uses your subscription (no per-token cost)

**Get started:**
```bash
cd review-tool
docker-compose build
docker-compose run --rm reviewer \
  --repo https://github.com/psf/requests \
  --reviewer python \
  --use-claude-cli
```

---

For more information:
- [README.md](./README.md) - Main documentation
- [AGENTIC.md](./AGENTIC.md) - Agentic mode guide
- [PROVIDERS.md](./PROVIDERS.md) - Provider comparison
