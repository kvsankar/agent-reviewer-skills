# Sources and References

## Methodology

This Python Test Reviewer skill was created through extensive research of authoritative testing resources, focusing on **quality over quantity**. The skill presents multiple testing strategies for each scenario (not just "good" vs "bad" examples), with complete runnable code, trade-off analysis, and recommendations based on established testing principles.

**Philosophy:** Show developers HOW to think about testing, not just WHAT patterns to use.

**Created:** January 2025

---

## Primary Sources

### 1. pytest Documentation
- **Official URL:** https://docs.pytest.org/
- **Used for:** pytest-specific patterns, fixtures, parametrization, best practices
- **License:** MIT License
- **Key Topics:**
  - How to parametrize fixtures and test functions
  - Good integration practices
  - Fixture scopes (function, module, session)
  - pytest.raises for exception testing

**Relevant Guidelines:**
- TEST-AAA - Adapted AAA pattern for pytest context
- TEST-PARAMETRIZE - Official parametrization patterns
- TEST-FIXTURES - Fixture scopes and composition
- TEST-EXCEPTIONS - pytest.raises patterns

**Key Resource:** "Good Integration Practices" - https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html

---

### 2. Martin Fowler - "Mocks Aren't Stubs"
- **URL:** https://martinfowler.com/articles/mocksArentStubs.html
- **Author:** Martin Fowler
- **Published:** January 2, 2007
- **Used for:** Test double taxonomy, state vs behavior verification, testing philosophies
- **License:** Public article

**Key Concepts:**
- **Test Double Taxonomy** (Gerard Meszaros):
  - Dummy Objects - passed but never used
  - Fake Objects - working implementations with shortcuts
  - Stubs - provide canned answers
  - Spies - stubs that record interactions
  - Mocks - pre-programmed with expectations

**Testing Philosophies:**
- **Classical TDD:** Uses real objects when practical, state verification
- **Mockist TDD:** Always mocks interesting behavior, behavior verification

**Relevant Guidelines:**
- TEST-MOCK-VS-STUB - Complete taxonomy with 4 strategies (mock, stub, fake, real)
- TEST-FAKE - Building effective fakes
- TEST-SPY - Using test spies
- TEST-NO-MOCK - When to avoid mocking

**Key Quote:**
> "The vocabulary of testing is getting blurred - to many people, all test doubles are "mocks". Understanding the differences is crucial."

---

### 3. James Cooke - AAA Pattern for Python
- **URL:** https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html
- **Author:** James Cooke
- **Used for:** AAA pattern structure, Python-specific implementation
- **Additional Resource:** flake8-aaa plugin for enforcing AAA

**The Three Sections:**

**1. Arrange:**
- Single contiguous block without empty lines
- Avoid assertions during arrangement
- Extract to fixture if complex

**2. Act:**
- Single line starting with `result =`
- Even when no return value, capture it
- Separate with blank lines above and below

**3. Assert:**
- One contiguous block of assertions
- Test returned value first, then side effects
- Extract repeated patterns to helper functions

**Relevant Guidelines:**
- TEST-AAA - Complete AAA pattern with 3 strategies
- TEST-ONE-ASSERT - One behavior per test (related to AAA structure)
- TEST-STRUCTURE - Test organization principles

**Benefits:**
- Clarity through visual structure
- Consistency across test suite
- Maintainability through separation of concerns

**Tool:** flake8-aaa plugin enforces AAA pattern compliance

---

### 4. Harry Percival - "Test-Driven Development with Python"
- **Book:** "Test-Driven Development with Python: Obey the Testing Goat" (3rd Edition)
- **Publisher:** O'Reilly Media
- **Used for:** TDD principles, test structure, Django/Selenium testing patterns
- **URL:** https://www.orei lly.com/library/view/test-driven-development-with/9781098148706/

**Key Principles:**
- **TDD Workflow:** Red/Green/Refactor
- **Test Organization:** Unit tests for functions/classes, functional tests for user interactions
- **Best Practices:**
  - Each test should test one thing
  - Small design when necessary, YAGNI
  - Test isolation in functional tests
  - Listening to your tests

**Relevant Guidelines:**
- TEST-ONE-ASSERT - Testing one behavior per test
- TEST-INTEGRATION - Integration vs unit testing strategies
- TEST-STRUCTURE - Test organization
- General TDD philosophy throughout

**Philosophy:**
> "The goal is to use TDD to reliably achieve 'clean code that works.'"

---

### 5. Real Python - "Effective Python Testing With pytest"
- **URL:** https://realpython.com/pytest-python-testing/
- **Updated:** December 2024
- **Used for:** pytest best practices, fixture patterns, parametrization examples
- **License:** Educational content

**Key Topics:**
- Managing test dependencies with fixtures
- Parametrization to avoid redundant test code
- Test organization and structure
- pytest ecosystem and plugins

**Statistics:**
- 50% of Python developers use pytest (Python Developers Survey)
- Most popular Python testing framework

**Relevant Guidelines:**
- TEST-FIXTURES - Fixture patterns and dependency injection
- TEST-PARAMETRIZE - Parametrization strategies
- TEST-STRUCTURE - Test organization

---

### 6. Pytest with Eric - Testing Best Practices
- **Blog:** https://pytest-with-eric.com/
- **Author:** Eric (Python testing educator)
- **Updated:** January 2025
- **Used for:** Practical pytest patterns, test organization, advanced techniques

**Key Articles:**
1. **"5 Best Practices For Organizing Tests"**
   - Mirror application folder structure
   - Separate tests from application code
   - Use conftest.py for shared fixtures
   - Follow naming conventions (test_*.py)

2. **"Python Unit Testing Best Practices"**
   - AAA pattern
   - Separate test functions
   - Meaningful test names
   - Test isolation

3. **"How to Use Hypothesis and Pytest for Property-Based Testing"**
   - Hypothesis integration with pytest
   - Strategy composition
   - Shrinking examples

**Relevant Guidelines:**
- TEST-STRUCTURE - Test organization patterns
- TEST-PROPERTY - Property-based testing with Hypothesis
- TEST-FIXTURES - conftest.py patterns

---

### 7. Hypothesis - Property-Based Testing Library
- **Documentation:** https://hypothesis.readthedocs.io/
- **Repository:** https://github.com/HypothesisWorks/hypothesis
- **License:** Mozilla Public License 2.0
- **Used for:** Property-based testing strategies, test generation

**Key Features:**
- Automatic test case generation
- Example shrinking (finding minimal failing cases)
- Built-in strategies for common types
- Composite strategies for complex data

**Basic Usage:**
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_matches_builtin(ls):
    assert sorted(ls) == my_sort(ls)
```

**Relevant Guidelines:**
- TEST-PROPERTY - Complete property-based testing guide
- TEST-PURE-FUNC - Strategy 3 uses Hypothesis
- TEST-EDGE-CASES - Strategy 3 uses property-based testing

**Philosophy:**
> "Write tests which should pass for all inputs in whatever range you describe, and let Hypothesis choose which inputs to check."

---

### 8. Gerard Meszaros - xUnit Test Patterns
- **Book:** "xUnit Test Patterns: Refactoring Test Code"
- **Publisher:** Addison-Wesley Professional
- **Used for:** Test double taxonomy, test patterns catalog
- **Referenced through:** Martin Fowler's article

**Test Double Types:**
1. **Dummy** - Passed but never used
2. **Fake** - Working implementation with shortcuts
3. **Stub** - Provides canned answers
4. **Spy** - Records information about calls
5. **Mock** - Pre-programmed with expectations

**Relevant Guidelines:**
- TEST-MOCK-VS-STUB - Complete taxonomy
- TEST-FAKE - Fake implementation patterns
- TEST-SPY - Spy patterns

---

### 9. NerdWallet Engineering - "5 Pytest Best Practices"
- **URL:** https://www.nerdwallet.com/blog/engineering/5-pytest-best-practices/
- **Published:** 2023
- **Used for:** Practical production pytest patterns

**Best Practices:**
1. Use fixtures for setup/teardown
2. Parametrize tests to reduce duplication
3. Use marks to organize tests
4. Keep tests fast
5. Test one thing at a time

**Relevant Guidelines:**
- TEST-FAST - Keeping tests fast
- TEST-PARAMETRIZE - Parametrization patterns
- TEST-FIXTURES - Fixture usage

---

### 10. Testing Design Patterns and Principles
- **Various Sources:** Stack Overflow, Medium, testing blogs
- **Used for:** Test anti-patterns, test smells, practical examples

**Common Test Smells:**
- Assertion Roulette - Multiple assertions without clear messages
- Test Code Duplication - Repeated setup/teardown
- Mystery Guest - Dependencies on external resources
- Eager Test - Testing too many things in one test
- Conditional Test Logic - Using if/else in tests
- Test Fixture Pollution - Shared state between tests

**Relevant Guidelines:**
- TEST-FLAKY - Avoiding flaky tests
- TEST-COVERAGE-QUALITY - Quality over coverage
- TEST-ONE-ASSERT - Testing one behavior

---

## Research Process

### Web Searches Performed
1. **"pytest best practices authoritative guide 2024"** - Found Real Python, Pytest with Eric, Lambda Test resources
2. **"Python testing strategies patterns Kent Beck Martin Fowler"** - Located Fowler's "Mocks Aren't Stubs"
3. **"Test-Driven Development with Python Harry Percival best practices"** - Found TDD principles and book
4. **"Python test patterns fixtures mocks stubs fakes test doubles"** - Comprehensive test double research
5. **"AAA pattern Arrange Act Assert Python testing examples"** - James Cooke's AAA pattern guide
6. **"pytest parametrize examples multiple test strategies"** - Parametrization patterns
7. **"Python hypothesis property-based testing examples strategies"** - Hypothesis documentation
8. **"Python test organization structure best practices pytest"** - Test structure patterns
9. **"Python integration testing strategies patterns examples pytest"** - Integration testing approaches

### Methodology
1. **Identify authoritative sources** - pytest docs, Martin Fowler, established authors
2. **Research multiple approaches** - Not just one "right" way
3. **Gather complete examples** - Full, runnable code
4. **Understand trade-offs** - Pros/cons of each approach
5. **Focus on quality** - Depth over breadth

---

## Guideline Structure

Each guideline follows this format:

### Code to Test
Shows the production code FIRST, so readers understand what's being tested.

### Multiple Strategies (2-4 per guideline)
Each strategy includes:
- **Complete, runnable test code**
- **Pros** - Benefits of this approach
- **Cons** - Drawbacks and limitations
- **When to use** - Specific scenarios

### Trade-offs
Explicit comparison of when to use each strategy.

### Recommendation
Best practice guidance based on authoritative sources.

---

## Key Differentiators from Other Testing Guides

### 1. Multiple Strategies vs Single "Right" Way
Most testing guides show one approach. This skill shows 2-4 alternatives with trade-offs.

**Example:**
- TEST-PURE-FUNC shows 4 strategies: simple tests, parametrize, property-based, combination
- Each with complete code, pros/cons, and recommendations

### 2. Complete, Runnable Examples
Every example shows:
- Production code being tested
- Complete test code (not snippets)
- Full imports and setup
- Actual assertions

### 3. Trade-Off Analysis
Explicitly discusses:
- Speed vs thoroughness
- Simplicity vs coverage
- Coupling vs isolation
- Maintainability vs flexibility

### 4. Quality Over Quantity
25 guidelines instead of 50+, but each is MUCH more detailed:
- 4 strategies per guideline
- Complete examples for each
- Detailed trade-off analysis
- Clear recommendations

---

## Mnemonic ID Convention

All guidelines use the **TEST-** prefix to identify testing patterns:
- Format: `TEST-KEYWORD`
- Examples: `TEST-AAA`, `TEST-MOCK-VS-STUB`, `TEST-PARAMETRIZE`
- Consistent with project's mnemonic ID pattern (all caps, hyphenated)
- Searchable and distinct from other reviewer skills

---

## Code Example Attribution

All code examples were:
1. **Inspired by** authoritative sources listed above
2. **Adapted for Python/pytest** - Made Pythonic and pytest-specific
3. **Created as original examples** - Demonstrating specific testing strategies
4. **Structured for education** - Production code → Multiple test strategies → Trade-offs

### Example Pattern:
- **Production Code:** Original, demonstrating testing challenge
- **Test Strategies:** Inspired by pytest docs, Martin Fowler principles, community patterns
- **Trade-offs:** Based on real-world testing experience and authoritative guidance

---

## Testing Philosophy Sources

### "Test Behavior, Not Implementation"
- **Source:** Martin Fowler, Michael Feathers, Kent Beck
- **Principle:** Tests should verify what code does, not how it does it
- **Applied in:** TEST-MOCK-VS-STUB, TEST-COVERAGE-QUALITY

### "Quality Over Coverage"
- **Source:** Testing community consensus, Real Python
- **Principle:** 100% coverage ≠ 100% tested
- **Applied in:** TEST-COVERAGE-QUALITY guideline

### "Test Isolation"
- **Source:** xUnit Test Patterns, pytest documentation
- **Principle:** Each test should be independent
- **Applied in:** TEST-FIXTURES, TEST-STATEFUL, TEST-FLAKY

### "AAA Pattern"
- **Source:** Bill Wake (2001), James Cooke (Python-specific)
- **Principle:** Arrange-Act-Assert structure
- **Applied in:** TEST-AAA guideline

---

## Tools and Frameworks Referenced

### Testing Frameworks
- **pytest** - Primary Python testing framework (MIT License)
- **unittest** - Python standard library testing framework
- **Hypothesis** - Property-based testing (Mozilla Public License 2.0)

### Testing Tools
- **unittest.mock** - Standard library mocking
- **pytest-mock** - pytest plugin for mocking
- **flake8-aaa** - AAA pattern enforcement
- **pytest-cov** - Coverage reporting

### Related Tools
- **mypy** - Static type checking (helps with test type hints)
- **mutmut** - Mutation testing for test quality
- **faker** - Test data generation

---

## Verification

All guidelines were verified against:
1. ✅ Official pytest documentation
2. ✅ Martin Fowler's testing articles
3. ✅ Harry Percival's TDD book
4. ✅ James Cooke's AAA pattern guide
5. ✅ Hypothesis documentation
6. ✅ Real-world pytest usage patterns
7. ✅ Python testing community best practices

---

## Updates and Maintenance

- **Version:** 1.0
- **Created:** January 2025
- **Last Updated:** January 2025
- **Python Version Compatibility:** Python 3.7+ (pytest 6.0+)
- **Hypothesis Version:** 6.0+

**Future Updates May Include:**
- Additional testing strategies as pytest evolves
- More advanced fixture patterns
- Testing patterns for Python 3.12+ features
- Additional property-based testing examples

---

## Acknowledgments

Special thanks to:
- **pytest Development Team** - For excellent documentation and framework
- **Martin Fowler** - For "Mocks Aren't Stubs" and testing principles
- **Harry Percival** - For "Test-Driven Development with Python"
- **James Cooke** - For AAA pattern documentation and flake8-aaa
- **Gerard Meszaros** - For xUnit Test Patterns taxonomy
- **David MacIver** - For Hypothesis library
- **Testing Community** - For establishing best practices and patterns

---

## Legal and Attribution

### Official Documentation
- **pytest, Hypothesis, Python docs:** Open source licenses (MIT, Mozilla Public License 2.0)
- **Usage:** Freely referenceable for educational purposes

### Published Articles and Books
- **Martin Fowler's articles:** Public articles, freely quotable
- **Harry Percival's book:** Commercial book, principles referenced (not copied)
- **James Cooke's blog:** Public blog posts, attributed

### Code Examples
- **Original examples:** Created for this skill
- **Inspired by:** Authoritative sources listed above
- **License:** Provided as-is for educational use with Claude Code

---

**Note:** This skill emphasizes teaching testing strategies and trade-offs, not just showing patterns. The goal is to help developers make informed testing decisions based on their specific scenarios.

---

**Created:** January 2025
**Last Updated:** January 2025
**Skill Version:** 1.0
**Focus:** Quality over quantity, strategies over dogma
