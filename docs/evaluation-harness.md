# Evaluation Harness

> [!NOTE]
> This is the reproducibility guide for a concluded experiment. The final result
> is summarized in
> [Experiment Conclusion](experiment-conclusion-2026-08-08.md).

This repository evaluates whether reviewer skills help models find real problems,
especially smaller models hosted locally. It deliberately separates model review
ability from coding-agent behavior.

## Real-Code-Only Policy

All effectiveness benchmarks use code from immutable revisions of real,
independently maintained production repositories. Synthetic code, planted
defects, and benchmark-authored fixtures are excluded.

Intentionally vulnerable teaching applications such as DVNA and PyGoat are real
upstream projects, but their defect distribution is deliberately contrived. They
may be used to test harness plumbing, never as primary evidence that a skill
helps on ordinary software.

Every scored target must record its upstream URL and commit SHA. Ground truth
must come from one or more of:

- a real bug-fix commit evaluated at its parent revision
- a regression test that fails before the fix and passes after it
- a published security advisory or accepted upstream issue
- documented adjudication by reviewers who inspected the actual source

Model-generated findings cannot become ground truth merely because another model
agrees with them.

## Experimental Design

The harness has two subject tracks, a hosted baseline, and two judging stages:

| Track | Subject | Repository tools | What it measures |
| --- | --- | --- | --- |
| Non-agentic | Ollama model | None | Prompt and skill effectiveness on supplied code |
| Agentic local | Pi plus Ollama model | Read, Bash, Grep, Find, Ls | Repository exploration and tool use |
| Agentic baseline | Codex exec | Codex tools | Hosted-agent reference performance |
| Reference matcher | Claude Code | None | Semantic matching against a frozen reference |
| Novel adjudicator | Claude Code | Read-only source exploration | Validation of findings outside that reference |

Pi is the local-model agent harness. Codex is a separate hosted agent baseline,
not the judge. The frozen-reference matcher does not inspect the repository. A
different source-aware Claude pass explores the repository only for anonymous
novel candidates, whose verdicts are then folded into the revised overall
finding set.

The deprecated Docker harness in `review-tool/` remains available only for
reproducing old results. Do not extend it for new evaluations.

## Discovery and Reference Construction

The first discovery pass is one source-aware Claude seed review:

```bash
python3 experiments/run_claude_baseline.py \
  --repo experiments/repos/doit-repo \
  --output experiments/results/real-pool/doit \
  --model sonnet
```

Its findings are candidates, not ground truth. Later model reviews are generated
independently without seeing this seed. The seed and model findings are then
normalized, deduplicated, and adjudicated against the source. Only validated
issues enter a versioned reference inventory, after which every contributing
review—including Claude's seed—is scored again.

After all independent agentic reviews finish:

```bash
python3 experiments/build_review_pool.py \
  --repo experiments/repos/doit-repo \
  --pool-dir experiments/results/real-pool/doit \
  --model sonnet
```

The pipeline first atomizes review prose without repository tools, strips origin
labels, clusters anonymous duplicates, and then gives the anonymous groups to a
source-aware Claude adjudicator. The private origin map is reintroduced only
after verdicts to calculate precision, pooled coverage, and unique validated
discoveries for every review, including B1.

## Prerequisites

- Ollama running on `tsmac`, reachable through the local SSH configuration
- The selected Ollama models already pulled on `tsmac`
- Pi installed locally as the `pi` command
- Codex CLI authenticated for the hosted baseline
- Claude Code authenticated for judging
- Python with PyYAML installed

The runners use the existing SSH host alias and do not expose Ollama publicly.
The direct runner sends requests through SSH. The Pi runner opens a temporary
local SSH tunnel to Ollama's OpenAI-compatible endpoint.

## Prompt Conditions

The earlier Rhodes experiments used these conditions:

- `zero-shot`: generic review instructions
- `ids-only`: the skill's mnemonic checklist without detailed guidelines
- `hybrid`: the checklist plus selected detailed guidelines
- `full-skill`: the complete skill, useful when context capacity permits

The decisive Codex A/B used only:

- `regular`: ordinary repository review with no skill guidance
- `lean-skill`: the same task plus a compact mnemonic-and-one-line checklist

Compare conditions within the same subject, model, fixture, and run count. Do
not compare raw finding counts as a quality metric: formatting varies by model,
and a longer review can contain more unsupported advice.

## Non-Agentic Local Runs

```bash
python3 experiments/run_ollama.py \
  --models devstral-small-2:latest qwen3-coder:30b \
  --conditions zero-shot ids-only hybrid \
  --runs 1 \
  --host tsmac \
  --code experiments/repos/doit-repo/doit/action.py \
  --output experiments/results/direct-real/doit
```

Defaults use temperature `0`, seed `42`, a 32K context window, and a 4K output
budget. The runner saves the prompt, response, Ollama timing and token metrics,
and any separate thinking text returned by the model.

## Agentic Local Runs with Pi

```bash
python3 experiments/run_pi_agentic.py \
  --models devstral-small-2:latest qwen3-coder:30b \
  --conditions zero-shot ids-only hybrid \
  --runs 1 \
  --host tsmac \
  --repo experiments/repos/doit-repo \
  --output experiments/results/agentic-real/doit
```

Every run receives a fresh copy of the target repository and an ephemeral Pi
configuration. Project context files, extensions, skills, prompt templates, and
session persistence are disabled. Pi can use read-oriented discovery tools and
Bash, but edit and write tools are not enabled. Its JSONL transcript records
tool calls, errors, the final review, elapsed time, and any workspace changes.

Pi does not present permission dialogs; this is its non-interactive, unrestricted
execution model. The disposable copy protects the benchmark source from model
edits but is not full operating-system isolation.

## Codex Agentic Baseline

```bash
python3 experiments/run_codex_agentic.py \
  --conditions zero-shot ids-only hybrid \
  --runs 1 \
  --repo experiments/repos/doit-repo \
  --output experiments/results/agentic-real/doit
```

The runner uses ephemeral `codex exec` JSONL sessions and the configured default
model unless `--model` is supplied. It invokes Codex with
`--dangerously-bypass-approvals-and-sandbox`, the explicit non-interactive yolo
mode intended for externally controlled automation.

The repository copy is disposable, but the yolo flag removes Codex's own sandbox.
Run only trusted fixtures and prompts. Add an external sandbox before evaluating
untrusted repositories or adversarial instructions.

## Claude Code Judge

```bash
python3 experiments/evaluate_judge.py \
  --gt experiments/results/real-pool/doit/reference-v1/reference.json \
  --results-dir experiments/results/agentic-real/doit \
  --model sonnet
```

The matcher discovers both legacy `condition/run-N-review.md` outputs and nested
`subject/model/condition/run-N-review.md` outputs. One Claude invocation matches
all frozen reference issues in one review. Claude runs with:

- print mode for non-interactive operation
- permission checks bypassed as requested for automation
- an empty tool allowlist
- no session persistence
- a strict JSON output schema

The output reports semantic recall, unsupported findings, usefulness,
specificity, per-issue evidence, and judge validity. Findings not matched to the
frozen reference are separately grouped without origin labels and adjudicated by
a source-aware Claude run. Both stages remain model judgments and can be wrong;
the retained source citations and verdict rationales make them auditable.

## Output Layout

```text
results/<experiment>/<fixture>/
├── pi-ollama/<model>/<condition>/
│   ├── prompt.md
│   ├── run-1-review.md
│   ├── run-1-events.jsonl
│   └── run-1.json
├── codex/<model>/<condition>/
│   └── ...
├── *-manifest.json
└── judge-evaluation.json
```

Direct Ollama results omit the subject level and begin with the model directory.

## Sequence Used for the Final Experiment

1. Pin a real upstream repository revision.
2. Generate one source-aware seed review, then independent subject reviews.
3. Blind, group, and source-adjudicate their union into reference v1.
4. Freeze reference v1 before the decisive comparison.
5. Run regular and lean-skill Codex reviews three times each.
6. Match each review against reference v1 without repository tools.
7. Blind and source-adjudicate every novel candidate from all six reviews.
8. Recompute final coverage and diversity from the revised union of findings.

Regression tests:

```bash
PYTHONPATH=experiments python3 -m unittest discover \
  -s experiments -p 'test_*.py' -v
```
