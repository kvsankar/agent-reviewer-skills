# Project History

This is the canonical project timeline. It records decisions and outcomes, not
session-by-session activity.

## October-November 2025: Origins and expansion

- Began on 30 October by researching
  [Brandon Rhodes](https://rhodesmill.org/brandon/)' teaching material,
  extracting Python design guidance, assigning short mnemonic IDs, and packaging
  the result as a Claude Code reviewer skill.
- Used the early Rhodes and functional Python skills as practical review aids,
  including reviewing the examples in other skills.
- Created the first repository commit on 10 November and expanded the collection
  across Python, JavaScript, React, Django, APIs, databases, security,
  performance, testing, and refactoring.
- Built the Docker-based Claude review tool for isolated agentic runs and worked
  around WSL Docker issues with an Ubuntu VM.
- Standardized language-prefixed names and structured Markdown findings with
  mnemonic IDs, evidence, suggested changes, and rationale.

## December 2025-January 2026: Research and full collection

- Added expected-good-pattern checks, Playwright coverage, the
  code-authenticity reviewer, cross-platform installation, and split skill files
  that had grown too large.
- Researched few-shot and in-context learning for code review and compared those
  findings with the skills' static before-and-after examples.
- Started an embedding-based guideline retrieval prototype after identifying
  dynamic selection and quantitative benchmarking as gaps.
- Published the Rhodes Python reviewer with
  [Brandon Rhodes](https://rhodesmill.org/brandon/)' permission.
- Added React Native/Expo and Appium reviewers in January, bringing the
  collection to 23.

## March 2026: Retrieval and automated evaluation

- Revisited the retrieval prototype with embeddings and tree-sitter code units,
  then abandoned it because similarity matching did not reliably select
  architectural or philosophical guidance.
- Recovered and expanded the in-context-learning research before returning to
  direct experiments on review quality.
- Built automated runners, ground-truth matching, and LLM-as-judge evaluation.
- Compared zero-shot and generic prompts with full skills, principles-only,
  IDs-only, trimmed, and hybrid variants.
- Found high run-to-run variance and answer leakage in synthetic fixtures. Real
  repository reviews were attempted, but the evidence was not strong enough to
  support a conclusion.

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
