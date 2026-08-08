# Zen of Python Code Reviewer Skill

A Claude Code skill that reviews Python code against the 19 principles of the Zen of Python (PEP 20) to ensure Pythonic, readable, and maintainable code.

## What This Skill Does

This skill transforms Claude into a Zen of Python expert who:
- Reviews code against all 19 Zen of Python principles
- Identifies violations of Pythonic style and philosophy
- Suggests improvements aligned with Python's design philosophy
- Provides concrete before/after examples following PEP 20
- Promotes beautiful, explicit, simple, and readable code
- References Tim Peters' original Zen of Python aphorisms

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r zen-of-python-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "zen-of-python-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r zen-of-python-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/zen-of-python-reviewer
git commit -m "Add Zen of Python Reviewer skill"
```

**✅ Self-Contained:** All 40+ guidelines are embedded directly in SKILL.md - no external file references needed!

## How to Use

Simply ask Claude to review your Python code for Pythonic style:

```
"Review this code against the Zen of Python"
"Is this code Pythonic?"
"Check this against PEP 20"
"Make this code more Pythonic"
"Review for Python philosophy violations"
"Apply Zen of Python principles"
```

The skill will automatically activate based on keywords like:
- Zen of Python, Pythonic, PEP 20
- Python philosophy, Python style
- idiomatic Python, beautiful code
- explicit, simple, readable

## What You'll Get

A structured Zen of Python review with:
- ✅ **Pythonic Strengths** - What follows Zen principles (with mnemonic IDs)
- 🐍 **Zen of Python Recommendations** - Violations with principle + mnemonic ID (e.g., **EXPLICIT: ZEN-TYPE-HINTS**)
- **Before/After Code** - Concrete Pythonic refactoring examples
- **Zen Principle Quoted** - The relevant PEP 20 aphorism
- **Why This Matters** - How it aligns with Python philosophy

### Example Review

````markdown
## Zen of Python Review: user_manager.py

### ✅ Pythonic Strengths
- **ZEN-CONTEXT**: Properly uses context manager for file operations (lines 45-47)
- **ZEN-ENUMERATE**: Uses enumerate() for indexed iteration (line 62)

### 🐍 Zen of Python Recommendations

#### EXPLICIT: ZEN-TYPE-HINTS - Add Type Hints for Clarity

**Current code:**
```python
def process_users(users, filter_active):
    return [u for u in users if u.active == filter_active]
```

**Pythonic code:**
```python
def process_users(users: list[User], filter_active: bool) -> list[User]:
    """Filter users by active status."""
    return [user for user in users if user.active == filter_active]
```

**Why this matters:**
Type hints make function contracts explicit, improve IDE support, and enable static type checking with mypy. They serve as inline documentation for other developers.

**Zen principle:**
> "Explicit is better than implicit."

---

#### SIMPLE: ZEN-BUILTIN - Use Built-in Functions

**Current code:**
```python
def calculate_total(prices):
    total = 0
    for price in prices:
        total += price
    return total
```

**Pythonic code:**
```python
def calculate_total(prices: list[float]) -> float:
    """Calculate sum of all prices."""
    return sum(prices)
```

**Why this matters:**
Python's built-in sum() is optimized, well-tested, and immediately recognizable to Python developers. Simple solutions using built-ins are preferred over manual implementations.

**Zen principle:**
> "Simple is better than complex."

### 🎓 Zen Wisdom
> "Beautiful is better than ugly. Explicit is better than implicit."
````

## The 40+ Guidelines

### Code Aesthetics & Readability (8 guidelines)
- **ZEN-BEAUTIFUL** - Beautiful is better than ugly
- **ZEN-FORMAT** - Consistent PEP 8 formatting
- **ZEN-SPACING** - Proper use of whitespace
- **ZEN-NAMING** - Descriptive and consistent naming
- **ZEN-SPARSE** - Sparse is better than dense
- **ZEN-DENSE** - Avoid packing too much logic
- **ZEN-READABLE** - Readability counts
- **ZEN-COMPREHENSION** - Use comprehensions wisely

### Explicitness & Clarity (7 guidelines)
- **ZEN-EXPLICIT** - Explicit is better than implicit
- **ZEN-IMPLICIT** - Avoid hidden behavior
- **ZEN-TYPE-HINTS** - Use type hints for clarity
- **ZEN-MAGIC-IMPORT** - Avoid star imports
- **ZEN-ARGS** - Explicit function arguments
- **ZEN-RETURN** - Explicit return types
- **ZEN-MUTATE** - Make mutation explicit

### Simplicity (6 guidelines)
- **ZEN-SIMPLE** - Simple is better than complex
- **ZEN-COMPLEX** - Complex is better than complicated
- **ZEN-COMPLICATED** - Avoid over-engineering
- **ZEN-OVERDESIGN** - Avoid premature abstraction
- **ZEN-BUILTIN** - Use built-in functions
- **ZEN-STDLIB** - Leverage standard library

### Structure (5 guidelines)
- **ZEN-FLAT** - Flat is better than nested
- **ZEN-NESTED** - Avoid deep nesting
- **ZEN-EARLY-RETURN** - Use early returns
- **ZEN-INDENTATION** - Limit indentation depth
- **ZEN-CHAIN** - Avoid long method chains

### Error Handling (5 guidelines)
- **ZEN-ERRORS** - Errors should never pass silently
- **ZEN-BARE-EXCEPT** - Never use bare except
- **ZEN-SILENT** - Handle errors explicitly
- **ZEN-EXPLICIT-SILENCE** - Unless explicitly silenced
- **ZEN-SPECIFIC** - Catch specific exceptions

### Ambiguity & Assumptions (4 guidelines)
- **ZEN-AMBIGUITY** - Refuse the temptation to guess
- **ZEN-GUESS** - Don't make assumptions
- **ZEN-VALIDATE** - Validate input rather than assume
- **ZEN-DEFAULTS** - Make defaults explicit

### Pythonic Idioms (6 guidelines)
- **ZEN-ONE-WAY** - There should be one obvious way
- **ZEN-IDIOMS** - Use Pythonic idioms
- **ZEN-ENUMERATE** - Use enumerate() for indexed iteration
- **ZEN-CONTEXT** - Use context managers
- **ZEN-UNPACKING** - Use tuple unpacking
- **ZEN-COMPREHENSION-IDIOM** - Prefer comprehensions over map/filter

### Implementation Quality (4 guidelines)
- **ZEN-HARD-EXPLAIN** - If implementation is hard to explain, it's a bad idea
- **ZEN-EASY-EXPLAIN** - If implementation is easy to explain, it may be a good idea
- **ZEN-CLEVER** - Avoid clever code
- **ZEN-OBVIOUS** - Make code self-documenting

### Pragmatism (3 guidelines)
- **ZEN-PRACTICAL** - Practicality beats purity
- **ZEN-SPECIAL-CASE** - Special cases aren't special enough to break the rules
- **ZEN-NOW-NEVER** - Now is better than never (although never is often better than right now)

### Namespaces (3 guidelines)
- **ZEN-NAMESPACE** - Namespaces are one honking great idea
- **ZEN-GLOBAL** - Avoid global variables
- **ZEN-MODULE** - Organize code into modules

## The 19 Zen of Python Principles

```python
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

## Example Use Cases

### Code Quality Reviews
- "Review this module for Zen of Python violations"
- "Is this function Pythonic?"
- "Check this class against Python philosophy"

### Learning Python Style
- "How can I make this code more Pythonic?"
- "What Zen principles does this violate?"
- "Teach me Pythonic patterns for this code"

### Team Standards
- "Review PR #123 for Pythonic style"
- "Ensure this follows PEP 20 principles"
- "Check codebase alignment with Zen of Python"

### Refactoring Guidance
- "Apply Zen of Python to this legacy code"
- "Make this more explicit and simple"
- "Refactor following Python philosophy"

## Benefits

- ✓ **Learn Python Philosophy** - Understand the 19 core principles deeply
- ✓ **Write Pythonic Code** - Follow established Python conventions
- ✓ **Improve Readability** - Beautiful, explicit, simple code
- ✓ **Better Maintainability** - Code that aligns with Python's design
- ✓ **Team Consistency** - Shared understanding of Pythonic style
- ✓ **Catch Anti-Patterns** - Identify un-Pythonic code early
- ✓ **Educational** - Learn with concrete examples and explanations
- ✓ **Standards-Based** - Grounded in PEP 20 and Python best practices

## What Gets Checked

### Code Aesthetics
- Beautiful formatting (PEP 8 alignment)
- Proper whitespace and spacing
- Descriptive, consistent naming
- Sparse vs dense code balance

### Clarity & Explicitness
- Type hints and explicit contracts
- No hidden behavior or side effects
- Clear imports (no star imports)
- Explicit arguments and returns

### Simplicity
- Simple solutions over complex ones
- Organized complexity when needed
- Avoiding over-engineering
- Using built-ins and standard library

### Structure
- Flat over nested structures
- Limited indentation depth
- Early returns and guard clauses
- Readable control flow

### Error Handling
- No silent errors
- Specific exception handling
- Explicit error silencing when needed
- Proper exception types

### Pythonic Patterns
- The "one obvious way" idioms
- Context managers for resources
- enumerate(), unpacking, comprehensions
- List comprehensions over map/filter

### Code Quality
- Easy to explain implementations
- Self-documenting code
- Avoiding clever/obscure code
- Clear and obvious solutions

### Organization
- Proper use of namespaces
- Avoiding global state
- Module organization
- Clean separation of concerns

## Sources and Attribution

All guidelines are based on:
- **PEP 20** - The Zen of Python by Tim Peters
- **PEP 8** - Style Guide for Python Code
- **PEP 484** - Type Hints
- Established Python best practices and community standards

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## License

This skill is licensed under MIT. The Zen of Python (PEP 20) is in the public domain. Code examples and guidelines are based on established Python best practices.

---

**Make your Python code beautiful, explicit, and simple - the Pythonic way.**
