# Expected Good Patterns (Check for Absence)

Beyond flagging test issues, check whether **expected testing patterns are missing**. The absence of good practices is itself a finding.

Based on [Common mistakes with React Testing Library](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library), [Testing Library query documentation](https://testing-library.com/docs/queries/about/), [Node.js Testing Best Practices](https://github.com/goldbergyoni/nodejs-testing-best-practices), and [Infinum Frontend Handbook](https://infinum.com/handbook/frontend/react/testing/best-practices).

## How to Use This Section

When reviewing tests, check if these patterns are present. If missing, flag using the mnemonic ID:
- **🔴 Critical** - Missing pattern creates significant test quality issues
- **⚠️ Warning** - Missing pattern weakens test reliability
- **💡 Recommendation** - Missing pattern is best practice

---

## Testing Library Queries (React/DOM)

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-GETBYROLE** | `getByRole` as primary query method | Tests don't reflect accessibility |
| **MISSING-ACCESSIBLE-NAME** | `getByRole('button', { name: /submit/i })` | Queries too broad or fragile |
| **MISSING-SCREEN** | Use `screen.getByRole()` not destructured queries | Inconsistent query access |
| **MISSING-FINDBY-ASYNC** | `findBy*` for async elements (not `waitFor` + `getBy`) | Worse error messages, slower |
| **MISSING-QUERYBY-ABSENCE** | `queryBy*` only for non-existence assertions | Wrong query type for presence |

**What to look for:**
```typescript
// PRESENT: Proper query priority (from Testing Library docs)
// 1. Accessible queries (best)
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText(/email/i);
screen.getByPlaceholderText(/enter name/i);
screen.getByText(/welcome/i);

// 2. Semantic queries
screen.getByAltText(/profile/i);

// 3. Test IDs (last resort)
screen.getByTestId('custom-element');

// PRESENT: findBy for async
const submitButton = await screen.findByRole('button', { name: /submit/i });

// PRESENT: queryBy only for non-existence
expect(screen.queryByRole('alert')).not.toBeInTheDocument();
```

**Attribution:** [Testing Library Query Priority](https://testing-library.com/docs/queries/about/)

---

## User Event Over FireEvent

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-USEREVENT** | `userEvent.click()` over `fireEvent.click()` | Less realistic user simulation |
| **MISSING-USEREVENT-TYPE** | `userEvent.type()` over `fireEvent.change()` | Missing keyDown/keyUp events |
| **MISSING-USEREVENT-SETUP** | `const user = userEvent.setup()` before interactions | Performance issues, missing setup |
| **MISSING-AWAIT-USEREVENT** | `await user.click()` (userEvent is async) | Race conditions in tests |

**What to look for:**
```typescript
// PRESENT: Proper userEvent usage
import userEvent from '@testing-library/user-event';

test('form submission', async () => {
  const user = userEvent.setup();

  render(<LoginForm />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /sign in/i }));

  expect(await screen.findByText(/welcome/i)).toBeInTheDocument();
});

// MISSING: fireEvent doesn't simulate real user behavior
fireEvent.change(input, { target: { value: 'text' } }); // No keyboard events!
```

**Attribution:** [Kent C. Dodds - Common Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

## Test Structure & Naming

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-AAA-COMMENTS** | Clear Arrange/Act/Assert sections | Tests hard to read |
| **MISSING-DESCRIBE-WHEN** | Nested `describe('when ...')` for scenarios | Flat, unorganized tests |
| **MISSING-IT-SHOULD** | `it('should ...')` describing behavior | Unclear test intent |
| **MISSING-SINGLE-ASSERT** | One logical assertion per test | Tests fail for multiple reasons |
| **MISSING-BEHAVIOR-NAME** | Names describe behavior, not implementation | "tests handleClick" vs "submits form" |

**What to look for:**
```typescript
// PRESENT: Proper test organization (from Infinum Handbook)
describe('useAuth', () => {
  it('should throw context error when used outside provider', () => { });

  describe('when user exists', () => {
    it('should return user object with profile data', () => { });
    it('should return isAuthenticated as true', () => { });
  });

  describe('when user does not exist', () => {
    it('should return guest user', () => { });
    it('should return isAuthenticated as false', () => { });
  });
});
```

**Attribution:** [Infinum Frontend Handbook](https://infinum.com/handbook/frontend/react/testing/best-practices)

---

## Assertions & Matchers

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-JEST-DOM** | `@testing-library/jest-dom` matchers | Poor DOM assertions |
| **MISSING-TOBEINDOM** | `toBeInTheDocument()` for presence | Using `toBeTruthy()` on elements |
| **MISSING-TOHAVEATTR** | `toHaveAttribute()`, `toHaveClass()` | Manual attribute checking |
| **MISSING-TOBEDISABLED** | `toBeDisabled()`, `toBeEnabled()` | `expect(el.disabled).toBe(true)` |
| **MISSING-EXPLICIT-ASSERT** | Explicit assertions after queries | `getByRole` without `expect()` |

**What to look for:**
```typescript
// PRESENT: jest-dom matchers
import '@testing-library/jest-dom';

expect(screen.getByRole('button')).toBeDisabled();
expect(screen.getByRole('alert')).toHaveTextContent(/error/i);
expect(screen.getByRole('link')).toHaveAttribute('href', '/home');
expect(screen.getByRole('checkbox')).toBeChecked();

// PRESENT: Explicit assertion (not just query)
const alert = screen.getByRole('alert');
expect(alert).toBeInTheDocument(); // Explicit, clear intent

// MISSING: Implicit assertion (confusing)
screen.getByRole('alert'); // Does this assert existence?
```

**Attribution:** [Kent C. Dodds - Common Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

## Async Testing Patterns

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-WAITFOR-ASSERT** | Assertions inside `waitFor` callback | Assertions outside miss retries |
| **MISSING-SINGLE-WAITFOR** | One assertion per `waitFor` | Slow failure on first assertion |
| **MISSING-NO-SIDE-EFFECTS** | No `fireEvent` inside `waitFor` | Side effects called multiple times |
| **MISSING-FINDBY-PREFER** | `findBy*` over `waitFor` + `getBy*` | Worse error messages |

**What to look for:**
```typescript
// PRESENT: Proper waitFor usage
await waitFor(() => {
  expect(screen.getByRole('alert')).toHaveTextContent('Success');
});

// PRESENT: findBy for appearing elements
const successMessage = await screen.findByText(/success/i);
expect(successMessage).toBeInTheDocument();

// MISSING: Empty waitFor (assertions outside)
await waitFor(() => {}); // Does nothing!
expect(screen.getByText('Success')).toBeInTheDocument();

// MISSING: Side effects in waitFor (gets called multiple times!)
await waitFor(() => {
  fireEvent.click(button); // BAD: clicked many times!
  expect(result).toBe('done');
});
```

**Attribution:** [Kent C. Dodds - Common Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

## Test Isolation & Setup

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-AUTO-CLEANUP** | No manual `cleanup()` calls | Outdated pattern, already automatic |
| **MISSING-MOCK-RESET** | `vi.resetAllMocks()` or `jest.resetAllMocks()` in beforeEach | Mock state leaks between tests |
| **MISSING-SETUP-RENDER** | Render in test or beforeEach, not module scope | Shared component state |
| **MISSING-MOCK-TIMERS** | `vi.useFakeTimers()` for time-dependent tests | Flaky tests |
| **MISSING-DETERMINISTIC** | Seeded random, mocked Date.now() | Non-reproducible failures |

**What to look for:**
```typescript
// PRESENT: Proper test isolation
beforeEach(() => {
  vi.resetAllMocks();
});

// PRESENT: Fake timers for time-dependent code
beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2024-01-15'));
});

afterEach(() => {
  vi.useRealTimers();
});

// MISSING: Manual cleanup (automatic since RTL v9)
import { cleanup } from '@testing-library/react';
afterEach(cleanup); // Unnecessary!
```

---

## Mocking Best Practices

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-MOCK-BOUNDARY** | Mock at system boundaries (API, timers) | Mocking internal modules |
| **MISSING-MSW** | MSW for API mocking | Manual fetch mocking |
| **MISSING-MOCK-IMPL** | `mockImplementation` when behavior matters | Only `mockReturnValue` |
| **MISSING-SPY-RESTORE** | `vi.spyOn().mockRestore()` or auto-restore | Spy leaks to other tests |
| **MISSING-MOCK-TYPES** | Type-safe mocks with proper inference | `as any` casts everywhere |

**What to look for:**
```typescript
// PRESENT: MSW for API mocking (from goldbergyoni best practices)
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Test User' });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// PRESENT: Mock at boundary, not internal
vi.mock('./api/client'); // OK: boundary module

// MISSING: Mocking internal implementation details
vi.mock('./utils/formatDate'); // Bad: internal utility
```

**Attribution:** [Node.js Testing Best Practices](https://github.com/goldbergyoni/nodejs-testing-best-practices)

---

## ESLint Plugins

| Mnemonic | Expected Pattern | If Missing |
|----------|------------------|------------|
| **MISSING-ESLINT-RTL** | `eslint-plugin-testing-library` configured | Common RTL mistakes not caught |
| **MISSING-ESLINT-JEST** | `eslint-plugin-jest` or `eslint-plugin-vitest` | Test anti-patterns not caught |
| **MISSING-ESLINT-JESTDOM** | `eslint-plugin-jest-dom` configured | DOM assertion mistakes |

**What to look for:**
```javascript
// PRESENT: ESLint config with testing plugins
// eslint.config.js
export default [
  {
    plugins: {
      'testing-library': testingLibraryPlugin,
      'jest-dom': jestDomPlugin,
    },
    rules: {
      'testing-library/prefer-screen-queries': 'error',
      'testing-library/prefer-user-event': 'error',
      'testing-library/no-wait-for-multiple-assertions': 'error',
      'jest-dom/prefer-to-have-attribute': 'error',
    },
  },
];
```

**Attribution:** [Kent C. Dodds - Common Mistakes](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

## Expected Good Patterns Checklist

Quick reference for absence checks:

### 🔴 Critical (Must Have)
- [ ] **MISSING-GETBYROLE** - Using `getByRole` as primary query
- [ ] **MISSING-USEREVENT** - Using userEvent over fireEvent
- [ ] **MISSING-WAITFOR-ASSERT** - Assertions inside waitFor callbacks
- [ ] **MISSING-MOCK-BOUNDARY** - Mocking at system boundaries
- [ ] **MISSING-DETERMINISTIC** - Tests are deterministic

### ⚠️ Warning (Should Have)
- [ ] **MISSING-SCREEN** - Using `screen` object for queries
- [ ] **MISSING-JEST-DOM** - jest-dom matchers configured
- [ ] **MISSING-DESCRIBE-WHEN** - Organized describe blocks
- [ ] **MISSING-FINDBY-ASYNC** - findBy for async elements
- [ ] **MISSING-MOCK-RESET** - Mocks reset between tests

### 💡 Recommendation (Nice to Have)
- [ ] **MISSING-MSW** - MSW for API mocking
- [ ] **MISSING-ESLINT-RTL** - Testing Library ESLint plugin
- [ ] **MISSING-USEREVENT-SETUP** - userEvent.setup() pattern
- [ ] **MISSING-SINGLE-ASSERT** - One assertion per test
- [ ] **MISSING-ACCESSIBLE-NAME** - Role queries with name option

---

Remember: Good tests are **readable, reliable, fast, and meaningful**. They test behavior from the user's perspective, not implementation details. They give confidence that code works and catch bugs when it doesn't.

**Testing Wisdom:**
> "Write tests. Not too many. Mostly integration." - Kent C. Dodds
> "The more your tests resemble the way your software is used, the more confidence they can give you." - Testing Library
