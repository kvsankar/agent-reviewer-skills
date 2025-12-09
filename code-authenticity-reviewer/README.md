# Code Authenticity Reviewer

Detect fabricated, hallucinated, and unearned code assertions - a critical skill for reviewing AI-generated code.

## Purpose

This reviewer identifies code that **claims results without actually computing them**. As LLMs become more prevalent in software development, fabrication detection becomes essential for maintaining code quality and trust.

## What It Detects

### Magic Constants & Hardcoded Results
- Functions returning constants instead of computed values
- Fabricated metrics and statistics
- Confidence scores that appear from nowhere
- Mock data presented as real computation

### Disconnected Input/Output
- Parameters never used in computation
- Output unrelated to any computation
- Computation performed but results discarded
- Functions that always return the same value

### Phantom References
- References to non-existent line numbers, files, or functions
- Cross-references that don't match actual code
- Error messages describing impossible states

### Unsubstantiated Claims
- Complexity claims that don't match implementation (O(1) for O(n²))
- Performance claims without benchmarks
- Success messages without verification
- Counts and totals that aren't computed

### Brittle & Fake Tests
- Tests that always pass (`assert True`)
- Tests checking type but not content
- Tests that don't use the function's return value
- Verifying mock returns what mock was told to return
- Tautology tests (`assert x == x`)

### Dead & Unreachable Logic
- Code after return statements
- Conditionals that always take the same branch
- Computations overwritten before use
- Loops that never execute

## Example Findings

### AUTH-MAGIC-CONST: Hardcoded Value Instead of Computation

**Fabricated:**
```python
def calculate_average(numbers):
    return 42.5  # Magic constant!
```

**Authentic:**
```python
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```

### AUTH-UNUSED-PARAM: Parameters Never Used

**Fabricated:**
```python
def calculate_tax(income, deductions, filing_status):
    return 5000.00  # None of the parameters are used!
```

**Authentic:**
```python
def calculate_tax(income, deductions, filing_status):
    taxable_income = income - deductions
    rate = TAX_RATES[filing_status]
    return taxable_income * rate
```

### AUTH-ALWAYS-TRUE: Test That Always Passes

**Fabricated:**
```python
def test_user_validation():
    assert True  # Always passes!
```

**Authentic:**
```python
def test_user_validation():
    valid_user = {"name": "Test", "email": "test@example.com"}
    assert validate_user(valid_user) == True

    invalid_user = {"name": ""}
    assert validate_user(invalid_user) == False
```

## Guidelines (40+)

### Magic Constants (8)
- `AUTH-MAGIC-CONST` - Hardcoded values instead of computation
- `AUTH-MAGIC-RETURN` - Functions returning constants regardless of input
- `AUTH-FAKE-METRIC` - Fabricated metrics/statistics
- `AUTH-PHANTOM-SCORE` - Confidence scores without computation
- `AUTH-MOCK-AS-REAL` - Mock data presented as computed
- `AUTH-TEMPLATE-OUTPUT` - Template strings with placeholder values
- `AUTH-ROUND-NUMBER` - Suspiciously round numbers
- `AUTH-COPY-PASTE-RESULT` - Results that look copy-pasted

### Disconnected I/O (6)
- `AUTH-UNUSED-PARAM` - Parameters never used
- `AUTH-ORPHAN-OUTPUT` - Output unconnected to computation
- `AUTH-IGNORED-INPUT` - Input read but never influences result
- `AUTH-DEAD-COMPUTE` - Computation performed but discarded
- `AUTH-CONSTANT-FUNC` - Function always returns same value
- `AUTH-INPUT-THEATER` - Code that pretends to use input

### Phantom References (5)
- `AUTH-FAKE-LINE` - References to non-existent line numbers
- `AUTH-FAKE-FILE` - References to non-existent files
- `AUTH-FAKE-FUNC` - References to non-existent functions
- `AUTH-WRONG-XREF` - Cross-references that don't match
- `AUTH-FAKE-ERROR` - Error messages describing impossible states

### Unsubstantiated Claims (6)
- `AUTH-CLAIM-NO-PROOF` - Claims without supporting computation
- `AUTH-FAKE-COMPLEXITY` - Wrong complexity claims
- `AUTH-FAKE-COVERAGE` - Test coverage claims without measurement
- `AUTH-FAKE-PERF` - Performance claims without benchmarks
- `AUTH-FAKE-SUCCESS` - Success messages without verification
- `AUTH-FAKE-COUNT` - Counts that aren't computed

### Brittle Tests (10)
- `AUTH-ALWAYS-TRUE` - Tests that always pass
- `AUTH-ALWAYS-FALSE` - Tests that always fail
- `AUTH-TYPE-ONLY` - Tests checking type but not content
- `AUTH-SHALLOW-ASSERT` - Assertions that don't verify behavior
- `AUTH-IGNORED-RETURN` - Test doesn't use function's return value
- `AUTH-MOCK-VERIFY-MOCK` - Verifying mock returns what mock was told
- `AUTH-TAUTOLOGY-TEST` - Test asserts something equals itself
- `AUTH-NO-ASSERT` - Test with no assertions
- `AUTH-ASSERT-EXIST` - Only checking existence, not value
- `AUTH-TRIVIAL-EXPECT` - Expecting trivially true conditions

### Dead Logic (5)
- `AUTH-DEAD-CODE` - Code that can never execute
- `AUTH-UNREACHABLE-PATH` - Logic paths that can't be reached
- `AUTH-SHADOW-COMPUTE` - Computation overwritten before use
- `AUTH-FAKE-BRANCH` - Conditional always takes same branch
- `AUTH-LOOP-NEVER` - Loops that never execute

## Usage

### With Claude Code Skills

```bash
# Using the review tool
./review-cli.py \
  --repo https://github.com/user/repo \
  --reviewer code-authenticity-reviewer
```

### As a Claude Code Skill

```
Review src/api/ for code authenticity issues using the code-authenticity-reviewer skill
and write findings to reviews/authenticity.md
```

## Output Format

```markdown
## Code Authenticity Review: [File/Function Name]

### Authenticity Score: [HIGH/MEDIUM/LOW]

### Critical Fabrications

#### AUTH-MAGIC-CONST: Hardcoded average value
**Fabricated code:**
```python
def calculate_average(numbers):
    return 42.5
```

**Why it's fabricated:**
The return value has no relationship to the input parameter.

**Authentic implementation:**
```python
def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0
```

### Authenticity Checklist
- [ ] All outputs derived from inputs
- [ ] No magic constants for computed values
- [ ] Tests verify actual behavior
- [ ] Claims backed by computation
```

## Why This Matters

1. **LLM Code Generation** - AI models can confidently generate plausible-looking but fabricated code
2. **Trust** - Fabricated results erode trust in software systems
3. **Debugging** - Fake outputs make debugging nearly impossible
4. **Testing** - Brittle tests provide false confidence
5. **Documentation** - Phantom references mislead developers

## Language Support

This reviewer is **language-agnostic** and can detect fabrication patterns in:
- Python
- JavaScript/TypeScript
- Java
- Go
- Ruby
- And other languages

The patterns (magic constants, unused parameters, brittle tests) are universal across programming languages.

## See Also

- [SKILL.md](./SKILL.md) - Complete guidelines with examples
- [SOURCES.md](./SOURCES.md) - References and attribution
