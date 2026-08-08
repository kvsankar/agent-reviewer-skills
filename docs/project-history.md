# Project History

This is the canonical project timeline. It records decisions and outcomes, not
session-by-session activity.

## November 2025: Initial system

- Created the first Python, API, and database reviewer skills.
- Standardized language-prefixed skill names and mnemonic finding IDs.
- Built the Docker-based Claude review tool and worked around WSL Docker issues
  with an Ubuntu VM.
- Expanded the collection to JavaScript, React, Django, security, performance,
  testing, and refactoring reviews.
- Established isolated reviewer contexts and structured Markdown output with
  evidence, suggested changes, and rationale.

## December 2025: Expansion and research

- Added expected-good-pattern checks, Playwright coverage, and the
  code-authenticity reviewer.
- Added cross-platform installation and split several oversized skill files.
- Published the Rhodes Python reviewer with Brandon Rhodes' permission.
- Researched few-shot code review and built an embedding-based guideline
  retrieval prototype. The prototype was abandoned because lexical similarity
  did not handle architectural guidance reliably.

## March 2026: Mobile coverage

- Added React Native/Expo and Appium reviewers, bringing the collection to 23.
- Updated the legacy review tool's tags and documentation.

## August 2026: Evaluation and closure

- Replaced the Docker harness for new evaluations with direct Ollama calls,
  Pi for local agentic runs, Codex for a hosted agentic baseline, and Claude for
  reference matching and source-aware novel-finding adjudication.
- Withdrew synthetic-fixture runs as effectiveness evidence and adopted a
  real-code-only policy.
- Tested Qwen3 Coder 30B and Devstral Small 2 through Ollama and Pi; neither
  produced validated evidence that the skills improved real-repository review.
- Compared three ordinary Codex reviews with three reviews using a compact
  Rhodes-inspired skill. The guided condition did not materially improve review
  quality and found fewer distinct validated defects.
- Concluded the experiment, deprecated the Docker harness, retained auditable
  evidence, and stopped active skill expansion.

The final decision, measurements, and limitations are in
[Experiment Conclusion](experiment-conclusion-2026-08-08.md). The reproducible
evaluation design is in [Evaluation Harness](evaluation-harness.md).
