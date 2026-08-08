# Exploration History

The repository followed several branches of exploration. Some were literature
or product research, some were prototypes, and some were measured experiments.
They are listed together because each tested a possible way to make in-context
review guidance more useful.

The sequence matters. The skills were built and used before formal measurement
began; early experiments then exposed weaknesses in both the skills and the
evaluation method; the final real-code comparison was designed in response to
those weaknesses.

## Exploration Branches

| Exploration | Objective | When | Result summary | Details |
| --- | --- | --- | --- | --- |
| Curated in-context review guidance | Test whether principles, mnemonic IDs, and before-and-after examples could help frontier coding agents perform focused reviews. | Oct 2025-Jan 2026 | Produced 23 AI-assisted reviewer skills, researched and drafted primarily with Claude, that were used as practical aids. Their usefulness was not measured during this phase. | [Disclosure](../README.md#ai-assistance-disclosure), [skill index](../README.md#skill-index) |
| Docker-based agentic review runner | Make Claude reviews repeatable and isolated across repositories and reviewer perspectives. | Nov-Dec 2025 | Worked as an execution harness, including through an Ubuntu VM when WSL Docker was troublesome, but was operationally heavy and was later deprecated. | [Deprecated review tool](../review-tool/README.md) |
| In-context-learning and industry research | Find evidence that examples improve code review and identify how comparable tools select and structure guidance. | Dec 2025; updated Mar 2026 | The literature suggested that example selection, compact context, decomposition, and hybrid static-analysis approaches mattered. It did not establish that this repository's large static skills improved agentic reviews. | [In-context-learning research](icl-code-review-research.md) |
| Embedding-based guideline retrieval | Select only the guidelines most relevant to the code under review. | Dec 2025-Mar 2026 | Embeddings matched surface-level code patterns but did not reliably select architectural guidance such as functional-core/imperative-shell. The prototype was abandoned. | [Retrieval assessment](icl-code-review-research.md#5-failed-experiment-embedding-based-guideline-retrieval-mar-2026) |
| Security baseline and prompt ablations | Compare zero-shot, generic, full-skill, principles-only, IDs-only, trimmed, and hybrid prompts. | 5-6 Mar 2026 | Some variants appeared to improve recall, but the runs had weak ground-truth matching, deliberately vulnerable targets, and substantial single-run variance. These results became exploratory evidence, not the project conclusion. | [Experiments 1-3](../experiments/results/experiment-report.md#1-experiment-design) |
| Rhodes skill evaluations | Test code-quality guidance on synthetic examples and real `doit` code, including multiple runs and a second model. | 6-8 Mar 2026 | Synthetic results were distorted by answer leakage and remained unstable after cleanup. Real-code reviews changed emphasis but did not show that the skill found more useful issues. | [Experiments 4-6](../experiments/results/experiment-report.md#experiments-4-6-rhodes-python-code-quality-skill) |
| Agentic and non-agentic local-model harness | Determine separately whether guidance helps a model review supplied code and whether it helps a coding agent explore a repository. | 8 Aug 2026 | Direct Ollama, Pi with Ollama, Codex, and two Claude judging stages replaced the Docker design. Synthetic runs were retained only as plumbing checks and a real-code-only policy was adopted. | [Evaluation harness](evaluation-harness.md), [withdrawn pilot](evaluation-pilot.md) |
| Real-code local-model pilot | Test whether Qwen3 Coder 30B or Devstral Small 2 benefited from guidance while reviewing a pinned real repository. | 8 Aug 2026 | Neither model produced validated evidence of improvement; some guided Devstral agentic runs did not produce usable final reviews. The sample was too small for a universal claim about local models. | [Local-model result](experiment-conclusion.md#local-models) |
| Pooled reference and revised finding union | Avoid treating a single baseline review as complete ground truth by validating the union of baseline and experimental findings. | 8 Aug 2026 | Anonymous, source-aware adjudication produced a frozen reference and then incorporated valid novel findings from both A/B conditions. This exposed useful discoveries that baseline-only scoring would have missed. | [Method](evaluation-harness.md#discovery-and-reference-construction), [reference](../experiments/results/real-pool-20260808/doit/reference-v1/summary.md) |
| Regular Codex versus lean skill | Test the strongest remaining hypothesis: a compact list of mnemonic IDs plus one or two sentences might help even if the full skill did not. | 8 Aug 2026 | Three runs per condition showed no material advantage. The lean skill had slightly higher frozen-reference recall, but one fewer validated hit and five fewer distinct validated defects. | [Final conclusion](experiment-conclusion.md), [A/B evidence](../experiments/results/codex-lean-ab-20260808/doit/final/summary.md) |

## Overall Progression

The project moved from authoring broad static guidance, to researching how
in-context examples might work, to trying relevance selection and prompt
compression, and finally to direct comparison on real code. Each later branch
addressed a weakness found in the earlier one: excessive prompt size, weak
selection, synthetic answer leakage, incomplete ground truth, or failure to
separate model ability from agent behavior.

No branch produced conclusive evidence that these reviewer skills improve
agentic code-review quality. The [final conclusion](experiment-conclusion.md)
records the decision and limitations; the [evaluation harness](evaluation-harness.md)
records the final reproducible method.
