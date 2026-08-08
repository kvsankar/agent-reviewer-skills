# Local-Model Evaluation Pilot

**Run date:** 8 August 2026

> [!CAUTION]
> **Withdrawn as effectiveness evidence.** This run used benchmark-authored
> synthetic code. It validates harness execution only and must not be used to
> claim that a skill helps a model. All future benchmarks use immutable real
> production code and externally grounded defects.

This pilot validated early harness plumbing on the 15-issue Rhodes synthetic
fixture. It is not evidence that the skills or a finishing sprint were
worthwhile, and it is not a statistically reliable model or prompt ranking.

## Setup

- Fixture: `experiments/repos/rhodes-synthetic/order_processor.py`
- Ground truth: 15 planted Rhodes issues
- Local inference: Ollama on `tsmac`
- Local models: `devstral-small-2:latest`, `qwen3-coder:30b`
- Agent harness: Pi in non-interactive mode with read-oriented tools and Bash
- Hosted baseline: Codex exec in non-interactive yolo mode
- Judge: Claude Code Sonnet, non-interactive, no tools, strict JSON schema
- Tool versions: Pi 0.79.10, Codex CLI 0.147.0, Claude Code 2.1.177,
  Ollama 0.31.2
- Runs: one per subject, model, and condition

## Results

Recall is the number of planted issues semantically detected out of 15. “Unsup.”
is the judge's count of concrete findings unsupported by the review's own quoted
evidence. Usefulness is scored from 1 to 5.

### Non-Agentic Direct Ollama

| Model | Condition | Recall | Unsup. | Usefulness | Duration |
| --- | --- | ---: | ---: | ---: | ---: |
| Devstral Small 2 | Zero-shot | 5/15 (33.3%) | 2 | 2 | 195 s |
| Devstral Small 2 | IDs-only | 8/15 (53.3%) | 1 | 3 | 215 s |
| Devstral Small 2 | Hybrid | 7/15 (46.7%) | 2 | 3 | 219 s |
| Qwen3 Coder 30B | Zero-shot | 4/15 (26.7%) | 2 | 2 | 44 s |
| Qwen3 Coder 30B | IDs-only | 5/15 (33.3%) | 5 | 2 | 30 s |
| Qwen3 Coder 30B | Hybrid | 4/15 (26.7%) | 4 | 2 | 42 s |

### Agentic Pi and Codex

| Subject | Condition | Recall | Unsup. | Usefulness | Duration | Tools |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pi / Devstral Small 2 | Zero-shot | 3/15 (20.0%) | 2 | 2 | 182 s | 2 |
| Pi / Devstral Small 2 | IDs-only | 7/15 (46.7%) | 4 | 3 | 256 s | 12 |
| Pi / Devstral Small 2 | Hybrid | 9/15 (60.0%) | 4 | 3 | 252 s | 9 |
| Pi / Qwen3 Coder 30B | Zero-shot | 4/15 (26.7%) | 2 | 2 | 30 s | 2 |
| Pi / Qwen3 Coder 30B | IDs-only | 6/15 (40.0%) | 4 | 2 | 55 s | 2 |
| Pi / Qwen3 Coder 30B | Hybrid | 6/15 (40.0%) | 4 | 2 | 71 s | 2 |
| Codex / configured default | Zero-shot | 4/15 (26.7%) | 0 | 3 | 96 s | 2 |
| Codex / configured default | IDs-only | 10/15 (66.7%) | 2 | 4 | 93 s | 2 |
| Codex / configured default | Hybrid | 5/15 (33.3%) | 3 | 3 | 95 s | 3 |

No agentic run created, removed, or changed a file in its disposable workspace.
Tool errors occurred in Devstral IDs-only and all three Codex runs, but each run
recovered and produced a terminal review.

## Historical Observations (Not Effectiveness Findings)

1. Guided conditions sometimes scored higher on planted issues, with the largest
   synthetic-fixture difference appearing in the Devstral agentic hybrid run.
   This did not survive as evidence on real code.
2. Prompt compression matters. IDs-only was best for direct Devstral and for the
   Codex baseline. More detailed guidance was not consistently better.
3. Agentic and non-agentic tests answer different questions. Devstral preferred
   IDs-only directly but hybrid through Pi. A separate Pi/Qwen smoke also showed
   a model drafting a detailed review during tool use and then replacing it with
   a weak terminal summary.
4. Recall gains currently come with noise. Guided Pi outputs doubled unsupported
   findings for both local models. The next skill revision should emphasize
   evidence thresholds and omission over speculative checklist completion.
5. Qwen was faster on this hardware, but this run cannot support a comparative
   claim about which local model benefits from Rhodes guidance.

## Limitations

- Each matrix cell has only one run; agent behavior and judge output can vary.
- The Codex run used the CLI's configured default model rather than recording an
  explicit model ID. Future benchmark commands must pass `--model`.
- Pi's agentic sampling parameters were not explicitly fixed by the CLI.
- The Claude judge is a semantic measurement instrument, not ground truth.
- One synthetic Python file cannot establish general usefulness across skills,
  languages, repository sizes, or real-world issue distributions.
- Unsupported-finding counts assess whether the review substantiated its claims,
  not whether every extra non-planted finding was objectively wrong.

## Follow-up

The follow-up moved to immutable real repository code, a pooled and source-aware
reference, and a three-run regular-versus-lean comparison. It did not show a
material skill benefit. See the
[experiment conclusion](experiment-conclusion.md).
