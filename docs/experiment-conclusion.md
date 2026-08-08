# Experiment Conclusion: Reviewer Skills

## Decision

This experiment is complete. The evidence collected here does not justify
continued investment in a large collection of specialized code-review skills.
The repository is retained as a public experimental archive, including the
negative result and enough artifacts to audit how it was reached.

This is not a claim that prompts never help or that no model can benefit from a
specialized checklist. It is the narrower conclusion that, under the tested
conditions, these skills did not materially improve a capable agent's review and
did not rescue the tested smaller local models.

## Question

Does adding a compact, Rhodes-inspired review skill help a coding agent find more
real defects than asking the same agent to perform a regular code review?

The final comparison deliberately used a lean skill: mnemonic IDs plus one- or
two-line reminders. This removed the obvious objection that the original
60-kilobyte skill was simply too large and distracting.

## Method

- Target: the real `pydoit/doit` repository pinned at commit
  `1f9cbbce`.
- Subjects: six independent agentic Codex reviews—three regular and three using
  the lean skill.
- Initial reference: findings pooled from independent reviews, anonymized,
  deduplicated, inspected against source, and frozen before the A/B runs were
  scored.
- Revised findings: candidates outside the frozen reference were pooled across
  both conditions, anonymized, source-adjudicated, and added to the final union
  when valid.
- Judge: Claude Code, tool-free for semantic reference matching and source-aware
  only for blind novel-finding adjudication.
- Fixtures: real code only. Synthetic results were withdrawn as effectiveness
  evidence.

## Result

| Condition | Runs | Frozen-reference recall | Validated per run | Total valid hits | Distinct validated defects |
| --- | ---: | ---: | ---: | ---: | ---: |
| Regular review | 3 | 28.5% | 8.67 | 26 | 18 |
| Lean skill | 3 | 30.2% | 8.33 | 25 | 13 |

The skill produced a 1.7 percentage-point increase in recall against the frozen
reference, but one fewer total validated hit and five fewer distinct validated
defects. Runtime was essentially unchanged: 106.5 seconds per regular run versus
104.7 seconds with the lean skill. The guided reviews repeated known categories
slightly more often while exploring less broadly.

Seven previously unreferenced defect groups were validated by the final
source-aware pass. Regular reviews discovered all seven across their runs; lean
reviews discovered four. This is why the revised overall finding set matters:
scoring only against the initial baseline would have hidden some of the regular
condition's useful discoveries.

## Local Models

The real-repository Pi/Ollama pilot used Qwen3 Coder 30B and Devstral Small 2.
Neither produced validated evidence that skill guidance improved review quality.
Some guided Devstral runs also failed to produce a usable terminal review. An
earlier synthetic pilot showed apparent gains on planted issues, but that result
was withdrawn because synthetic checklist-shaped defects favor checklist-shaped
prompts and do not answer the real question.

The local-model evidence is small, so it cannot establish a universal result
about all local models. It does show that the tested skills were not an obvious
way to make these tested local models competitive on this task.

## Interpretation

The mnemonic checklist appears to steer attention, but steering has an
opportunity cost. It can improve repetition of anticipated issue categories
while narrowing open-ended repository exploration. A capable coding agent
already carries substantial code-review knowledge and can inspect source, run
searches, and form hypotheses dynamically; a static checklist did not add enough
new information to offset that narrowing.

For smaller models, the bottleneck appeared broader than missing review advice:
repository navigation, tool use, evidence synthesis, and producing a coherent
terminal answer all mattered. More prompt content did not solve those problems.

## Limitations

- The decisive comparison covers one repository, one lean skill, one configured
  Codex model, and three runs per condition.
- The reference and novel-finding verdicts depend partly on Claude judgments,
  although prompts were blinded and source rationales are retained.
- The experiment measures issue discovery, not whether the skills are useful as
  teaching material or personal reminders.
- Model and agent implementations will change; these results are a dated
  observation, not a permanent law.

## Retained Evidence

- Final A/B summary:
  [`experiments/results/codex-lean-ab-20260808/doit/final/summary.md`](../experiments/results/codex-lean-ab-20260808/doit/final/summary.md)
- Final scores and source adjudication: adjacent JSON files in that directory
- Frozen reference and source adjudication:
  [`experiments/results/real-pool-20260808/doit/reference-v1/summary.md`](../experiments/results/real-pool-20260808/doit/reference-v1/summary.md)
- Evaluation design and commands: [Evaluation Harness](evaluation-harness.md)
- Historical synthetic pilot, explicitly withdrawn:
  [Local-Model Evaluation Pilot](evaluation-pilot.md)

Raw agent event streams, scratch runs, local repository symlinks, and raw Claude
conversation exports are intentionally excluded. They are large, regenerable,
machine-specific, or private; they are not necessary to verify the conclusion.
