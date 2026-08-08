# Research: In-Context Learning for Code Reviews

> [!IMPORTANT]
> **Historical pre-evaluation research.** This document records the hypotheses
> that motivated the experiment; it is not evidence that these particular
> skills improve reviews. The subsequent real-code experiment did not show a
> material advantage over regular Codex review. See the
> [experiment conclusion](../experiment-conclusion-2026-08-08.md).

**Original research:** December 2025
**Updated:** March 2026

## 1. Our Approach

The claude-skills project uses **structured before/after code examples** embedded directly in skill prompts. Each SKILL.md contains:

- 40-70+ guidelines with mnemonic IDs (e.g., SQL-INJECT, PII-LOG)
- Before/after code pairs showing the anti-pattern and the fix
- Compliance mapping (OWASP, CWE, GDPR)
- Self-contained — all knowledge embedded in the prompt, not relying on model training
- 23 skills, 1,064 total guidelines

## 2. What Others Are Doing

### Commercial Tools

| Tool | Guideline Format | Code Examples | Relevance Filtering | Auto-Discovery |
|------|-----------------|---------------|---------------------|----------------|
| **CodeRabbit** | Natural language + AST-grep YAML rules | Via AST-grep pattern/fix pairs | Path-based globs + code graph + 1:1 context ratio | Imports from Cursor/Copilot/Cline/Claude files |
| **Qodo** | AI-generated from code patterns and PR history | Derived from codebase, not manually authored | RAG with code-embedding models | Yes — core differentiator |
| **GitHub Copilot** | Markdown `.instructions.md` files | Yes — correct/incorrect snippets recommended | Path-scoped `applyTo` + precedence hierarchy | No |
| **Sourcery** | YAML `.sourcery.yaml` config | Rule enable/disable, not example-based | Rule type filtering | Learns from feedback |
| **Codacy** | 22K+ rules from 34 static analysis tools | Tool-specific rule formats | PR intent analysis + metadata | No |
| **ast-grep** (standalone) | YAML rules with pattern/fix/message | Before (pattern) / after (fix) is native | File path filtering | No |

**Key observations:**

- **CodeRabbit** now uses "context engineering" — assembling a **1:1 code-to-context ratio** from PR metadata, code graphs, linters, web queries, and verification scripts. They combine AST-grep (deterministic structural matching) with LLM reasoning. Their community rule repository: [coderabbitai/ast-grep-essentials](https://github.com/coderabbitai/ast-grep-essentials).
- **Qodo 2.1** (Feb 2026) introduced auto-discovered rules from codebase patterns and PR history. A "Rules Discovery Agent" generates standards; a "Rules Expert Agent" prunes conflicts and duplicates. Fundamentally different from manual rule authoring.
- **GitHub Copilot** deprecated its structured "Coding Guidelines" feature (Sep 2025), replacing it with markdown instruction files. They explicitly recommend including before/after code snippets. **4,000 character limit** per instruction file.
- **Amazon CodeGuru** was deprecated Nov 2025. Did not support custom rules.

### ast-grep Deep Dive

ast-grep is a Rust CLI tool using tree-sitter for structural code matching. Supports 26+ languages.

**How it relates to our skills:** Each of our "bad example" code blocks could theoretically be converted to an ast-grep pattern rule, and the "good example" to a `fix` template. This would enable deterministic structural matching of anti-patterns — no LLM needed for detection, only for explanation and context.

**Comparison with semgrep:**

| Aspect | ast-grep | Semgrep |
|--------|----------|---------|
| Focus | Development (refactoring, linting) | Security (SAST, vulnerability detection) |
| Performance | Very fast, multi-threaded Rust | Slower |
| Parser | tree-sitter (precise ASTs) | Custom parser with "generic" mode |
| Semantic analysis | None (syntactic only) | Yes — type info, data flow, taint analysis |
| Library use | Rust, Node.js, Python, WASM | CLI/service only |

**Limitation:** ast-grep is purely syntactic. It cannot detect architectural patterns like "functional core, imperative shell" or "single responsibility" — these require semantic reasoning that only an LLM can provide.

## 3. Academic Evidence

### 3.1 Few-Shot Examples Improve Code Review Quality

| Paper | Venue | Key Finding |
|-------|-------|-------------|
| Prompting and Fine-tuning LLMs for Code Review Comment Generation ([2411.10129](https://arxiv.org/abs/2411.10129)) | arXiv 2024 | Function call graph-augmented few-shot on GPT-3.5 surpassed baseline by ~90% BLEU-4. Few-shot + structured context = 25-83% improvement. |
| Code Refactoring with LLM: Few-Shot Evaluation ([2511.21788](https://arxiv.org/abs/2511.21788)) | arXiv 2025 | Java achieved 99.99% correctness in 10-shot. Performance varies by language and shot count. |
| Retrieval-Augmented Few-Shot Prompting vs Fine-Tuning for Vulnerability Detection ([2512.04106](https://arxiv.org/abs/2512.04106)) | arXiv 2025 | At 20 shots, retrieval-augmented prompting achieves F1=74.05% vs zero-shot F1=36.35% (2x improvement). |
| Prompting vs Fine-tuning for Code Review (Guo et al.) | IST 2024 | Few-shot without persona achieves best results. Few-shot boosted Exact Match by 46-659% over zero-shot. |
| LLMs for Code Quality: Systematic Literature Review | ScienceDirect 2025 | Across 49 studies, few-shot is the leading prompting method for code quality tasks. |

**Research hypothesis at the time:** several studies reported benefits from
few-shot prompting on their own tasks and metrics. Those results did not
establish that this repository's long, manually curated skills would improve an
agentic repository review.

### 3.2 Example Selection Is Critical

| Paper | Venue | Key Finding |
|-------|-------|-------------|
| CEDAR: Retrieval-Based Prompt Selection ([ICSE 2023](https://dl.acm.org/doi/10.1109/icse48619.2023.00205)) | ICSE 2023 | Retrieval-based example selection achieved 76% exact match on assertion generation — outperforming task-specific models by 333%. ~300 citations. |
| Selecting Few-Shot Examples for Vulnerability Detection ([2510.27675](https://arxiv.org/abs/2510.27675)) | NDSS LaSTX 2026 | Selection effectiveness is language-dependent. "Hard example" strategy (examples the model gets wrong) is novel. Python/JS benefit most. |
| Does Few-Shot Help in Code Synthesis? ([2412.02906](https://arxiv.org/abs/2412.02906)) | arXiv 2024 | Complex examples are more informative than simple edge cases. Selection strategy matters more than quantity. |

**Implication for our skills:** Our current approach loads all 40-70+ guidelines regardless of the code being reviewed. Research strongly suggests that selecting the most relevant examples per review target would significantly improve quality.

### 3.3 Many-Shot: More Examples Plateau or Degrade

| Paper | Venue | Key Finding |
|-------|-------|-------------|
| Many-Shot In-Context Learning ([2404.11018](https://arxiv.org/abs/2404.11018)) | NeurIPS 2024 Spotlight | Performance improves few-shot → many-shot, but **code-related tasks plateau or slightly degrade** beyond a threshold. Quality > quantity. |
| Many-Shot for Long-Context Evaluation | ACL 2025 | Next-token prediction loss continues decreasing even as task performance plateaus. Example order influences many-shot performance. |
| The Few-shot Dilemma: Over-prompting LLMs ([2509.13196](https://arxiv.org/pdf/2509.13196)) | arXiv 2025 | Increasing few-shot examples past an optimal point degrades performance. Optimal number varies per model and task. |

**Implication:** Loading all 1,064 guidelines simultaneously would almost certainly degrade quality. A selective approach is essential.

### 3.4 Hybrid Approaches (LLM + Static Analysis)

| Paper | Venue | Key Finding |
|-------|-------|-------------|
| Combining LLMs with Static Analyzers for Code Review ([2502.06633](https://arxiv.org/abs/2502.06633)) | MSR 2025 | Three strategies tested (data-augmented training, RAG, naive concatenation). Combining precision of static analysis with LLM comprehensiveness produces better reviews. |
| Automated Code Review with Symbolic Reasoning ([2507.18476](https://arxiv.org/abs/2507.18476)) | arXiv 2025 | Hybrid approach improves accuracy by 16% over LLM alone. Knowledge maps of best practices and defect patterns enhance detection. |
| IRIS: LLM-Assisted Static Analysis ([2405.17238](https://arxiv.org/abs/2405.17238)) | ICLR 2025 | Detects 55 vulnerabilities vs CodeQL's 27 (+104%). Found 4 previously unknown vulnerabilities. |
| Augmenting LLMs with Static Analysis ([2506.10330](https://arxiv.org/abs/2506.10330)) | FORGE 2025 | Static analysis feeds structured issue information to LLM with RAG for more precise revisions. |
| Ericsson Experience Report ([2507.19115](https://arxiv.org/abs/2507.19115)) | ICSME 2025 | Adding enclosing method context (via static analysis) to prompts produced better reviews. Iterative human expert validation loop for prompt calibration. |

**Implication:** Our before/after examples are a form of structured knowledge. The evidence says combining this with static analysis output (linter findings, AST patterns) would be more effective than either alone.

### 3.5 Prompt Optimization for Code Review

**Token efficiency:**
- Anthropic recommends "the smallest possible set of high-signal tokens" ([context engineering blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents))
- XML-tagged structure yields 15-20% better performance than plain text
- 200K-optimized systems: 83% accuracy on code tasks. Million-token windows: 67% ([Augment Code](https://www.augmentcode.com/tools/context-window-wars-200k-vs-1m-token-strategies))
- Data serialization overhead consumes 40-70% of tokens through unnecessary formatting

**Prompt ordering:**
- "Lost in the middle" effect ([Liu et al., TACL 2024](https://aclanthology.org/2024.tacl-1.9/)): LLMs perform best when relevant info is at the beginning or end. Information in the middle is degraded.
- Best structure: guidelines at start, code in middle, key priorities restated at end ("sandwich" pattern)

**Two-pass review:**
- Decomposed Prompting (DecomP, [ICLR 2023](https://openreview.net/forum?id=_nGgzQjzaRy)): breaking complex tasks into sub-tasks handled by specialized handlers
- MelcotCR ([2509.21170](https://arxiv.org/abs/2509.21170)): decomposes code review into sub-tasks (summarization, logic analysis, impact analysis, issue inspection). A 14B model matches 671B DeepSeek-R1 with this approach.
- LAURA ([ASE 2025](https://arxiv.org/abs/2512.01356)): three-component RAG — context augmentation, review exemplar retrieval, systematic guidance. State-of-the-art for automated code review.

**Chain-of-thought:**
- Generic "think step by step" provides marginal gains with 20-80% increased response time for reasoning models ([Wharton, 2506.07142](https://arxiv.org/abs/2506.07142))
- Structured decomposition into specific review dimensions (security, performance, etc.) is effective — which is essentially what our multi-reviewer approach already does

**Multiple passes:**
- Running multiple reviewers independently (our current approach) is a valid form of self-consistency
- Research shows 2-3 focused passes with different perspectives suffices ([CISC, ACL 2025](https://aclanthology.org/2025.findings-acl.1030/))

## 4. How Our Approach Compares (Updated Assessment)

### What we do well

1. **Structured before/after examples** — validated by research as superior to rules-only (2x+ improvement)
2. **Mnemonic IDs** — unique in the ecosystem; no other tool does this
3. **Self-contained skills** — portable, no infrastructure dependency
4. **Multiple independent reviewers** — effectively a multi-pass approach, validated by self-consistency research
5. **Compliance mapping** — OWASP, CWE, GDPR references are uncommon in competing tools

### What we could improve

1. **No relevance filtering** — we load all 40-70+ guidelines regardless of code. Research says selection matters enormously (CEDAR: 333% improvement with retrieval-based selection).
2. **No static analysis integration** — hybrid approaches improve accuracy by 16%+. We could feed linter/AST-grep findings into the review prompt.
3. **No measurement** — we have zero data on whether our skills improve review quality vs bare Claude. Every competing tool and paper measures outcomes.
4. **Prompt structure** — we don't optimize for the "lost in the middle" effect or use XML-tagged structure (15-20% improvement).
5. **No example curation** — research shows complex, representative examples outperform simple ones. We haven't analyzed which of our 1,064 guidelines actually get used.

## 5. Failed Experiment: Embedding-Based Guideline Retrieval (Mar 2026)

We attempted to pre-filter guidelines using embeddings:
- Parsed SKILL.md files into individual guidelines
- Embedded principle + bad example using OpenAI text-embedding-3-small
- Extracted code units (functions, classes) via tree-sitter
- Queried ChromaDB for semantically similar guidelines

**Why abandoned:** Embedding similarity works for surface-level patterns (~60% of guidelines) but cannot handle architectural guidelines ("functional core, imperative shell", "single responsibility"). These require reasoning, not lexical matching.

**What research suggests instead:**
- **Two-pass with LLM** (MelcotCR approach): Claude selects relevant guidelines in pass 1, reviews with them in pass 2
- **AST-grep for structural matching**: convert before/after examples to ast-grep rules for deterministic detection of syntactic anti-patterns
- **GraphRAG**: encode relationships via graphs to capture architectural patterns (emerging research, not yet practical)
- **LLM-based design pattern detection** ([Schindler & Rausch, 2502.18458](https://arxiv.org/abs/2502.18458)): LLMs can identify roles classes play within patterns — semantically aware matching that embeddings can't do

## 6. Publishability Assessment

### The proposed claim before measurement

"Structured before/after code examples in LLM prompts improve code review
quality compared to rules-only or zero-shot approaches."

The repository's later real-code experiment did not support this claim. It
should not be presented as an outcome of this project.

### What's needed to publish

1. **Baseline measurements** — run reviews with and without skills on codebases with known issues
2. **Ablation study** — full skill vs principles-only vs mnemonic-IDs-only
3. **Guideline utilization analysis** — which of the 1,064 guidelines actually get referenced in reviews?
4. **Comparison with competing approaches** — CodeRabbit's AST-grep + LLM vs our pure in-context approach
5. **Optimal skill size** — test 20 vs 40 vs 70 guidelines per skill

### Optimization opportunities

1. **Two-pass review** — LLM selects relevant guidelines first, then reviews with only those (supported by MelcotCR and DecomP research)
2. **AST-grep pre-screening** — convert syntactic anti-patterns to ast-grep rules for fast deterministic detection, use LLM only for architectural/semantic issues
3. **Prompt structure optimization** — XML tags, sandwich ordering, trimming low-value guidelines
4. **Static analysis integration** — feed linter findings into the review prompt alongside guidelines

## 7. Key Papers to Read

1. **CEDAR** — [ICSE 2023](https://dl.acm.org/doi/10.1109/icse48619.2023.00205) — Retrieval-based few-shot selection for code tasks (~300 citations)
2. **LAURA** — [ASE 2025](https://arxiv.org/abs/2512.01356) — RAG for code review (state-of-the-art)
3. **MelcotCR** — [2509.21170](https://arxiv.org/abs/2509.21170) — Structured decomposition for code review
4. **Many-Shot ICL** — [NeurIPS 2024](https://arxiv.org/abs/2404.11018) — Scaling behavior of examples
5. **Few-shot Dilemma** — [2509.13196](https://arxiv.org/pdf/2509.13196) — Over-prompting degradation
6. **Lost in the Middle** — [TACL 2024](https://aclanthology.org/2024.tacl-1.9/) — Positional bias in long contexts
7. **Ericsson Experience Report** — [ICSME 2025](https://arxiv.org/abs/2507.19115) — Industry deployment
8. **IRIS** — [ICLR 2025](https://arxiv.org/abs/2405.17238) — LLM + static analysis for security
9. **Combining LLMs with Static Analyzers** — [MSR 2025](https://arxiv.org/abs/2502.06633) — Hybrid code review
10. **Anthropic Context Engineering** — [Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Practical guidance
