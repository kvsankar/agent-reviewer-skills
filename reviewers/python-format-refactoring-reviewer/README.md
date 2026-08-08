# Format/Style Refactoring Reviewer Skill

A Claude Code skill that solves Python formatting and style issues through refactoring rather than just wrapping lines or suppressing warnings.

## What This Skill Does

This skill transforms Claude into a format/style refactoring expert who:
- **Solves style issues through refactoring** - not just formatting
- **Goes beyond pylint/ruff** - suggests structural improvements
- **Eliminates root causes** - not just symptoms
- **Applies [Brandon Rhodes](https://rhodesmill.org/brandon/)' principles** - format follows structure
- **Provides refactoring patterns** - for each style issue
- **Shows before/after examples** - with proper refactoring

## Philosophy

> **"Don't fight the linter—refactor so it has nothing to complain about."** - [Brandon Rhodes](https://rhodesmill.org/brandon/)

When pylint says "line too long", don't just wrap it. Extract a variable or method so the line naturally fits.

When ruff says "too complex", don't suppress it. Simplify the logic with guard clauses or extract methods.

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## How to Use

Simply ask Claude to review your Python code for format/style refactoring:

```
"This line is too long - how should I refactor it?"
"Pylint says this is too complex - help me refactor it"
"How can I fix this formatting issue structurally?"
"Refactor this to solve the style warnings"
"This has too many parameters - what refactoring should I use?"
```

The skill will automatically activate based on keywords like:
- format refactoring, style refactoring
- line too long refactoring
- too complex refactoring
- extract variable, extract method
- parameter object, guard clause

## What You'll Get

A structured refactoring review with:
- ✅ **Well-Structured Code** - What's already good structurally
- 🔧 **Refactoring Opportunities** - Style issues with root causes
- **Linter Warnings** - What pylint/ruff would say
- **Root Cause Analysis** - Why the style issue exists
- **Refactored Code** - Proper structural fix (not just formatting)
- **Why Better** - Benefits beyond just passing linters

### Example Review

````markdown
## Format/Style Refactoring Review: order_processor.py

### ✅ Well-Structured Code
- **FMT-EARLY-RETURN**: Good use of guard clauses in validate_order() (lines 15-20)

### 🔧 Refactoring Opportunities

#### LINE TOO LONG: FMT-EXTRACT-VAR - Extract Variable for Clarity

**Linter would say:**
> "Line too long (95/79)" [E501]

**Root cause:**
Expression packs too much information on one line, making it hard to read and extending past the line limit.

**Current code:**
```python
canvas.drawString(x * em, y * lineheight, 'Please press {}'.format(key))
```

**Refactored code:**
```python
message = 'Please press {}'.format(key)
canvas.drawString(x * em, y * lineheight, message)
```

**Why this is better:**
- Line naturally fits within 79 characters
- Variable name `message` documents intent
- Easier to debug and modify the message
- No awkward line wrapping needed
- Can reuse message variable if needed

**Refactoring applied:** Extract Variable

---

#### TOO COMPLEX: FMT-GUARD-CLAUSE - Use Guard Clauses

**Linter would say:**
> "Function is too complex (15/10)" [C901]

**Root cause:**
Nested conditions increase cyclomatic complexity unnecessarily. Happy path logic is buried deep in nesting.

**Current code:**
```python
def process_order(order):
    if order is not None:
        if order.is_valid():
            if order.items:
                # Process order logic here
                return True
    return False
```

**Refactored code:**
```python
def process_order(order):
    if order is None:
        return False
    if not order.is_valid():
        return False
    if not order.items:
        return False

    # Process order logic here
    return True
```

**Why this is better:**
- Complexity score reduced (flatter structure)
- Each guard clause is a clear precondition
- Happy path logic is unindented and obvious
- Easier to add new validation rules
- More readable and maintainable

**Refactoring applied:** Replace Nested Conditional with Guard Clauses

### 💡 Refactoring Wisdom
> "Good structure leads to good style automatically. Refactor for clarity, and formatting takes care of itself."
````

## The 40+ Guidelines

### Line Length Issues (8 guidelines)
- **FMT-EXTRACT-VAR** - Extract meaningful variable instead of wrapping
- **FMT-EXTRACT-METHOD** - Extract method for long expressions
- **FMT-PARAM-OBJECT** - Parameter object for long signatures
- **FMT-ARG-PER-LINE** - Format multi-arg calls properly
- **FMT-BREAK-EXPR** - Break complex expressions
- **FMT-INTERMEDIATE** - Use intermediate variables
- **FMT-BUILDER** - Builder pattern for many optional params
- **FMT-SIMPLIFY-CALL** - Simplify nested function calls

### Complexity Issues (7 guidelines)
- **FMT-GUARD-CLAUSE** - Guard clauses for complexity
- **FMT-DECOMPOSE-COND** - Decompose complex conditionals
- **FMT-EXTRACT-BOOL** - Extract boolean variables
- **FMT-SIMPLIFY-LOGIC** - Simplify boolean logic
- **FMT-REDUCE-BRANCHES** - Replace if-elif with lookup
- **FMT-PATTERN-MATCH** - Use pattern matching (3.10+)
- **FMT-LOOKUP-TABLE** - Replace logic with data

### Nesting Issues (6 guidelines)
- **FMT-EARLY-RETURN** - Early returns to reduce nesting
- **FMT-CONTINUE** - Use continue in loops
- **FMT-EXTRACT-NESTED** - Extract nested logic to method
- **FMT-EXTRACT-ITER** - Extract iterator/generator
- **FMT-FLATTEN-LOOP** - Flatten nested loops
- **FMT-INVERT-COND** - Invert conditions to reduce nesting

### Parameter Issues (5 guidelines)
- **FMT-PARAM-DATACLASS** - Dataclass for related parameters
- **FMT-WHOLE-OBJECT** - Pass whole object vs fields
- **FMT-CONFIG-OBJECT** - Configuration object pattern
- **FMT-KWARGS** - Keyword arguments with validation
- **FMT-BUILDER-PATTERN** - Builder for complex construction

### Expression Clarity (5 guidelines)
- **FMT-NAME-BOOL** - Name complex boolean expressions
- **FMT-NAME-CALC** - Name intermediate calculations
- **FMT-COMMENT-TO-NAME** - Replace comments with names
- **FMT-CHAIN-STEPS** - Break method chains into steps
- **FMT-TEMP-EXPLAIN** - Temporary variables for explanation

### Method Organization (5 guidelines)
- **FMT-LONG-METHOD** - Extract method to reduce length
- **FMT-EXTRACT-CLASS** - Extract class for related methods
- **FMT-SINGLE-RESP** - One responsibility per method
- **FMT-COMPOSE-METHOD** - Compose method pattern
- **FMT-REPLACE-LOOP** - Replace loop with comprehension

### Operators & Formatting (4 guidelines)
- **FMT-BREAK-BEFORE-OP** - Break before binary operators
- **FMT-BREAK-BEFORE-DOT** - Break before method calls
- **FMT-TRAILING-COMMA** - Use trailing commas
- **FMT-ALIGN-TERNARY** - Format ternary expressions

### Import & Organization (3 guidelines)
- **FMT-GROUP-IMPORTS** - Group and organize imports
- **FMT-LAZY-IMPORT** - Lazy imports for heavy modules
- **FMT-STAR-IMPORT** - Avoid star imports

## Common Style Issues → Refactoring Solutions

| Linter Says | Root Cause | Refactoring Solution |
|------------|------------|---------------------|
| Line too long (E501) | Complex expression | Extract Variable / Extract Method |
| Too many arguments (R0913) | Related params separate | Introduce Parameter Object (Dataclass) |
| Too complex (C901) | Nested conditions | Guard Clauses / Extract Method |
| Too many nested blocks | Deep nesting | Early Returns / Extract Iterator |
| Function too long (C0302) | Does too much | Extract Method / Compose Method |
| Too many branches (R0912) | Long if-elif chain | Dictionary Lookup / Pattern Match |
| Expression too complex | Unclear logic | Extract Boolean Variable |
| Wrong import order (I001) | Disorganized imports | Group Imports (PEP 8) |

## Example Use Cases

### Refactoring for Line Length
- "This line is 120 chars - how do I refactor it?"
- "Extract variable to fix this long line"
- "Too many parameters causing long signature"

### Refactoring for Complexity
- "Pylint says too complex (15/10) - help refactor"
- "Simplify this nested conditional"
- "Reduce cyclomatic complexity structurally"

### Refactoring for Readability
- "Make this expression clearer through refactoring"
- "Extract method from this long function"
- "Flatten this deeply nested code"

### Learning Refactoring Patterns
- "What refactoring fixes too many parameters?"
- "Show me guard clause pattern"
- "How to use parameter objects in Python?"

## Benefits

- ✓ **Deeper than formatters** - Structural improvements, not just cosmetic
- ✓ **Root cause fixes** - Solve problems, don't suppress warnings
- ✓ **Learn refactoring** - 40+ patterns with examples
- ✓ **Brandon Rhodes inspired** - Based on "A Python Aesthetic" talk
- ✓ **Beyond linters** - Understand *why* linters complain
- ✓ **Better code** - More maintainable, testable, readable
- ✓ **Pattern-based** - Catalog of proven solutions
- ✓ **Educational** - Learn to think structurally

## What Gets Checked

### Style Issues That Indicate Deeper Problems
- Lines too long → Extract variables/methods needed
- Functions too complex → Simplification needed
- Too many parameters → Parameter object needed
- Deep nesting → Guard clauses/extraction needed
- Complex expressions → Naming needed
- Long methods → Decomposition needed
- Too many branches → Lookup table/polymorphism needed

### Refactoring Solutions Applied
- Extract Variable - for clarity and line length
- Extract Method - for complexity and reuse
- Introduce Parameter Object - for parameter lists
- Guard Clauses - for nesting and complexity
- Extract Iterator/Generator - for nested loops
- Decompose Conditional - for complex logic
- Replace Conditional with Lookup - for branches
- Compose Method - for long methods

## Difference from Other Skills

| Skill | Focus |
|-------|-------|
| **python-format-refactoring-reviewer** | Solve style issues through refactoring |
| python-refactoring-reviewer | General code quality refactoring |
| python-zen-reviewer | Python philosophy and Pythonic code |
| python-security-privacy-reviewer | Security vulnerabilities |
| python-functional-reviewer | Functional programming patterns |

This skill specifically addresses **formatting/style warnings by refactoring the structure**, not just reformatting.

## Sources and Attribution

All guidelines are based on:
- **Brandon Rhodes** - "A Python Aesthetic" (PyCon Canada 2012)
- **Brandon Rhodes** - PyCon 2013 talk on code formatting
- **Refactoring Guru** - Extract Method, Extract Variable, Introduce Parameter Object
- **Martin Fowler** - Refactoring catalog
- **PEP 8** - Style Guide for Python Code

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## License

This skill is licensed under MIT. It is based on public talks, documentation, and established refactoring patterns.

---

**Refactor for structure, and style follows naturally.**
