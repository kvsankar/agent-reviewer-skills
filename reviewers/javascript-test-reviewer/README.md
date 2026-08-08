# JavaScript Test Reviewer Skill

A Claude Code skill that reviews JavaScript/TypeScript tests for quality and suggests multiple testing strategies for different scenarios. **Quality over coverage** - shows detailed approaches for Jest, Vitest, Testing Library, and more.

## What This Skill Does

This skill transforms Claude into a JavaScript testing expert who:
- **Shows multiple testing strategies** for the same code (not just one "right" way)
- **Explains trade-offs** between different approaches (Jest vs Vitest, enzyme vs Testing Library)
- **Provides complete, runnable examples** for each strategy
- **Teaches user-centric testing** - focus on behavior, not implementation
- **Reviews for test quality** - not just coverage percentage
- **Identifies test anti-patterns** and suggests fixes

## Philosophy

> **"Write tests. Not too many. Mostly integration."** - Kent C. Dodds

> **"The more your tests resemble the way your software is used, the more confidence they can give you."** - Testing Library

The skill compares JavaScript-specific strategies—unit tests, component tests,
network-level interception, and browser tests—so the recommendation reflects
the confidence and runtime cost appropriate to the behavior.

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## How to Use

Simply ask Claude to review your tests or suggest testing strategies:

```
"Review these Jest tests for quality"
"Show me different ways to test this React component"
"How should I test this async function?"
"What testing strategies work for this API call?"
"Review test coverage - am I testing the right things?"
```

The skill will automatically activate based on keywords like:
- test review, testing strategies
- Jest, Vitest, test quality, test coverage
- React testing, component tests
- Testing Library, Cypress
- mocking, async tests, E2E tests

## What You'll Get

A comprehensive test review with:
- **Code to Test** - Shows the production code first
- **Multiple Strategies** - 2-4 different testing approaches
- **Complete Examples** - Full, runnable test code for each strategy (Jest, Vitest, Testing Library)
- **Trade-offs** - Pros and cons of each approach
- **Recommendations** - When to use each strategy

### Example Review

````markdown
## Test Review: LoginForm Component

### TEST-COMPONENT: Testing React Components

**Code to test:**
```jsx
function LoginForm({ onSubmit }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Email and password are required');
      return;
    }
    onSubmit({ email, password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" placeholder="Email" value={email}
        onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" value={password}
        onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Login</button>
      {error && <div role="alert">{error}</div>}
    </form>
  );
}
```

**Strategy 1: Testing Library (User-Centric)**
```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits email and password', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByPlaceholderText('Email'), 'test@example.com');
  await user.type(screen.getByPlaceholderText('Password'), 'password123');
  await user.click(screen.getByRole('button', { name: 'Login' }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123'
  });
});
```
**Pros:** Tests user behavior, resilient to refactoring, finds accessibility issues
**Cons:** Requires understanding Testing Library principles

**Strategy 2: Enzyme (Avoid - Implementation-Focused)**
```javascript
// DON'T DO THIS - Tests implementation details
const wrapper = shallow(<LoginForm />);
wrapper.find('input[type="email"]').simulate('change', { target: { value: 'test' } });
expect(wrapper.state('email')).toBe('test'); // ❌ Tests state, not behavior
```
**Why this is bad:** Tests implementation (state), breaks when refactoring to hooks, doesn't test UX

**Recommendation:**
Use Testing Library (Strategy 1) with user-centric queries and userEvent. Test from the user's perspective, not implementation details.
````

## The 55+ Guidelines

### Test Structure & Organization (6)
- **TEST-AAA** - The Arrange-Act-Assert pattern (3 strategies)
- **TEST-NAMING** - Descriptive test names that survive refactoring
- **TEST-DESCRIBE** - Effective test organization with describe blocks
- **TEST-SETUP** - beforeEach, afterEach, and test lifecycle
- **TEST-ISOLATION** - Ensuring tests don't affect each other
- **TEST-FILE-LOCATION** - Co-located vs __tests__ folders

### Testing Strategies for Different Scenarios (7)
- **TEST-PURE-FUNC** - Testing pure functions (3 strategies: simple, test.each, grouped)
- **TEST-COMPONENT** - Testing React/Vue components (user-centric vs implementation)
- **TEST-HOOK** - Testing custom React hooks
- **TEST-ASYNC** - Testing async code (4 strategies: async/await, promises, callbacks, resolves/rejects)
- **TEST-ERROR** - Testing error paths and exceptions
- **TEST-EVENT** - Testing DOM events and user interactions
- **TEST-INTEGRATION** - Integration vs unit testing

### Assertions & Matchers (6)
- **ASSERT-EQUALITY** - toBe vs toEqual vs toStrictEqual vs toMatchObject
- **ASSERT-DOM** - DOM assertions with jest-dom matchers
- **ASSERT-ASYNC** - Async assertions (resolves, rejects, waitFor)
- **ASSERT-SNAPSHOT** - Snapshot testing (when and how)
- **ASSERT-CUSTOM** - Custom matchers for domain logic
- **ASSERT-NEGATIVE** - Testing what should NOT happen

### Mocking & Stubbing (10)
- **MOCK-MODULE** - Mocking ES6 modules (4 strategies)
- **MOCK-FUNCTION** - jest.fn() and mock functions
- **MOCK-API** - Mocking HTTP APIs (4 strategies: fetch mock, MSW, axios mock, manual)
- **MOCK-TIMER** - Mocking timers and dates
- **MOCK-PARTIAL** - Partial module mocks
- **MOCK-CLEAR** - Clearing and resetting mocks
- **MOCK-MINIMAL** - Avoid over-mocking (4 strategies showing pitfalls)
- **MOCK-MSW** - Mock Service Worker for realistic API mocking
- **MOCK-SPY** - Spying on real implementations
- **MOCK-IMPLEMENTATION** - Custom mock implementations

### Async Testing (6)
- **ASYNC-AWAIT** - async/await pattern (recommended)
- **ASYNC-PROMISE** - Testing promises with .then()
- **ASYNC-CALLBACK** - Testing callback-based code
- **ASYNC-WAITFOR** - Testing Library's waitFor
- **ASYNC-ERROR** - Testing async error handling
- **ASYNC-TIMEOUT** - Configuring timeouts

### Component Testing (React/Vue) (8)
- **COMP-RENDER** - Rendering components with Testing Library
- **COMP-QUERY** - Query priority (role > label > text > test-id)
- **COMP-USER-EVENT** - userEvent vs fireEvent
- **COMP-ACCESSIBILITY** - Testing accessibility
- **COMP-PROPS** - Testing props and prop validation
- **COMP-STATE** - Testing stateful components (avoid testing state directly)
- **COMP-CONTEXT** - Testing React Context
- **COMP-NO-IMPL** - Avoiding implementation details

### E2E Testing (6)
- **E2E-WHEN** - When to use E2E tests (test pyramid)
- **E2E-PAGE-OBJECT** - Page Object pattern (4 strategies)
- **E2E-DATA** - Test data management
- **E2E-FLAKY** - Preventing flaky E2E tests
- **E2E-PARALLEL** - Parallel execution
- **E2E-VISUAL** - Visual regression testing

### Test Quality (6)
- **QUALITY-DETERMINISTIC** - Avoiding flaky tests (4 anti-patterns with fixes)
- **QUALITY-FAST** - Keeping tests fast
- **QUALITY-INDEPENDENT** - Test independence
- **QUALITY-MAINTAINABLE** - Maintainable tests
- **QUALITY-COVERAGE** - Coverage vs test quality (behavior over coverage)
- **QUALITY-MUTATION** - Mutation testing for test quality

## Key Differentiators

### Shows MULTIPLE Strategies

Unlike other testing guides that show one "right" way, this skill shows 2-4 different approaches for each testing scenario:

**Example: Testing Async Code**
1. async/await (recommended)
2. return Promise
3. done callback (legacy)
4. resolves/rejects matchers

Each with complete code, pros/cons, and when to use it.

### Complete, Runnable Examples

Every example shows:
- The production code being tested
- Complete test code (not just snippets)
- Full imports and setup (Jest, Vitest, Testing Library)
- Actual assertions with modern matchers

### Trade-Off Analysis

For each scenario, it explains framework fit, isolation level, execution cost,
and whether Jest/Vitest, Testing Library, MSW, or a browser runner provides the
most credible evidence.

### Framework Coverage

Covers all major JavaScript testing tools:
- **Jest** - Most popular, zero-config
- **Vitest** - Vite-native, fast
- **Mocha** - Flexible, minimalist
- **Testing Library** - User-centric component testing
- **Cypress** - E2E testing
- **Playwright** - Modern E2E alternative

### Authoritative Sources

Based on:
- **Jest Documentation** - Official best practices
- **Testing Library** - Guiding principles (Kent C. Dodds)
- **Vitest Documentation** - Modern testing patterns
- **Martin Fowler** - Testing principles, test doubles
- **Kent C. Dodds** - Testing JavaScript, Common Testing Mistakes
- **JavaScript Testing Best Practices** - Yoni Goldberg's comprehensive guide

## Testing Philosophy

### Test Behavior, Not Implementation

> "The more your tests resemble the way your software is used, the more confidence they can give you." - Testing Library

Don't test state, props, or internal methods. Test what the user sees and does.

### User-Centric Testing

Query elements the way users do:
- **Priority 1:** Accessible queries (getByRole, getByLabelText)
- **Priority 2:** User-visible text (getByText)
- **Priority 3:** Test IDs (last resort)

This approach tests accessibility and creates resilient tests.

### Quality Over Coverage

Don't chase 100% coverage. Write tests that would fail if the code was broken in important ways.

### Multiple Strategies for Different Needs

No single testing approach fits all scenarios. Learn when to use:
- Jest vs Vitest vs Mocha
- Testing Library vs Enzyme (avoid Enzyme)
- Unit vs Integration vs E2E tests
- Mocks vs Real implementations

### Test Pyramid

- **70% Unit Tests** - Fast, focused, many
- **20% Integration Tests** - Medium speed, fewer
- **10% E2E Tests** - Slow, high confidence, few

## Example Use Cases

### Reviewing Existing Tests
- "Review these Jest tests - are they testing the right things?"
- "This test is flaky, help me fix it"
- "Are my assertions strong enough?"

### Learning Testing Strategies
- "Show me different ways to test this React component"
- "When should I use MSW vs mocking fetch?"
- "How do I test this async function with error handling?"

### Improving Test Quality
- "How can I make this component test less coupled to markup?"
- "Why is this Vitest suite slow?"
- "Which browser and async edge cases are missing?"

### Framework Migration
- "Help me migrate from Enzyme to Testing Library"
- "Convert these Jest tests to Vitest"
- "Modernize these tests to use async/await"

## Benefits

- ✓ **Learn testing strategies** - See multiple approaches with trade-offs
- ✓ **Write better tests** - Quality-focused, user-centric
- ✓ **Make informed decisions** - Understand when to use which framework/approach
- ✓ **Complete examples** - Copy-paste-ready test code
- ✓ **Avoid anti-patterns** - Learn what NOT to do (Enzyme, over-mocking)
- ✓ **Authoritative guidance** - Based on Testing Library, Kent C. Dodds, Jest docs
- ✓ **Modern patterns** - async/await, userEvent, MSW
- ✓ **Framework coverage** - Jest, Vitest, Testing Library, Cypress

## What Gets Checked

### Test Structure
- AAA (Arrange-Act-Assert) pattern clarity
- Test naming conventions (behavior vs implementation)
- Test organization (describe blocks)
- Setup/teardown patterns

### Test Quality
- Strong vs weak assertions (toBe vs toEqual vs toStrictEqual)
- User behavior vs implementation details
- Test isolation and independence
- Edge case coverage

### Testing Strategies
- Appropriate testing level (unit vs integration vs E2E)
- Query priority (role > label > text > test-id)
- userEvent vs fireEvent
- async/await vs promises
- Mock vs real dependencies

### Test Completeness
- Happy path and error path coverage
- Async handling
- User interactions
- Accessibility

### Test Maintainability
- Test readability and clarity
- Mock management (setup, cleanup)
- Test speed and performance
- Avoiding flaky tests (time, randomness, order)

## Supported Frameworks

### Test Runners
- **Jest** - Most popular, zero-config, great ecosystem
- **Vitest** - Vite-native, extremely fast, Jest-compatible API
- **Mocha** - Flexible, minimalist, bring your own assertion library

### Component Testing
- **Testing Library** (@testing-library/react, @testing-library/vue)
- Avoid Enzyme (implementation-focused, deprecated)

### E2E Testing
- **Cypress** - Developer-friendly E2E testing
- **Playwright** - Modern, cross-browser E2E testing

### Mocking
- **jest.mock** - Built-in Jest mocking
- **MSW** (Mock Service Worker) - Network-level API mocking
- **jest-fetch-mock** - Fetch-specific mocking
- **axios-mock-adapter** - Axios-specific mocking

## Sources and Attribution

All guidelines are based on:
- **Jest Documentation** - [jestjs.io](https://jestjs.io/)
- **Vitest Documentation** - [vitest.dev](https://vitest.dev/)
- **Testing Library** - [testing-library.com](https://testing-library.com/)
- **Kent C. Dodds** - Testing JavaScript, Common Testing Mistakes
- **Martin Fowler** - Test Pyramid, Mocks Aren't Stubs
- **Yoni Goldberg** - JavaScript Testing Best Practices
- **Cypress Documentation** - [cypress.io](https://www.cypress.io/)

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## Common Patterns This Skill Teaches

### ✅ Do This
```javascript
// User-centric component testing
test('submits form when valid', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByRole('textbox', { name: 'Email' }), 'test@example.com');
  await user.type(screen.getByLabelText('Password'), 'password');
  await user.click(screen.getByRole('button', { name: 'Login' }));

  expect(onSubmit).toHaveBeenCalledWith({ email: 'test@example.com', password: 'password' });
});
```

### ❌ Not This
```javascript
// Implementation-focused testing
test('updates email state on change', () => {
  const wrapper = shallow(<LoginForm />);
  wrapper.find('input[type="email"]').simulate('change', { target: { value: 'test' } });
  expect(wrapper.state('email')).toBe('test'); // Tests implementation!
});
```

### ✅ Do This
```javascript
// Async testing with async/await
test('fetches user data', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ id: 1, name: 'John' })
  });

  const user = await fetchUser(1);

  expect(user).toEqual({ id: 1, name: 'John' });
});
```

### ❌ Not This
```javascript
// Async testing without proper waiting
test('fetches user data', () => {
  fetchUser(1); // Not awaited!
  expect(user).toEqual({ id: 1, name: 'John' }); // Flaky!
});
```

### ✅ Do This
```javascript
// Mock at boundary
test('processes payment', async () => {
  const mockApi = { charge: jest.fn().mockResolvedValue({ success: true }) };
  const service = new PaymentService(mockApi);

  await service.processPayment(100, 'credit');

  expect(mockApi.charge).toHaveBeenCalledWith(100, 'credit');
});
```

### ❌ Not This
```javascript
// Over-mocking internal methods
test('processes payment', async () => {
  const service = new PaymentService(api);
  jest.spyOn(service, 'validateCard').mockReturnValue(true); // Don't mock internals!
  // ...
});
```

## Tips for Getting the Most Out of This Skill

1. **Ask for specific scenarios**: "How do I test this async function?" is better than "Review my tests"
2. **Include your code**: Paste both production code and existing tests for better feedback
3. **Specify your framework**: Mention Jest, Vitest, Testing Library, etc.
4. **Ask about trade-offs**: "What are the pros and cons of mocking vs using real API?"
5. **Request comparisons**: "Show me Testing Library vs Enzyme for this component"

## License

This skill is licensed under MIT. It is based on public documentation, established testing principles, and community best practices.

---

**Quality over coverage. Behavior over implementation. User-centric over implementation-focused.**
