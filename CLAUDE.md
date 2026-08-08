# CLAUDE.md

## Purpose and Status

This repository is a concluded experiment in prompt-based code review. Its
real-code evaluation did not show a material advantage over ordinary Codex
review. Preserve it for reproducibility and attribution; do not expand it as an
active skill product.

Use the canonical documents instead of repeating their content here:

| Question | Canonical document |
| --- | --- |
| What is this repository and which skills exist? | [`README.md`](README.md) |
| What was the final result? | [`docs/experiment-conclusion-2026-08-08.md`](docs/experiment-conclusion-2026-08-08.md) |
| How did the evaluation work? | [`docs/evaluation-harness.md`](docs/evaluation-harness.md) |
| How did the project evolve? | [`docs/project-history.md`](docs/project-history.md) |
| How did the old Docker tool work? | [`review-tool/README.md`](review-tool/README.md) |

## Repository-Specific Rules

- Each `*-reviewer/` directory owns its `SKILL.md`, user-facing `README.md`, and
  attribution `SOURCES.md`. Keep a skill self-contained.
- New effectiveness claims must use immutable real upstream code. Synthetic or
  planted fixtures may test plumbing only and must never support a quality claim.
- Keep non-agentic Ollama and agentic Pi results separate; they answer different
  questions.
- Treat Claude matching and adjudication as auditable model judgments, not truth
  by agreement.
- The Docker and Claude Agent SDK code under `review-tool/` is deprecated. Do
  not add new evaluation features there.
- Do not commit raw conversations, local repository symlinks, private origin
  maps, credentials, or large regenerable event streams.
- Preserve source attribution and Brandon Rhodes' permission statement.

## Validation

Run the harness regression tests after changing `experiments/`:

```bash
PYTHONPATH=experiments python3 -m unittest discover \
  -s experiments -p 'test_*.py' -v
```

Run the repository Markdown hook after documentation changes:

```bash
pre-commit run markdownlint --all-files
```

## Working Agreements

- Fix hook failures; do not skip hooks or rewrite history to hide them.
- Diagnose root causes before changing behavior.
- After two failed approaches to the same problem, stop and reassess.
- Read source documents before editing them; do not fabricate documentation.
