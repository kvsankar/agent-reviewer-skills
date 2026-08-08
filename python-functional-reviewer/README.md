# Functional Python Reviewer Skill

A Claude Code skill that reviews Python code using functional programming principles extracted from Python official documentation and educational resources.

## What This Skill Does

This skill transforms Claude into a code reviewer who:
- Applies functional programming principles to Python code
- Provides structured feedback with specific guideline references (mnemonic IDs)
- Explains the "why" behind each suggestion
- Balances functional purity with Pythonic pragmatism

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r functional-python-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "functional-python-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r functional-python-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/functional-python-reviewer
git commit -m "Add Functional Python Reviewer skill"
```

**✅ Self-Contained:** This skill includes everything needed - all 40+ guidelines are embedded in SKILL.md!

## How to Use

Simply ask Claude to review your Python code:

```
"Review this code for functional programming patterns"
"Check this function for side effects and purity"
"Suggest functional improvements for this code"
"Can this use generators instead of lists?"
```

The skill will automatically activate based on keywords like:
- functional, FP, pure function, immutability
- generator, map, filter, reduce
- comprehension, functools, itertools

## What You'll Get

A structured review with:
- ✅ **Strengths** - What follows FP principles (with mnemonic IDs)
- ⚠️ **Suggestions** - Issues with guideline IDs (e.g., **PURE-FUNC**, **GEN-LAZY**)
- 💡 **FP Wisdom** - Relevant quotes from sources

### Example Review

````markdown
## Review: data_processor.py

### ✅ Strengths
- **GEN-EXPR**: Excellent use of generator expression (line 15) for memory efficiency
- **USE-ENUMERATE**: Proper use of enumerate() for indexed iteration

### ⚠️ Suggestions

#### PURE-FUNC: Function relies on external state

**Current code:**
```python
total = 0
def add_to_total(value):
    global total
    total += value
    return total
```

**Suggested refactoring:**
```python
def add_to_total(current_total, value):
    return current_total + value

# Caller maintains state
total = 0
total = add_to_total(total, 5)
```

**Why this matters:**
Pure functions are easier to test, debug, and reason about. They always return the same output for the same input, eliminating unpredictability.

**FP principle:**
"The same input will always return the same output" - pure functions eliminate side effects and global state dependencies.

### 💡 Functional Programming Wisdom
> "Python is a multi-paradigm language. Combine functional with imperative approaches as needed—don't force pure functional style."
> — Python Functional Programming HOWTO
````

## The 40+ Guidelines

### Categories

1. **Pure Functions and Side Effects** (2)
   - PURE-FUNC, NO-MODIFY-INPUT

2. **Immutability and State** (3)
   - USE-IMMUTABLE, AVOID-MUTABLE-REF, TUPLE-SAFETY

3. **Higher-Order Functions** (3)
   - HOF-PATTERN, LAMBDA-SIMPLE, AVOID-LAMBDA-COMPLEX

4. **Lazy Evaluation** (3)
   - GEN-LAZY, YIELD-GENERATOR, GEN-SEND

5. **Built-in Functional Tools** (7)
   - USE-MAP, USE-FILTER, COMBINE-MAP-FILTER, USE-ENUMERATE, USE-ZIP, USE-ANY-ALL, USE-SORTED

6. **functools Module** (3)
   - USE-PARTIAL, USE-REDUCE, USE-LRU-CACHE

7. **itertools Module** (8)
   - ITER-COUNT, ITER-CYCLE, ITER-CHAIN, ITER-ISLICE, ITER-COMBINATIONS, ITER-PERMUTATIONS, ITER-GROUPBY, ITER-ACCUMULATE

8. **Comprehensions and Pythonic Style** (2)
   - PREFER-COMPREHENSION, GEN-EXPR

9. **Monads and Advanced Patterns** (3)
   - FUNCTOR-PATTERN, MAYBE-MONAD, RESULT-MONAD

10. **Best Practices** (6)
    - RECURSION-SIMPLE, USE-NAMEDTUPLE, FUNC-COMPOSE, MULTI-PARADIGM, ITERATOR-PROTOCOL

All guidelines with complete examples are embedded in SKILL.md.

## Skill Files

```
functional-python-reviewer/
├── SKILL.md       - Self-contained skill (instructions + 40+ embedded guidelines)
└── README.md      - This file (human documentation)
```

**Total:** 2 files, ~52 KB, fully self-contained

## When to Use This Skill

✅ **Good use cases:**
- Reviewing code for functional patterns
- Refactoring to reduce side effects
- Improving immutability and purity
- Learning functional programming concepts
- Optimizing with generators and itertools
- Team code review standards for FP

❌ **Not ideal for:**
- Non-Python code
- Pure OOP design patterns
- Performance profiling (use specialized tools)
- Security audits (use security-focused tools)

## Core FP Philosophy

The skill emphasizes these recurring themes:

1. **Pure Functions** - Same input → same output, no side effects
2. **Immutability** - Data doesn't change once created
3. **Higher-Order Functions** - Functions as first-class objects
4. **Lazy Evaluation** - Generators for memory efficiency
5. **Composition** - Building complex operations from simple functions
6. **Pythonic Balance** - Functional when beneficial, not dogmatic
7. **Built-in Tools** - Leverage map, filter, itertools, functools
8. **Comprehensions** - Prefer list comprehensions over map/filter

## Sources

The guidelines are compiled from:

**Official Documentation:**
- Python Functional Programming HOWTO (docs.python.org)
- functools module documentation
- itertools module documentation

**Educational Resources:**
- ArjanCodes - Functional Programming Principles & Monads
- Stack Abuse - Functional Programming in Python
- Stack Builders - Functional Programming Principles & Tools

All guidelines include authentic code examples quoted directly from these sources.

## Attribution

This skill compiles functional programming principles from publicly available educational materials. All code examples are quoted directly from these sources with proper attribution.

**Primary Sources:**

**Python Software Foundation**
- Python Functional Programming HOWTO
- functools and itertools module documentation
- License: Python Software Foundation License
- [docs.python.org](https://docs.python.org/)

**Arjan Egges (ArjanCodes)**
- "Core Functional Programming Principles for Python"
- "Python Functors and Monads: A Practical Guide"
- Educational blog content
- [arjancodes.com](https://arjancodes.com/)

**Stack Abuse**
- "Functional Programming in Python"
- Technical educational articles
- [stackabuse.com](https://stackabuse.com/)

**Stack Builders**
- "Functional Programming in Python: Principles & Tools"
- Educational insights and examples
- [stackbuilders.com](https://www.stackbuilders.com/)

**Copyright Notice:**
- Python documentation: © Python Software Foundation (PSF License - open and permissive)
- Educational blog content: Used with attribution for educational purposes
- Code examples: Many represent common functional programming patterns and idioms
- This skill: Created for educational purposes to help developers learn FP principles

All contributors retain their original copyrights. This skill is licensed under MIT.

## Customization

To modify this skill:
1. Edit `SKILL.md` to change Claude's review behavior or update guidelines
2. The skill will automatically reload on next use
3. For reference, see `../docs/functional-python/guidelines.md` for the source guidelines

## Troubleshooting

### Skill Not Activating

If Claude doesn't use the skill, try:
- Use explicit keywords: "review using functional programming principles"
- Mention specific concepts: "check for pure functions and immutability"
- Check that SKILL.md exists in the correct directory
- Verify YAML frontmatter is valid (no tabs)

### Want More Detail

Ask for deeper analysis:
```
"Review this thoroughly for all functional programming patterns"
"What functional improvements can be made to this code?"
"Check this against all FP guidelines"
```

---

**Version:** 1.0
**Last Updated:** October 30, 2025
**Guideline Count:** 40+ principles from official docs and educational resources
**Files:** 2 (SKILL.md with embedded guidelines, README.md)
