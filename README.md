# Reviewer Skills Experiment

> [!NOTE]
> **Experiment concluded in August 2026.** The final real-code comparison found
> no material advantage from a compact reviewer skill over an ordinary Codex
> review, and the guided reviews found fewer distinct validated defects. The
> tested local models also showed no validated benefit. This repository is an
> experimental archive, not a demonstrated review-quality product.

The repository contains 23 reviewer skills, the evaluation harness, and the
evidence behind that negative result. The canonical account is the
[experiment conclusion](docs/experiment-conclusion-2026-08-08.md).

## Final Result

| Condition | Runs | Frozen-reference recall | Validated per run | Distinct validated defects |
| --- | ---: | ---: | ---: | ---: |
| Regular Codex review | 3 | 28.5% | 8.67 | 18 |
| Codex with lean skill | 3 | 30.2% | 8.33 | 13 |

The small recall difference did not translate into more useful discovery. The
regular condition produced one more validated finding overall and five more
distinct validated defects. See the conclusion for methodology, local-model
results, interpretation, and limitations.

## Repository Map

| Path | Canonical purpose |
| --- | --- |
| `*-reviewer/` | Individual skill prompt, usage README, and source attribution |
| `experiments/` | Current evaluation runners and retained evidence |
| [`docs/evaluation-harness.md`](docs/evaluation-harness.md) | Evaluation methodology and reproduction commands |
| [`docs/experiment-conclusion-2026-08-08.md`](docs/experiment-conclusion-2026-08-08.md) | Final decision and results |
| [`docs/project-history.md`](docs/project-history.md) | Concise project timeline |
| [`docs/research/icl-code-review-research.md`](docs/research/icl-code-review-research.md) | Historical research hypothesis |
| [`review-tool/`](review-tool/README.md) | Deprecated Docker harness retained for reproduction |

## Skill Index

Each linked skill README is the canonical description of that skill. The root
README intentionally does not repeat its detailed guidelines or examples.

### Python

| Skill | Focus |
| --- | --- |
| [Python refactoring](python-refactoring-reviewer/README.md) | Code smells, SOLID, and maintainability |
| [Python functional](python-functional-reviewer/README.md) | Pure functions, composition, and side effects |
| [Python Zen](python-zen-reviewer/README.md) | PEP 20 and Pythonic design |
| [Python format refactoring](python-format-refactoring-reviewer/README.md) | Structural fixes for style problems |
| [Python testing](python-test-reviewer/README.md) | Test design, confidence, and strategies |
| [Python security and privacy](python-security-privacy-reviewer/README.md) | OWASP, privacy, and secure coding |
| [Python performance](python-performance-reviewer/README.md) | Profiling, algorithms, I/O, and memory |
| [Rhodes Python](python-rhodes-reviewer/README.md) | Brandon Rhodes-inspired architecture guidance |

### JavaScript and TypeScript

| Skill | Focus |
| --- | --- |
| [JavaScript testing](javascript-test-reviewer/README.md) | Jest, Vitest, Testing Library, and Cypress |
| [JavaScript refactoring](javascript-refactoring-reviewer/README.md) | Code smells, SOLID, and modern patterns |
| [JavaScript format refactoring](javascript-format-refactoring-reviewer/README.md) | Structural ESLint and Prettier fixes |
| [JavaScript functional](javascript-functional-reviewer/README.md) | Immutability, composition, and effects |
| [JavaScript security and privacy](javascript-security-privacy-reviewer/README.md) | Web and Node.js security |
| [JavaScript performance](javascript-performance-reviewer/README.md) | Browser, Node.js, and React performance |
| [React](react-reviewer/README.md) | Components, hooks, state, accessibility, and testing |
| [React Native and Expo](javascript-react-native-expo-reviewer/README.md) | Mobile architecture and platform behavior |

### Framework, testing, and cross-language

| Skill | Focus |
| --- | --- |
| [Agile requirements](agile-requirements-reviewer/README.md) | Stories, use cases, and acceptance criteria |
| [Django](django-reviewer/README.md) | Production readiness, security, and performance |
| [OpenAPI](openapi-reviewer/README.md) | API contract quality |
| [Database schema](database-schema-reviewer/README.md) | Normalization, indexing, and migrations |
| [Code authenticity](code-authenticity-reviewer/README.md) | Fabricated APIs, dependencies, and citations |
| [Playwright testing](playwright-test-reviewer/README.md) | Stable end-to-end browser testing |
| [Appium testing](appium-test-reviewer/README.md) | Reliable mobile automation |

## Installation and Use

Clone over SSH and install all skills:

```bash
git clone git@github.com:kvsankar/claude-skills.git
cd claude-skills
python install_skills.py
```

For a manual Linux or macOS installation:

```bash
cp -r *-reviewer ~/.claude/skills/
```

To install one skill, copy only its directory. Invoke a skill by name, for
example:

```text
Use the python-security-privacy-reviewer on this API.
```

## Evaluation

Effectiveness tests use immutable revisions of real upstream code. The two
subject modes are direct, non-agentic Ollama review and agentic repository review
through Pi; Codex provides the hosted agentic comparison. Claude matches reviews
against a frozen reference without tools, followed by a separate source-aware
pass for novel findings.

- Design and commands: [Evaluation Harness](docs/evaluation-harness.md)
- Final A/B evidence:
  [Codex regular versus lean skill](experiments/results/codex-lean-ab-20260808/doit/final/summary.md)
- Frozen reference:
  [Real review pool](experiments/results/real-pool-20260808/doit/reference-v1/summary.md)
- Withdrawn synthetic pilot:
  [Local-Model Evaluation Pilot](docs/evaluation-pilot-2026-08-08.md)

The Docker-based [review tool](review-tool/README.md) is deprecated and must not
be extended for new evaluations.

## Repository Status

This is a completed experiment. Corrections to documentation, attribution, or
reproducibility are appropriate; new reviewer skills are outside its scope.

Raw conversations, machine-specific repository links, and large regenerable
agent event streams are intentionally excluded from the public tree. Historical
synthetic results remain clearly marked as withdrawn and are not effectiveness
evidence.

## License

No repository-wide open-source license is currently granted. The repository is
published as source-available experimental history. Individual skills provide
source attribution in their `SOURCES.md` files; reuse or redistribution requires
permission until an explicit license is added.

## Brandon Rhodes Permission

> Hey, folks, this is Brandon Rhodes, making a personal comment on this project,
> since Sankar was kind enough to ask my permission before making it public!
> While I myself am dismayed at the broad impact of AI on society so far, and
> have always been skeptical about automated code review (I've always used
> 'pyflakes' instead of 'flake8' because flake8's clumsy attempts to apply PEP-8
> produce so much noise), I see no reason to stand in the way of this experiment.
> It tries to distill some of the guidelines that I've offered in my talks into
> a set of rules that can be applied by machine. I can't guess whether Claude
> Code will really understand when my ideas are useful and when they're not, but
> it's interesting to see how many pieces of advice worked their way into my
> talks over so many years.
>
> — Brandon Rhodes (December 2025)

The Rhodes skill was released with Brandon Rhodes' permission. Its detailed
attribution is in
[`python-rhodes-reviewer/SOURCES.md`](python-rhodes-reviewer/SOURCES.md).
