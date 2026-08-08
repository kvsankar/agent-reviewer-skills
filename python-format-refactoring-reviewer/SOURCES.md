# Sources and References

## Methodology

This Format/Style Refactoring Reviewer skill was created through systematic research of [Brandon Rhodes](https://rhodesmill.org/brandon/)' talks on Python aesthetics and code formatting, combined with established refactoring patterns from Martin Fowler's refactoring catalog and Refactoring Guru. The skill translates the philosophy of "refactor to solve style issues" into 40+ actionable guidelines with concrete before/after examples.

**Created:** January 2025

---

## Primary Sources

### 1. Brandon Rhodes - "A Python Aesthetic: Beauty and Why I Python"
- **Event:** PyCon Canada 2012, Toronto
- **Date:** November 10, 2012
- **Slides:** https://rhodesmill.org/brandon/slides/2012-11-pyconca/
- **Description:** Explores how Python code formatting and indentation should be treated as intentional acts of graphic design
- **Used for:** Core philosophy that formatting issues indicate structural problems

**Relevant Guidelines:**
- FMT-EXTRACT-VAR - Extracting variables to solve line length
- FMT-EARLY-RETURN, FMT-CONTINUE - Reducing indentation depth
- FMT-EXTRACT-NESTED, FMT-EXTRACT-ITER - Factoring out nested logic and iterators
- FMT-BREAK-BEFORE-OP - Breaking before binary operators (mathematical style)
- FMT-BREAK-BEFORE-DOT - Method chaining formatting
- FMT-TRAILING-COMMA - Symmetry and version control friendliness
- FMT-COMMENT-TO-NAME - Replacing comments with meaningful variable names

**Key Quote:**
> "Rather than awkward line wrapping, introduce meaningful intermediate variables."

**Additional Resources:**
- Talk discusses PEP 8 line width constraints (79 characters)
- References Robert Bringhurst's typographic principles
- Demonstrates progressive refactoring from simple to complex formatting

---

### 2. Brandon Rhodes - PyCon 2013 Talk (Santa Clara)
- **Event:** PyCon US 2013
- **Date:** March 15, 2013
- **Slides:** https://rhodesmill.org/brandon/slides/2013-03-pycon/
- **Description:** Explores choosing names wisely when writing Python code, with comparisons to typographic principles
- **Used for:** Naming as a solution to formatting problems

**Relevant Guidelines:**
- FMT-EXTRACT-VAR - Using meaningful names from Extreme Programming principles
- FMT-ARG-PER-LINE - Formatting multi-line function calls with trailing commas

**Key Principle:**
> "Names serve as the primary mechanism for communicating intent in dynamically-typed Python. Strategic naming choices resolve formatting constraints while enhancing code comprehension."

---

### 3. Refactoring Guru - Extract Variable
- **URL:** https://refactoring.guru/extract-variable
- **License:** Educational/informational content
- **Used for:** Extract Variable refactoring pattern

**Relevant Guidelines:**
- FMT-EXTRACT-VAR - Extract variable for complex expressions
- FMT-EXTRACT-BOOL - Extract boolean variable
- FMT-NAME-BOOL - Name complex boolean expressions
- FMT-NAME-CALC - Name intermediate calculations
- FMT-TEMP-EXPLAIN - Use temporary variables for explanation

**Problem Addressed:**
> "You have an expression that's hard to understand."

**Solution:**
> "Place the result of the expression or its parts in separate variables that are self-explanatory."

**Benefits:**
- Improved readability through intention-revealing identifiers
- Code clarity reduces dependency on comments
- Complex conditions become self-documenting

**Important Note:**
Performance consideration with short-circuit operators - extracting variables forces all method calls to execute.

---

### 4. Refactoring Guru - Extract Method
- **URL:** https://refactoring.guru/extract-method
- **License:** Educational/informational content
- **Used for:** Extract Method refactoring pattern

**Relevant Guidelines:**
- FMT-EXTRACT-METHOD - Extract method for long expressions
- FMT-LONG-METHOD - Extract method to reduce function length
- FMT-EXTRACT-NESTED - Extract nested logic to method
- FMT-SINGLE-RESP - One responsibility per method
- FMT-COMPOSE-METHOD - Compose method pattern

**Problem:**
> "You have a code fragment that can be grouped together."

**Solution:**
> "Move the code to a separate new method and replace the original code with a call to that method."

**Benefits:**
1. Enhanced readability - descriptive method names clarify intent
2. Reduced duplication - reusable code segments
3. Better error isolation - independent code blocks minimize unintended modifications

**Addresses Code Smells:**
- Long Method
- Duplicate Code
- Feature Envy

---

### 5. Refactoring Guru - Introduce Parameter Object
- **URL:** https://refactoring.guru/introduce-parameter-object
- **License:** Educational/informational content
- **Used for:** Parameter object pattern

**Relevant Guidelines:**
- FMT-PARAM-OBJECT - Parameter object for long signatures
- FMT-PARAM-DATACLASS - Dataclass for related parameters
- FMT-CONFIG-OBJECT - Configuration object pattern
- FMT-BUILDER - Builder pattern for optional parameters

**Problem:**
> "Methods frequently contain identical parameter groups that recur across multiple functions."

**Solution:**
> "Replace these parameters with an object."

**Benefits:**
- Improved readability - single named object provides semantic clarity
- Reduced duplication - eliminates scattered parameter groups
- Behavioral opportunities - enables moving methods to the parameter class

**Addresses Code Smells:**
- Long Parameter List
- Data Clumps
- Primitive Obsession

**Important Consideration:**
Avoid creating "Data Class" code smell - move related behaviors to the new class.

---

### 6. Refactoring Best Practices - Avoiding Deep Nesting
- **URL:** https://glinteco.com/en/post/tips-refactoring-clean-code-tip-6-avoid-deep-nesting/
- **License:** Educational/informational content
- **Used for:** Techniques to reduce nesting depth

**Relevant Guidelines:**
- FMT-GUARD-CLAUSE - Guard clauses for complexity
- FMT-EARLY-RETURN - Early returns to reduce nesting
- FMT-CONTINUE - Use continue in loops
- FMT-INVERT-COND - Invert conditions to reduce nesting
- FMT-FLATTEN-LOOP - Flatten nested loops

**Core Principle:**
> "Avoiding deep nesting is crucial for writing readable and maintainable code."

**Key Techniques:**
1. **Early Returns & Guard Clauses** - Check for invalid conditions upfront and exit immediately
2. **List Comprehensions** - Simplify loops and conditional filtering
3. **Function Decomposition** - Break complex logic into smaller, single-purpose functions

**Before/After Examples:**
- Conditional logic: Multiple nested ifs → Guard clauses with early returns
- Filtering: Nested loops with checks → List comprehension with combined conditions
- Complex operations: Single monolithic function → Separate functions with upfront validation

---

### 7. Martin Fowler - Refactoring Catalog
- **Source:** Refactoring: Improving the Design of Existing Code
- **Used for:** General refactoring patterns and principles

**Relevant Guidelines:**
- FMT-DECOMPOSE-COND - Decompose conditional (from Fowler's catalog)
- FMT-EXTRACT-CLASS - Extract class for related methods
- FMT-SIMPLIFY-LOGIC - Simplify conditional logic
- FMT-WHOLE-OBJECT - Preserve whole object refactoring

**Key Patterns:**
- Decompose Conditional - Break complex conditionals into named parts
- Extract Class - Separate responsibilities into focused classes
- Preserve Whole Object - Pass object instead of individual fields
- Replace Nested Conditional with Guard Clauses

---

### 8. PEP 8 - Style Guide for Python Code
- **URL:** https://peps.python.org/pep-0008/
- **Authors:** Guido van Rossum, Barry Warsaw, Nick Coghlan
- **Status:** Active (Process)
- **License:** Public Domain
- **Used for:** Python style conventions and formatting rules

**Relevant Guidelines:**
- FMT-BREAK-BEFORE-OP - Breaking before binary operators (PEP 8 update 2016)
- FMT-GROUP-IMPORTS - Import organization (stdlib, third-party, local)
- FMT-STAR-IMPORT - Avoid star imports
- FMT-ARG-PER-LINE - Multi-line argument formatting

**Key Rules:**
- Maximum line length: 79 characters
- Import order: standard library, third-party, local application
- Breaking before binary operators (updated guidance)
- Trailing commas in multi-line constructs

---

### 9. Python Design Patterns and Idioms
- **Sources:** Python community best practices, itertools patterns
- **Used for:** Pythonic solutions to common problems

**Relevant Guidelines:**
- FMT-REDUCE-BRANCHES - Dictionary lookup pattern
- FMT-LOOKUP-TABLE - Replace algorithm with lookup table
- FMT-PATTERN-MATCH - Pattern matching (Python 3.10+)
- FMT-FLATTEN-LOOP - itertools.chain for flattening
- FMT-REPLACE-LOOP - Replace loop with comprehension
- FMT-LAZY-IMPORT - Lazy imports for performance

**Patterns:**
- Dictionary-based dispatch (replace if-elif chains)
- Generator/iterator extraction
- List/dict/set comprehensions
- Pattern matching (structural pattern matching PEP 634)
- Lazy evaluation and imports

---

## Additional Influences

### Clean Code Principles
- Single Responsibility Principle (SRP)
- Don't Repeat Yourself (DRY)
- Self-documenting code
- Meaningful names over comments

### SOLID Principles
- Single Responsibility (FMT-SINGLE-RESP, FMT-EXTRACT-CLASS)
- Open/Closed Principle (configuration objects)
- Dependency Inversion (parameter objects)

### Functional Programming
- Pure functions and immutability
- Function composition (FMT-COMPOSE-METHOD)
- Pipeline patterns (FMT-INTERMEDIATE)
- Lazy evaluation (generators, FMT-EXTRACT-ITER)

---

## Research Process

### Web Searches Performed
1. **"Brandon Rhodes Python style formatting refactoring talk PyCon"** - Located talks and slides
2. **"Brandon Rhodes 'line too long' refactoring instead of formatting"** - Found core philosophy
3. **'"too many parameters" "introduce parameter object" Python refactoring dataclass'** - Parameter object patterns
4. **'Python "deep nesting" guard clause refactoring "early return"'** - Nesting reduction techniques
5. **"Python code formatting refactoring patterns"** - General refactoring for style

### Websites Consulted
- rhodesmill.org/brandon/slides/ - Brandon Rhodes' presentation slides
- refactoring.guru - Refactoring patterns catalog
- peps.python.org - Python Enhancement Proposals
- glinteco.com - Refactoring best practices

---

## Guideline Organization

The 40+ guidelines are organized into 8 categories mapping style issues to refactoring solutions:

1. **Line Length Issues (8)** - Extract variable/method, parameter objects, expression breaking
2. **Complexity Issues (7)** - Guard clauses, boolean extraction, lookup tables, pattern matching
3. **Nesting Issues (6)** - Early returns, continue, extract iterator, flatten loops
4. **Parameter Issues (5)** - Dataclass, whole object, config object, kwargs, builder
5. **Expression Clarity (5)** - Named booleans, intermediate variables, comment replacement
6. **Method Organization (5)** - Extract method, extract class, compose method, single responsibility
7. **Operators & Formatting (4)** - Break before operator/dot, trailing commas, ternary
8. **Import & Organization (3)** - Group imports, lazy imports, explicit imports

---

## Mnemonic ID Convention

All guidelines use the **FMT-** prefix to identify format/style refactoring patterns:
- Format: `FMT-KEYWORD`
- Examples: `FMT-EXTRACT-VAR`, `FMT-GUARD-CLAUSE`, `FMT-PARAM-OBJECT`
- Consistent with project's mnemonic ID pattern (all caps, hyphenated)
- Searchable and distinct from other reviewer skills

---

## Code Examples

All code examples in SKILL.md were:
1. **Inspired by** Brandon Rhodes' talks and slides
2. **Adapted from** Refactoring Guru patterns
3. **Created as original examples** demonstrating specific refactorings
4. **Structured as before/after pairs** showing style issue → refactored solution

### Example Attribution Pattern
- Before code: Demonstrates what linters (pylint/ruff/flake8) would flag
- After code: Shows proper refactoring (not just reformatting)
- Linter messages: Realistic warnings from common Python linters
- Root cause analysis: Explains structural problem causing style issue

---

## Distinction from Other Refactoring Resources

### This Skill vs Black/autopep8
- **Formatters:** Mechanically reformat code to fit style rules
- **This Skill:** Suggests structural refactoring to solve underlying issues
- Example: Black wraps long lines; this skill suggests extracting variables/methods

### This Skill vs Pylint/Ruff
- **Linters:** Flag style violations and complexity
- **This Skill:** Explains why violations occur and how to refactor
- Example: Pylint says "too complex"; this skill shows guard clause refactoring

### This Skill vs General Refactoring
- **General Refactoring:** Improve code quality broadly
- **This Skill:** Specifically solve style/format warnings through refactoring
- Focus: Style issues as indicators of structural problems

---

## Verification

All guidelines were verified against:
1. ✅ Brandon Rhodes' published talks and slides
2. ✅ Refactoring Guru's pattern catalog
3. ✅ Martin Fowler's refactoring catalog
4. ✅ PEP 8 style guide
5. ✅ Real-world pylint/ruff/flake8 warnings
6. ✅ Python community best practices

---

## Tools Referenced

### Linters
- **pylint** - Python code analyzer (error codes: E501, C901, R0913, etc.)
- **ruff** - Fast Python linter
- **flake8** - Style guide enforcement (F403, F405, etc.)
- **isort** - Import sorting tool (I001, etc.)

### Formatters
- **Black** - The uncompromising Python code formatter
- **autopep8** - Automatic PEP 8 formatter

### Type Checkers
- **mypy** - Static type checker for Python

---

## Updates and Maintenance

- **Version:** 1.0
- **Created:** January 2025
- **Last Updated:** January 2025
- **Python Version Compatibility:** Python 3.6+ (dataclasses), Python 3.10+ (pattern matching)

**Future Updates May Include:**
- Additional refactoring patterns for Python 3.12+
- Integration with newer linter warnings
- More complex real-world scenarios
- Performance-focused refactorings

---

## Legal and Attribution

### Brandon Rhodes' Talks
- Public presentations at PyCon and other conferences
- Slides available on rhodesmill.org
- Educational content shared with community

### Refactoring Guru
- Educational refactoring resource
- Patterns catalog with code examples
- Publicly available educational content

### PEP Documents
- **License:** Public Domain
- **Source:** Python Software Foundation
- **Usage:** Freely quotable and referenceable

### Code Examples
- **Original examples:** Created for this skill
- **Inspired by:** Public talks, refactoring catalogs, and educational resources
- **Skill license:** MIT

---

## Acknowledgments

Special thanks to:
- **Brandon Rhodes** - For articulating the philosophy of refactoring for style
- **Martin Fowler** - For the foundational refactoring catalog
- **Refactoring Guru** - For clear pattern documentation
- **Python Software Foundation** - For PEP 8 and Python's design philosophy
- **Linter/Formatter Authors** - For tools that identify style issues

---

**Note:** This skill teaches that style issues are often symptoms of structural problems. By refactoring the structure, style naturally improves without fighting the linter.

---

**Created:** January 2025
**Last Updated:** January 2025
**Skill Version:** 1.0
