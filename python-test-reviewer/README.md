# Python Test Reviewer Skill

A Claude Code skill that reviews Python tests for quality and suggests multiple testing strategies for different scenarios. **Quality over quantity** - shows detailed approaches, not just good/bad examples.

## What This Skill Does

This skill transforms Claude into a testing expert who:
- **Shows multiple testing strategies** for the same code (not just one "right" way)
- **Explains trade-offs** between different approaches
- **Provides complete, runnable examples** for each strategy
- **Teaches test thinking** - when to use mocks vs stubs vs fakes
- **Reviews for test quality** - not just coverage percentage
- **Identifies test anti-patterns** and suggests fixes

## Philosophy

> **"Tests should verify behavior, not implementation."** - Martin Fowler

This skill doesn't just show "bad test" vs "good test". Instead, it shows 2-4 different testing strategies for each scenario with detailed explanations of when to use each approach.

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r python-test-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "python-test-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r python-test-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/python-test-reviewer
git commit -m "Add Python Test Reviewer skill"
```

**✅ Self-Contained:** All 25 guidelines are embedded directly in SKILL.md - no external file references needed!

## How to Use

Simply ask Claude to review your tests or suggest testing strategies:

```
"Review these tests for quality"
"Show me different ways to test this function"
"How should I test this class with external dependencies?"
"What testing strategies work for this async code?"
"Review test coverage - am I testing the right things?"
```

The skill will automatically activate based on keywords like:
- test review, testing strategies
- pytest, test quality, test coverage
- mocking, fixtures, parametrize
- AAA pattern, test patterns

## What You'll Get

A comprehensive test review with:
- **Code to Test** - Shows the production code first
- **Multiple Strategies** - 2-4 different testing approaches
- **Complete Examples** - Full, runnable test code for each strategy
- **Trade-offs** - Pros and cons of each approach
- **Recommendations** - When to use each strategy

### Example Review

```markdown
## Test Review: shopping_cart.py

### TEST-STATEFUL: Testing Stateful Objects

**Code to test:**
```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
        self.items.append({'item': item, 'quantity': quantity})
```

**Strategy 1: Fresh Instance Per Test**
```python
def test_add_item():
    cart = ShoppingCart()  # Fresh instance
    cart.add_item(item, 1)
    assert len(cart.items) == 1
```
**Pros:** Perfect test isolation, no state leakage
**Cons:** Duplication in setup

**Strategy 2: Fixture-Based Setup**
```python
@pytest.fixture
def cart():
    return ShoppingCart()

def test_add_item(cart):  # Injected
    cart.add_item(item, 1)
    assert len(cart.items) == 1
```
**Pros:** DRY, Pythonic, pytest idiomatic
**Cons:** Setup hidden in fixture

**Trade-offs:**
- Use Strategy 1 when each test needs different setup
- Use Strategy 2 when all tests need same initial state (most common)

**Recommendation:**
Use fixture-based setup as default for stateful objects. It's most Pythonic and works well with pytest.
```

## The 25 High-Quality Guidelines

### Test Structure & Organization (5)
- **TEST-AAA** - The Arrange-Act-Assert pattern (3 strategies)
- **TEST-ONE-ASSERT** - Test one behavior per test (3 strategies)
- **TEST-NAMING** - Descriptive test names
- **TEST-STRUCTURE** - Test file organization
- **TEST-FIXTURE-SCOPE** - Function vs module vs session scope

### Testing Strategies for Different Scenarios (6)
- **TEST-PURE-FUNC** - Testing pure functions (4 strategies: simple, parametrize, property-based, combined)
- **TEST-STATEFUL** - Testing stateful objects (4 strategies: fresh instance, fixtures, factory, class-based)
- **TEST-EXCEPTIONS** - Testing error paths (4 strategies)
- **TEST-ASYNC** - Testing async code
- **TEST-CLASS** - Testing classes and methods
- **TEST-INTEGRATION** - Integration vs unit testing

### Test Doubles & Isolation (5)
- **TEST-MOCK-VS-STUB** - Choosing the right test double (4 strategies: mock, stub, fake, real)
- **TEST-FAKE** - Building effective fakes
- **TEST-SPY** - Using test spies
- **TEST-NO-MOCK** - When to avoid mocking
- **TEST-PATCH-WHERE** - Where to patch in Python

### Advanced Testing Patterns (4)
- **TEST-PARAMETRIZE** - Effective parametrized testing (4 strategies)
- **TEST-PROPERTY** - Property-based testing with Hypothesis
- **TEST-FIXTURES** - Advanced fixture patterns (4 strategies with different scopes)
- **TEST-FACTORIES** - Factory fixtures for flexibility

### Test Quality & Completeness (5)
- **TEST-EDGE-CASES** - Testing boundaries (4 strategies: explicit, parametrize, property-based, equivalence partitioning)
- **TEST-ERROR-PATHS** - Comprehensive error testing
- **TEST-COVERAGE-QUALITY** - Coverage vs test quality (4 strategies)
- **TEST-FLAKY** - Avoiding flaky tests
- **TEST-FAST** - Keeping tests fast

## Key Differentiators

### Shows MULTIPLE Strategies

Unlike other testing guides that show one "right" way, this skill shows 2-4 different approaches for each testing scenario:

**Example: Testing Pure Functions**
1. Simple example-based tests
2. Parametrized tests
3. Property-based testing (Hypothesis)
4. Combination approach

Each with complete code, pros/cons, and when to use it.

### Complete, Runnable Examples

Every example shows:
- The production code being tested
- Complete test code (not just snippets)
- Full imports and setup
- Actual assertions

### Trade-Off Analysis

For each scenario, explains:
- When to use each strategy
- Pros and cons of each approach
- Realistic trade-offs (speed vs thoroughness, simplicity vs coverage)
- Best practices and recommendations

### Authoritative Sources

Based on:
- **pytest documentation** - Official best practices
- **Martin Fowler** - Mocks Aren't Stubs, testing principles
- **Harry Percival** - Test-Driven Development with Python
- **James Cooke** - AAA pattern for Python
- **Gerard Meszaros** - xUnit Test Patterns

## Testing Philosophy

### Quality Over Coverage

Don't chase 100% coverage. Write tests that would fail if the code was broken in important ways.

### Test Behavior, Not Implementation

Tests should verify what code does, not how it does it. Implementation details can change.

### Multiple Strategies for Different Needs

No single testing approach fits all scenarios. Learn when to use:
- Mocks vs Stubs vs Fakes vs Real dependencies
- Simple tests vs Parametrized vs Property-based
- Function-scoped vs Module-scoped vs Session-scoped fixtures

### Test Isolation

Each test should be independent. No shared state, no test execution order dependencies.

## Example Use Cases

### Reviewing Existing Tests
- "Review these tests - are they testing the right things?"
- "This test is flaky, help me fix it"
- "Are my assertions strong enough?"

### Learning Testing Strategies
- "Show me different ways to test this function"
- "When should I use mocks vs stubs?"
- "How do I test this class with database dependencies?"

### Improving Test Quality
- "How can I make these tests more maintainable?"
- "These tests are slow, how can I speed them up?"
- "Am I testing edge cases properly?"

### Test-Driven Development
- "I'm about to write this function - what tests should I write first?"
- "Show me test strategies for this use case"
- "Help me write comprehensive tests for this API"

## Benefits

- ✓ **Learn testing strategies** - See multiple approaches with trade-offs
- ✓ **Write better tests** - Quality-focused, not coverage-focused
- ✓ **Make informed decisions** - Understand when to use which approach
- ✓ **Complete examples** - Copy-paste-ready test code
- ✓ **Avoid anti-patterns** - Learn what NOT to do
- ✓ **Authoritative guidance** - Based on established testing principles
- ✓ **Pytest best practices** - Pythonic testing patterns
- ✓ **Educational** - Teaches test thinking, not just patterns

## What Gets Checked

### Test Structure
- AAA (Arrange-Act-Assert) pattern clarity
- Test naming conventions
- Test organization and grouping
- Fixture usage and scope

### Test Quality
- Strong vs weak assertions
- Behavior verification vs implementation details
- Test isolation and independence
- Edge case coverage

### Testing Strategies
- Appropriate test double usage (mock/stub/fake)
- Parametrization effectiveness
- Property-based testing opportunities
- Fixture patterns and composition

### Test Completeness
- Happy path and error path coverage
- Boundary value testing
- Integration point verification
- Side effect validation

### Test Maintainability
- Test readability and clarity
- Fixture reusability
- Test speed and performance
- Avoiding flaky tests

## Sources and Attribution

All guidelines are based on:
- **pytest Documentation** - Official pytest patterns and best practices
- **Martin Fowler** - "Mocks Aren't Stubs", testing principles
- **Harry Percival** - "Test-Driven Development with Python"
- **James Cooke** - AAA pattern for Python developers
- **Gerard Meszaros** - xUnit Test Patterns, test double taxonomy
- **Hypothesis Documentation** - Property-based testing patterns

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## License

This skill is provided as-is for use with Claude Code. Based on public documentation, established testing principles, and community best practices.

---

**Quality over quantity. Behavior over implementation. Strategies over dogma.**
