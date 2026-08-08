# Reviewer Skills: In-Context Guidance for Code Review

## Introduction

This repository records an experiment in using specialized, in-context guidance
to improve agentic code reviews. The central question was simple: can a coding
agent produce a better review when its context includes curated principles,
mnemonic reminders, and concrete examples of good and bad code?

The repository grew into 23 reviewer skills covering Python, JavaScript,
frameworks, testing, security, performance, refactoring, and API and database
design. Each skill was intended to give a general-purpose coding agent a focused
review perspective without training or fine-tuning a separate model.

The skills began as practical tools for Claude Code and other frontier coding
agents available at the time. The project later became an evaluation of its own
premise: whether this extra context actually finds more real problems than a
capable agent asked to perform an ordinary code review.

## Brief History

### Building and practical use: October 2025-January 2026

The work began in late October 2025 with an effort to extract Python design
guidance from [Brandon Rhodes](https://rhodesmill.org/brandon/)' talks and
teaching material. Its principles were organized as mnemonic IDs, explanations,
and before-and-after examples, then packaged as a Claude Code reviewer skill.
The approach expanded across languages and review concerns, reaching 23 skills
by January 2026. They were used as practical review aids before the project had
a formal benchmark. A Docker runner supported early agentic use but proved
operationally heavy.

### Research and prototypes: December 2025-March 2026

The project then asked whether the skills actually improved review quality over
an ordinary agent review. Research into few-shot and in-context learning
suggested that example selection, compact context, and hybrid approaches might
matter more than loading every guideline. An embedding and structural-code
prototype tried to select relevant guidance, but it matched surface patterns
more reliably than architectural ideas and was abandoned.

### Automated evaluation: March 2026

The first automated evaluations compared ordinary prompts with full skills,
principles-only guidance, mnemonic IDs, trimmed lists, and hybrid prompts.
Security tests and Rhodes-inspired code-quality tests produced some apparently
positive results, especially for compact guidance, but also exposed substantial
run-to-run variance, weak reference construction, deliberately vulnerable
targets, and answer leakage in synthetic fixtures. Reviews of real `doit` code
changed emphasis without demonstrating that the skills found more useful
issues. These runs remained exploratory rather than supporting a conclusion.

### Real-code evaluation and closure: August 2026

The final evaluation adopted a real-code-only policy and separated direct model
review from agentic repository review. It tested local models through Ollama and
Pi, used Codex for the hosted comparison, and used separate Claude passes for
reference matching and source-aware adjudication. The final regular-versus-lean
comparison also evaluated valid new findings from both conditions instead of
treating one baseline as complete ground truth.

Across full skills, compact IDs, short guidance, retrieval, frontier agents, and
smaller local models, the retained evidence provides no conclusive indication
that these skills improve agentic code-review quality. The Docker harness was
deprecated and active expansion stopped. This is a dated experimental result,
not a claim that in-context guidance can never help.

The [exploration history](docs/exploration-history.md) presents the research,
prototypes, and experiments together in chronological order, with links to the
retained detail and evidence. The
[experiment conclusion](docs/experiment-conclusion.md) explains the final
decision, measurements, and limitations.

## Repository Map

| Path | Canonical purpose |
| --- | --- |
| `reviewers/` | Individual reviewer skill packages and their source attribution |
| `experiments/` | Current evaluation runners and retained evidence |
| [`docs/evaluation-harness.md`](docs/evaluation-harness.md) | Evaluation methodology and reproduction commands |
| [`docs/exploration-history.md`](docs/exploration-history.md) | Chronological index of research, prototypes, and experiments |
| [`docs/experiment-conclusion.md`](docs/experiment-conclusion.md) | Final decision and results |
| [`docs/icl-code-review-research.md`](docs/icl-code-review-research.md) | Detailed historical research hypothesis |
| [`review-tool/`](review-tool/README.md) | Deprecated Docker harness retained for reproduction |

## Skill Index

Each linked skill README is the canonical description of that skill. The root
README intentionally does not repeat its detailed guidelines or examples.

### Python

| Skill | Focus |
| --- | --- |
| [Python refactoring](reviewers/python-refactoring-reviewer/README.md) | Code smells, SOLID, and maintainability |
| [Python functional](reviewers/python-functional-reviewer/README.md) | Pure functions, composition, and side effects |
| [Python Zen](reviewers/python-zen-reviewer/README.md) | PEP 20 and Pythonic design |
| [Python format refactoring](reviewers/python-format-refactoring-reviewer/README.md) | Structural fixes for style problems |
| [Python testing](reviewers/python-test-reviewer/README.md) | Test design, confidence, and strategies |
| [Python security and privacy](reviewers/python-security-privacy-reviewer/README.md) | OWASP, privacy, and secure coding |
| [Python performance](reviewers/python-performance-reviewer/README.md) | Profiling, algorithms, I/O, and memory |
| [Rhodes Python](reviewers/python-rhodes-reviewer/README.md) | [Brandon Rhodes](https://rhodesmill.org/brandon/)-inspired architecture guidance |

### JavaScript and TypeScript

| Skill | Focus |
| --- | --- |
| [JavaScript testing](reviewers/javascript-test-reviewer/README.md) | Jest, Vitest, Testing Library, and Cypress |
| [JavaScript refactoring](reviewers/javascript-refactoring-reviewer/README.md) | Code smells, SOLID, and modern patterns |
| [JavaScript format refactoring](reviewers/javascript-format-refactoring-reviewer/README.md) | Structural ESLint and Prettier fixes |
| [JavaScript functional](reviewers/javascript-functional-reviewer/README.md) | Immutability, composition, and effects |
| [JavaScript security and privacy](reviewers/javascript-security-privacy-reviewer/README.md) | Web and Node.js security |
| [JavaScript performance](reviewers/javascript-performance-reviewer/README.md) | Browser, Node.js, and React performance |
| [React](reviewers/react-reviewer/README.md) | Components, hooks, state, accessibility, and testing |
| [React Native and Expo](reviewers/javascript-react-native-expo-reviewer/README.md) | Mobile architecture and platform behavior |

### Framework, testing, and cross-language

| Skill | Focus |
| --- | --- |
| [Agile requirements](reviewers/agile-requirements-reviewer/README.md) | Stories, use cases, and acceptance criteria |
| [Django](reviewers/django-reviewer/README.md) | Production readiness, security, and performance |
| [OpenAPI](reviewers/openapi-reviewer/README.md) | API contract quality |
| [Database schema](reviewers/database-schema-reviewer/README.md) | Normalization, indexing, and migrations |
| [Code authenticity](reviewers/code-authenticity-reviewer/README.md) | Fabricated APIs, dependencies, and citations |
| [Playwright testing](reviewers/playwright-test-reviewer/README.md) | Stable end-to-end browser testing |
| [Appium testing](reviewers/appium-test-reviewer/README.md) | Reliable mobile automation |

## Installation and Use

The installer supports Windows, WSL, macOS, and Linux and requires Python 3.10
or newer. Clone the repository over SSH:

```bash
git clone git@github.com:kvsankar/claude-skills.git
cd claude-skills
```

On macOS, Linux, or WSL, run:

```bash
python3 install_skills.py
```

On Windows PowerShell, run:

```powershell
py -3 install_skills.py
```

Windows and WSL have separate home directories and agent installations. If you
use agents in both environments, run the installer once from Windows and once
from WSL. The installer does not modify the other environment implicitly.

The installer writes personal skills to the locations documented by each agent:

| Agent | Destination |
| --- | --- |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/` |
| [Codex](https://developers.openai.com/codex/skills) | `~/.agents/skills/` |
| [Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md) | `~/.pi/agent/skills/` |
| [GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | `~/.copilot/skills/` |

The Copilot destination serves both VS Code agent mode and GitHub Copilot CLI.
Existing skill directories are left untouched unless `--force` is supplied.
Useful variants include:

```bash
# Preview the default all-agent installation.
python3 install_skills.py --dry-run

# Install one skill for Claude Code and Pi.
python3 install_skills.py --agent claude --agent pi \
  --skill python-rhodes-reviewer

# Replace existing copies when updating an installation.
python3 install_skills.py --force
```

Use `py -3` instead of `python3` in the examples when running from Windows.
Run `python3 install_skills.py --help` for all options. Invoke a skill by name,
for example:

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
- Research and experiment sequence:
  [Exploration History](docs/exploration-history.md)
- Final A/B evidence:
  [Codex regular versus lean skill](experiments/results/codex-lean-ab-20260808/doit/final/summary.md)
- Frozen reference:
  [Real review pool](experiments/results/real-pool-20260808/doit/reference-v1/summary.md)
- Withdrawn synthetic pilot:
  [Local-Model Evaluation Pilot](docs/evaluation-pilot.md)

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

This repository is licensed under the [MIT License](LICENSE). Linked source
materials remain under their respective licenses; attribution details are in
each skill's `SOURCES.md`.

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
> — [Brandon Rhodes](https://rhodesmill.org/brandon/) (December 2025)

The Rhodes skill was released with
[Brandon Rhodes](https://rhodesmill.org/brandon/)' permission. Its detailed
attribution is in
[`reviewers/python-rhodes-reviewer/SOURCES.md`](reviewers/python-rhodes-reviewer/SOURCES.md).
