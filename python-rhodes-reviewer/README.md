# Rhodes Python Code Reviewer Skill

A Claude Code skill that reviews Python code using Brandon Rhodes' 70 coding principles extracted from 15+ years of conference presentations (2010-2024) and his Python Patterns Guide.

## A Note from Brandon Rhodes

> Hey, folks, this is Brandon Rhodes, making a personal comment on this project, since Sankar was kind enough to ask my permission before making it public! While I myself am dismayed at the broad impact of AI on society so far, and have always been skeptical about automated code review (I've always used 'pyflakes' instead of 'flake8' because flake8's clumsy attempts to apply PEP-8 produce so much noise), I see no reason to stand in the way of this experiment. It tries to distill some of the guidelines that I've offered in my talks into a set of rules that can be applied by machine. I can't guess whether Claude Code will really understand when my ideas are useful and when they're not, but it's interesting to see how many pieces of advice worked their way into my talks over so many years.
>
> — Brandon Rhodes (December 2025)

## What This Skill Does

This skill transforms Claude into a code reviewer who:
- Applies Brandon Rhodes' Python coding guidelines
- Provides structured feedback with specific guideline references (mnemonic IDs)
- Explains the "why" behind each suggestion
- Channels Rhodes' thoughtful, pedagogical teaching style

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r python-rhodes-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "python-rhodes-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r python-rhodes-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/python-rhodes-reviewer
git commit -m "Add Rhodes Reviewer skill"
```

**✅ Self-Contained:** All 70 guidelines are embedded directly in SKILL.md - no external file references needed!

## How to Use

Simply ask Claude to review your Python code:

```
"Review this Python function using Rhodes guidelines"
"Can you check this code against Rhodes principles?"
"What would Brandon Rhodes say about this architecture?"
```

The skill will automatically activate based on keywords like:
- review, code review, Python review
- Rhodes, guidelines, best practices
- feedback, critique

## What You'll Get

A structured review with:
- ✅ **Strengths** - What follows Rhodes' principles (with mnemonic IDs)
- ⚠️ **Suggestions** - Issues with guideline IDs (e.g., **HOIST-IO**, **NO-MOCK**)
- 💡 **Rhodes Wisdom** - Relevant quotes from his talks

### Example Review

`````markdown
## Review: data_processor.py

### ✅ Strengths
- **DICT-COMP**: Excellent use of dictionary comprehension (line 15)
- **PRECISE-NOUN**: Variable names clearly indicate their purpose

### ⚠️ Suggestions

#### HOIST-IO: I/O operations mixed with business logic

**Current code:**
```python
def process_users():
    with open('users.csv') as f:
        data = parse_csv(f)
        return transform_data(data)
```

**Suggested refactoring:**
```python
def process_users(file_content):
    """Process user data from file content."""
    data = parse_csv(file_content)
    return transform_data(data)

# Caller handles I/O at top level
with open('users.csv') as f:
    result = process_users(f.read())
```

**Why this matters:**
Separating I/O from business logic makes `process_users()` testable without
file mocking. You can now test with simple string data in memory.

**Rhodes' principle:**
"Move all I/O operations to the program's top level, allowing core logic
to remain pure and testable."

### 💡 Rhodes Wisdom
> "Using mock.patch() indicates code has coupled I/O that should be separated."
> — Hoisting Your I/O (2015)
`````

## The 70 Guidelines

### Categories

1. **Testing and Test Design** (5)
   - FUNC-TEST, PURE-TEST, NO-MOCK, BREAK-TEST, REDUND-OK

2. **Architecture and Design Patterns** (11)
   - HOIST-IO, FUNC-SHELL, COPERNICAN, CHAIN-PARAM, CONFIG-OBJ, CONTROL-CALLER, LANG-PATTERN, GEN-ITER, DJANGO-CMD, COMP-INHERIT, PYTHON-PATTERNS

3. **API Design** (6)
   - EXPLICIT-NAME, NO-MUTSTATE, SHOW-COST, NO-MUTARGS, SCALAR-NUMPY, SAFE-DEFAULT

4. **Code Organization** (3)
   - NO-IMPORT-FX, TOP-DOWN, DATA-FLOW

5. **Object-Oriented Programming** (3)
   - EXPLICIT-BOOL, NO-CALL, NO-GLOBAL-MUT

6. **Data Structures** (6)
   - DICT-JOIN, NAMED-TUPLE, NUMPY-VECTOR, LIST-FRONT, DICT-COMP, KEY-SHARE

7. **Performance** (3)
   - ORM-KNOW, SELENIUM-HIGH, NO-EVAL

8. **Naming** (4)
   - PRECISE-NOUN, USE-VERBS, NO-SYNEC, AVOID-PLURAL

9. **Style** (6)
   - LINE-LENGTH, OP-BEFORE, DOT-START, ARG-PER-LINE, NAME-COMMENT, INDENT-LIMIT

10. **Productivity** (1)
    - TOOL-INVEST

11. **Advanced Topics** (10)
    - EXCEPT-HIER, VENV-SANDBOX, CTYPES-INTRO, TERM-SETTINGS, ANSI-ESC, CANVAS-DATA, PASS-FUNC, DJANGO-TXN, DATA-COMMENT, HASH-CLASS

12. **Module Design and Patterns** (12) - from python-patterns.guide
    - MODULE-CONST, IMPORT-COMPUTE, NO-IMPORT-IO, NO-MUTABLE-GLOBAL, PREBOUND-METHOD, SENTINEL-OBJ, DECORATOR-DYNAMIC, NO-SINGLETON, NO-BUILDER-ARGS, COMPOSITE-SYM, NO-SCATTERED-IFS, NO-MULTI-INHERIT

All 70 guidelines with complete code examples are embedded in SKILL.md.

## Skill Files

```
python-rhodes-reviewer/
├── SKILL.md       - Claude instructions + embedded 70 guidelines (self-contained)
├── README.md      - This file (human documentation)
└── SOURCES.md     - Attribution and Brandon Rhodes' statement
```

**Total:** ~65 KB, fully self-contained, no external dependencies

## When to Use This Skill

✅ **Good use cases:**
- Reviewing new Python functions or classes
- Architectural design feedback
- Refactoring guidance
- Learning Rhodes' principles through code review
- Team code review standards

❌ **Not ideal for:**
- Non-Python code
- Performance profiling (use specialized tools)
- Security audits (use security-focused tools)
- Auto-fixing code (provides guidance, not automatic fixes)

## Rhodes' Core Philosophy

The skill emphasizes Rhodes' recurring themes:

1. **Separation of Concerns** - Keep I/O separate from business logic
2. **Pure Functions** - Prefer pure functions that are easy to test
3. **Explicit Over Implicit** - Clear naming and explicit operations
4. **Data Over Control Flow** - Show data structures, not flowcharts
5. **Composition Over Inheritance** - Use functions and data structures
6. **Avoid Mocking** - Architecture problems, not testing solutions
7. **Language Features Over Patterns** - Use Python's built-in capabilities
8. **Readable Code** - Self-documenting through good naming and structure

## About Brandon Rhodes

Brandon Rhodes is a Python programmer and conference speaker known for:
- Open source astronomy libraries (PyEphem, Skyfield)
- Author of "Foundations of Python Network Programming"
- PyCon US Chair (2016-2017)
- Creator of python-patterns.guide
- 60+ conference talks on Python best practices (2008-2025)

**Sources:**
- Website: https://rhodesmill.org/brandon/
- Talks: https://rhodesmill.org/brandon/talks/
- Python Patterns: https://python-patterns.guide/
- GitHub: https://github.com/brandon-rhodes

## Attribution

The guidelines in this skill are summarized from Brandon Rhodes' public conference presentations and python-patterns.guide.

This skill was released with Brandon Rhodes' permission. See SOURCES.md for his full statement.

## Customization

To modify this skill:
1. Edit `SKILL.md` to change Claude's review behavior or update guidelines
2. The skill will automatically reload on next use
3. See `SOURCES.md` for detailed attribution of each guideline

## Troubleshooting

### Skill Not Activating

If Claude doesn't use the skill, try:
- Use explicit keywords: "review using Rhodes guidelines"
- Check that SKILL.md exists in the correct directory
- Verify YAML frontmatter is valid (no tabs)

### Want More Detail

Ask for deeper analysis:
```
"Review this thoroughly against all applicable Rhodes guidelines"
"What would Rhodes say about every aspect of this code?"
```

---

**Version:** 2.1
**Last Updated:** December 15, 2025
**Guideline Count:** 70 principles (58 from talks + 12 from python-patterns.guide)
**Files:** 3 (SKILL.md, README.md, SOURCES.md)
