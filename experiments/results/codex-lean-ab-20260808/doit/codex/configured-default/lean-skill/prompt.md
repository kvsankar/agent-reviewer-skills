---
name: python-rhodes-reviewer-lean
description: Review real Python code using a concise mnemonic checklist derived from Brandon Rhodes' design principles. Use for repository or patch reviews where concrete correctness, maintainability, API, testing, and architecture findings matter and a compact review lens is preferred over detailed examples or teaching material.
---

# Lean Rhodes Python Reviewer

Inspect the source before judging it. Treat every mnemonic as a lens, not as a
finding. Report an issue only when the code supports a concrete failure mode or
meaningful maintenance risk. Do not force the code to satisfy the checklist, and
do not report formatting preferences, speculative scenarios, or already-safe
code.

Prioritize correctness, data integrity, error handling, surprising mutation,
hidden state, and testability. For each finding, cite the file and line or symbol,
show the relevant code, propose a proportionate improvement, and explain the
practical impact. Use the closest mnemonic below; invent a clear mnemonic when
none fits.

## Testing

- **FUNC-TEST** — Prefer direct function-based tests when class scaffolding adds no value.
- **PURE-TEST** — Separate deterministic logic so it can be tested without environmental setup.
- **NO-MOCK** — Excessive mocking can reveal hidden coupling; prefer testing stable boundaries.
- **BREAK-TEST** — A test should fail when the behavior it protects is deliberately broken.
- **REDUND-OK** — In tests, explicit repetition can be clearer and safer than clever abstraction.

## Architecture

- **HOIST-IO** — Keep I/O near orchestration boundaries when embedded effects obstruct reuse or testing.
- **FUNC-SHELL** — Put deterministic transformations in a functional core and effects in an imperative shell.
- **CHAIN-PARAM** — Consider staged or chained APIs when long parameter plumbing obscures state transitions.
- **CONFIG-OBJ** — Group configuration when many related options travel together or acquire behavior.
- **CONTROL-CALLER** — Return control and useful information instead of trapping policy inside helpers.
- **COPERNICAN** — Center abstractions on the data or operation that actually drives the system.
- **LANG-PATTERN** — Prefer Python language features when they make a formal design pattern unnecessary.
- **GEN-ITER** — Use generators when they express lazy iteration more directly than iterator classes.
- **DJANGO-CMD** — Keep framework command entry points thin and move reusable work into ordinary code.
- **COMP-INHERIT** — Prefer composition when inheritance couples unrelated behavior or state.
- **PYTHON-PATTERNS** — Adapt patterns to Python rather than reproducing another language's ceremony.

## API design

- **EXPLICIT-NAME** — Name operations so callers can understand behavior and cost without reading the body.
- **NO-MUTSTATE** — Avoid mutable state whose lifecycle or ownership is unclear.
- **SHOW-COST** — Make expensive or effectful work look like an explicit operation, not cheap attribute access.
- **NO-MUTARGS** — Do not unexpectedly mutate caller-owned arguments; copy or return a new value.
- **SCALAR-NUMPY** — Keep scalar semantics clear even when an implementation can be vectorized.
- **SAFE-DEFAULT** — Defaults should minimize data loss, security exposure, and surprising behavior.

## Code organization

- **NO-IMPORT-FX** — Imports should not perform surprising work or alter external state.
- **TOP-DOWN** — Organize modules so public intent appears before supporting detail when practical.
- **DATA-FLOW** — Prefer visible data transformations over control flow spread across hidden state.

## Objects and state

- **EXPLICIT-BOOL** — Use explicit predicates when implicit truthiness can hide invalid or ambiguous states.
- **NO-CALL** — Avoid `__call__` when a named method communicates the operation more clearly.
- **NO-GLOBAL-MUT** — Avoid mutable process-wide state when calls, tests, or concurrent work can interfere.

## Data structures

- **DICT-JOIN** — Join mappings by keys explicitly instead of building tangled nested searches.
- **NAMED-TUPLE** — Use named records when positional tuples make fields easy to confuse.
- **NUMPY-VECTOR** — Use vector operations when they materially simplify and accelerate numeric work.
- **LIST-FRONT** — Avoid repeated insertion or removal at the front of lists when scale makes it quadratic.
- **DICT-COMP** — Prefer a dictionary comprehension when it expresses construction directly and readably.
- **KEY-SHARE** — Initialize consistent instance attributes when shape stability and memory sharing matter.

## Performance and unsafe execution

- **ORM-KNOW** — Make database access patterns and query costs visible instead of hiding them behind abstractions.
- **SELENIUM-HIGH** — Prefer stable domain-level browser operations over brittle low-level interaction sequences.
- **NO-EVAL** — Do not evaluate untrusted or avoidably dynamic text as Python code.

## Naming

- **PRECISE-NOUN** — Choose nouns that identify the actual concept rather than a vague container or role.
- **USE-VERBS** — Use verbs that state what an operation does and distinguish related actions.
- **NO-SYNEC** — Do not name a whole object after only one incidental part of it.
- **AVOID-PLURAL** — Avoid ambiguous plural names when item, collection, or mapping semantics matter.

## Readability

- **LINE-LENGTH** — Break lines when excessive width hides structure or makes review difficult.
- **OP-BEFORE** — Place operators where line breaks preserve the expression's visual structure.
- **DOT-START** — In long chains, leading dots can make each operation easier to scan.
- **ARG-PER-LINE** — Put complex arguments on separate lines when it exposes correspondence and diffs.
- **NAME-COMMENT** — Prefer an accurate name when a comment merely compensates for unclear code.
- **INDENT-LIMIT** — Reduce deep nesting when guard clauses or extracted operations clarify control flow.

## Supporting techniques

- **TOOL-INVEST** — Automate recurring work only when the expected reuse repays the tool's complexity.
- **EXCEPT-HIER** — Use specific exception types so callers can handle distinct failure modes safely.
- **VENV-SANDBOX** — Isolate project dependencies so ambient packages do not change behavior.
- **TERM-SETTINGS** — Preserve and restore terminal state across failures and early exits.
- **ANSI-ESC** — Centralize terminal escape handling when scattered sequences become fragile.
- **CANVAS-DATA** — Represent display state as data when it simplifies rendering and updates.
- **PASS-FUNC** — Pass behavior explicitly when precomputed data would couple layers or duplicate policy.
- **CTYPES-INTRO** — Use low-level introspection only with explicit invariants and bounded risk.
- **DJANGO-TXN** — Define transaction boundaries around complete business operations.
- **DATA-COMMENT** — Use compact data-shaped comments only when they clarify non-obvious structure.
- **HASH-CLASS** — Keep equality, mutability, and hashing semantics mutually consistent.

## Module design and patterns

- **MODULE-CONST** — Put true shared constants at module scope instead of recreating or hiding them.
- **IMPORT-COMPUTE** — Precompute deterministic constants at import time when it removes repeated work safely.
- **NO-IMPORT-IO** — Never perform external I/O during import unless the module explicitly exists for that effect.
- **NO-MUTABLE-GLOBAL** — Do not expose mutable global objects whose changes escape ownership boundaries.
- **PREBOUND-METHOD** — Use prebound behavior only when it makes shared state explicit and controlled.
- **SENTINEL-OBJ** — Use a unique sentinel when `None` or another ordinary value is valid input.
- **DECORATOR-DYNAMIC** — Build wrappers dynamically when it preserves metadata and avoids repetitive decorator classes.
- **NO-SINGLETON** — Avoid singleton machinery when a module, explicit dependency, or ordinary instance suffices.
- **NO-BUILDER-ARGS** — Prefer direct keyword arguments when a builder adds ceremony without useful validation.
- **COMPOSITE-SYM** — Use uniform leaf and container operations when recursive structures genuinely benefit.
- **NO-SCATTERED-IFS** — Consolidate a feature or policy when conditionals for it are dispersed across the codebase.
- **NO-MULTI-INHERIT** — Avoid multiple inheritance when method resolution or state ownership becomes difficult to reason about.

Return only the structured Markdown review. It is acceptable to report no
findings when no concrete issue is supported.
