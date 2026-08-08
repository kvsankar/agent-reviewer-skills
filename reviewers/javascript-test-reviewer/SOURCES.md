# Sources and References

## Methodology

This JavaScript Test Reviewer skill was created through extensive research of authoritative testing resources, focusing on **quality over quantity** and **user-centric testing**. The skill presents multiple testing strategies for each scenario (not just "good" vs "bad" examples), with complete runnable code, trade-off analysis, and recommendations based on established testing principles.

**Philosophy:** Teach developers HOW to think about testing in JavaScript/TypeScript, emphasizing Testing Library principles and user-centric approaches.

**Created:** November 2025

---

## Primary Sources

### 1. Jest Documentation

- **Official URL:** https://jestjs.io/
- **Used for:** Jest-specific patterns, matchers, mocking, async testing, best practices
- **License:** MIT License
- **Key Topics:**
  - Matchers (toBe, toEqual, toStrictEqual, toMatchObject)
  - Mocking (jest.mock, jest.fn, jest.spyOn)
  - Async testing (async/await, resolves, rejects)
  - Timer mocks (jest.useFakeTimers)
  - Snapshot testing
  - Configuration and setup

**Relevant Guidelines:**
- TEST-AAA - AAA pattern adapted for Jest
- ASSERT-EQUALITY - toBe vs toEqual vs toStrictEqual
- MOCK-MODULE - jest.mock patterns
- MOCK-TIMER - jest.useFakeTimers
- ASYNC-AWAIT - Jest async testing patterns
- ASSERT-SNAPSHOT - Snapshot testing best practices

**Key Resources:**
- "Getting Started" - https://jestjs.io/docs/getting-started
- "Using Matchers" - https://jestjs.io/docs/using-matchers
- "Mock Functions" - https://jestjs.io/docs/mock-functions
- "Testing Asynchronous Code" - https://jestjs.io/docs/asynchronous

**Statistics:**
- Most popular JavaScript testing framework
- Used by Facebook, Airbnb, Twitter, and others
- 40+ million weekly npm downloads

---

### 2. Testing Library Documentation

- **Official URL:** https://testing-library.com/
- **Maintainer:** Kent C. Dodds and contributors
- **License:** MIT License
- **Used for:** User-centric testing principles, component testing, query priorities, accessibility

**Guiding Principles:**
1. "The more your tests resemble the way your software is used, the more confidence they can give you."
2. Test behavior, not implementation details
3. Query priority: role > label > text > test-id
4. Use userEvent, not fireEvent

**Key Topics:**
- Query priorities (getByRole, getByLabelText, getByText)
- userEvent for realistic user interactions
- waitFor and async utilities
- Accessibility-focused testing
- Avoiding implementation details

**Relevant Guidelines:**
- TEST-COMPONENT - User-centric component testing
- COMP-QUERY - Query priority (role > label > text > test-id)
- COMP-USER-EVENT - userEvent vs fireEvent
- COMP-ACCESSIBILITY - Testing accessibility
- COMP-NO-IMPL - Avoiding implementation details
- ASSERT-DOM - DOM assertions

**Key Resources:**
- "Guiding Principles" - https://testing-library.com/docs/guiding-principles
- "Queries" - https://testing-library.com/docs/queries/about
- "React Testing Library" - https://testing-library.com/docs/react-testing-library/intro
- "user-event" - https://testing-library.com/docs/user-event/intro

**Philosophy:**
> "We try to only expose methods and utilities that encourage you to write tests that closely resemble how your web pages are used."

---

### 3. Vitest Documentation

- **Official URL:** https://vitest.dev/
- **Maintainer:** Anthony Fu and Vite team
- **License:** MIT License
- **Used for:** Modern testing patterns, Vite integration, Jest compatibility

**Key Features:**
- Jest-compatible API
- Native ESM support
- Extremely fast (Vite-powered)
- TypeScript support out of the box
- Component testing with Vite

**Key Topics:**
- Test runner configuration
- Watch mode and filtering
- Mocking and spies
- Snapshot testing
- Coverage reports

**Relevant Guidelines:**
- TEST-PURE-FUNC - Test organization patterns
- ASYNC-AWAIT - Async testing
- MOCK-MODULE - Module mocking (similar to Jest)

**Key Resources:**
- "Getting Started" - https://vitest.dev/guide/
- "API Reference" - https://vitest.dev/api/
- "Mocking" - https://vitest.dev/guide/mocking

**Note:** Most Jest patterns work in Vitest due to API compatibility

---

### 4. Kent C. Dodds - Testing JavaScript

- **Website:** https://testingjavascript.com/
- **Blog:** https://kentcdodds.com/blog
- **Author:** Kent C. Dodds (creator of Testing Library)
- **Used for:** Testing philosophy, best practices, common mistakes

**Key Articles:**

1. **"Common Mistakes with React Testing Library"**
   - URL: https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
   - Topics: Query priorities, userEvent, avoiding implementation details
   - Relevant to: COMP-QUERY, COMP-USER-EVENT, COMP-NO-IMPL

2. **"Write Tests. Not Too Many. Mostly Integration."**
   - Philosophy: Test pyramid with emphasis on integration tests
   - Relevant to: E2E-WHEN, MOCK-MINIMAL, TEST-INTEGRATION

3. **"Testing Implementation Details"**
   - URL: https://kentcdodds.com/blog/testing-implementation-details
   - Why testing implementation is harmful
   - Relevant to: COMP-NO-IMPL

4. **"Avoid the Test User"**
   - Focus on user behavior
   - Accessible queries
   - Relevant to: COMP-QUERY, COMP-ACCESSIBILITY

**Relevant Guidelines:**
- All component testing guidelines
- MOCK-MINIMAL - Avoid over-mocking
- E2E-WHEN - Test pyramid
- COMP-NO-IMPL - Avoid implementation details

**Key Quotes:**
> "Write tests. Not too many. Mostly integration."
> "The more your tests resemble the way your software is used, the more confidence they can give you."

---

### 5. Martin Fowler - Testing Principles

- **Website:** https://martinfowler.com/
- **Author:** Martin Fowler
- **Used for:** Test doubles, test pyramid, testing philosophy

**Key Articles:**

1. **"Mocks Aren't Stubs"**
   - URL: https://martinfowler.com/articles/mocksArentStubs.html
   - Test double taxonomy
   - State vs behavior verification
   - Relevant to: MOCK-MODULE, MOCK-FUNCTION, MOCK-MINIMAL, MOCK-SPY

2. **"Test Pyramid"**
   - URL: https://martinfowler.com/bliki/TestPyramid.html
   - Unit vs integration vs E2E balance
   - Relevant to: E2E-WHEN

**Test Double Taxonomy (Gerard Meszaros via Fowler):**
- **Dummy** - Passed but never used
- **Fake** - Working implementation with shortcuts
- **Stub** - Provides canned answers
- **Spy** - Records information about calls
- **Mock** - Pre-programmed with expectations

**Relevant Guidelines:**
- MOCK-MODULE - Module mocking strategies
- MOCK-MINIMAL - When to mock vs use real implementations
- E2E-WHEN - Test pyramid approach

---

### 6. Yoni Goldberg - JavaScript Testing Best Practices

- **Repository:** https://github.com/goldbergyoni/javascript-testing-best-practices
- **Author:** Yoni Goldberg
- **License:** MIT
- **Used for:** Comprehensive testing best practices

**Key Sections:**

1. **The Test Anatomy (AAA Pattern)**
   - Arrange, Act, Assert structure
   - Relevant to: TEST-AAA

2. **Avoid Global Test Fixtures**
   - Test isolation principles
   - Relevant to: TEST-ISOLATION

3. **Don't Catch Errors, Expect Them**
   - Error testing patterns
   - Relevant to: TEST-ERROR, ASYNC-ERROR

4. **Tag Your Tests**
   - Organization and categorization
   - Relevant to: TEST-DESCRIBE

5. **Measure Code Coverage, But Don't Let It Fool You**
   - Coverage vs quality
   - Relevant to: QUALITY-COVERAGE

**Relevant Guidelines:**
- TEST-AAA - AAA pattern
- TEST-ISOLATION - Test independence
- TEST-ERROR - Error handling
- QUALITY-COVERAGE - Coverage vs quality
- QUALITY-DETERMINISTIC - Avoiding flaky tests

---

### 7. Cypress Documentation

- **Official URL:** https://www.cypress.io/
- **Used for:** E2E testing patterns, page objects, best practices
- **License:** MIT License

**Key Topics:**
- E2E test organization
- Page object pattern
- Custom commands
- Handling async operations
- Preventing flaky tests
- Test data management

**Relevant Guidelines:**
- E2E-WHEN - When to use E2E tests
- E2E-PAGE-OBJECT - Page object pattern (4 strategies)
- E2E-FLAKY - Preventing flaky E2E tests
- E2E-DATA - Test data management

**Key Resources:**
- "Best Practices" - https://docs.cypress.io/guides/references/best-practices
- "Custom Commands" - https://docs.cypress.io/api/cypress-api/custom-commands
- "Organizing Tests" - https://docs.cypress.io/guides/core-concepts/writing-and-organizing-tests

---

### 8. Mock Service Worker (MSW)

- **Official URL:** https://mswjs.io/
- **Used for:** Network-level API mocking
- **License:** MIT License
- **Maintainer:** Artem Zakharchenko

**Key Features:**
- Network-level interception
- Works with any HTTP client
- Reusable between Node and browser
- REST and GraphQL support

**Philosophy:**
> "Stop mocking fetch. Intercept requests on the network level."

**Relevant Guidelines:**
- MOCK-API - API mocking strategies (MSW recommended)
- MOCK-MSW - Dedicated MSW patterns

**Key Resources:**
- "Getting Started" - https://mswjs.io/docs/getting-started
- "Recipes" - https://mswjs.io/docs/recipes

**Why MSW:**
- More realistic than mocking fetch/axios
- Tests work with real HTTP stack
- Can share handlers with browser
- Doesn't pollute global namespace

---

### 9. Mocha Documentation

- **Official URL:** https://mochajs.org/
- **Used for:** Flexible test organization, async patterns
- **License:** MIT License

**Key Topics:**
- Flexible test organization
- Async testing patterns
- Hooks (before, after, beforeEach, afterEach)
- Timeouts and retries

**Relevant Guidelines:**
- TEST-DESCRIBE - Test organization
- TEST-SETUP - beforeEach/afterEach patterns
- ASYNC-CALLBACK - Callback-based async testing

---

### 10. jest-dom Library

- **Repository:** https://github.com/testing-library/jest-dom
- **Maintainer:** Testing Library team
- **License:** MIT License
- **Used for:** Custom DOM matchers

**Custom Matchers:**
- toBeInTheDocument()
- toBeVisible()
- toHaveTextContent()
- toHaveClass()
- toBeDisabled()
- toHaveAttribute()

**Relevant Guidelines:**
- ASSERT-DOM - DOM assertions
- COMP-RENDER - Component rendering assertions

---

## Research Process

### Web Searches Performed
1. **"Jest best practices official documentation 2025"** - Found Jest docs, patterns
2. **"Testing Library principles Kent C Dodds"** - Located Testing Library philosophy
3. **"JavaScript testing strategies patterns 2025"** - Yoni Goldberg's guide
4. **"React Testing Library vs Enzyme comparison"** - User-centric vs implementation testing
5. **"MSW Mock Service Worker examples patterns"** - API mocking best practices
6. **"Cypress E2E testing best practices page object pattern"** - E2E organization
7. **"Jest mock module examples strategies"** - Module mocking patterns
8. **"userEvent vs fireEvent Testing Library"** - User interaction patterns
9. **"JavaScript test pyramid Martin Fowler"** - Test level balance

### Methodology
1. **Identify authoritative sources** - Jest, Testing Library, Kent C. Dodds, Martin Fowler
2. **Research multiple approaches** - Not just one "right" way
3. **Gather complete examples** - Full, runnable code for Jest, Vitest, Testing Library
4. **Understand trade-offs** - Pros/cons of each approach
5. **Focus on user-centric testing** - Testing Library principles
6. **Prioritize quality over coverage** - Meaningful tests over percentages

---

## Guideline Structure

Each guideline follows this format:

### Code to Test
Shows the production code FIRST, so readers understand what's being tested.

### Multiple Strategies (2-4 per guideline)
Each strategy includes:
- **Complete, runnable test code** (Jest/Vitest/Testing Library)
- **Pros** - Benefits of this approach
- **Cons** - Drawbacks and limitations
- **When to use** - Specific scenarios

### Trade-offs
Explicit comparison of when to use each strategy.

### Recommendation
Best practice guidance based on authoritative sources (Testing Library, Jest docs, Kent C. Dodds).

---

## Key Differentiators from Other Testing Guides

### 1. User-Centric Focus
Based on Testing Library principles:
- Test behavior users care about
- Query by accessibility (role, label)
- Use userEvent for realistic interactions
- Avoid implementation details

### 2. Multiple Strategies with Trade-offs
Most testing guides show one approach. This skill shows 2-4 alternatives with:
- Complete examples
- Pros and cons
- When to use each
- Recommendations

**Example:**
- MOCK-API shows 4 strategies: jest.fn(), MSW, axios-mock-adapter, fetch-mock
- Each with complete code, pros/cons, and recommendation (MSW for most cases)

### 3. Modern Patterns
- async/await (not callbacks)
- userEvent (not fireEvent)
- MSW (not fetch mocking)
- Testing Library (not Enzyme)
- Vitest (modern alternative to Jest)

### 4. Framework Coverage
Covers all major tools:
- Jest (most popular)
- Vitest (modern, fast)
- Testing Library (user-centric)
- Cypress (E2E)
- MSW (API mocking)

### 5. Quality Over Coverage
Emphasizes meaningful tests over coverage percentage:
- Behavior over implementation
- User perspective
- Edge cases and error paths
- Mutation testing concepts

---

## Mnemonic ID Convention

All guidelines use category-based prefixes:
- **TEST-** - Test structure and organization
- **ASSERT-** - Assertions and matchers
- **MOCK-** - Mocking and stubbing
- **ASYNC-** - Async testing
- **COMP-** - Component testing
- **E2E-** - End-to-end testing
- **QUALITY-** - Test quality

Format: `CATEGORY-KEYWORD`
Examples: `TEST-AAA`, `MOCK-API`, `COMP-QUERY`, `E2E-PAGE-OBJECT`

---

## Code Example Attribution

All code examples were:
1. **Inspired by** authoritative sources listed above
2. **Adapted for modern JavaScript/TypeScript** - ES6+, async/await, Testing Library
3. **Created as original examples** - Demonstrating specific testing strategies
4. **Structured for education** - Production code → Multiple test strategies → Trade-offs

### Example Pattern:
- **Production Code:** Original, demonstrating testing challenge
- **Test Strategies:** Inspired by Jest docs, Testing Library, Kent C. Dodds, community patterns
- **Trade-offs:** Based on real-world testing experience and authoritative guidance

---

## Testing Philosophy Sources

### "Test Behavior, Not Implementation"
- **Source:** Kent C. Dodds, Testing Library
- **Principle:** Tests should verify what code does from user's perspective
- **Applied in:** COMP-NO-IMPL, COMP-QUERY, TEST-COMPONENT

### "Write Tests. Not Too Many. Mostly Integration."
- **Source:** Kent C. Dodds (inspired by Guillermo Rauch)
- **Principle:** Balance unit, integration, and E2E tests
- **Applied in:** E2E-WHEN, MOCK-MINIMAL, TEST-INTEGRATION

### "The Test Pyramid"
- **Source:** Martin Fowler, Mike Cohn
- **Principle:** Many unit tests, fewer integration, few E2E
- **Applied in:** E2E-WHEN guideline

### "Query Priority"
- **Source:** Testing Library documentation
- **Principle:** role > label > placeholder > text > test-id
- **Applied in:** COMP-QUERY guideline

### "Use userEvent, Not fireEvent"
- **Source:** Testing Library, Kent C. Dodds
- **Principle:** Realistic user interactions
- **Applied in:** COMP-USER-EVENT guideline

### "Quality Over Coverage"
- **Source:** Testing community consensus
- **Principle:** 100% coverage ≠ 100% tested
- **Applied in:** QUALITY-COVERAGE guideline

---

## Tools and Frameworks Referenced

### Test Runners
- **Jest** - Most popular (MIT License)
- **Vitest** - Vite-native, fast (MIT License)
- **Mocha** - Flexible, minimalist (MIT License)

### Component Testing
- **Testing Library** (@testing-library/react, @testing-library/vue) - MIT License
- **Enzyme** (deprecated, avoid) - User-centric approach preferred

### E2E Testing
- **Cypress** - Developer-friendly (MIT License)
- **Playwright** - Modern, cross-browser (Apache 2.0)

### Mocking
- **jest.mock** - Built-in Jest mocking
- **MSW** (Mock Service Worker) - Network-level mocking (MIT License)
- **jest-fetch-mock** - Fetch-specific mocking (MIT License)
- **axios-mock-adapter** - Axios-specific mocking (MIT License)

### Assertion Libraries
- **jest-dom** - Custom DOM matchers (MIT License)
- **Chai** - BDD/TDD assertion library (MIT License)

### User Interactions
- **@testing-library/user-event** - Realistic user interactions (MIT License)

---

## Verification

All guidelines were verified against:
1. ✅ Jest official documentation
2. ✅ Testing Library documentation and guiding principles
3. ✅ Vitest official documentation
4. ✅ Kent C. Dodds' testing articles and courses
5. ✅ Martin Fowler's testing articles
6. ✅ Yoni Goldberg's JavaScript Testing Best Practices
7. ✅ Cypress best practices documentation
8. ✅ MSW documentation and examples
9. ✅ Real-world usage patterns in open-source projects

---

## Updates and Maintenance

- **Version:** 1.0
- **Created:** November 2025
- **Last Updated:** November 2025
- **JavaScript Compatibility:** ES6+, modern async/await
- **Framework Versions:**
  - Jest 29+
  - Vitest 1.0+
  - Testing Library (React 14+, Vue 6+)
  - Cypress 13+
  - MSW 2.0+

**Future Updates May Include:**
- Additional E2E testing patterns (Playwright)
- More advanced MSW patterns
- Testing patterns for newer React features (Server Components)
- Vue 3 Composition API testing patterns
- Svelte testing strategies

---

## Acknowledgments

Special thanks to:
- **Kent C. Dodds** - For Testing Library and testing philosophy
- **Jest Team** - For excellent documentation and framework
- **Vitest Team** (Anthony Fu and contributors) - For modern testing innovation
- **Testing Library Team** - For user-centric testing principles
- **Martin Fowler** - For testing principles and test doubles taxonomy
- **Yoni Goldberg** - For comprehensive JavaScript testing best practices
- **Cypress Team** - For E2E testing best practices
- **Artem Zakharchenko** - For MSW library and documentation
- **JavaScript Testing Community** - For establishing best practices

---

## Anti-Patterns Explicitly Avoided

This skill teaches developers to AVOID:

### 1. Enzyme / Shallow Rendering
- **Why avoided:** Tests implementation details (state, props)
- **What to use instead:** Testing Library with user-centric queries
- **Guideline:** COMP-NO-IMPL

### 2. fireEvent
- **Why avoided:** Unrealistic, doesn't trigger all events
- **What to use instead:** userEvent for realistic interactions
- **Guideline:** COMP-USER-EVENT

### 3. Test IDs as Primary Query
- **Why avoided:** Implementation detail, not accessible
- **What to use instead:** Query by role, label, text
- **Guideline:** COMP-QUERY

### 4. Over-Mocking Internal Methods
- **Why avoided:** Tests implementation, brittle
- **What to use instead:** Mock at boundaries only
- **Guideline:** MOCK-MINIMAL

### 5. done Callbacks for Async
- **Why avoided:** Legacy, error-prone, verbose
- **What to use instead:** async/await
- **Guideline:** ASYNC-AWAIT

### 6. Coverage-Focused Testing
- **Why avoided:** 100% coverage ≠ quality tests
- **What to use instead:** Behavior-focused, meaningful assertions
- **Guideline:** QUALITY-COVERAGE

---

## Real-World Examples Referenced

While creating examples, consulted:
- React Testing Library examples repository
- Jest example projects
- Vitest example projects
- Open-source projects on GitHub (React, Vue, Next.js)
- Testing Library community examples
- Kent C. Dodds' blog examples

All examples were then:
1. Simplified for clarity
2. Made self-contained
3. Annotated with explanations
4. Structured to show multiple approaches

---

## Legal and Attribution

### Official Documentation
- **Jest, Vitest, Testing Library, Cypress, MSW:** Open source licenses (MIT)
- **Usage:** Freely referenceable for educational purposes

### Published Articles and Resources
- **Kent C. Dodds' articles:** Public articles, freely quotable with attribution
- **Martin Fowler's articles:** Public articles, freely quotable with attribution
- **Yoni Goldberg's guide:** MIT licensed, GitHub repository

### Code Examples
- **Original examples:** Created for this skill
- **Inspired by:** Authoritative sources listed above
- **Skill license:** MIT

---

## Testing Principles Summary

This skill emphasizes:

1. **User-Centric Testing** - Test from user's perspective
2. **Query Priority** - role > label > text > test-id
3. **userEvent** - Realistic user interactions
4. **async/await** - Modern async testing
5. **Minimal Mocking** - Mock at boundaries
6. **Test Pyramid** - Balance unit/integration/E2E
7. **Quality over Coverage** - Meaningful over percentage
8. **Avoid Implementation Details** - Test behavior, not internals

All based on Testing Library, Kent C. Dodds, Jest documentation, and modern JavaScript testing best practices.

---

**Note:** This skill prioritizes teaching testing strategies and user-centric approaches based on Testing Library principles. The goal is to help developers write tests that give confidence and survive refactoring.

---

**Created:** November 2025
**Last Updated:** November 2025
**Skill Version:** 1.0
**Focus:** User-centric testing, quality over coverage, multiple strategies with trade-offs
