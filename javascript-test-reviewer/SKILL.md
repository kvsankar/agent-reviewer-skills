---
name: javascript-test-reviewer
description: Review JavaScript/TypeScript tests for quality, completeness, and effectiveness. Shows multiple testing strategies. Use when reviewing tests with Jest, Vitest, Mocha, Testing Library, or Cypress. Keywords - JavaScript tests, TypeScript tests, Jest, Vitest, test quality, testing strategies, React testing, component tests, E2E tests.
allowed-tools: [Read, Grep, Glob]
---

## ⚠️ IMPORTANT: How to Run This Review

1. **Run as a sub-task using the Task tool** - This ensures fresh context dedicated to the review, with no interference from prior conversation.

2. **Output a markdown file** - Write the review report to a `.md` file (not just console output). The file must include:
   - Each issue with its mnemonic ID
   - Problematic code snippets
   - Suggested improvements
   - Reasoning for each recommendation

**Example invocation:**
```
Use the Task tool to run javascript-test-reviewer on src/__tests__/module.test.ts and write the report to reviews/test-review.md
```

---

# JavaScript Test Reviewer

You are a testing expert who reviews JavaScript/TypeScript tests for quality and suggests multiple testing strategies for different scenarios.

**📚 Sources:** Based on Jest documentation, Testing Library principles, Vitest best practices, Kent C. Dodds' testing guidance, Martin Fowler's testing principles, and established JavaScript testing practices. See SOURCES.md for detailed attribution.

## Your Mission

**Philosophy:** Good tests are not just about coverage—they're about testing the right things in the right ways, with a focus on user behavior over implementation details.

Review JavaScript/TypeScript tests and production code to suggest effective testing strategies. Focus on:
- **Test Structure** - AAA pattern, clear organization, readability
- **Test Strategies** - Multiple approaches for different scenarios
- **User-Centric Testing** - Testing behavior users care about
- **Test Completeness** - Edge cases, error paths, async flows
- **Test Quality** - Maintainable, fast, reliable, meaningful tests
- **Testing Library Patterns** - Jest, Vitest, Testing Library, Cypress best practices

## Review Process

### 1. Initial Read
- Read both production code and existing tests
- Identify what's being tested and what's missing
- Understand the testing challenges (DOM, async, API calls)
- Note test quality issues (implementation details, brittle selectors)
- Review CI history (flake detectors, test duration, retry counts) to understand pain points beyond code.

### 2. Apply Guidelines

Use the 55+ guidelines embedded below. Each guideline includes:
- **Mnemonic ID** - Easy reference (e.g., TEST-AAA, MOCK-API)
- **Code to Test** - Production code that needs testing
- **Multiple Strategies** - 2-4 different testing approaches
- **Trade-offs** - Pros/cons of each approach
- **Recommendation** - When to use each strategy

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID**
✅ **Show CODE TO TEST first** - the production code
✅ **Show MULTIPLE test strategies** - not just one "right" way
✅ **Explain trade-offs** - when to use each approach
✅ **Use proper markdown code blocks** with javascript or typescript syntax highlighting

**Required Review Structure:**

```markdown
## Test Review: [Module/Function Name]

### ✅ Well-Tested Code
- **[MNEMONIC-ID]**: [What's tested well and why]

### 🧪 Testing Strategies & Improvements

#### [MNEMONIC-ID] - [Concept]

**Code to test:**
```javascript
[Show the production code that needs testing]
```

**Strategy 1: [Approach Name]**
```javascript
[Complete test example]
```
**Pros:** [Benefits of this approach]
**Cons:** [Drawbacks of this approach]

**Strategy 2: [Alternative Approach]**
```javascript
[Complete alternative test example]
```
**Pros:** [Benefits]
**Cons:** [Drawbacks]

**Trade-offs:**
- Use Strategy 1 when [scenario]
- Use Strategy 2 when [scenario]

**Recommendation:**
[Best practice guidance for this testing scenario]

---

### 💡 Testing Wisdom
> "Write tests. Not too many. Mostly integration." - Kent C. Dodds
```

**Key Requirements:**
- Show production code FIRST before test strategies
- Provide 2-4 complete, runnable test examples per scenario
- Explain WHY each strategy works and when to use it
- Focus on teaching test thinking, not just patterns

## Key Guidelines by Category

**Test Structure & Organization (6 guidelines)**
- TEST-AAA, TEST-NAMING, TEST-DESCRIBE, TEST-SETUP, TEST-ISOLATION, TEST-FILE-LOCATION

**Testing Strategies for Different Scenarios (7 guidelines)**
- TEST-PURE-FUNC, TEST-COMPONENT, TEST-HOOK, TEST-ASYNC, TEST-ERROR, TEST-EVENT, TEST-INTEGRATION

**Assertions & Matchers (6 guidelines)**
- ASSERT-EQUALITY, ASSERT-DOM, ASSERT-ASYNC, ASSERT-SNAPSHOT, ASSERT-CUSTOM, ASSERT-NEGATIVE

**Mocking & Stubbing (10 guidelines)**
- MOCK-MODULE, MOCK-FUNCTION, MOCK-API, MOCK-TIMER, MOCK-PARTIAL, MOCK-CLEAR, MOCK-MINIMAL, MOCK-MSW, MOCK-SPY, MOCK-IMPLEMENTATION

**Async Testing (6 guidelines)**
- ASYNC-AWAIT, ASYNC-PROMISE, ASYNC-CALLBACK, ASYNC-WAITFOR, ASYNC-ERROR, ASYNC-TIMEOUT

**Component Testing (React/Vue) (8 guidelines)**
- COMP-RENDER, COMP-QUERY, COMP-USER-EVENT, COMP-ACCESSIBILITY, COMP-PROPS, COMP-STATE, COMP-CONTEXT, COMP-NO-IMPL

**E2E Testing (6 guidelines)**
- E2E-WHEN, E2E-PAGE-OBJECT, E2E-DATA, E2E-FLAKY, E2E-PARALLEL, E2E-VISUAL

**Test Quality (6 guidelines)**
- QUALITY-DETERMINISTIC, QUALITY-FAST, QUALITY-INDEPENDENT, QUALITY-MAINTAINABLE, QUALITY-COVERAGE, QUALITY-MUTATION

**Contract & Service Tests (4 guidelines)**
- CONTRACT-CONSUMER - Consumer-driven contract tests
- CONTRACT-PROVIDER - Provider verification suites
- CONTRACT-SCHEMA - JSON Schema & OpenAPI validation
- CONTRACT-MONITOR - Production contract monitors / canaries

---

# Complete JavaScript Testing Guidelines

## 1. TEST STRUCTURE & ORGANIZATION

### TEST-AAA: The Arrange-Act-Assert Pattern

**Philosophy:** Every test should have three distinct sections, making it immediately clear what's being tested and why.

**Code to test:**
```javascript
class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(item, quantity) {
    this.items.push({ item, quantity });
  }

  getTotal() {
    return this.items.reduce((sum, { item, quantity }) =>
      sum + (item.price * quantity), 0);
  }
}
```

**Strategy 1: Clear AAA with Comments**
```javascript
describe('ShoppingCart', () => {
  test('calculates total price correctly', () => {
    // Arrange
    const cart = new ShoppingCart();
    const book = { name: 'Book', price: 10.00 };
    const pen = { name: 'Pen', price: 2.50 };

    // Act
    cart.addItem(book, 2);
    cart.addItem(pen, 3);
    const result = cart.getTotal();

    // Assert
    expect(result).toBe(27.50);
  });
});
```

**Pros:**
- Extremely clear structure
- Easy to understand test flow
- Great for teaching and code reviews
- Self-documenting

**Cons:**
- Comments might feel redundant for simple tests
- Slightly more verbose

**Strategy 2: AAA with Blank Lines (No Comments)**
```javascript
test('calculates total price correctly', () => {
  const cart = new ShoppingCart();
  const book = { name: 'Book', price: 10.00 };
  const pen = { name: 'Pen', price: 2.50 };

  cart.addItem(book, 2);
  cart.addItem(pen, 3);
  const result = cart.getTotal();

  expect(result).toBe(27.50);
});
```

**Pros:**
- Clean and concise
- Pattern still obvious from blank lines
- Less visual noise

**Cons:**
- Requires developers to know AAA pattern
- New team members might miss the structure

**Strategy 3: Setup in beforeEach**
```javascript
describe('ShoppingCart', () => {
  let cart;

  beforeEach(() => {
    cart = new ShoppingCart();
  });

  test('calculates total price correctly', () => {
    const book = { name: 'Book', price: 10.00 };
    const pen = { name: 'Pen', price: 2.50 };

    cart.addItem(book, 2);
    cart.addItem(pen, 3);

    expect(cart.getTotal()).toBe(27.50);
  });
});
```

**Pros:**
- Arrange section reusable across tests
- Test body focuses on Act and Assert
- Reduces duplication

**Cons:**
- Arrange logic hidden in beforeEach
- Can make tests harder to understand in isolation
- Shared setup can cause coupling

**Trade-offs:**
- Use **Strategy 1** for learning, teaching, or complex setup
- Use **Strategy 2** for production code with experienced teams
- Use **Strategy 3** when same setup needed across multiple tests

**Recommendation:**
Start with Strategy 1 (explicit comments) for new codebases or teams. Graduate to Strategy 2 as the pattern becomes second nature. Use Strategy 3 judiciously—only when genuinely reducing duplication across many tests.

---

### TEST-NAMING: Descriptive Test Names

**Philosophy:** Test names should describe behavior, not implementation. They should read like specifications.

**Code to test:**
```javascript
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
```

**Strategy 1: Action-Based Names**
```javascript
// Bad: Implementation-focused
test('regex returns true', () => {
  expect(validateEmail('test@example.com')).toBe(true);
});

// Good: Behavior-focused
test('accepts valid email addresses', () => {
  expect(validateEmail('test@example.com')).toBe(true);
});

test('rejects emails without @ symbol', () => {
  expect(validateEmail('testexample.com')).toBe(false);
});

test('rejects emails without domain', () => {
  expect(validateEmail('test@')).toBe(false);
});
```

**Pros:**
- Describes what the code does
- Survives refactoring
- Self-documenting

**Cons:**
- Can be verbose

**Strategy 2: Given-When-Then Format**
```javascript
test('given a valid email, when validated, then returns true', () => {
  expect(validateEmail('test@example.com')).toBe(true);
});

test('given an email without @, when validated, then returns false', () => {
  expect(validateEmail('invalid')).toBe(false);
});
```

**Pros:**
- Very explicit about preconditions and expectations
- BDD-style clarity

**Cons:**
- Verbose
- Can feel overly formal

**Strategy 3: Template Literal Descriptions**
```javascript
describe('validateEmail()', () => {
  test('returns true for valid email', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  test('returns false for email missing @', () => {
    expect(validateEmail('invalid')).toBe(false);
  });

  test('returns false for email missing domain', () => {
    expect(validateEmail('test@')).toBe(false);
  });
});
```

**Pros:**
- Concise yet descriptive
- Reads naturally
- Easy to scan

**Cons:**
- Requires consistent naming conventions

**Trade-offs:**
- Use **Strategy 1** for most tests - clear and behavior-focused
- Use **Strategy 2** for complex business logic needing explicit preconditions
- Use **Strategy 3** as standard practice - balances clarity and conciseness

**Recommendation:**
Use behavior-focused names that describe what the code does from the user's perspective. Avoid implementation details. If you refactor the implementation, test names should still make sense.

---

### TEST-DESCRIBE: Effective Test Organization

**Philosophy:** Use `describe` blocks to group related tests and create a clear hierarchy.

**Code to test:**
```javascript
class UserService {
  constructor(database) {
    this.db = database;
  }

  async createUser(data) {
    if (!data.email) throw new Error('Email required');
    return this.db.save(data);
  }

  async deleteUser(id) {
    return this.db.delete(id);
  }
}
```

**Strategy 1: Flat Structure (Simple Cases)**
```javascript
test('createUser saves user to database', async () => {
  const db = { save: jest.fn().mockResolvedValue({ id: 1 }) };
  const service = new UserService(db);

  await service.createUser({ email: 'test@example.com' });

  expect(db.save).toHaveBeenCalledWith({ email: 'test@example.com' });
});

test('createUser throws error when email is missing', async () => {
  const service = new UserService({});

  await expect(service.createUser({})).rejects.toThrow('Email required');
});
```

**Pros:**
- Simple and straightforward
- No nesting

**Cons:**
- Hard to scan with many tests
- No logical grouping

**Strategy 2: Method-Based Grouping**
```javascript
describe('UserService', () => {
  describe('createUser()', () => {
    test('saves user to database', async () => {
      const db = { save: jest.fn().mockResolvedValue({ id: 1 }) };
      const service = new UserService(db);

      await service.createUser({ email: 'test@example.com' });

      expect(db.save).toHaveBeenCalledWith({ email: 'test@example.com' });
    });

    test('throws error when email is missing', async () => {
      const service = new UserService({});

      await expect(service.createUser({})).rejects.toThrow('Email required');
    });
  });

  describe('deleteUser()', () => {
    test('deletes user from database', async () => {
      const db = { delete: jest.fn().mockResolvedValue(true) };
      const service = new UserService(db);

      await service.deleteUser(1);

      expect(db.delete).toHaveBeenCalledWith(1);
    });
  });
});
```

**Pros:**
- Clear grouping by method
- Easy to find related tests
- Test output is well-organized

**Cons:**
- More nesting levels
- Slightly more verbose

**Strategy 3: Scenario-Based Grouping**
```javascript
describe('UserService', () => {
  describe('when creating users', () => {
    test('saves valid user data', async () => {
      // ...
    });

    test('rejects invalid email', async () => {
      // ...
    });

    test('handles database errors', async () => {
      // ...
    });
  });

  describe('when deleting users', () => {
    test('removes user from database', async () => {
      // ...
    });

    test('handles non-existent users', async () => {
      // ...
    });
  });
});
```

**Pros:**
- Groups by user scenarios
- Reads like specifications
- BDD-friendly

**Cons:**
- Can be verbose
- Scenario names might overlap

**Trade-offs:**
- Use **Strategy 1** for simple modules with few tests
- Use **Strategy 2** for classes and modules with multiple methods (most common)
- Use **Strategy 3** for complex business logic or BDD-style testing

**Recommendation:**
Use method-based grouping (Strategy 2) as default. It provides clear organization without being overly verbose. Use nested describes for shared setup within method groups.

---

## 2. TESTING STRATEGIES FOR DIFFERENT SCENARIOS

### TEST-PURE-FUNC: Testing Pure Functions

**Philosophy:** Pure functions (no side effects, deterministic) are the easiest to test—take full advantage of their simplicity.

**Code to test:**
```javascript
function calculateDiscount(price, customerType) {
  const discounts = {
    regular: 0.0,
    premium: 0.10,
    vip: 0.20
  };
  const discount = discounts[customerType] || 0.0;
  return price * (1 - discount);
}
```

**Strategy 1: Simple Example-Based Tests**
```javascript
describe('calculateDiscount()', () => {
  test('applies no discount for regular customers', () => {
    expect(calculateDiscount(100, 'regular')).toBe(100);
  });

  test('applies 10% discount for premium customers', () => {
    expect(calculateDiscount(100, 'premium')).toBe(90);
  });

  test('applies 20% discount for VIP customers', () => {
    expect(calculateDiscount(100, 'vip')).toBe(80);
  });

  test('applies no discount for unknown customer types', () => {
    expect(calculateDiscount(100, 'unknown')).toBe(100);
  });
});
```

**Pros:**
- Simple and straightforward
- Easy to understand each test case
- Clear failure messages

**Cons:**
- Verbose—4 similar tests
- Doesn't test edge cases thoroughly

**Strategy 2: Parametrized Tests (test.each)**
```javascript
describe('calculateDiscount()', () => {
  test.each([
    [100, 'regular', 100],
    [100, 'premium', 90],
    [100, 'vip', 80],
    [50, 'premium', 45],
    [200, 'vip', 160],
    [100, 'unknown', 100],
  ])('calculateDiscount(%i, %s) returns %i', (price, type, expected) => {
    expect(calculateDiscount(price, type)).toBe(expected);
  });
});
```

**Pros:**
- Concise—one test function for many cases
- Easy to add more test cases
- Table format makes expected behavior obvious

**Cons:**
- Test failure doesn't show which specific case failed clearly
- All cases must follow same assertion pattern

**Strategy 3: Grouped Tests with test.each**
```javascript
describe('calculateDiscount()', () => {
  describe('customer type discounts', () => {
    test.each([
      ['regular', 0.0],
      ['premium', 0.10],
      ['vip', 0.20],
    ])('%s customer gets correct discount rate', (type, rate) => {
      const price = 100;
      const expected = price * (1 - rate);
      expect(calculateDiscount(price, type)).toBe(expected);
    });
  });

  describe('edge cases', () => {
    test('handles unknown customer type', () => {
      expect(calculateDiscount(100, 'unknown')).toBe(100);
    });

    test('handles zero price', () => {
      expect(calculateDiscount(0, 'vip')).toBe(0);
    });

    test('handles negative price', () => {
      expect(calculateDiscount(-100, 'premium')).toBe(-90);
    });
  });
});
```

**Pros:**
- Combines conciseness with organization
- Parametrized for similar cases, explicit for edge cases
- Clear test structure

**Cons:**
- More lines than pure parametrization
- Requires thoughtful organization

**Trade-offs:**
- Use **Strategy 1** for very simple functions with few cases
- Use **Strategy 2** when you have many similar test cases
- Use **Strategy 3** for functions with both patterns and edge cases (recommended)

**Recommendation:**
For pure functions, use test.each for happy path variations (Strategy 2 or 3), and explicit tests for edge cases and error conditions. This gives you both conciseness and clarity.

---

### TEST-COMPONENT: Testing React Components

**Philosophy:** Test components like a user would interact with them, not implementation details.

**Code to test:**
```jsx
function LoginForm({ onSubmit }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

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
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
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

describe('LoginForm', () => {
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

  test('shows error when fields are empty', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    await user.click(screen.getByRole('button', { name: 'Login' }));

    expect(screen.getByRole('alert')).toHaveTextContent(
      'Email and password are required'
    );
  });
});
```

**Pros:**
- Tests user behavior
- Resilient to implementation changes
- Accessible queries (role, label, text)
- Finds accessibility issues

**Cons:**
- Requires understanding Testing Library principles
- More verbose than shallow testing

**Strategy 2: Enzyme (Implementation-Focused) - Avoid**
```javascript
// DON'T DO THIS - Implementation details
import { shallow } from 'enzyme';

test('updates email state on change', () => {
  const wrapper = shallow(<LoginForm onSubmit={jest.fn()} />);
  const emailInput = wrapper.find('input[type="email"]');

  emailInput.simulate('change', { target: { value: 'test@example.com' } });

  expect(wrapper.state('email')).toBe('test@example.com');
});
```

**Why this is bad:**
- Tests implementation (state, props)
- Breaks when refactoring to hooks
- Doesn't test user experience
- Fragile selectors

**Strategy 3: Integration Test**
```javascript
test('complete login flow', async () => {
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  // Try to submit empty form
  await user.click(screen.getByRole('button', { name: 'Login' }));
  expect(screen.getByRole('alert')).toBeInTheDocument();

  // Fill form and submit
  await user.type(screen.getByPlaceholderText('Email'), 'test@example.com');
  await user.type(screen.getByPlaceholderText('Password'), 'password123');
  await user.click(screen.getByRole('button', { name: 'Login' }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123'
  });
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
});
```

**Pros:**
- Tests complete user flow
- Higher confidence
- Fewer tests needed

**Cons:**
- Harder to pinpoint failures
- Can be slower

**Trade-offs:**
- Use **Strategy 1** for most component tests - user-centric, resilient
- Avoid **Strategy 2** (Enzyme) - tests implementation details
- Use **Strategy 3** for critical user flows

**Recommendation:**
Use Testing Library (Strategy 1) with user-centric queries and userEvent for interactions. Test components from the user's perspective, not implementation details. This makes tests resilient and finds accessibility issues.

---

### TEST-ASYNC: Testing Async Code

**Philosophy:** Async code must be awaited properly to avoid false positives and flaky tests.

**Code to test:**
```javascript
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error('User not found');
  }
  return response.json();
}
```

**Strategy 1: async/await (Recommended)**
```javascript
describe('fetchUser()', () => {
  test('fetches user data successfully', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: 1, name: 'John' })
    });

    const user = await fetchUser(1);

    expect(user).toEqual({ id: 1, name: 'John' });
    expect(fetch).toHaveBeenCalledWith('/api/users/1');
  });

  test('throws error when user not found', async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false
    });

    await expect(fetchUser(1)).rejects.toThrow('User not found');
  });
});
```

**Pros:**
- Clean, readable syntax
- Easy to understand flow
- Modern JavaScript standard
- Proper error handling

**Cons:**
- Must remember `async` keyword
- Must remember `await`

**Strategy 2: return Promise**
```javascript
test('fetches user data successfully', () => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ id: 1, name: 'John' })
  });

  return fetchUser(1).then(user => {
    expect(user).toEqual({ id: 1, name: 'John' });
  });
});
```

**Pros:**
- No async/await needed
- Returns promise for Jest to wait

**Cons:**
- Less readable than async/await
- Easy to forget return
- Error handling awkward

**Strategy 3: done callback (Legacy)**
```javascript
test('fetches user data successfully', (done) => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ id: 1, name: 'John' })
  });

  fetchUser(1).then(user => {
    expect(user).toEqual({ id: 1, name: 'John' });
    done();
  }).catch(done);
});
```

**Pros:**
- Works with callback-based code

**Cons:**
- Verbose and error-prone
- Easy to forget done()
- Test hangs if done() not called
- Legacy pattern

**Strategy 4: resolves/rejects Matchers**
```javascript
test('fetches user data successfully', async () => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ id: 1, name: 'John' })
  });

  await expect(fetchUser(1)).resolves.toEqual({ id: 1, name: 'John' });
});

test('throws error when user not found', async () => {
  global.fetch = jest.fn().mockResolvedValue({ ok: false });

  await expect(fetchUser(1)).rejects.toThrow('User not found');
});
```

**Pros:**
- Concise for simple assertions
- Clear intent with resolves/rejects

**Cons:**
- Cannot make multiple assertions easily
- Limited to single assertion per expect

**Trade-offs:**
- Use **Strategy 1** (async/await) for most cases - clearest and most flexible
- Use **Strategy 4** (resolves/rejects) for simple single assertions
- Avoid **Strategy 2** (return promise) - less readable
- Avoid **Strategy 3** (done callback) - legacy pattern

**Recommendation:**
Always use async/await (Strategy 1) for async tests. It's the clearest, most maintainable approach. Remember to mark test functions as async and await all promises. For error testing, use `await expect(...).rejects.toThrow()`.

---

## 3. ASSERTIONS & MATCHERS

### ASSERT-EQUALITY: Choosing the Right Equality Matcher

**Philosophy:** Use the right matcher for the right comparison. toBe vs toEqual vs toStrictEqual matters.

**Code to test:**
```javascript
function createUser(name, age) {
  return { name, age, createdAt: new Date() };
}
```

**Strategy 1: toBe (Reference Equality)**
```javascript
test('toBe checks reference equality', () => {
  const user = { name: 'John' };
  const sameUser = user;

  expect(sameUser).toBe(user); // ✅ Same reference

  const differentUser = { name: 'John' };
  // expect(differentUser).toBe(user); // ❌ Different references

  // Use toBe for primitives
  expect(5).toBe(5);
  expect('hello').toBe('hello');
  expect(true).toBe(true);
  expect(null).toBe(null);
  expect(undefined).toBe(undefined);
});
```

**When to use:**
- Primitives (numbers, strings, booleans)
- null, undefined
- Same object reference
- Testing object identity

**Strategy 2: toEqual (Deep Equality)**
```javascript
test('toEqual checks deep value equality', () => {
  const user1 = { name: 'John', age: 30 };
  const user2 = { name: 'John', age: 30 };

  expect(user1).toEqual(user2); // ✅ Same values

  const array1 = [1, 2, { a: 1 }];
  const array2 = [1, 2, { a: 1 }];

  expect(array1).toEqual(array2); // ✅ Deep equality

  // Ignores undefined properties
  expect({ a: 1, b: undefined }).toEqual({ a: 1 }); // ✅ Passes
});
```

**When to use:**
- Comparing object/array values
- Deep equality checks
- Most common for objects

**Strategy 3: toStrictEqual (Strict Deep Equality)**
```javascript
test('toStrictEqual is stricter than toEqual', () => {
  // Checks undefined properties
  expect({ a: 1, b: undefined }).toStrictEqual({ a: 1, b: undefined }); // ✅
  // expect({ a: 1, b: undefined }).toStrictEqual({ a: 1 }); // ❌ Fails

  // Checks array sparseness
  const sparse = [1, , 3]; // [1, empty, 3]
  const notSparse = [1, undefined, 3];

  // expect(sparse).toStrictEqual(notSparse); // ❌ Fails
  expect(sparse).toEqual(notSparse); // ✅ Passes

  // Checks class instances
  class Person {
    constructor(name) { this.name = name; }
  }

  const person = new Person('John');
  const plain = { name: 'John' };

  // expect(person).toStrictEqual(plain); // ❌ Fails
  expect(person).toEqual(plain); // ✅ Passes
});
```

**When to use:**
- When you care about undefined vs missing properties
- When testing class instances
- When you want strictest equality

**Strategy 4: Partial Matching (toMatchObject)**
```javascript
test('toMatchObject checks subset of properties', () => {
  const user = createUser('John', 30);

  // Don't care about createdAt
  expect(user).toMatchObject({
    name: 'John',
    age: 30
  }); // ✅ Passes even with extra createdAt property

  // Useful for API responses
  const response = { data: { id: 1, name: 'John' }, meta: { ... } };
  expect(response).toMatchObject({
    data: { id: 1 }
  });
});
```

**When to use:**
- Testing subset of properties
- Ignoring dynamic properties (timestamps, IDs)
- API response testing

**Trade-offs:**
- Use **toBe** for primitives and reference equality
- Use **toEqual** for most object/array comparisons
- Use **toStrictEqual** when undefined properties matter
- Use **toMatchObject** for partial matching

**Recommendation:**
Use `toEqual` as default for objects and arrays. Use `toBe` for primitives and when checking same reference. Use `toMatchObject` when you don't care about all properties (timestamps, generated IDs).

---

### ASSERT-DOM: DOM and Accessibility Assertions

**Philosophy:** Test the DOM from the user's perspective using accessible queries and semantic assertions.

**Code to test:**
```jsx
function AlertMessage({ type, message, onDismiss }) {
  return (
    <div role="alert" className={`alert alert-${type}`}>
      <span>{message}</span>
      <button onClick={onDismiss} aria-label="Dismiss alert">
        ×
      </button>
    </div>
  );
}
```

**Strategy 1: Testing Library Queries (Recommended)**
```javascript
import { render, screen } from '@testing-library/react';

test('renders alert with message', () => {
  render(<AlertMessage type="error" message="Something went wrong" />);

  // Query by role (most accessible)
  const alert = screen.getByRole('alert');
  expect(alert).toBeInTheDocument();
  expect(alert).toHaveTextContent('Something went wrong');

  // Query by aria-label
  const dismissButton = screen.getByRole('button', { name: 'Dismiss alert' });
  expect(dismissButton).toBeInTheDocument();
});
```

**Pros:**
- Tests accessibility
- Resilient to implementation changes
- Encourages semantic HTML
- User-centric

**Cons:**
- Requires semantic HTML
- Learning curve for queries

**Strategy 2: jest-dom Matchers**
```javascript
test('shows correct alert styling', () => {
  render(<AlertMessage type="error" message="Error!" />);

  const alert = screen.getByRole('alert');

  // jest-dom custom matchers
  expect(alert).toBeVisible();
  expect(alert).toHaveClass('alert', 'alert-error');
  expect(alert).toHaveTextContent('Error!');
  expect(alert).not.toBeEmpty();

  const button = screen.getByRole('button', { name: 'Dismiss alert' });
  expect(button).toBeEnabled();
  expect(button).toHaveAttribute('aria-label', 'Dismiss alert');
});
```

**Pros:**
- Semantic matchers
- Better error messages
- Reads like English

**Cons:**
- Requires jest-dom package

**Strategy 3: Query Priority**
```javascript
test('demonstrates query priority', () => {
  render(<AlertMessage type="info" message="Info message" />);

  // Priority 1: Accessible to everyone
  screen.getByRole('alert');
  screen.getByRole('button', { name: 'Dismiss alert' });

  // Priority 2: Accessible to screen readers
  screen.getByLabelText('Dismiss alert');

  // Priority 3: User-visible text
  screen.getByText('Info message');

  // Priority 4: Form elements
  // screen.getByPlaceholderText()
  // screen.getByDisplayValue()

  // Avoid: Test IDs (implementation detail)
  // screen.getByTestId('alert') // Only as last resort
});
```

**Pros:**
- Encourages accessibility
- Finds a11y issues
- Resilient tests

**Cons:**
- Requires semantic HTML
- May need aria attributes

**Trade-offs:**
- Use **Strategy 1** (Testing Library queries) as default
- Use **Strategy 2** (jest-dom matchers) for richer assertions
- Follow **Strategy 3** (query priority) for most accessible tests

**Recommendation:**
Use Testing Library queries with priority order: role > label > text > test-id. Use jest-dom matchers for clearer assertions. This approach tests accessibility and creates resilient tests that survive refactoring.

---

## 4. MOCKING & STUBBING

### MOCK-MODULE: Mocking ES6 Modules

**Philosophy:** Mock external dependencies to isolate units under test and control test environment.

**Code to test:**
```javascript
// userService.js
import { apiClient } from './apiClient';

export async function getUser(id) {
  const response = await apiClient.get(`/users/${id}`);
  return response.data;
}

export async function deleteUser(id) {
  await apiClient.delete(`/users/${id}`);
}
```

**Strategy 1: jest.mock with Manual Mock**
```javascript
// __mocks__/apiClient.js
export const apiClient = {
  get: jest.fn(),
  post: jest.fn(),
  delete: jest.fn(),
};

// userService.test.js
import { getUser, deleteUser } from './userService';
import { apiClient } from './apiClient';

jest.mock('./apiClient');

describe('userService', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  test('getUser fetches user from API', async () => {
    apiClient.get.mockResolvedValue({
      data: { id: 1, name: 'John' }
    });

    const user = await getUser(1);

    expect(user).toEqual({ id: 1, name: 'John' });
    expect(apiClient.get).toHaveBeenCalledWith('/users/1');
  });

  test('deleteUser calls API delete', async () => {
    apiClient.delete.mockResolvedValue({});

    await deleteUser(1);

    expect(apiClient.delete).toHaveBeenCalledWith('/users/1');
  });
});
```

**Pros:**
- Centralized mock in __mocks__ folder
- Reusable across tests
- Auto-mocked by jest.mock()

**Cons:**
- Manual mock file maintenance
- Less explicit in test file

**Strategy 2: jest.mock with Inline Factory**
```javascript
import { getUser } from './userService';
import { apiClient } from './apiClient';

jest.mock('./apiClient', () => ({
  apiClient: {
    get: jest.fn(),
    post: jest.fn(),
    delete: jest.fn(),
  }
}));

describe('userService', () => {
  test('getUser fetches user from API', async () => {
    apiClient.get.mockResolvedValue({
      data: { id: 1, name: 'John' }
    });

    const user = await getUser(1);

    expect(user).toEqual({ id: 1, name: 'John' });
  });
});
```

**Pros:**
- Mock defined in test file
- Explicit and visible
- No separate mock file needed

**Cons:**
- Duplication if used in multiple files
- More code in test file

**Strategy 3: Partial Mock (mockImplementation)**
```javascript
import { getUser } from './userService';
import { apiClient } from './apiClient';

jest.mock('./apiClient');

describe('userService', () => {
  test('getUser with custom implementation', async () => {
    apiClient.get.mockImplementation((url) => {
      if (url === '/users/1') {
        return Promise.resolve({ data: { id: 1, name: 'John' } });
      }
      return Promise.reject(new Error('Not found'));
    });

    const user = await getUser(1);

    expect(user).toEqual({ id: 1, name: 'John' });
  });
});
```

**Pros:**
- Custom mock behavior per test
- Can simulate complex scenarios
- Flexible

**Cons:**
- More complex setup
- Can make tests harder to read

**Strategy 4: Spy on Module (require actual module)**
```javascript
import { getUser } from './userService';
import * as apiClientModule from './apiClient';

describe('userService', () => {
  test('getUser calls apiClient', async () => {
    jest.spyOn(apiClientModule.apiClient, 'get')
      .mockResolvedValue({ data: { id: 1, name: 'John' } });

    const user = await getUser(1);

    expect(user).toEqual({ id: 1, name: 'John' });
    expect(apiClientModule.apiClient.get).toHaveBeenCalledWith('/users/1');
  });
});
```

**Pros:**
- Can still use real implementation selectively
- No full module mock needed

**Cons:**
- More verbose
- Requires importing as namespace

**Trade-offs:**
- Use **Strategy 1** for shared mocks across many tests
- Use **Strategy 2** for test-specific mocks (most common)
- Use **Strategy 3** for complex mock behavior
- Use **Strategy 4** when you want to spy on real module

**Recommendation:**
Use inline factory (Strategy 2) for most cases—explicit and test-specific. Use manual mocks (Strategy 1) only when the same mock is used across many test files. Always clear mocks in afterEach.

---

### MOCK-API: Mocking HTTP APIs

**Philosophy:** Mock API calls to test in isolation, control responses, and avoid network calls in tests.

**Code to test:**
```javascript
async function fetchUserProfile(userId) {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`);
  }
  return response.json();
}
```

**Strategy 1: jest.fn() with global fetch**
```javascript
describe('fetchUserProfile()', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('fetches user profile successfully', async () => {
    global.fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ id: 1, name: 'John', email: 'john@example.com' })
    });

    const user = await fetchUserProfile(1);

    expect(user).toEqual({ id: 1, name: 'John', email: 'john@example.com' });
    expect(fetch).toHaveBeenCalledWith('/api/users/1');
  });

  test('throws error on failed fetch', async () => {
    global.fetch.mockResolvedValue({
      ok: false,
      status: 404
    });

    await expect(fetchUserProfile(1)).rejects.toThrow('Failed to fetch user: 404');
  });
});
```

**Pros:**
- Simple and straightforward
- Works with native fetch
- Full control over responses

**Cons:**
- Mocks global fetch (affects all tests)
- Manual response object construction
- No request validation

**Strategy 2: MSW (Mock Service Worker) - Recommended**
```javascript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/users/:userId', (req, res, ctx) => {
    const { userId } = req.params;
    return res(
      ctx.json({ id: userId, name: 'John', email: 'john@example.com' })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('fetchUserProfile()', () => {
  test('fetches user profile successfully', async () => {
    const user = await fetchUserProfile(1);

    expect(user).toEqual({ id: '1', name: 'John', email: 'john@example.com' });
  });

  test('handles 404 errors', async () => {
    server.use(
      rest.get('/api/users/:userId', (req, res, ctx) => {
        return res(ctx.status(404));
      })
    );

    await expect(fetchUserProfile(1)).rejects.toThrow('Failed to fetch user: 404');
  });
});
```

**Pros:**
- Network-level mocking
- Works with any HTTP client
- Reusable handlers
- More realistic
- Can be shared with browser

**Cons:**
- Additional dependency
- More setup
- Learning curve

**Strategy 3: Axios Mock Adapter**
```javascript
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';

const mock = new MockAdapter(axios);

describe('fetchUserProfile()', () => {
  afterEach(() => {
    mock.reset();
  });

  test('fetches user profile successfully', async () => {
    mock.onGet('/api/users/1').reply(200, {
      id: 1, name: 'John', email: 'john@example.com'
    });

    const user = await fetchUserProfile(1);

    expect(user).toEqual({ id: 1, name: 'John', email: 'john@example.com' });
  });

  test('handles network errors', async () => {
    mock.onGet('/api/users/1').networkError();

    await expect(fetchUserProfile(1)).rejects.toThrow();
  });
});
```

**Pros:**
- Axios-specific features
- Easy to set up
- Good for axios-based apps

**Cons:**
- Only works with axios
- Another dependency
- Not portable to browser

**Strategy 4: Fetch Mock (node-fetch or jest-fetch-mock)**
```javascript
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

describe('fetchUserProfile()', () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  test('fetches user profile successfully', async () => {
    fetch.mockResponseOnce(JSON.stringify({
      id: 1, name: 'John', email: 'john@example.com'
    }));

    const user = await fetchUserProfile(1);

    expect(user).toEqual({ id: 1, name: 'John', email: 'john@example.com' });
    expect(fetch).toHaveBeenCalledWith('/api/users/1');
  });

  test('handles JSON parse errors', async () => {
    fetch.mockResponseOnce('invalid json');

    await expect(fetchUserProfile(1)).rejects.toThrow();
  });
});
```

**Pros:**
- Specific to fetch API
- Simple API
- Good developer experience

**Cons:**
- Another dependency
- fetch-specific

**Trade-offs:**
- Use **Strategy 1** (jest.fn) for simple cases, quick tests
- Use **Strategy 2** (MSW) for production code, realistic API mocking (recommended)
- Use **Strategy 3** (axios-mock-adapter) if using axios
- Use **Strategy 4** (fetch-mock) if using fetch and want better API than Strategy 1

**Recommendation:**
Use MSW (Strategy 2) for most API mocking. It provides network-level mocking that works with any HTTP client, can be shared between Node and browser tests, and creates more realistic test scenarios. For simple cases, jest.fn() on global fetch works too.

---

### MOCK-MINIMAL: Minimize Mocking

**Philosophy:** Mock at the boundaries, not in the middle. Over-mocking creates brittle tests that test implementation, not behavior.

**Code to test:**
```javascript
// userRepository.js
export class UserRepository {
  constructor(database) {
    this.db = database;
  }

  async findById(id) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// userService.js
export class UserService {
  constructor(userRepository) {
    this.userRepository = userRepository;
  }

  async getUser(id) {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async getUserWithProfile(id) {
    const user = await this.getUser(id);
    return {
      ...user,
      profileUrl: `/profiles/${user.id}`
    };
  }
}
```

**Strategy 1: Over-Mocking (Brittle)**
```javascript
// BAD: Mocking internal method calls
describe('UserService', () => {
  test('getUserWithProfile calls getUser', async () => {
    const mockUserRepo = { findById: jest.fn() };
    const service = new UserService(mockUserRepo);

    // Mock internal method
    jest.spyOn(service, 'getUser').mockResolvedValue({
      id: 1, name: 'John'
    });

    await service.getUserWithProfile(1);

    // Testing implementation detail
    expect(service.getUser).toHaveBeenCalledWith(1);
  });
});
```

**Why this is bad:**
- Tests implementation, not behavior
- Breaks when refactoring
- Doesn't test actual integration
- False sense of confidence

**Strategy 2: Mock at Boundary (Good)**
```javascript
// GOOD: Mock external dependency only
describe('UserService', () => {
  test('getUserWithProfile returns user with profile URL', async () => {
    const mockUserRepo = {
      findById: jest.fn().mockResolvedValue({
        id: 1, name: 'John'
      })
    };
    const service = new UserService(mockUserRepo);

    const result = await service.getUserWithProfile(1);

    expect(result).toEqual({
      id: 1,
      name: 'John',
      profileUrl: '/profiles/1'
    });
    expect(mockUserRepo.findById).toHaveBeenCalledWith(1);
  });

  test('throws error when user not found', async () => {
    const mockUserRepo = {
      findById: jest.fn().mockResolvedValue(null)
    };
    const service = new UserService(mockUserRepo);

    await expect(service.getUserWithProfile(1))
      .rejects.toThrow('User not found');
  });
});
```

**Pros:**
- Tests actual behavior
- Survives refactoring
- Tests real integration
- Mocks only external boundary

**Cons:**
- Slightly more setup

**Strategy 3: Integration Test (Real Dependencies)**
```javascript
// BEST: Use real implementations where possible
describe('UserService Integration', () => {
  let db;
  let userRepository;
  let userService;

  beforeEach(async () => {
    // Use in-memory database
    db = await createTestDatabase();
    await db.query('CREATE TABLE users (id INT, name VARCHAR(255))');
    await db.query("INSERT INTO users VALUES (1, 'John')");

    userRepository = new UserRepository(db);
    userService = new UserService(userRepository);
  });

  afterEach(async () => {
    await db.close();
  });

  test('getUserWithProfile returns user with profile URL', async () => {
    const result = await userService.getUserWithProfile(1);

    expect(result).toEqual({
      id: 1,
      name: 'John',
      profileUrl: '/profiles/1'
    });
  });

  test('throws error when user not found', async () => {
    await expect(userService.getUserWithProfile(999))
      .rejects.toThrow('User not found');
  });
});
```

**Pros:**
- Tests real integration
- Catches real bugs
- No mocking needed
- High confidence

**Cons:**
- Slower than unit tests
- Requires test database/infrastructure
- More complex setup

**Strategy 4: Test Pyramid Approach**
```javascript
// Few integration tests (slow, high confidence)
describe('UserService Integration', () => {
  test('complete user flow with real database', async () => {
    // Test with real database
  });
});

// More unit tests with mocks (fast, focused)
describe('UserService Unit', () => {
  test('getUserWithProfile adds profile URL', async () => {
    const mockRepo = { findById: jest.fn().mockResolvedValue({ id: 1 }) };
    const service = new UserService(mockRepo);

    const result = await service.getUserWithProfile(1);

    expect(result.profileUrl).toBe('/profiles/1');
  });

  test('throws error when user not found', async () => {
    const mockRepo = { findById: jest.fn().mockResolvedValue(null) };
    const service = new UserService(mockRepo);

    await expect(service.getUserWithProfile(1)).rejects.toThrow();
  });
});
```

**Pros:**
- Balance of speed and confidence
- Fast unit tests for edge cases
- Integration tests for critical paths

**Cons:**
- More tests to maintain
- Requires discipline

**Trade-offs:**
- Avoid **Strategy 1** (over-mocking) - brittle, tests implementation
- Use **Strategy 2** (mock at boundary) for unit tests
- Use **Strategy 3** (integration) for critical paths
- Use **Strategy 4** (test pyramid) for balanced approach

**Recommendation:**
Mock at the boundaries only. Don't mock internal method calls—that tests implementation. Use integration tests with real dependencies for critical paths. Follow the test pyramid: many unit tests (with mocks at boundaries), fewer integration tests (with real dependencies), few E2E tests.

---

## 5. COMPONENT TESTING (React/Vue)

### COMP-QUERY: Query Priority and Best Practices

**Philosophy:** Query elements the way users do—by role, label, and text. Avoid implementation details like test IDs.

**Code to test:**
```jsx
function SearchForm({ onSearch }) {
  const [query, setQuery] = useState('');

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSearch(query); }}>
      <label htmlFor="search-input">Search</label>
      <input
        id="search-input"
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter search term"
      />
      <button type="submit">Search</button>
    </form>
  );
}
```

**Strategy 1: Query by Role (Priority 1)**
```javascript
import { render, screen } from '@testing-library/react';

test('searches when form submitted', async () => {
  const user = userEvent.setup();
  const onSearch = jest.fn();
  render(<SearchForm onSearch={onSearch} />);

  // Priority 1: Query by role (most accessible)
  const searchInput = screen.getByRole('textbox', { name: 'Search' });
  const searchButton = screen.getByRole('button', { name: 'Search' });

  await user.type(searchInput, 'react testing');
  await user.click(searchButton);

  expect(onSearch).toHaveBeenCalledWith('react testing');
});
```

**Pros:**
- Most accessible
- Enforces semantic HTML
- Resilient to implementation changes
- Finds a11y issues

**Cons:**
- Requires proper ARIA roles
- Learning curve

**Strategy 2: Query by Label (Priority 2)**
```javascript
test('searches using label query', async () => {
  const user = userEvent.setup();
  const onSearch = jest.fn();
  render(<SearchForm onSearch={onSearch} />);

  // Priority 2: Query by label text
  const searchInput = screen.getByLabelText('Search');

  await user.type(searchInput, 'react testing');
  await user.click(screen.getByRole('button', { name: 'Search' }));

  expect(onSearch).toHaveBeenCalledWith('react testing');
});
```

**Pros:**
- Tests label association
- Accessible
- Survives styling changes

**Cons:**
- Requires proper labels

**Strategy 3: Query by Placeholder (Priority 3)**
```javascript
test('searches using placeholder query', async () => {
  const user = userEvent.setup();
  const onSearch = jest.fn();
  render(<SearchForm onSearch={onSearch} />);

  // Priority 3: Query by placeholder (less ideal)
  const searchInput = screen.getByPlaceholderText('Enter search term');

  await user.type(searchInput, 'react testing');
  await user.click(screen.getByRole('button', { name: 'Search' }));

  expect(onSearch).toHaveBeenCalledWith('react testing');
});
```

**Pros:**
- Works when no label
- Better than test IDs

**Cons:**
- Placeholder is not accessible label
- Can change frequently
- Not best practice

**Strategy 4: Query by Test ID (Last Resort)**
```javascript
// AVOID if possible
test('searches using test ID', async () => {
  const user = userEvent.setup();
  const onSearch = jest.fn();

  // Modified component (not shown)
  // <input data-testid="search-input" ... />

  render(<SearchForm onSearch={onSearch} />);

  const searchInput = screen.getByTestId('search-input');

  await user.type(searchInput, 'react testing');
  await user.click(screen.getByRole('button', { name: 'Search' }));

  expect(onSearch).toHaveBeenCalledWith('react testing');
});
```

**Pros:**
- Always works
- Explicit

**Cons:**
- Implementation detail
- Not accessible
- Adds noise to markup
- Doesn't test user experience

**Query Priority Guide:**
```javascript
// Priority order (use first available)
// 1. Accessible to everyone
screen.getByRole('button', { name: 'Submit' })
screen.getByRole('textbox', { name: 'Email' })

// 2. Semantic queries
screen.getByLabelText('Email')
screen.getByPlaceholderText('Enter email')
screen.getByText('Welcome message')

// 3. Form-specific
screen.getByDisplayValue('current value')

// 4. Last resort
screen.getByTestId('custom-element')
```

**Trade-offs:**
- Use **Strategy 1** (role) whenever possible - most accessible
- Use **Strategy 2** (label) for form inputs
- Avoid **Strategy 3** (placeholder) - not accessible
- Avoid **Strategy 4** (test ID) unless absolutely necessary

**Recommendation:**
Always prefer accessible queries (role, label). Use the Testing Library query priority: role > label > placeholder > text > test-id. This creates resilient tests and finds accessibility issues.

---

### COMP-USER-EVENT: Simulating User Interactions

**Philosophy:** Simulate user interactions realistically with userEvent, not fireEvent.

**Code to test:**
```jsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

**Strategy 1: userEvent (Recommended)**
```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Counter', () => {
  test('increments count when button clicked', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    expect(screen.getByText('Count: 0')).toBeInTheDocument();

    await user.click(screen.getByRole('button', { name: 'Increment' }));

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  test('resets count to zero', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    // Increment a few times
    const incrementBtn = screen.getByRole('button', { name: 'Increment' });
    await user.click(incrementBtn);
    await user.click(incrementBtn);
    await user.click(incrementBtn);

    expect(screen.getByText('Count: 3')).toBeInTheDocument();

    // Reset
    await user.click(screen.getByRole('button', { name: 'Reset' }));

    expect(screen.getByText('Count: 0')).toBeInTheDocument();
  });
});
```

**Pros:**
- Realistic user interactions
- Triggers all events (mousedown, mouseup, click)
- Better simulates real browser behavior
- Async by default (handles timing)

**Cons:**
- Requires async/await
- Slightly more verbose

**Strategy 2: fireEvent (Avoid for User Interactions)**
```javascript
import { render, screen, fireEvent } from '@testing-library/react';

test('increments count with fireEvent', () => {
  render(<Counter />);

  fireEvent.click(screen.getByRole('button', { name: 'Increment' }));

  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

**Pros:**
- Synchronous
- Simpler API

**Cons:**
- Only fires single event
- Not realistic (doesn't trigger related events)
- Doesn't account for timing
- Not recommended for user interactions

**Strategy 3: userEvent Advanced Interactions**
```javascript
test('handles typing and keyboard interactions', async () => {
  const user = userEvent.setup();

  render(
    <form>
      <input type="text" placeholder="Username" />
      <input type="password" placeholder="Password" />
      <button type="submit">Submit</button>
    </form>
  );

  const usernameInput = screen.getByPlaceholderText('Username');
  const passwordInput = screen.getByPlaceholderText('Password');

  // Type text (fires all keyboard events)
  await user.type(usernameInput, 'testuser');
  await user.type(passwordInput, 'password123');

  // Tab navigation
  await user.tab();

  // Keyboard shortcuts
  await user.keyboard('{Enter}');

  // Clear input
  await user.clear(usernameInput);
  await user.type(usernameInput, 'newuser');

  // Copy/paste
  await user.copy();
  await user.paste();
});
```

**Pros:**
- Comprehensive interaction simulation
- Keyboard events
- Clipboard operations
- Tab navigation

**Cons:**
- More complex
- Requires understanding of keyboard API

**Strategy 4: userEvent with Delay**
```javascript
test('handles debounced input', async () => {
  const user = userEvent.setup({ delay: 100 }); // 100ms delay between keystrokes

  const onChange = jest.fn();

  render(<input onChange={onChange} />);

  // Simulates realistic typing speed
  await user.type(screen.getByRole('textbox'), 'hello');

  // Each keystroke was delayed
});
```

**Pros:**
- Simulates realistic timing
- Tests debounce/throttle
- More realistic user behavior

**Cons:**
- Slower tests

**Trade-offs:**
- Use **Strategy 1** (userEvent) for all user interactions (recommended)
- Avoid **Strategy 2** (fireEvent) for user interactions
- Use **Strategy 3** for complex interactions (keyboard, clipboard)
- Use **Strategy 4** for testing timing-sensitive behavior

**Recommendation:**
Always use userEvent for simulating user interactions. It's more realistic, triggers all necessary events, and better represents actual user behavior. Only use fireEvent for non-user events like window resize or focus.

---

## 6. E2E TESTING

### E2E-WHEN: When to Use E2E Tests

**Philosophy:** E2E tests are expensive. Use them for critical user journeys, not everything.

**Code to test:**
Full application flow from login to checkout

**Strategy 1: Critical User Journeys Only**
```javascript
// Cypress E2E test
describe('E2E: Purchase Flow', () => {
  test('user can complete purchase', () => {
    // Critical path: Login -> Browse -> Add to cart -> Checkout -> Purchase
    cy.visit('/');

    // Login
    cy.get('[data-testid="login-button"]').click();
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('password');
    cy.get('button[type="submit"]').click();

    // Browse products
    cy.get('[data-testid="products"]').should('be.visible');
    cy.get('[data-testid="product-1"]').click();

    // Add to cart
    cy.get('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="cart-count"]').should('contain', '1');

    // Checkout
    cy.get('[data-testid="checkout-button"]').click();
    cy.get('input[name="cardNumber"]').type('4111111111111111');
    cy.get('button[type="submit"]').click();

    // Verify success
    cy.get('[data-testid="order-confirmation"]').should('be.visible');
  });
});
```

**When to use:**
- Critical business flows (purchase, signup, payment)
- High-value user journeys
- Integration of multiple features
- End-to-end scenarios

**When NOT to use:**
- Individual component testing
- Edge cases
- Error states
- Unit-level logic

**Strategy 2: Test Pyramid Approach**
```javascript
// Many unit tests (fast, focused)
describe('Unit: calculateTotal()', () => {
  test('calculates total correctly', () => {
    expect(calculateTotal([1, 2, 3])).toBe(6);
  });
});

// Fewer integration tests (medium speed)
describe('Integration: ShoppingCart', () => {
  test('updates total when items added', () => {
    const cart = new ShoppingCart();
    cart.addItem({ price: 10 }, 2);
    expect(cart.getTotal()).toBe(20);
  });
});

// Few E2E tests (slow, high confidence)
describe('E2E: Complete purchase flow', () => {
  test('user can purchase product', () => {
    // Full flow test
  });
});
```

**Ratio:**
- 70% Unit tests
- 20% Integration tests
- 10% E2E tests

**Pros:**
- Balanced approach
- Fast feedback from unit tests
- Confidence from E2E tests
- Maintainable

**Cons:**
- Requires discipline
- Need to decide test level

**Strategy 3: Smoke Tests (Critical Paths)**
```javascript
describe('Smoke Tests', () => {
  test('home page loads', () => {
    cy.visit('/');
    cy.get('h1').should('be.visible');
  });

  test('user can login', () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type('test@example.com');
    cy.get('input[name="password"]').type('password');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });

  test('user can search products', () => {
    cy.visit('/');
    cy.get('[data-testid="search-input"]').type('laptop');
    cy.get('[data-testid="search-button"]').click();
    cy.get('[data-testid="search-results"]').should('not.be.empty');
  });
});
```

**Pros:**
- Quick validation of critical paths
- Runs before deployment
- Catches major breaks

**Cons:**
- Not comprehensive
- Shallow coverage

**Trade-offs:**
- Use **Strategy 1** for critical business journeys
- Use **Strategy 2** (pyramid) for overall test strategy
- Use **Strategy 3** (smoke tests) for deployment validation

**Recommendation:**
Use E2E tests sparingly for critical user journeys only. Follow the test pyramid: many fast unit tests, fewer integration tests, few E2E tests. Don't test everything E2E—it's slow, expensive, and brittle. Use E2E for happy paths of critical flows.

---

### E2E-PAGE-OBJECT: Page Object Pattern

**Philosophy:** Encapsulate page structure and interactions in page objects to reduce duplication and improve maintainability.

**Code to test:**
Login flow across multiple tests

**Strategy 1: Without Page Objects (Duplication)**
```javascript
describe('Login', () => {
  test('successful login', () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('password');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });

  test('failed login shows error', () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    cy.get('[data-testid="error-message"]').should('be.visible');
  });
});
```

**Problems:**
- Duplication of selectors
- Duplication of actions
- Hard to maintain when UI changes

**Strategy 2: Page Object Pattern**
```javascript
// pageObjects/LoginPage.js
class LoginPage {
  visit() {
    cy.visit('/login');
  }

  get emailInput() {
    return cy.get('input[name="email"]');
  }

  get passwordInput() {
    return cy.get('input[name="password"]');
  }

  get submitButton() {
    return cy.get('button[type="submit"]');
  }

  get errorMessage() {
    return cy.get('[data-testid="error-message"]');
  }

  login(email, password) {
    this.emailInput.type(email);
    this.passwordInput.type(password);
    this.submitButton.click();
  }
}

export default LoginPage;

// tests/login.spec.js
import LoginPage from '../pageObjects/LoginPage';

describe('Login', () => {
  const loginPage = new LoginPage();

  test('successful login', () => {
    loginPage.visit();
    loginPage.login('user@example.com', 'password');
    cy.url().should('include', '/dashboard');
  });

  test('failed login shows error', () => {
    loginPage.visit();
    loginPage.login('user@example.com', 'wrongpassword');
    loginPage.errorMessage.should('be.visible');
  });
});
```

**Pros:**
- Centralized selectors
- Reusable actions
- Easy to update when UI changes
- More readable tests

**Cons:**
- Additional abstraction
- More files to maintain
- Can be over-engineered

**Strategy 3: Cypress Commands (Alternative)**
```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login');
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
});

// tests/login.spec.js
describe('Login', () => {
  test('successful login', () => {
    cy.login('user@example.com', 'password');
    cy.url().should('include', '/dashboard');
  });

  test('user dashboard shows correct info after login', () => {
    cy.login('user@example.com', 'password');
    cy.get('[data-testid="user-name"]').should('contain', 'User');
  });
});
```

**Pros:**
- Global custom commands
- Very concise tests
- Cypress-specific

**Cons:**
- Global namespace pollution
- Less structured than page objects
- Harder to discover available commands

**Strategy 4: Hybrid Approach**
```javascript
// Page objects for complex pages
class CheckoutPage {
  fillShippingInfo(info) {
    cy.get('input[name="address"]').type(info.address);
    cy.get('input[name="city"]').type(info.city);
    cy.get('input[name="zip"]').type(info.zip);
  }

  fillPaymentInfo(payment) {
    cy.get('input[name="cardNumber"]').type(payment.cardNumber);
    cy.get('input[name="expiry"]').type(payment.expiry);
    cy.get('input[name="cvv"]').type(payment.cvv);
  }

  submitOrder() {
    cy.get('button[type="submit"]').click();
  }
}

// Commands for common actions
Cypress.Commands.add('login', (email, password) => {
  // ...
});

// Test
describe('Checkout', () => {
  const checkoutPage = new CheckoutPage();

  test('complete purchase', () => {
    cy.login('user@example.com', 'password');

    // Add product (command)
    cy.addToCart('product-1');

    // Checkout (page object)
    checkoutPage.fillShippingInfo({ address: '123 Main', city: 'NYC', zip: '10001' });
    checkoutPage.fillPaymentInfo({ cardNumber: '4111...', expiry: '12/25', cvv: '123' });
    checkoutPage.submitOrder();

    cy.get('[data-testid="order-confirmation"]').should('be.visible');
  });
});
```

**Pros:**
- Best of both worlds
- Commands for simple actions
- Page objects for complex pages

**Cons:**
- Need to decide which pattern to use
- More complexity

**Trade-offs:**
- Avoid **Strategy 1** (duplication) for maintainability
- Use **Strategy 2** (page objects) for complex pages with many interactions
- Use **Strategy 3** (commands) for simple, reusable actions
- Use **Strategy 4** (hybrid) for large test suites (recommended)

**Recommendation:**
Use page objects for complex pages with many elements and interactions. Use custom commands for simple, frequently-used actions (login, logout). This reduces duplication and makes tests more maintainable.

---

## 7. TEST QUALITY

### QUALITY-DETERMINISTIC: Avoiding Flaky Tests

**Philosophy:** Tests should be deterministic—same code, same result, every time. Flaky tests erode trust.

**Common Flaky Test Causes:**

**Anti-Pattern 1: Time-Based Flakiness**
```javascript
// FLAKY - Depends on system time
test('cache expires after 1 second', async () => {
  const cache = new Cache({ ttl: 1000 });
  cache.set('key', 'value');

  await new Promise(resolve => setTimeout(resolve, 1100)); // Flaky!

  expect(cache.get('key')).toBeNull();
});
```

**Fixed Version (Mock Time):**
```javascript
test('cache expires after TTL', () => {
  jest.useFakeTimers();

  const cache = new Cache({ ttl: 1000 });
  cache.set('key', 'value');

  // Fast-forward time
  jest.advanceTimersByTime(1100);

  expect(cache.get('key')).toBeNull();

  jest.useRealTimers();
});
```

**Anti-Pattern 2: Order-Dependent Tests**
```javascript
// FLAKY - Tests depend on execution order
describe('ShoppingCart', () => {
  const cart = new ShoppingCart(); // Shared state!

  test('add item', () => {
    cart.addItem('Book', 1);
    expect(cart.itemCount()).toBe(1);
  });

  test('remove item', () => {
    // Assumes first test ran!
    cart.removeItem('Book');
    expect(cart.itemCount()).toBe(0); // Flaky!
  });
});
```

**Fixed Version (Test Isolation):**
```javascript
describe('ShoppingCart', () => {
  let cart;

  beforeEach(() => {
    cart = new ShoppingCart(); // Fresh instance per test
  });

  test('add item', () => {
    cart.addItem('Book', 1);
    expect(cart.itemCount()).toBe(1);
  });

  test('remove item', () => {
    cart.addItem('Book', 1); // Explicit setup
    cart.removeItem('Book');
    expect(cart.itemCount()).toBe(0);
  });
});
```

**Anti-Pattern 3: Non-Deterministic Random Data**
```javascript
// FLAKY - Random data
test('sorts numbers', () => {
  const data = Array.from({ length: 10 }, () => Math.random()); // Different each run!
  const result = mySort(data);
  expect(result).toEqual(data.sort((a, b) => a - b));
});
```

**Fixed Version (Deterministic Data):**
```javascript
test('sorts numbers', () => {
  // Fixed test data
  const data = [5, 2, 8, 1, 9, 3, 7, 4, 6];
  const result = mySort(data);
  expect(result).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9]);
});

// Or use seeded random
test('sorts random numbers deterministically', () => {
  const rng = seedrandom('my-seed'); // Deterministic random
  const data = Array.from({ length: 10 }, () => rng());
  const result = mySort(data);
  expect(result).toEqual([...data].sort((a, b) => a - b));
});
```

**Anti-Pattern 4: Async Race Conditions**
```javascript
// FLAKY - Race condition
test('loads data', async () => {
  render(<DataComponent />);

  // Doesn't wait for loading to complete!
  expect(screen.getByText('Data loaded')).toBeInTheDocument(); // Flaky!
});
```

**Fixed Version (Wait for Async):**
```javascript
test('loads data', async () => {
  render(<DataComponent />);

  // Wait for element to appear
  const element = await screen.findByText('Data loaded');
  expect(element).toBeInTheDocument();
});

// Or with waitFor
test('loads data', async () => {
  render(<DataComponent />);

  await waitFor(() => {
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
});
```

**Recommendation:**
- Mock time with jest.useFakeTimers()
- Ensure test isolation (fresh state per test)
- Use deterministic data (no Math.random without seed)
- Always await async operations
- Avoid testing timing/performance in unit tests
- Use waitFor for async DOM updates

---

### QUALITY-COVERAGE: Coverage vs Test Quality

**Philosophy:** 100% code coverage doesn't mean 100% tested. Quality matters more than quantity.

**Code to test:**
```javascript
function processPayment(amount, method, userId) {
  if (amount <= 0) {
    throw new Error('Amount must be positive');
  }

  if (!['credit', 'debit', 'paypal'].includes(method)) {
    throw new Error('Invalid payment method');
  }

  const transactionId = `TXN-${userId}-${Date.now()}`;
  logTransaction(transactionId, amount, method);

  return transactionId;
}
```

**Strategy 1: Coverage-Focused (Bad)**
```javascript
// Gets 100% coverage but doesn't verify behavior!
test('processPayment runs', () => {
  const result = processPayment(100, 'credit', 'user123');
  expect(result).toBeTruthy(); // Weak assertion!
});
```

**Why this is bad:**
- Weak assertion (any truthy value passes)
- Doesn't verify transaction ID format
- Doesn't test error cases
- Doesn't verify logging
- 100% coverage but low quality

**Strategy 2: Behavior-Focused (Good)**
```javascript
describe('processPayment()', () => {
  test('returns transaction ID with correct format', () => {
    const result = processPayment(100, 'credit', 'user123');

    expect(result).toMatch(/^TXN-user123-\d+$/);
    expect(result).toContain('user123');
  });

  test('throws error for non-positive amount', () => {
    expect(() => processPayment(0, 'credit', 'user123'))
      .toThrow('Amount must be positive');

    expect(() => processPayment(-50, 'credit', 'user123'))
      .toThrow('Amount must be positive');
  });

  test('throws error for invalid payment method', () => {
    expect(() => processPayment(100, 'bitcoin', 'user123'))
      .toThrow('Invalid payment method');
  });

  test('accepts all valid payment methods', () => {
    expect(() => processPayment(100, 'credit', 'user123')).not.toThrow();
    expect(() => processPayment(100, 'debit', 'user123')).not.toThrow();
    expect(() => processPayment(100, 'paypal', 'user123')).not.toThrow();
  });

  test('logs transaction', () => {
    const logSpy = jest.spyOn(console, 'log'); // Assuming logTransaction uses console

    processPayment(100, 'credit', 'user123');

    expect(logSpy).toHaveBeenCalled();

    logSpy.mockRestore();
  });
});
```

**Pros:**
- Tests actual behavior
- Verifies transaction ID format
- Tests all error cases
- Tests all payment methods
- High quality, not just high coverage

**Cons:**
- More test code
- Takes more thought

**Strategy 3: Mutation Testing (Advanced)**
```javascript
// Mutation testing tools (like Stryker) modify your code to check if tests catch it

// Original code
if (amount <= 0) {
  throw new Error('Amount must be positive');
}

// Mutation 1: Change <= to <
if (amount < 0) {
  throw new Error('Amount must be positive');
}

// If tests still pass, they're not thorough enough!

// Strong test that would catch this mutation
test('rejects zero amount', () => {
  expect(() => processPayment(0, 'credit', 'user123'))
    .toThrow('Amount must be positive');
});
```

**Pros:**
- Validates test quality
- Finds weak tests
- Higher confidence

**Cons:**
- Slow to run
- Additional tooling
- Can be expensive

**Key Question:**
"If I break this code, will my tests catch it?"

**Trade-offs:**
- Don't chase **Strategy 1** (100% coverage with weak assertions)
- Use **Strategy 2** (behavior-focused) for quality tests
- Use **Strategy 3** (mutation testing) for critical code

**Recommendation:**
Don't chase 100% coverage—chase meaningful behavior verification. Write tests that would fail if the code was wrong in important ways. Test error cases and edge cases, not just happy paths. Ask: "If I introduce a bug, will this test catch it?"

---

## Contract & Service Testing Patterns

### CONTRACT-CONSUMER: Pact-style Contracts

```javascript
import { Pact } from '@pact-foundation/pact';

const provider = new Pact({ consumer: 'WebApp', provider: 'OrderAPI' });

describe('OrderAPI contract', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it('returns order details', async () => {
    await provider.addInteraction({
      state: 'order 42 exists',
      uponReceiving: 'GET /orders/42',
      withRequest: { method: 'GET', path: '/orders/42' },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          id: 42,
          total: Pact.Matchers.like(199.99),
          status: Pact.Matchers.term({ matcher: '^(paid|shipped)$', generate: 'paid' }),
        },
      },
    });

    const order = await api.getOrder(42);
    expect(order).toMatchObject({ id: 42, status: 'paid' });
  });
});
```

- Publish contracts to a broker and fail the CI build if the provider hasn't verified them.

### CONTRACT-PROVIDER: Provider Verification

```javascript
import { Verifier } from '@pact-foundation/pact';

await new Verifier({
  providerBaseUrl: process.env.API_URL,
  pactBrokerUrl: process.env.PACT_BROKER_URL,
  publishVerificationResult: true,
  providerVersion: process.env.GIT_SHA,
}).verifyProvider();
```

- Run this as part of backend CI/CD to guarantee backward compatibility.

### CONTRACT-SCHEMA: JSON Schema/OpenAPI Validation

```javascript
import Ajv from 'ajv';
const ajv = new Ajv({ strict: true });
const validate = ajv.compile(orderSchema);

const res = await request(app).get('/orders/42');
expect(validate(res.body)).toBe(true);
```

- Use when Pact is overkill but you still want schema drift detection.

### CONTRACT-MONITOR: Production Canaries

- Schedule synthetic monitors (Checkly, Pingdom, CloudWatch Synthetics) that call real endpoints with fixture data and validate schema.
- Alert on SLA breaches or payload mismatches.

## Summary

JavaScript/TypeScript testing emphasizes:

1. **User-Centric Testing** - Test behavior users care about, not implementation
2. **AAA Pattern** - Clear test structure (Arrange, Act, Assert)
3. **Testing Library Principles** - Query by role, label, text (not test IDs)
4. **async/await** - Properly handle async code
5. **Minimal Mocking** - Mock at boundaries, not in the middle
6. **userEvent** - Simulate realistic user interactions
7. **Test Pyramid** - Many unit tests, fewer integration, few E2E
8. **Deterministic Tests** - No flakiness, mock time and randomness
9. **Quality over Coverage** - Meaningful assertions over percentage

---

Remember: Good tests are **readable, reliable, fast, and meaningful**. They test behavior from the user's perspective, not implementation details. They give confidence that code works and catch bugs when it doesn't.

**Testing Wisdom:**
> "Write tests. Not too many. Mostly integration." - Kent C. Dodds
> "The more your tests resemble the way your software is used, the more confidence they can give you." - Testing Library
