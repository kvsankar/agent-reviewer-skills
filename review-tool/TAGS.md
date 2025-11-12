# Reviewer Tags Guide

Tags are shortcuts to run multiple related reviewers at once. Each reviewer runs with **fresh context**, generating separate reports.

**Tags are defined in `tags.yaml` - you can customize them for your needs!**

## Quick Start

```bash
# Use a tag instead of listing multiple reviewers
uv run review.py --repo https://github.com/psf/requests --reviewer python --provider claude

# Output shows expansion:
# Input: python
# Expanded to 6 reviewer(s): refactoring-reviewer, functional-python-reviewer, zen-of-python-reviewer, format-refactoring-reviewer, python-test-reviewer, security-privacy-reviewer
```

## Default Tags

The default `tags.yaml` includes these tags:

| Tag | Count | Description |
|-----|-------|-------------|
| `python` | 6 | Complete Python review (refactoring, FP, style, format, tests, security) |
| `javascript` / `js` | 1 | JavaScript/TypeScript functional programming |
| `quality` | 3 | Code quality and style (refactoring, zen, format) |
| `functional` / `fp` | 2 | Functional programming patterns (Python & JavaScript) |
| `security` / `privacy` | 1 | Security and privacy audit |
| `django` | 4 | Django framework (django, refactoring, security, tests) |
| `testing` / `tests` | 1 | Test quality review |
| `requirements` / `docs` | 1 | Requirements and documentation review |
| `complete` / `all` | 9 | All available reviewers |

## Customizing Tags

### Edit tags.yaml

The `tags.yaml` file has a simple structure:

```yaml
# Language-specific tags
python:
  description: Complete Python code review
  reviewers:
    - refactoring-reviewer
    - functional-python-reviewer
    - zen-of-python-reviewer
    - format-refactoring-reviewer
    - python-test-reviewer
    - security-privacy-reviewer

# Add your own tags
my-api-review:
  description: My custom API review workflow
  reviewers:
    - security-privacy-reviewer
    - refactoring-reviewer
```

### Format

```yaml
tag-name:
  description: What this tag does (shown in listings)
  reviewers:
    - reviewer-name-1
    - reviewer-name-2
    - reviewer-name-3
```

**Key points:**
- Tag names should be lowercase with hyphens
- Each tag must have `description` and `reviewers` fields
- Reviewers must match names from the available reviewers list
- Duplicates are automatically removed when combining tags

### Available Reviewers

```
agile-requirements-reviewer
django-reviewer
format-refactoring-reviewer
functional-javascript-reviewer
functional-python-reviewer
python-test-reviewer
refactoring-reviewer
security-privacy-reviewer
zen-of-python-reviewer
```

## Example Custom Tags

### Project-Specific Tags

```yaml
# For your React project
react-review:
  description: React application review
  reviewers:
    - functional-javascript-reviewer
    - security-privacy-reviewer

# For your FastAPI project
fastapi-review:
  description: FastAPI backend review
  reviewers:
    - refactoring-reviewer
    - security-privacy-reviewer
    - python-test-reviewer

# Pre-commit checks
pre-commit:
  description: Quick quality checks before commit
  reviewers:
    - refactoring-reviewer
    - zen-of-python-reviewer
```

### Team Workflow Tags

```yaml
# Junior developer review - focus on basics
junior-review:
  description: Basic code quality for learning
  reviewers:
    - zen-of-python-reviewer
    - format-refactoring-reviewer

# Senior review - comprehensive
senior-review:
  description: Production-ready review
  reviewers:
    - refactoring-reviewer
    - functional-python-reviewer
    - security-privacy-reviewer
    - python-test-reviewer

# Security-focused
security-audit:
  description: Security-focused review
  reviewers:
    - security-privacy-reviewer
    - refactoring-reviewer
```

### Language-Specific Tags

```yaml
# Backend Python
backend:
  description: Backend Python service review
  reviewers:
    - refactoring-reviewer
    - functional-python-reviewer
    - security-privacy-reviewer

# Frontend JavaScript
frontend:
  description: Frontend JavaScript review
  reviewers:
    - functional-javascript-reviewer

# Full-stack
fullstack:
  description: Full-stack application review
  reviewers:
    - refactoring-reviewer
    - functional-python-reviewer
    - functional-javascript-reviewer
    - security-privacy-reviewer
```

## Using Tags

### Single Tag

```bash
uv run review.py --repo URL --reviewer python --provider claude
```

### Multiple Tags

```bash
# Combines tags, removes duplicates
uv run review.py --repo URL --reviewer django --reviewer quality --provider claude
```

### Mix Tags and Reviewers

```bash
# Use tag + specific reviewer
uv run review.py --repo URL --reviewer python --reviewer agile-requirements-reviewer --provider claude
```

### Tag Expansion

The tool shows what tags expand to:

```
Input: django, quality
Expanded to 5 reviewer(s): django-reviewer, refactoring-reviewer, security-privacy-reviewer, python-test-reviewer, zen-of-python-reviewer, format-refactoring-reviewer
```

## How Tags Work

### Fresh Context

Each reviewer gets:
- **Independent context** - No shared state between reviewers
- **Full skill prompt** (~10K tokens)
- **Full code context** (~50K tokens)
- **Separate report** - Individual markdown file

### Duplicate Removal

When combining tags:
```bash
--reviewer python --reviewer django
```

The tool automatically removes duplicates. If both tags include `security-privacy-reviewer`, it only runs once.

### Order Preservation

Reviewers run in the order they appear after expansion, with duplicates removed.

## Cost Considerations

### Per-Tag Costs (approximate)

| Provider | `python` (6) | `django` (4) | `complete` (9) |
|----------|--------------|--------------|----------------|
| **Claude Sonnet 4** | $2.00 | $1.32 | $3.00 |
| **OpenAI GPT-4** | $5.16 | $3.44 | $7.74 |
| **Gemini Pro** | $0.24 | $0.16 | $0.36 |

### Cost Optimization Tips

1. **Start with Gemini** for broad tag reviews
2. **Use Claude** for targeted, critical reviews
3. **Create smaller tags** for specific needs instead of using `complete`
4. **Combine wisely** - Check expansion to avoid unnecessary reviewers

## Best Practices

### 1. Create Workflow Tags

Match your development workflow:
```yaml
pre-commit:
  description: Quick checks before commit
  reviewers:
    - refactoring-reviewer
    - format-refactoring-reviewer

pre-merge:
  description: Full review before merge
  reviewers:
    - refactoring-reviewer
    - security-privacy-reviewer
    - python-test-reviewer

pre-production:
  description: Production readiness check
  reviewers:
    - django-reviewer
    - security-privacy-reviewer
    - python-test-reviewer
```

### 2. Team-Specific Tags

Create tags for your team's needs:
```yaml
backend-team:
  description: Backend team's standard review
  reviewers:
    - refactoring-reviewer
    - functional-python-reviewer
    - security-privacy-reviewer

frontend-team:
  description: Frontend team's standard review
  reviewers:
    - functional-javascript-reviewer
```

### 3. Project Templates

Create tags for different project types:
```yaml
new-microservice:
  description: Review for new microservice
  reviewers:
    - refactoring-reviewer
    - security-privacy-reviewer
    - python-test-reviewer

legacy-refactor:
  description: Legacy code refactoring review
  reviewers:
    - refactoring-reviewer
    - zen-of-python-reviewer
    - python-test-reviewer
```

### 4. Keep It Simple

- Use clear, descriptive tag names
- Don't create too many tags (5-10 is usually enough)
- Document your tags in comments
- Start with defaults, customize as needed

## Troubleshooting

### "Tags file not found"

```
[!] Warning: Tags file not found: /path/to/tags.yaml
[!] Tag expansion will not work. Using individual reviewers only.
```

**Solution:** Create `tags.yaml` in the `review-tool/` directory.

### "Invalid tag format"

```
[!] Warning: Invalid tag format for 'my-tag' in tags.yaml
```

**Solution:** Check your YAML syntax. Each tag needs:
```yaml
my-tag:
  description: "Description here"
  reviewers:
    - reviewer-name
```

### "Invalid reviewer(s)"

```
[-] Error: Invalid reviewer(s): my-reviewer
```

**Solution:** Check the reviewer name. Use only these names:
- `agile-requirements-reviewer`
- `django-reviewer`
- `format-refactoring-reviewer`
- `functional-javascript-reviewer`
- `functional-python-reviewer`
- `python-test-reviewer`
- `refactoring-reviewer`
- `security-privacy-reviewer`
- `zen-of-python-reviewer`

### Tag Not Expanding

If a tag isn't expanding, check:
1. Tag name is lowercase in `tags.yaml`
2. YAML syntax is correct (use 2-space indentation)
3. `pyyaml` is installed: `uv pip install pyyaml`

## Version Control

### Commit tags.yaml

Commit your customized `tags.yaml` to version control:
```bash
git add tags.yaml
git commit -m "Add custom review tags for our workflow"
```

### Team Sharing

Share tags with your team:
1. Customize `tags.yaml`
2. Commit to repository
3. Team members pull and use the same tags

### Multiple Configurations

Create different tag files for different purposes:
```bash
# Development tags
cp tags.yaml tags-dev.yaml

# Production tags
cp tags.yaml tags-prod.yaml

# Use specific config (future feature)
# uv run review.py --tags-file tags-prod.yaml ...
```

## Summary

**Key points:**
- Tags defined in `tags.yaml` (customizable)
- Each reviewer runs with fresh context
- Duplicates automatically removed
- Create your own tags for workflows
- Simple YAML format
- Share with team via git

**Quick examples:**
```bash
# Use default tags
uv run review.py --repo URL --reviewer python --provider claude

# Combine tags
uv run review.py --repo URL --reviewer django --reviewer quality --provider claude

# Customize tags
# Edit tags.yaml, then use your custom tags
uv run review.py --repo URL --reviewer my-custom-tag --provider claude
```

---

For more information:
- [README.md](./README.md) - Main documentation
- [QUICKSTART.md](./QUICKSTART.md) - Quick start guide
- [PROVIDERS.md](./PROVIDERS.md) - Provider comparison
- [tags.yaml](./tags.yaml) - Tag configuration file
