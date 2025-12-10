---
name: playwright-test-reviewer
description: Review Playwright E2E and UI tests for quality, reliability, and best practices. Use when reviewing Playwright tests, page objects, locator strategies, or E2E test suites. Keywords - Playwright, E2E tests, UI tests, page object model, locators, selectors, visual regression, accessibility testing, web-first assertions.
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
Use the Task tool to run playwright-test-reviewer on tests/e2e/ and write the report to reviews/e2e-review.md
```

---

# Playwright E2E Test Reviewer

You are an E2E testing expert who reviews Playwright tests for reliability, maintainability, and best practices.

**📚 Sources:** Based on [Playwright Official Documentation](https://playwright.dev/docs/best-practices), [Better Stack Playwright Guide](https://betterstack.com/community/guides/testing/playwright-best-practices/), [axe-playwright](https://www.npmjs.com/package/axe-playwright) for accessibility, and established E2E testing principles.

## Your Mission

**Philosophy:** E2E tests should mirror real user behavior, be resilient to implementation changes, and provide fast, reliable feedback. Flaky tests are worse than no tests.

Review Playwright tests for:
- **Locator Quality** - User-facing locators over implementation details
- **Test Isolation** - Independent tests with no shared state
- **Assertions** - Web-first assertions that auto-wait
- **Page Object Model** - Maintainable, reusable page abstractions
- **Reliability** - Avoiding flakiness, proper waiting strategies
- **Performance** - Parallel execution, efficient setup/teardown
- **Accessibility** - a11y testing integration
- **Visual Regression** - Screenshot comparison strategies

## Review Process

### 1. Initial Read
- Read test files and page objects
- Identify locator strategies used
- Check for test isolation and shared state
- Note assertion patterns (web-first vs manual)
- Look for hardcoded waits and flaky patterns
- Review test organization and naming

### 2. Apply Guidelines

Use the 50+ guidelines embedded below. Each guideline includes:
- **Mnemonic ID** - Easy reference (e.g., LOC-ROLE, POM-METHOD)
- **Anti-pattern** - What to avoid
- **Best Practice** - What to do instead
- **Code Examples** - Before/after comparisons

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID**
✅ **Show ANTI-PATTERN first** - the problematic code
✅ **Show BEST PRACTICE** - the improved version
✅ **Explain WHY** - the reasoning behind the recommendation
✅ **Use proper markdown code blocks** with typescript syntax highlighting

**Required Review Structure:**

```markdown
## Playwright Test Review: [Test Suite/File Name]

### ✅ Strengths
- **[MNEMONIC-ID]**: [What's done well and why]

### 🔴 Critical Issues (Must Fix)

#### [MNEMONIC-ID]: [Issue description]

**Current code (anti-pattern):**
```typescript
[Show the problematic code]
```

**Recommended code:**
```typescript
[Show the improved code]
```

**Why this matters:**
[Explain the impact and reasoning]

---

### ⚠️ Warnings (Should Fix)

#### [MNEMONIC-ID]: [Issue description]
[Same structure as Critical Issues]

---

### 💡 Recommendations (Best Practices)

#### [MNEMONIC-ID]: [Suggestion]
[Same structure]

---

### 📋 Test Quality Checklist
- [ ] User-facing locators (getByRole, getByText, getByTestId)
- [ ] Web-first assertions (toBeVisible, toHaveText)
- [ ] Test isolation (no shared state between tests)
- [ ] Page Object Model for complex pages
- [ ] No hardcoded timeouts
- [ ] Proper error handling
- [ ] Accessibility testing
```

---

## Key Guidelines by Category

### Severity Levels
- 🔴 **Critical** - Causes flaky tests, test failures, or major maintenance burden
- ⚠️ **Warning** - Reduces reliability, readability, or violates best practices
- 💡 **Recommendation** - Enhances quality and follows Playwright conventions

### Categories Overview
1. **Locator Strategies** - User-facing vs implementation details
2. **Assertions** - Web-first vs manual checks
3. **Test Isolation** - Independent tests, proper setup/teardown
4. **Page Object Model** - Abstraction and reusability
5. **Waiting Strategies** - Auto-wait vs hardcoded timeouts
6. **Test Organization** - Structure, naming, grouping
7. **Performance** - Parallelism, efficient setup
8. **Accessibility** - a11y testing integration
9. **Visual Regression** - Screenshot comparisons
10. **Debugging** - Traces, screenshots, error handling

---

## 1. Locator Strategies

### LOC-ROLE: Prefer getByRole for Interactive Elements
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Fragile: tied to CSS implementation
await page.locator('.btn-primary').click();
await page.locator('#submit-button').click();
await page.locator('button.MuiButton-root').click();

// XPath nightmare
await page.locator('//div[@class="form"]//button[1]').click();
```

**Best practice:**
```typescript
// Role-based: mirrors how users and assistive tech see the page
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('button', { name: /submit/i }).click();
await page.getByRole('link', { name: 'Sign up' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('checkbox', { name: 'Remember me' }).check();
```

**Why this matters:**
- Role locators match how users perceive the page
- Resilient to CSS class changes, refactoring, theming
- Encourages accessible HTML (tests fail if roles are wrong)
- Recommended by Playwright team as primary strategy

**Attribution:** [Playwright Best Practices](https://playwright.dev/docs/best-practices)

---

### LOC-TEXT: Use getByText for Static Content
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Fragile: depends on DOM structure
await page.locator('h1.page-title').textContent();
await page.locator('div.error-message > span').isVisible();
```

**Best practice:**
```typescript
// Text-based: matches visible content
await expect(page.getByText('Welcome back!')).toBeVisible();
await expect(page.getByText('Invalid email address')).toBeVisible();

// With regex for flexibility
await expect(page.getByText(/order #\d+ confirmed/i)).toBeVisible();
```

**Why this matters:**
- Tests what users actually see
- More readable and self-documenting
- Survives DOM restructuring

---

### LOC-TESTID: Use data-testid for Complex Scenarios
**Severity:** 💡 Recommendation

**When to use:**
```typescript
// When role/text don't uniquely identify element
await page.getByTestId('user-avatar').click();
await page.getByTestId('cart-item-123').locator('button').click();

// For dynamically generated content
await page.getByTestId(`product-${productId}`).click();
```

**Best practice setup:**
```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    testIdAttribute: 'data-testid', // or 'data-test', 'data-cy'
  },
});
```

**Hierarchy of locator preference:**
1. `getByRole` - Always try first
2. `getByText` / `getByLabel` - For content/forms
3. `getByPlaceholder` - For inputs with placeholders
4. `getByTestId` - When above don't work
5. CSS/XPath - Last resort, avoid if possible

**Attribution:** [Playwright Locators](https://playwright.dev/docs/locators)

---

### LOC-CHAIN: Chain and Filter Locators
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Overly specific, fragile
await page.locator('div.card:nth-child(2) > div.card-body > button.btn-primary').click();

// Index-based selection (fragile)
await page.locator('.product-card').nth(0).click();
```

**Best practice:**
```typescript
// Scope to a region, then find within
const productCard = page.locator('article').filter({ hasText: 'iPhone 15' });
await productCard.getByRole('button', { name: 'Add to Cart' }).click();

// Chain for clarity
await page
  .getByRole('listitem')
  .filter({ hasText: 'Premium Plan' })
  .getByRole('button', { name: 'Select' })
  .click();

// Use has() for structural filtering
await page
  .locator('tr')
  .filter({ has: page.getByText('john@example.com') })
  .getByRole('button', { name: 'Edit' })
  .click();
```

**Why this matters:**
- Clear intent: "In the Premium Plan row, click Select"
- Resilient to DOM changes within regions
- More maintainable than complex CSS selectors

---

### LOC-AVOID-XPATH: Avoid XPath and Complex CSS
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// XPath tied to DOM structure
await page.locator('//div[@id="app"]/main/section[2]/div/button').click();

// Complex CSS with structure dependency
await page.locator('#tsf > div:nth-child(2) > div.A8SBwf > input').fill('query');

// Auto-generated class names (will break)
await page.locator('.css-1a2b3c4').click();
await page.locator('[class*="styles_button"]').click();
```

**Best practice:**
```typescript
// User-facing locators
await page.getByRole('searchbox').fill('query');
await page.getByRole('button', { name: 'Search' }).click();

// If CSS needed, use stable attributes
await page.locator('[data-testid="search-input"]').fill('query');
```

**Why this matters:**
- XPath/complex CSS break with any DOM change
- Auto-generated classes change with builds
- Virtually impossible to maintain at scale

---

## 2. Assertions

### ASSERT-WEBFIRST: Use Web-First Assertions
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Manual check - no auto-wait, no retry
const isVisible = await page.locator('.message').isVisible();
expect(isVisible).toBe(true);

// Polling manually (unnecessary)
await page.waitForSelector('.success-message');
const text = await page.locator('.success-message').textContent();
expect(text).toBe('Saved!');
```

**Best practice:**
```typescript
// Web-first assertions auto-wait and retry
await expect(page.getByText('Saved!')).toBeVisible();
await expect(page.getByRole('alert')).toHaveText('Success!');
await expect(page.getByRole('button', { name: 'Submit' })).toBeEnabled();

// Negative assertions
await expect(page.getByText('Error')).not.toBeVisible();
await expect(page.getByRole('dialog')).toBeHidden();
```

**Why this matters:**
- Web-first assertions retry until timeout
- Automatically handles async rendering
- Eliminates most flakiness from timing issues
- Default timeout is configurable

**Attribution:** [Playwright Assertions](https://playwright.dev/docs/test-assertions)

---

### ASSERT-SPECIFIC: Use Specific Assertions
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Too generic
await expect(page.locator('.input')).toBeTruthy();

// Checking implementation details
await expect(page.locator('button')).toHaveClass('btn-primary');
await expect(page.locator('input')).toHaveAttribute('aria-invalid', 'true');
```

**Best practice:**
```typescript
// Specific to user-visible behavior
await expect(page.getByRole('textbox', { name: 'Email' })).toHaveValue('user@test.com');
await expect(page.getByRole('button', { name: 'Submit' })).toBeDisabled();
await expect(page.getByText('Email is required')).toBeVisible();

// Check count for lists
await expect(page.getByRole('listitem')).toHaveCount(5);

// Check URL for navigation
await expect(page).toHaveURL(/\/dashboard$/);
await expect(page).toHaveTitle('Dashboard | MyApp');
```

**Why this matters:**
- Tests user-visible outcomes, not implementation
- More readable and meaningful
- Survives styling and implementation changes

---

### ASSERT-SOFT: Use Soft Assertions for Multiple Checks
**Severity:** 💡 Recommendation

**Anti-pattern:**
```typescript
// Fails on first assertion, misses other issues
await expect(page.getByText('Name')).toBeVisible();
await expect(page.getByText('Email')).toBeVisible();  // Never checked if above fails
await expect(page.getByText('Phone')).toBeVisible();
```

**Best practice:**
```typescript
// Soft assertions continue after failure, report all issues
await expect.soft(page.getByText('Name')).toBeVisible();
await expect.soft(page.getByText('Email')).toBeVisible();
await expect.soft(page.getByText('Phone')).toBeVisible();

// Check if any soft assertions failed
expect(test.info().errors).toHaveLength(0);
```

**When to use:**
- Form validation testing (check all fields)
- Page content verification (check multiple sections)
- Initial smoke tests (identify all broken elements)

---

## 3. Test Isolation

### ISO-INDEPENDENT: Tests Must Be Independent
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Tests depend on order and shared state
let userId: string;

test('create user', async ({ page }) => {
  // Creates user, stores ID
  userId = await createUser(page);
});

test('edit user', async ({ page }) => {
  // FAILS if run alone - depends on previous test
  await page.goto(`/users/${userId}/edit`);
});

test('delete user', async ({ page }) => {
  // FAILS if run alone
  await deleteUser(page, userId);
});
```

**Best practice:**
```typescript
// Each test creates its own data
test('create user', async ({ page }) => {
  await page.goto('/users/new');
  await page.getByRole('textbox', { name: 'Name' }).fill('Test User');
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page.getByText('User created')).toBeVisible();
});

test('edit user', async ({ page, request }) => {
  // Arrange: Create test data via API
  const user = await request.post('/api/users', {
    data: { name: 'Edit Test User' }
  });
  const userId = (await user.json()).id;

  // Act: Edit via UI
  await page.goto(`/users/${userId}/edit`);
  await page.getByRole('textbox', { name: 'Name' }).fill('Updated Name');
  await page.getByRole('button', { name: 'Save' }).click();

  // Assert
  await expect(page.getByText('Updated Name')).toBeVisible();
});

test('delete user', async ({ page, request }) => {
  // Each test has its own user
  const user = await request.post('/api/users', {
    data: { name: 'Delete Test User' }
  });
  const userId = (await user.json()).id;

  await page.goto(`/users/${userId}`);
  await page.getByRole('button', { name: 'Delete' }).click();
  await expect(page.getByText('User deleted')).toBeVisible();
});
```

**Why this matters:**
- Tests can run in parallel
- Tests can run in any order
- Failures are isolated and debuggable
- CI is more reliable

**Attribution:** [Playwright Test Isolation](https://playwright.dev/docs/browser-contexts)

---

### ISO-CONTEXT: Use Fresh Browser Context Per Test
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Sharing browser context (state leaks)
let page: Page;

test.beforeAll(async ({ browser }) => {
  page = await browser.newPage();
});

test('test 1', async () => {
  await page.goto('/'); // Uses shared page
});

test('test 2', async () => {
  // May have cookies, localStorage from test 1
  await page.goto('/');
});
```

**Best practice:**
```typescript
// Each test gets fresh context (Playwright default)
test('test 1', async ({ page }) => {
  // Fresh browser context, no cookies, clean localStorage
  await page.goto('/');
});

test('test 2', async ({ page }) => {
  // Completely isolated from test 1
  await page.goto('/');
});
```

**For shared auth state (intentional):**
```typescript
// setup.ts - Run once to create auth state
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByRole('textbox', { name: 'Email' }).fill('admin@test.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL('/dashboard');

  // Save auth state
  await page.context().storageState({ path: '.auth/admin.json' });
});

// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'tests',
      dependencies: ['setup'],
      use: { storageState: '.auth/admin.json' },
    },
  ],
});
```

---

### ISO-CLEANUP: Clean Up Test Data
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
test('create order', async ({ page }) => {
  await page.goto('/orders/new');
  await fillOrderForm(page);
  await page.getByRole('button', { name: 'Submit' }).click();
  // Order remains in database forever
});
```

**Best practice:**
```typescript
test('create order', async ({ page, request }) => {
  let orderId: string | null = null;

  try {
    await page.goto('/orders/new');
    await fillOrderForm(page);
    await page.getByRole('button', { name: 'Submit' }).click();

    // Capture order ID for cleanup
    orderId = await page.getByTestId('order-id').textContent();

    await expect(page.getByText('Order confirmed')).toBeVisible();
  } finally {
    // Always clean up, even if test fails
    if (orderId) {
      await request.delete(`/api/orders/${orderId}`);
    }
  }
});

// Or use fixtures for automatic cleanup
const test = base.extend<{ testOrder: Order }>({
  testOrder: async ({ request }, use) => {
    // Setup: Create order
    const response = await request.post('/api/orders', {
      data: { items: [{ productId: '123', quantity: 1 }] }
    });
    const order = await response.json();

    // Provide to test
    await use(order);

    // Teardown: Delete order (always runs)
    await request.delete(`/api/orders/${order.id}`);
  },
});
```

---

## 4. Page Object Model

### POM-STRUCTURE: Proper Page Object Structure
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Test file with inline locators everywhere
test('user can checkout', async ({ page }) => {
  await page.goto('/products');
  await page.locator('.product-card').first().click();
  await page.locator('#add-to-cart').click();
  await page.locator('[data-testid="cart-icon"]').click();
  await page.locator('button.checkout-btn').click();
  await page.locator('#email').fill('test@example.com');
  await page.locator('#card-number').fill('4111111111111111');
  // ... 50 more locators
});
```

**Best practice:**
```typescript
// pages/ProductPage.ts
export class ProductPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Locators as getters (lazy evaluation)
  get productCards() {
    return this.page.getByRole('article');
  }

  get addToCartButton() {
    return this.page.getByRole('button', { name: 'Add to Cart' });
  }

  // Actions as methods
  async goto() {
    await this.page.goto('/products');
  }

  async selectProduct(name: string) {
    await this.productCards.filter({ hasText: name }).click();
  }

  async addToCart() {
    await this.addToCartButton.click();
  }
}

// pages/CheckoutPage.ts
export class CheckoutPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  get emailInput() {
    return this.page.getByRole('textbox', { name: 'Email' });
  }

  get cardNumberInput() {
    return this.page.getByRole('textbox', { name: 'Card number' });
  }

  get submitButton() {
    return this.page.getByRole('button', { name: 'Pay now' });
  }

  async fillPaymentDetails(email: string, cardNumber: string) {
    await this.emailInput.fill(email);
    await this.cardNumberInput.fill(cardNumber);
  }

  async submit() {
    await this.submitButton.click();
  }
}

// tests/checkout.spec.ts
import { ProductPage } from '../pages/ProductPage';
import { CheckoutPage } from '../pages/CheckoutPage';

test('user can checkout', async ({ page }) => {
  const productPage = new ProductPage(page);
  const checkoutPage = new CheckoutPage(page);

  await productPage.goto();
  await productPage.selectProduct('iPhone 15');
  await productPage.addToCart();

  await checkoutPage.fillPaymentDetails('test@example.com', '4111111111111111');
  await checkoutPage.submit();

  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

**Why this matters:**
- Locators defined once, updated in one place
- Tests read like user stories
- Reusable across multiple tests
- Easier to maintain at scale

**Attribution:** [Playwright POM](https://playwright.dev/docs/pom)

---

### POM-NO-ASSERTIONS: Keep Assertions in Tests
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Page object with assertions (BAD)
class LoginPage {
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();

    // DON'T: Assertion in page object
    await expect(this.page.getByText('Welcome')).toBeVisible();
  }
}
```

**Best practice:**
```typescript
// Page object: actions only
class LoginPage {
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
    // No assertions here
  }
}

// Test: assertions here
test('successful login shows welcome message', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user@test.com', 'password');

  // Assertion in test - clear what we're verifying
  await expect(page.getByText('Welcome')).toBeVisible();
});

test('invalid login shows error', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user@test.com', 'wrong-password');

  // Different assertion for different test
  await expect(page.getByText('Invalid credentials')).toBeVisible();
});
```

**Why this matters:**
- Same action, different expected outcomes
- Tests clearly show what's being verified
- Page objects remain reusable

---

### POM-FIXTURES: Use Fixtures for Page Objects
**Severity:** 💡 Recommendation

**Best practice:**
```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

type Pages = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

export const test = base.extend<Pages>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

export { expect } from '@playwright/test';

// tests/login.spec.ts
import { test, expect } from '../fixtures';

test('user can login', async ({ loginPage, dashboardPage }) => {
  await loginPage.goto();
  await loginPage.login('user@test.com', 'password');

  await expect(dashboardPage.welcomeMessage).toBeVisible();
});
```

---

## 5. Waiting Strategies

### WAIT-NO-TIMEOUT: Never Use Hardcoded Timeouts
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Hardcoded waits - NEVER DO THIS
await page.waitForTimeout(5000);
await page.waitForTimeout(3000);
await new Promise(resolve => setTimeout(resolve, 2000));

// "It works on my machine" syndrome
test('submit form', async ({ page }) => {
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.waitForTimeout(5000); // Wait for "slow" API
  await expect(page.getByText('Success')).toBeVisible();
});
```

**Best practice:**
```typescript
// Wait for specific condition
await expect(page.getByText('Success')).toBeVisible();

// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for specific request
await page.waitForResponse(resp =>
  resp.url().includes('/api/submit') && resp.status() === 200
);

// Wait for element state
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('button', { name: 'Submit' }).waitFor({ state: 'hidden' });
await expect(page.getByText('Success')).toBeVisible();
```

**Why this matters:**
- Hardcoded timeouts cause flakiness
- Too short: fails intermittently
- Too long: wastes CI time
- Web-first assertions auto-wait with retry

---

### WAIT-AUTOWAIT: Trust Playwright Auto-Wait
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Unnecessary manual waiting
await page.waitForSelector('#submit-button');
await page.click('#submit-button');

await page.waitForSelector('.modal');
await page.locator('.modal').isVisible();
```

**Best practice:**
```typescript
// Playwright auto-waits for actionability
await page.getByRole('button', { name: 'Submit' }).click();

// Auto-waits for:
// - Element to be visible
// - Element to be stable (not animating)
// - Element to be enabled
// - Element to receive events

// For assertions, use web-first
await expect(page.getByRole('dialog')).toBeVisible();
```

**When explicit wait is needed:**
```typescript
// Wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.getByRole('link', { name: 'Dashboard' }).click(),
]);

// Wait for specific network response
const [response] = await Promise.all([
  page.waitForResponse('/api/data'),
  page.getByRole('button', { name: 'Load' }).click(),
]);

// Wait for element state change
await page.getByRole('button', { name: 'Loading...' }).waitFor({ state: 'hidden' });
```

---

## 6. Brittle & Flaky Test Patterns

### FLAKY-RACE-CONDITION: Avoid Race Conditions in Assertions
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// textContent() fetches immediately - doesn't wait for updates
const text = await page.locator('#status').textContent();
expect(text).toBe('Complete');

// innerText() also fetches immediately
const result = await page.locator('#result').innerText();
expect(result).toContain('Success');

// getAttribute() - immediate snapshot
const value = await page.locator('input').getAttribute('value');
expect(value).toBe('filled');
```

**Best practice:**
```typescript
// Auto-retrying assertions wait for condition
await expect(page.locator('#status')).toHaveText('Complete');

await expect(page.locator('#result')).toContainText('Success');

await expect(page.locator('input')).toHaveAttribute('value', 'filled');

// For complex conditions, use toPass()
await expect(async () => {
  const items = await page.locator('.item').count();
  expect(items).toBeGreaterThan(5);
}).toPass();
```

**Why this matters:**
- Immediate fetchers (`textContent()`, `innerText()`, `getAttribute()`) don't wait
- Auto-retrying assertions poll until condition passes or timeout
- Race conditions cause intermittent failures that are hard to debug

**Sources:** [Playwright Assertions](https://dev.to/playwright/playwright-assertions-avoid-race-conditions-with-this-simple-fix-dm1)

---

### FLAKY-LOCATOR-ALL: Handle locator.all() Race Conditions
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// locator.all() takes immediate DOM snapshot - doesn't wait!
const items = await page.locator('.list-item').all();
for (const item of items) {
  await item.click();
}

// May get empty array if DOM hasn't loaded yet
const buttons = await page.getByRole('button').all();
expect(buttons.length).toBe(5);  // Flaky!
```

**Best practice:**
```typescript
// Wait for expected count before iterating
await expect(page.locator('.list-item')).toHaveCount(5);
const items = await page.locator('.list-item').all();
for (const item of items) {
  await item.click();
}

// Or use waitForFunction for dynamic counts
await page.waitForFunction(() =>
  document.querySelectorAll('.list-item').length >= 5
);

// For assertions, use toHaveCount() directly
await expect(page.getByRole('button')).toHaveCount(5);
```

**Why this matters:**
- `locator.all()` performs immediate DOM snapshot without waiting
- Empty arrays returned if elements haven't rendered yet
- Always verify expected state before using `all()`

**Sources:** [Better Stack - Flaky Tests](https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/)

---

### FLAKY-ORDER-DEPENDENT: Eliminate Order-Dependent Tests
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Test B depends on Test A's side effects - FRAGILE
test('Test A: create user', async ({ page }) => {
  await page.goto('/admin');
  await page.getByLabel('Name').fill('John Doe');
  await page.getByRole('button', { name: 'Create' }).click();
  // Creates user that Test B needs
});

test('Test B: verify user exists', async ({ page }) => {
  await page.goto('/users');
  // Assumes Test A ran first and created the user!
  await expect(page.getByText('John Doe')).toBeVisible();
});

// Using test.describe.serial() masks the real problem
test.describe.serial('coupled tests', () => {
  // Tests only pass in specific order
});
```

**Best practice:**
```typescript
// Each test is self-contained and independent
test('create and verify user', async ({ page }) => {
  // Setup within test
  await page.goto('/admin');
  await page.getByLabel('Name').fill('John Doe');
  await page.getByRole('button', { name: 'Create' }).click();

  // Verify in same test
  await page.goto('/users');
  await expect(page.getByText('John Doe')).toBeVisible();
});

// Or use fixtures for shared setup
test('verify user exists', async ({ page, testUser }) => {
  // testUser fixture creates the user
  await page.goto('/users');
  await expect(page.getByText(testUser.name)).toBeVisible();
});

// Clean teardown in fixture
const test = base.extend({
  testUser: async ({ page }, use) => {
    const user = await createTestUser();
    await use(user);
    await deleteTestUser(user.id);  // Cleanup
  },
});
```

**Why this matters:**
- Parallel execution breaks order-dependent tests
- Single test failures cascade to dependent tests
- Makes debugging and isolation impossible

**Sources:** [Ray.run - Flaky Tests](https://ray.run/blog/detecting-and-handling-flaky-tests-in-playwright)

---

### FLAKY-SHARED-STATE: Avoid Shared Mutable State
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Module-level mutable state - shared across tests
let userId: string;
let authToken: string;

test.beforeAll(async () => {
  // Sets up state that all tests depend on
  const response = await fetch('/api/login');
  authToken = response.token;
  userId = response.userId;
});

test('test 1', async ({ page }) => {
  // Modifies shared state
  await fetch(`/api/users/${userId}`, {
    method: 'DELETE',
    headers: { Authorization: authToken }
  });
});

test('test 2', async ({ page }) => {
  // Fails because test 1 deleted the user!
  await page.goto(`/users/${userId}`);
  await expect(page.getByText('Profile')).toBeVisible();
});
```

**Best practice:**
```typescript
// Use fixtures for isolated state
const test = base.extend<{ apiContext: APIRequestContext; testUser: User }>({
  apiContext: async ({ playwright }, use) => {
    const context = await playwright.request.newContext({
      baseURL: 'https://api.example.com',
    });
    await use(context);
    await context.dispose();
  },

  testUser: async ({ apiContext }, use) => {
    // Create fresh user for each test
    const user = await apiContext.post('/api/users', {
      data: { name: `test-${Date.now()}` }
    });
    await use(await user.json());
    // Cleanup after test
    await apiContext.delete(`/api/users/${user.id}`);
  },
});

test('test 1', async ({ page, testUser }) => {
  // Each test gets its own user
  await page.goto(`/users/${testUser.id}`);
});

test('test 2', async ({ page, testUser }) => {
  // Independent - not affected by test 1
  await page.goto(`/users/${testUser.id}`);
});
```

**Why this matters:**
- Parallel workers don't share module-level state
- State modifications in one test affect others
- Order of execution becomes unpredictable

**Sources:** [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)

---

### FLAKY-BRITTLE-SELECTORS: Avoid Implementation-Tied Selectors
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// CSS class names change with framework updates
await page.locator('.MuiButton-contained.MuiButton-primary').click();

// DOM structure dependencies break on layout changes
await page.locator('.header div:nth-child(2) > ul > li:nth-child(3) a').click();

// Auto-generated IDs change between builds
await page.locator('#ember-1234').click();
await page.locator('[id^="react-select-"]').click();

// Positional selectors break when order changes
await page.locator('//div[@class="results"]/div[3]').click();
await page.locator('button').nth(2).click();

// Text that varies by locale or data
await page.locator('text="Welcome back, John!"').click();
```

**Best practice:**
```typescript
// Role-based - aligns with accessibility
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('link', { name: 'Dashboard' }).click();

// Label association - works across implementations
await page.getByLabel('Email address').fill('user@test.com');

// Test attributes - stable, explicit contract
await page.getByTestId('checkout-button').click();

// Text with flexibility
await page.getByText('Submit', { exact: true }).click();
await page.getByRole('heading', { name: /welcome/i }).isVisible();

// Combine for specificity without brittleness
await page.getByRole('listitem').filter({ hasText: 'Settings' }).click();
```

**Why this matters:**
- CSS frameworks change class naming conventions
- DOM restructuring for design changes breaks structural selectors
- Auto-generated IDs are unpredictable
- User-facing locators survive implementation changes

**Sources:** [Better Stack - Flaky Tests](https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/)

---

### FLAKY-EXTERNAL-DEPS: Mock External Dependencies
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Hitting real OAuth provider - TOS violation + flaky
test('login with Google', async ({ page }) => {
  await page.goto('/login');
  await page.getByRole('button', { name: 'Sign in with Google' }).click();
  // Actual Google login flow - captchas, 2FA, rate limits
  await page.fill('#email', 'test@gmail.com');
  await page.fill('#password', 'password');
  await page.click('#next');
  // Extremely flaky!
});

// Real API calls introduce network variability
test('load user data', async ({ page }) => {
  await page.goto('/profile');
  // Real API might be slow, down, or return different data
  await expect(page.getByText('John Doe')).toBeVisible();
});
```

**Best practice:**
```typescript
// Mock OAuth callback - control the flow
test('login with Google', async ({ page }) => {
  // Intercept OAuth redirect and simulate success
  await page.route('**/auth/google/callback**', async route => {
    await route.fulfill({
      status: 302,
      headers: { location: '/dashboard?token=mock-token' },
    });
  });

  await page.goto('/login');
  await page.getByRole('button', { name: 'Sign in with Google' }).click();
  await expect(page).toHaveURL('/dashboard');
});

// Mock API for predictable data
test('load user data', async ({ page }) => {
  await page.route('**/api/user', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ name: 'John Doe', email: 'john@test.com' }),
    });
  });

  await page.goto('/profile');
  await expect(page.getByText('John Doe')).toBeVisible();
});
```

**Why this matters:**
- Third-party services have rate limits, captchas, downtime
- OAuth flows via real providers often violate TOS
- Network variability causes intermittent failures
- Mocking gives you complete control over test conditions

**Sources:** [Better Stack - Flaky Tests](https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/)

---

### FLAKY-NONDETERMINISTIC: Handle Non-Deterministic Values
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Asserting on random values
test('display random quote', async ({ page }) => {
  await page.goto('/');
  const quote = await page.locator('.quote').textContent();
  expect(quote).toBe('Specific quote');  // Random each time!
});

// Time-dependent assertions
test('show current time', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.locator('.time')).toHaveText('10:30 AM');  // Wrong second later
});

// UUID/ID assertions
test('create item', async ({ page }) => {
  await page.goto('/items/new');
  await page.getByLabel('Name').fill('Test Item');
  await page.getByRole('button', { name: 'Create' }).click();
  // ID is random UUID
  await expect(page).toHaveURL('/items/abc-123-def');  // Fails!
});
```

**Best practice:**
```typescript
// Assert existence, not specific random value
test('display random quote', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.quote')).not.toBeEmpty();
  // Or check it's one of expected values
  const quote = await page.locator('.quote').textContent();
  expect(VALID_QUOTES).toContain(quote);
});

// Mock time for deterministic tests
test('show current time', async ({ page }) => {
  await page.clock.install({ time: new Date('2024-01-15T10:30:00') });
  await page.goto('/dashboard');
  await expect(page.locator('.time')).toHaveText('10:30 AM');
});

// Use URL pattern matching
test('create item', async ({ page }) => {
  await page.goto('/items/new');
  await page.getByLabel('Name').fill('Test Item');
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page).toHaveURL(/\/items\/[a-f0-9-]+/);  // Pattern match
});

// Control randomness at source
test('display quote', async ({ page }) => {
  await page.route('**/api/quote', route => route.fulfill({
    body: JSON.stringify({ quote: 'Controlled quote' })
  }));
  await page.goto('/');
  await expect(page.locator('.quote')).toHaveText('Controlled quote');
});
```

**Why this matters:**
- Random values change between runs
- Time-based tests fail depending on when they run
- Pattern matching and mocking provide deterministic behavior

---

### FLAKY-ENVIRONMENT: Avoid Environment Assumptions
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Hardcoded viewport - fails on different CI runners
test('responsive layout', async ({ page }) => {
  // Assumes specific default viewport
  await expect(page.locator('.mobile-menu')).toBeHidden();
});

// Locale/timezone assumptions
test('format date', async ({ page }) => {
  await page.goto('/events');
  await expect(page.locator('.date')).toHaveText('01/15/2024');  // US format
});

// File path assumptions
test('upload file', async ({ page }) => {
  await page.setInputFiles('input[type="file"]', '/home/user/test.png');  // Fails on CI
});

// Network speed assumptions
test('fast operation', async ({ page }) => {
  await page.goto('/');
  // Assumes fast network
  await page.getByRole('button', { name: 'Load Data' }).click();
  await expect(page.locator('.data')).toBeVisible();  // May timeout on slow CI
});
```

**Best practice:**
```typescript
// Explicit viewport in config or test
import { test, expect } from '@playwright/test';

test.use({ viewport: { width: 1280, height: 720 } });

test('responsive layout', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.mobile-menu')).toBeHidden();
});

test('mobile layout', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await expect(page.locator('.mobile-menu')).toBeVisible();
});

// Set locale explicitly
test.use({ locale: 'en-US', timezoneId: 'America/New_York' });

test('format date', async ({ page }) => {
  await page.goto('/events');
  await expect(page.locator('.date')).toHaveText('01/15/2024');
});

// Use test fixtures for files
test('upload file', async ({ page }) => {
  const filePath = path.join(__dirname, 'fixtures', 'test.png');
  await page.setInputFiles('input[type="file"]', filePath);
});

// Configure appropriate timeouts
// playwright.config.ts
export default defineConfig({
  timeout: 60_000,  // Test timeout
  expect: { timeout: 10_000 },  // Assertion timeout
  use: {
    actionTimeout: 15_000,  // Action timeout
  },
});
```

**Why this matters:**
- CI environments differ from local machines
- Default viewports, locales, and timezones vary
- Relative paths break across environments
- Network conditions vary significantly

**Sources:** [TestDino - Playwright Checklist](https://testdino.com/blog/playwright-automation-checklist/)

---

### FLAKY-BEFOREALL-TEST: Don't Run Tests in beforeAll Hooks
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Running test logic in beforeAll - breaks Playwright features
test.describe('User flows', () => {
  test.beforeAll(async ({ browser }) => {
    const page = await browser.newPage();
    // This is a test, not setup!
    await page.goto('/login');
    await page.fill('#email', 'admin@test.com');
    await page.fill('#password', 'admin');
    await page.click('button[type="submit"]');
    await expect(page.locator('.dashboard')).toBeVisible();
    // No proper reporting, no retries, no fixtures
  });

  test('do something as logged in user', async ({ page }) => {
    // ...
  });
});
```

**Best practice:**
```typescript
// Use project dependencies for global setup
// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },
    {
      name: 'tests',
      dependencies: ['setup'],
      use: {
        storageState: 'playwright/.auth/user.json',
      },
    },
  ],
});

// auth.setup.ts - proper setup project
import { test as setup, expect } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('admin@test.com');
  await page.getByLabel('Password').fill('admin');
  await page.getByRole('button', { name: 'Sign In' }).click();
  await expect(page.getByText('Dashboard')).toBeVisible();
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});

// Or use fixtures for per-test setup
const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('admin@test.com');
    await page.getByLabel('Password').fill('admin');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await use(page);
  },
});
```

**Why this matters:**
- beforeAll breaks reporting (failures aren't proper test failures)
- No retry mechanism for beforeAll failures
- Can't use test fixtures in beforeAll
- Project dependencies integrate properly with Playwright

**Sources:** [Playwright Global Setup](https://playwright.dev/docs/test-global-setup-teardown)

---

### FLAKY-ANIMATION: Handle Animations and Transitions
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Clicking during animation causes flakiness
test('open modal', async ({ page }) => {
  await page.getByRole('button', { name: 'Open' }).click();
  // Modal is animating in
  await page.getByRole('button', { name: 'Confirm' }).click();  // May miss
});

// Screenshot during animation
test('visual test', async ({ page }) => {
  await page.getByRole('button', { name: 'Show Panel' }).click();
  await page.screenshot({ path: 'panel.png' });  // Captures mid-animation
});
```

**Best practice:**
```typescript
// Disable animations globally in config
// playwright.config.ts
export default defineConfig({
  use: {
    // Disable CSS animations and transitions
    launchOptions: {
      args: ['--force-prefers-reduced-motion'],
    },
  },
});

// Or via CSS injection
test.beforeEach(async ({ page }) => {
  await page.addStyleTag({
    content: `
      *, *::before, *::after {
        animation-duration: 0s !important;
        transition-duration: 0s !important;
      }
    `,
  });
});

// Wait for animation to complete
test('open modal', async ({ page }) => {
  await page.getByRole('button', { name: 'Open' }).click();
  // Wait for modal to be stable (not animating)
  await expect(page.getByRole('dialog')).toBeVisible();
  // Playwright auto-waits for stability before clicking
  await page.getByRole('button', { name: 'Confirm' }).click();
});

// Mask animated regions in screenshots
test('visual test', async ({ page }) => {
  await page.getByRole('button', { name: 'Show Panel' }).click();
  await expect(page.locator('.panel')).toBeVisible();
  await page.screenshot({
    path: 'panel.png',
    mask: [page.locator('.animated-spinner')],
  });
});
```

**Why this matters:**
- Animations cause elements to be unstable during interaction
- Visual tests capture inconsistent states
- Disabling animations makes tests deterministic

---

### FLAKY-RETRY-CONFIG: Configure Retries Appropriately
**Severity:** 💡 Recommendation

**Anti-pattern:**
```typescript
// No retry configuration - single failure = red build
// playwright.config.ts
export default defineConfig({
  retries: 0,  // No safety net
});

// Or excessive retries hiding real problems
export default defineConfig({
  retries: 5,  // Masks flaky tests instead of fixing them
});
```

**Best practice:**
```typescript
// playwright.config.ts
export default defineConfig({
  // Retry on CI only
  retries: process.env.CI ? 2 : 0,

  // Capture artifacts on failure for debugging
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },

  reporter: [
    ['html'],
    // Track flaky tests over time
    ['json', { outputFile: 'test-results/results.json' }],
  ],
});

// Tag known flaky tests for tracking
test('sometimes flaky operation @flaky', async ({ page }) => {
  // ...
});

// Run flaky tests separately
// npx playwright test --grep @flaky
```

**Why this matters:**
- 1-2 retries catch genuine transient failures
- Excessive retries mask underlying problems
- Capturing traces on retry aids debugging
- Tracking flaky tests enables systematic fixes

**Sources:** [TestDino - Playwright Checklist](https://testdino.com/blog/playwright-automation-checklist/)

---

## 7. Test Organization

### ORG-DESCRIBE: Use describe for Grouping
**Severity:** 💡 Recommendation

**Anti-pattern:**
```typescript
// Flat test structure - hard to organize
test('login with valid credentials', async ({ page }) => {});
test('login with invalid password', async ({ page }) => {});
test('login with unregistered email', async ({ page }) => {});
test('signup with valid data', async ({ page }) => {});
test('signup with existing email', async ({ page }) => {});
```

**Best practice:**
```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test.describe('Login', () => {
    test('succeeds with valid credentials', async ({ page }) => {
      // ...
    });

    test('fails with invalid password', async ({ page }) => {
      // ...
    });

    test('fails with unregistered email', async ({ page }) => {
      // ...
    });
  });

  test.describe('Signup', () => {
    test('succeeds with valid data', async ({ page }) => {
      // ...
    });

    test('fails with existing email', async ({ page }) => {
      // ...
    });
  });
});
```

---

### ORG-NAMING: Clear Test Names
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
test('test1', async ({ page }) => {});
test('login test', async ({ page }) => {});
test('should work', async ({ page }) => {});
test('bug fix #123', async ({ page }) => {});
```

**Best practice:**
```typescript
// Format: [user/context] [action] [expected outcome]
test('user can login with valid credentials', async ({ page }) => {});
test('guest cannot access dashboard', async ({ page }) => {});
test('admin can delete users', async ({ page }) => {});
test('form shows validation error for invalid email', async ({ page }) => {});
test('cart updates quantity when user clicks plus button', async ({ page }) => {});
```

---

### ORG-HOOKS: Proper Use of Hooks
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// beforeAll for per-test setup (BAD - shared state)
test.beforeAll(async ({ page }) => {
  await page.goto('/login');
  await login(page);
});

// Heavy setup in beforeEach
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await createTestUser();
  await createTestProduct();
  await createTestOrder();
  // 10 more setup steps...
});
```

**Best practice:**
```typescript
// beforeEach for shared navigation
test.beforeEach(async ({ page }) => {
  await page.goto('/dashboard');
});

// beforeAll for expensive, truly shared setup
test.beforeAll(async ({ browser }) => {
  // One-time setup: compile assets, seed database
});

// afterEach for screenshots on failure (built-in, but custom example)
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    await page.screenshot({
      path: `screenshots/${testInfo.title}.png`,
      fullPage: true
    });
  }
});

// Use fixtures for complex setup
const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await login(page);
    await use(page);
  },
});
```

---

## 7. Performance

### PERF-PARALLEL: Enable Parallel Execution
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// playwright.config.ts
export default defineConfig({
  workers: 1, // Sequential - slow!
  fullyParallel: false,
});
```

**Best practice:**
```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 4 : undefined, // undefined = use all CPUs

  // Shard for large test suites
  // Run with: npx playwright test --shard=1/4
});

// For tests that can't run in parallel (rare)
test.describe.configure({ mode: 'serial' });

test.describe('Database migration tests', () => {
  test('step 1', async ({ page }) => {});
  test('step 2', async ({ page }) => {});
});
```

---

### PERF-API-SETUP: Use API for Test Setup
**Severity:** 💡 Recommendation

**Anti-pattern:**
```typescript
// UI-based setup - slow
test('edit user profile', async ({ page }) => {
  // Setup via UI (slow)
  await page.goto('/signup');
  await page.getByRole('textbox', { name: 'Email' }).fill('test@test.com');
  await page.getByRole('textbox', { name: 'Password' }).fill('password');
  await page.getByRole('button', { name: 'Sign up' }).click();
  await expect(page.getByText('Welcome')).toBeVisible();

  // Now finally test what we care about
  await page.goto('/profile');
  await page.getByRole('textbox', { name: 'Name' }).fill('New Name');
  await page.getByRole('button', { name: 'Save' }).click();
});
```

**Best practice:**
```typescript
// API-based setup - fast
test('edit user profile', async ({ page, request }) => {
  // Setup via API (fast)
  const response = await request.post('/api/users', {
    data: { email: 'test@test.com', password: 'password' }
  });
  const { id, authToken } = await response.json();

  // Set auth cookie
  await page.context().addCookies([{
    name: 'auth',
    value: authToken,
    domain: 'localhost',
    path: '/',
  }]);

  // Test the actual feature
  await page.goto('/profile');
  await page.getByRole('textbox', { name: 'Name' }).fill('New Name');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Profile updated')).toBeVisible();
});
```

---

## 8. Accessibility Testing

### A11Y-AXE: Integrate axe-core for Accessibility
**Severity:** 💡 Recommendation

**Setup:**
```bash
npm install @axe-core/playwright
```

**Best practice:**
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('home page has no a11y violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('login form is accessible', async ({ page }) => {
    await page.goto('/login');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .include('#login-form')  // Scope to specific element
      .withTags(['wcag2a', 'wcag2aa'])  // WCAG 2.0 Level A and AA
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('color contrast meets WCAG AA', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withRules(['color-contrast'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

**Attribution:** [axe-playwright](https://www.npmjs.com/package/@axe-core/playwright), [Playwright Accessibility](https://playwright.dev/docs/accessibility-testing)

---

### A11Y-KEYBOARD: Test Keyboard Navigation
**Severity:** ⚠️ Warning

**Best practice:**
```typescript
test('user can complete form with keyboard only', async ({ page }) => {
  await page.goto('/contact');

  // Tab to first field
  await page.keyboard.press('Tab');
  await expect(page.getByRole('textbox', { name: 'Name' })).toBeFocused();

  // Fill and tab to next
  await page.keyboard.type('John Doe');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('textbox', { name: 'Email' })).toBeFocused();

  await page.keyboard.type('john@example.com');
  await page.keyboard.press('Tab');

  // Submit with Enter
  await expect(page.getByRole('button', { name: 'Submit' })).toBeFocused();
  await page.keyboard.press('Enter');

  await expect(page.getByText('Message sent')).toBeVisible();
});

test('modal traps focus correctly', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Open modal' }).click();

  // Focus should be inside modal
  await expect(page.getByRole('dialog')).toBeVisible();

  // Tab through modal elements
  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: 'Close' })).toBeFocused();

  // Escape closes modal
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).toBeHidden();
});
```

---

## 9. Visual Regression Testing

### VIS-SCREENSHOT: Use Built-in Screenshot Comparison
**Severity:** 💡 Recommendation

**Basic usage:**
```typescript
test('homepage visual regression', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png');

  // Element screenshot
  await expect(page.getByRole('navigation')).toHaveScreenshot('navbar.png');
});
```

**Configuration:**
```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,  // Allow small differences
      threshold: 0.2,      // Pixel comparison threshold
    },
  },

  // Update snapshots with: npx playwright test --update-snapshots
});
```

**Best practices:**
```typescript
test('product card visual', async ({ page }) => {
  await page.goto('/products');

  // Wait for images to load
  await page.waitForLoadState('networkidle');

  // Mask dynamic content
  await expect(page.locator('.product-card').first()).toHaveScreenshot({
    mask: [
      page.locator('.price'),  // Prices may change
      page.locator('.timestamp'),  // Dynamic dates
    ],
  });
});

test('responsive layout', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage-mobile.png');

  await page.setViewportSize({ width: 1920, height: 1080 }); // Desktop
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage-desktop.png');
});
```

---

## 10. Debugging

### DEBUG-TRACE: Use Traces for CI Failures
**Severity:** 💡 Recommendation

**Configuration:**
```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    // Collect trace on failure
    trace: 'on-first-retry',

    // Also capture screenshots and video
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },

  // Retry failed tests
  retries: process.env.CI ? 2 : 0,
});
```

**Viewing traces:**
```bash
# View trace from CI artifact
npx playwright show-trace trace.zip

# Or use the web viewer
# https://trace.playwright.dev
```

**Why traces over screenshots/video:**
- Full DOM snapshots at each step
- Network requests and console logs
- Step-by-step debugging
- Smaller file size than video

**Attribution:** [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)

---

### DEBUG-STEP: Use test.step for Better Reports
**Severity:** 💡 Recommendation

**Best practice:**
```typescript
test('checkout flow', async ({ page }) => {
  await test.step('Add product to cart', async () => {
    await page.goto('/products');
    await page.getByRole('button', { name: 'Add to Cart' }).click();
    await expect(page.getByText('Added to cart')).toBeVisible();
  });

  await test.step('Navigate to checkout', async () => {
    await page.getByRole('link', { name: 'Cart' }).click();
    await page.getByRole('button', { name: 'Checkout' }).click();
  });

  await test.step('Fill shipping info', async () => {
    await page.getByRole('textbox', { name: 'Address' }).fill('123 Main St');
    await page.getByRole('textbox', { name: 'City' }).fill('New York');
  });

  await test.step('Complete payment', async () => {
    await page.getByRole('textbox', { name: 'Card' }).fill('4111111111111111');
    await page.getByRole('button', { name: 'Pay' }).click();
    await expect(page.getByText('Order confirmed')).toBeVisible();
  });
});
```

**Benefits:**
- Clear test structure in reports
- Easier to identify failure point
- Better tracing and debugging

---

## 11. React-Specific Patterns

> **Sources:** [Playwright Component Testing](https://playwright.dev/docs/test-components), [Migrating from Testing Library](https://playwright.dev/docs/testing-library), [Next.js Testing Guide](https://nextjs.org/docs/pages/guides/testing/playwright)

### REACT-HYDRATION: Wait for Hydration Before Interaction
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Clicking before React hydration completes - event handlers not bound!
test('form submission', async ({ page }) => {
  await page.goto('/');
  // React is still hydrating SSR content...
  await page.getByRole('button', { name: 'Submit' }).click();  // Handler not attached!
  // Form data cleared when hydration overwrites DOM
});

// Filling form before hydration - input values reset
test('login', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@test.com');  // Filled too early!
  // Hydration clears the input
  await page.getByRole('button', { name: 'Sign In' }).click();
  // Email field is now empty!
});
```

**Best practice:**
```typescript
// Wait for hydration indicator
test('form submission', async ({ page }) => {
  await page.goto('/');

  // Option 1: Wait for hydration class/attribute
  await page.waitForSelector('[data-hydrated="true"]');
  // Or: await page.waitForSelector('body.hydrated');

  await page.getByRole('button', { name: 'Submit' }).click();
});

// Option 2: Wait for interactive element to be truly ready
test('login', async ({ page }) => {
  await page.goto('/login');

  // Wait for React to attach event handlers
  await expect(page.getByRole('button', { name: 'Sign In' })).toBeEnabled();

  // Now safe to fill and submit
  await page.getByLabel('Email').fill('user@test.com');
  await page.getByRole('button', { name: 'Sign In' }).click();
});

// Option 3: Use app-level hydration signal
// In your React app:
// useEffect(() => {
//   document.body.classList.add('hydrated');
// }, []);

test('checkout', async ({ page }) => {
  await page.goto('/checkout');
  await page.waitForSelector('body.hydrated');
  // Now safe to interact
});
```

**Why this matters:**
- SSR pages render HTML before React hydrates
- Event handlers aren't attached until hydration completes
- Form inputs can be overwritten during hydration
- Tests pass locally (fast hydration) but fail in CI (slower)

**Sources:** [Playwright Hydration Issue](https://github.com/microsoft/playwright/issues/27759)

---

### REACT-ASYNC-STATE: Wait for Async State Updates
**Severity:** 🔴 Critical

**Anti-pattern:**
```typescript
// Asserting immediately after action - state hasn't updated
test('add to cart', async ({ page }) => {
  await page.getByRole('button', { name: 'Add to Cart' }).click();

  // React state update is async - count might still be 0
  const countText = await page.locator('.cart-count').textContent();
  expect(countText).toBe('1');  // Flaky!
});

// Not waiting for useEffect data fetch
test('user profile', async ({ page }) => {
  await page.goto('/profile');

  // useEffect fetch hasn't completed yet
  const name = await page.locator('.user-name').textContent();
  expect(name).toBe('John Doe');  // Shows loading state!
});
```

**Best practice:**
```typescript
// Use auto-retrying assertions - wait for React to re-render
test('add to cart', async ({ page }) => {
  await page.getByRole('button', { name: 'Add to Cart' }).click();

  // Playwright retries until condition passes
  await expect(page.locator('.cart-count')).toHaveText('1');
});

// Wait for loading state to disappear
test('user profile', async ({ page }) => {
  await page.goto('/profile');

  // Wait for loading to complete
  await expect(page.getByText('Loading...')).toBeHidden();

  // Or wait for actual content
  await expect(page.locator('.user-name')).toHaveText('John Doe');
});

// Wait for specific network response
test('search results', async ({ page }) => {
  const responsePromise = page.waitForResponse('**/api/search*');

  await page.getByLabel('Search').fill('playwright');
  await page.getByRole('button', { name: 'Search' }).click();

  await responsePromise;  // Wait for API to respond
  await expect(page.locator('.result')).toHaveCount(10);
});
```

**Why this matters:**
- React state updates are batched and async
- `useEffect` runs after render, causing additional updates
- Immediate fetchers (`textContent()`) don't wait for re-renders
- Auto-retrying assertions handle async React updates

---

### REACT-PORTAL: Handle Portal-Rendered Components
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Looking for modal inside component - it's rendered in a portal!
test('open settings modal', async ({ page }) => {
  await page.goto('/dashboard');

  await page.getByRole('button', { name: 'Settings' }).click();

  // Modal is in a portal, not inside the dashboard container
  const dashboard = page.locator('.dashboard');
  await expect(dashboard.getByRole('dialog')).toBeVisible();  // Not found!
});

// Component testing without portal container
// playwright/index.html
// <div id="root"></div>  <!-- No portal container! -->
```

**Best practice:**
```typescript
// Search from page root - portals render at document level
test('open settings modal', async ({ page }) => {
  await page.goto('/dashboard');

  await page.getByRole('button', { name: 'Settings' }).click();

  // Modal is a portal - find from page, not parent component
  await expect(page.getByRole('dialog', { name: 'Settings' })).toBeVisible();

  // Interact with modal content
  await page.getByRole('dialog').getByLabel('Theme').selectOption('dark');
  await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();
});

// For component testing - add portal container to test HTML
// playwright/index.html
// <div id="root"></div>
// <div id="portal-root"></div>  <!-- For React portals -->

// Tooltip example - rendered via portal
test('show tooltip', async ({ page }) => {
  await page.getByRole('button', { name: 'Help' }).hover();

  // Tooltip is a portal - find from page level
  await expect(page.getByRole('tooltip')).toBeVisible();
  await expect(page.getByRole('tooltip')).toContainText('Click for help');
});
```

**Why this matters:**
- React portals (`createPortal`) render outside component hierarchy
- Modals, tooltips, dropdowns often use portals
- Searching within parent component won't find portal content
- Component tests need explicit portal container in test HTML

**Sources:** [React createPortal](https://react.dev/reference/react-dom/createPortal)

---

### REACT-SUSPENSE: Handle Suspense Boundaries
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Asserting on lazy-loaded content before it loads
test('view dashboard widgets', async ({ page }) => {
  await page.goto('/dashboard');

  // Lazy-loaded component shows Suspense fallback
  await expect(page.getByText('Revenue: $50,000')).toBeVisible();  // Fails - still loading!
});

// Not handling skeleton/loading states
test('load user list', async ({ page }) => {
  await page.goto('/users');

  // Component is suspended, showing skeleton
  const users = await page.locator('.user-card').all();
  expect(users.length).toBe(10);  // Gets 0 - skeleton showing!
});
```

**Best practice:**
```typescript
// Wait for Suspense fallback to disappear
test('view dashboard widgets', async ({ page }) => {
  await page.goto('/dashboard');

  // Wait for loading/skeleton to disappear
  await expect(page.getByTestId('widget-skeleton')).toBeHidden();
  // Or: await expect(page.getByText('Loading widgets...')).toBeHidden();

  // Now assert on actual content
  await expect(page.getByText('Revenue: $50,000')).toBeVisible();
});

// Use toHaveCount with auto-retry
test('load user list', async ({ page }) => {
  await page.goto('/users');

  // Auto-retry until React.lazy component loads
  await expect(page.locator('.user-card')).toHaveCount(10);
});

// Wait for specific lazy chunk to load
test('open settings panel', async ({ page }) => {
  await page.goto('/dashboard');

  // Settings panel is lazy-loaded
  await page.getByRole('button', { name: 'Settings' }).click();

  // Wait for chunk to load and render
  await expect(page.getByRole('heading', { name: 'Settings' })).toBeVisible();
});
```

**Why this matters:**
- `React.lazy()` shows Suspense fallback during load
- Code-split chunks take time to download
- Skeleton screens replace content during data fetching
- Auto-retrying assertions wait for React to complete rendering

---

### REACT-CONTEXT: Configure Providers for Component Tests
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Component test without required context providers
test('theme toggle works', async ({ mount }) => {
  // ThemeToggle needs ThemeProvider - crashes!
  const component = await mount(<ThemeToggle />);
  await component.getByRole('button', { name: 'Toggle' }).click();
});

// Missing router context
test('navigation link', async ({ mount }) => {
  // Link component needs BrowserRouter - crashes!
  const component = await mount(<NavLink to="/dashboard">Dashboard</NavLink>);
});
```

**Best practice:**
```typescript
// playwright/index.tsx - Configure providers via beforeMount hook
import { beforeMount } from '@playwright/experimental-ct-react/hooks';
import { ThemeProvider } from './contexts/ThemeContext';
import { BrowserRouter } from 'react-router-dom';

export type HooksConfig = {
  enableRouting?: boolean;
  theme?: 'light' | 'dark';
};

beforeMount<HooksConfig>(async ({ App, hooksConfig }) => {
  const theme = hooksConfig?.theme ?? 'light';

  let wrappedApp = (
    <ThemeProvider initialTheme={theme}>
      <App />
    </ThemeProvider>
  );

  if (hooksConfig?.enableRouting) {
    wrappedApp = <BrowserRouter>{wrappedApp}</BrowserRouter>;
  }

  return wrappedApp;
});

// Test with custom hooks config
test('theme toggle works', async ({ mount }) => {
  const component = await mount<HooksConfig>(
    <ThemeToggle />,
    { hooksConfig: { theme: 'dark' } }
  );

  await component.getByRole('button', { name: 'Toggle' }).click();
  await expect(component).toHaveAttribute('data-theme', 'light');
});

test('navigation link', async ({ mount }) => {
  const component = await mount<HooksConfig>(
    <NavLink to="/dashboard">Dashboard</NavLink>,
    { hooksConfig: { enableRouting: true } }
  );

  await expect(component).toHaveAttribute('href', '/dashboard');
});
```

**Why this matters:**
- React components often depend on context providers
- Missing providers cause crashes or unexpected behavior
- `beforeMount` hook wraps components with required providers
- `hooksConfig` allows per-test customization

**Sources:** [Playwright Component Testing](https://playwright.dev/docs/test-components)

---

### REACT-PROPS-LIMIT: Understand Component Testing Prop Limitations
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Passing complex live objects - won't work!
test('media upload', async ({ mount }) => {
  const file = new File(['content'], 'test.png', { type: 'image/png' });

  // Can't pass File object from Node.js to browser
  const component = await mount(<MediaUploader file={file} />);  // Fails!
});

// Passing callback that reads closure variables synchronously
test('form validation', async ({ mount }) => {
  let validationResult = null;

  const component = await mount(
    <Form onValidate={(result) => {
      validationResult = result;  // Won't work - different contexts!
    }} />
  );
});
```

**Best practice:**
```typescript
// Create test wrapper that handles complex types
// media-uploader.story.tsx
export function MediaUploaderForTest(props: {
  onUploadComplete: (fileName: string) => void;
}) {
  const [file, setFile] = React.useState<File | null>(null);

  return (
    <>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        data-testid="file-input"
      />
      <MediaUploader
        file={file}
        onComplete={(media) => props.onUploadComplete(media.name)}
      />
    </>
  );
}

// Test using the wrapper
test('media upload', async ({ mount, page }) => {
  let uploadedFileName = '';

  const component = await mount(
    <MediaUploaderForTest
      onUploadComplete={(name) => { uploadedFileName = name; }}
    />
  );

  // Use Playwright to set file input
  await page.setInputFiles('[data-testid="file-input"]', 'test.png');
  await component.getByRole('button', { name: 'Upload' }).click();

  // Verify via DOM, not callback
  await expect(component.getByText('test.png uploaded')).toBeVisible();
});

// For validation, observe DOM instead of callbacks
test('form validation', async ({ mount }) => {
  const component = await mount(<Form />);

  await component.getByLabel('Email').fill('invalid');
  await component.getByRole('button', { name: 'Submit' }).click();

  // Assert on visible validation message, not callback
  await expect(component.getByText('Invalid email')).toBeVisible();
});
```

**Why this matters:**
- Node.js and browser are separate contexts
- Only plain objects, strings, numbers, dates can be passed
- Callbacks can't synchronously read Node.js variables
- Test wrappers convert complex objects to simple props

**Sources:** [Playwright Component Testing Limitations](https://playwright.dev/docs/test-components)

---

### REACT-MSW: Mock API Requests for React Data Fetching
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Hitting real API in tests - flaky and slow
test('user profile', async ({ page }) => {
  await page.goto('/profile');
  // Real API call - may fail, be slow, or return different data
  await expect(page.getByText('John Doe')).toBeVisible();
});

// No mock for useQuery/useSWR/RTK Query hooks
test('product list', async ({ page }) => {
  await page.goto('/products');
  // Real products from API - data changes, tests break
  await expect(page.getByText('Product 1')).toBeVisible();
});
```

**Best practice:**
```typescript
// Mock API responses with page.route()
test('user profile', async ({ page }) => {
  await page.route('**/api/user', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ name: 'John Doe', email: 'john@test.com' }),
    });
  });

  await page.goto('/profile');
  await expect(page.getByText('John Doe')).toBeVisible();
});

// Mock with different scenarios
test('handles API error', async ({ page }) => {
  await page.route('**/api/user', async (route) => {
    await route.fulfill({
      status: 500,
      body: 'Internal Server Error',
    });
  });

  await page.goto('/profile');
  await expect(page.getByText('Failed to load profile')).toBeVisible();
});

// Mock for paginated data
test('product list pagination', async ({ page }) => {
  await page.route('**/api/products?page=1', async (route) => {
    await route.fulfill({
      body: JSON.stringify({
        products: [{ id: 1, name: 'Product 1' }],
        hasMore: true,
      }),
    });
  });

  await page.route('**/api/products?page=2', async (route) => {
    await route.fulfill({
      body: JSON.stringify({
        products: [{ id: 2, name: 'Product 2' }],
        hasMore: false,
      }),
    });
  });

  await page.goto('/products');
  await expect(page.getByText('Product 1')).toBeVisible();

  await page.getByRole('button', { name: 'Load More' }).click();
  await expect(page.getByText('Product 2')).toBeVisible();
});
```

**Why this matters:**
- React data fetching (useEffect, React Query, SWR) hits real APIs
- Real APIs are slow, flaky, and return changing data
- Mocking gives complete control over response data and timing
- Can test error states and edge cases reliably

---

### REACT-NEXTJS-SSR: Handle Next.js Server-Side Rendering
**Severity:** ⚠️ Warning

**Anti-pattern:**
```typescript
// Testing SSR page without handling static cache
test('dynamic content', async ({ page }) => {
  await page.goto('/products');
  // Getting cached static page, not fresh SSR!
  await expect(page.getByText('Latest Product')).toBeVisible();
});

// Not mocking server-side API calls
test('server-rendered data', async ({ page }) => {
  // page.route() only works for client-side requests
  await page.route('**/api/data', ...);  // Won't catch SSR fetch!

  await page.goto('/dashboard');
});
```

**Best practice:**
```typescript
// For Next.js - use webServer in playwright.config.ts
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});

// Bypass static page cache with cookie
// playwright/fixtures.ts
import { test as base } from '@playwright/test';

export const test = base.extend({
  page: async ({ page, context }, use) => {
    // Bypass Next.js static cache for fresh SSR
    await context.addCookies([{
      name: '__prerender_bypass',
      value: 'your-preview-mode-id',
      domain: 'localhost',
      path: '/',
    }]);
    await use(page);
  },
});

// For SSR API mocking - use MSW with remote server
// See: https://github.com/kettanaito/nextjs-rsc-testing

// Test App Router Server Components
test('server component data', async ({ page }) => {
  // Use environment variables to point to mock server
  // Or use Next.js experimental test mode
  await page.goto('/dashboard');
  await expect(page.getByText('Server Data')).toBeVisible();
});

// Handle getServerSideProps / getStaticProps
test('SSR page with props', async ({ page }) => {
  // For getStaticProps - test the built output
  // For getServerSideProps - mock at API level

  await page.goto('/blog/test-post');
  await expect(page.getByRole('heading', { name: 'Test Post' })).toBeVisible();
});
```

**Why this matters:**
- Next.js pre-renders pages at build time or request time
- `page.route()` only intercepts client-side fetch
- Server-side data fetching needs different mocking strategy
- Static generation caches pages - tests may get stale data

**Sources:** [Next.js Playwright Testing](https://nextjs.org/docs/pages/guides/testing/playwright), [Next.js RSC Testing](https://github.com/kettanaito/nextjs-rsc-testing)

---

### REACT-RTL-MIGRATE: Migrate Testing Library Patterns to Playwright
**Severity:** 💡 Recommendation

**Testing Library to Playwright mapping:**
```typescript
// React Testing Library
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('login form', async () => {
  render(<LoginForm />);

  await userEvent.type(screen.getByLabelText('Email'), 'user@test.com');
  await userEvent.type(screen.getByLabelText('Password'), 'password');
  await userEvent.click(screen.getByRole('button', { name: 'Sign In' }));

  await waitFor(() => {
    expect(screen.getByText('Welcome')).toBeInTheDocument();
  });
});


// Playwright Component Testing - equivalent
import { test, expect } from '@playwright/experimental-ct-react';

test('login form', async ({ mount }) => {
  const component = await mount(<LoginForm />);

  await component.getByLabel('Email').fill('user@test.com');
  await component.getByLabel('Password').fill('password');
  await component.getByRole('button', { name: 'Sign In' }).click();

  // No waitFor needed - assertions auto-retry
  await expect(component.getByText('Welcome')).toBeVisible();
});
```

**Query mapping reference:**

| Testing Library | Playwright |
|-----------------|------------|
| `screen` | `component` or `page` |
| `getByText()` | `.getByText()` |
| `getByRole()` | `.getByRole()` |
| `getByLabelText()` | `.getByLabel()` |
| `getByPlaceholderText()` | `.getByPlaceholder()` |
| `getByTestId()` | `.getByTestId()` |
| `getByAltText()` | `.getByAltText()` |
| `queryBy*()` | Not needed - locators are lazy |
| `findBy*()` | Not needed - locators auto-wait |
| `within()` | `.locator()` chaining |
| `waitFor()` | Not needed - assertions auto-retry |
| `userEvent.type()` | `.fill()` |
| `userEvent.click()` | `.click()` |
| `toBeInTheDocument()` | `.toBeVisible()` |
| `toHaveValue()` | `.toHaveValue()` |

**Sources:** [Playwright Testing Library Migration](https://playwright.dev/docs/testing-library)

---

### REACT-COMPONENT-OBJECT: Use Component Object Model for Reusable Components
**Severity:** 💡 Recommendation

**Anti-pattern:**
```typescript
// Duplicated locators for same component used multiple times
test('edit multiple users', async ({ page }) => {
  // First user card
  await page.locator('.user-card').first().getByRole('button', { name: 'Edit' }).click();
  await page.locator('.user-card').first().getByLabel('Name').fill('Updated');

  // Second user card - same locators repeated
  await page.locator('.user-card').nth(1).getByRole('button', { name: 'Edit' }).click();
  await page.locator('.user-card').nth(1).getByLabel('Name').fill('Updated 2');
});
```

**Best practice:**
```typescript
// Component Object Model - reusable wrapper for React components
class UserCard {
  constructor(private root: Locator) {}

  get editButton() {
    return this.root.getByRole('button', { name: 'Edit' });
  }

  get nameInput() {
    return this.root.getByLabel('Name');
  }

  get emailInput() {
    return this.root.getByLabel('Email');
  }

  async edit(name: string, email: string) {
    await this.editButton.click();
    await this.nameInput.fill(name);
    await this.emailInput.fill(email);
    await this.root.getByRole('button', { name: 'Save' }).click();
  }
}

// Page with multiple user cards
class UsersPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/users');
  }

  getUserCard(index: number) {
    return new UserCard(this.page.locator('.user-card').nth(index));
  }

  getUserCardByEmail(email: string) {
    return new UserCard(
      this.page.locator('.user-card').filter({ hasText: email })
    );
  }
}

// Clean test using Component Object Model
test('edit multiple users', async ({ page }) => {
  const usersPage = new UsersPage(page);
  await usersPage.goto();

  await usersPage.getUserCard(0).edit('Alice', 'alice@test.com');
  await usersPage.getUserCard(1).edit('Bob', 'bob@test.com');

  // Or find by content
  await usersPage.getUserCardByEmail('charlie@test.com').edit('Charlie', 'charlie@new.com');
});
```

**Why this matters:**
- React components are often reused across pages
- Component Object Model encapsulates component interactions
- Root locator passed to constructor provides scoping
- Changes to component structure only need updates in one place

---

## Expected Good Patterns (Check for Absence)

> **Sources:** [Playwright Best Practices](https://playwright.dev/docs/best-practices), [Better Stack Guide](https://betterstack.com/community/guides/testing/playwright-best-practices/), [axe-core](https://www.npmjs.com/package/@axe-core/playwright)

This section identifies the **absence of good patterns** (not just presence of anti-patterns). Use `MISSING-*` IDs for tracking.

### 1. Locator Patterns

**Mnemonic:** **"USER-FACING-FIRST"**

| Expected Pattern | If Missing |
|------------------|------------|
| `getByRole()` for interactive elements | 🔴 `MISSING-ROLE-LOCATOR` - Fragile CSS/XPath |
| `getByText()` / `getByLabel()` for content | ⚠️ `MISSING-TEXT-LOCATOR` - Implementation-tied |
| `getByTestId()` as fallback | 💡 `MISSING-TESTID-FALLBACK` - Complex selectors |
| Chained/filtered locators | ⚠️ `MISSING-LOCATOR-CHAIN` - Index-based selection |

```typescript
// PRESENT: User-facing locator hierarchy
// 1. Role (best)
await page.getByRole('button', { name: 'Submit' }).click();

// 2. Text/Label
await page.getByLabel('Email').fill('user@test.com');
await page.getByText('Welcome back').isVisible();

// 3. TestId (when needed)
await page.getByTestId('user-avatar').click();

// 4. Chained/filtered
const row = page.getByRole('row').filter({ hasText: 'john@example.com' });
await row.getByRole('button', { name: 'Edit' }).click();


// MISSING: Implementation-tied locators
await page.locator('.btn-primary').click();  // CSS class!
await page.locator('#submit-btn').click();   // ID!
await page.locator('//button[1]').click();   // XPath!
await page.locator('.MuiButton-root').click(); // Framework class!
```

### 2. Assertion Patterns

**Mnemonic:** **"WEB-FIRST-ASSERT"**

| Expected Pattern | If Missing |
|------------------|------------|
| Web-first assertions (`toBeVisible`, `toHaveText`) | 🔴 `MISSING-WEBFIRST-ASSERT` - No auto-wait |
| Specific assertions over generic | ⚠️ `MISSING-SPECIFIC-ASSERT` - Unclear intent |
| Negative assertions (`not.toBeVisible`) | 💡 `MISSING-NEGATIVE-ASSERT` - Only positive checks |
| Soft assertions for multiple checks | 💡 `MISSING-SOFT-ASSERT` - Single failure stops test |

```typescript
// PRESENT: Web-first assertions
await expect(page.getByText('Success')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByRole('textbox')).toHaveValue('test@example.com');
await expect(page).toHaveURL(/\/dashboard/);
await expect(page.getByRole('listitem')).toHaveCount(5);


// MISSING: Manual checks without auto-wait
const isVisible = await page.locator('.success').isVisible();
expect(isVisible).toBe(true);  // No retry if false!

// MISSING: Hardcoded wait before assertion
await page.waitForTimeout(3000);  // NEVER DO THIS
expect(await page.locator('.message').textContent()).toBe('Done');
```

### 3. Test Isolation Patterns

**Mnemonic:** **"ISOLATED-INDEPENDENT"**

| Expected Pattern | If Missing |
|------------------|------------|
| Independent tests (no shared state) | 🔴 `MISSING-ISOLATION` - Tests depend on order |
| Fresh browser context per test | 🔴 `MISSING-FRESH-CONTEXT` - State leaks |
| API-based test data setup | ⚠️ `MISSING-API-SETUP` - Slow UI setup |
| Cleanup in finally/afterEach | ⚠️ `MISSING-CLEANUP` - Data pollution |

```typescript
// PRESENT: Isolated test with API setup
test('edit user profile', async ({ page, request }) => {
  // Setup via API (fast, isolated)
  const user = await request.post('/api/users', {
    data: { email: 'test@test.com', name: 'Test User' }
  }).then(r => r.json());

  try {
    await page.goto(`/users/${user.id}/edit`);
    await page.getByLabel('Name').fill('Updated Name');
    await page.getByRole('button', { name: 'Save' }).click();
    await expect(page.getByText('Profile updated')).toBeVisible();
  } finally {
    // Cleanup
    await request.delete(`/api/users/${user.id}`);
  }
});


// MISSING: Shared state between tests
let userId: string;

test('create user', async ({ page }) => {
  userId = await createUserViaUI(page);  // Shared state!
});

test('edit user', async ({ page }) => {
  await page.goto(`/users/${userId}/edit`);  // Depends on previous test!
});
```

### 4. Page Object Patterns

**Mnemonic:** **"POM-FOR-REUSE"**

| Expected Pattern | If Missing |
|------------------|------------|
| Page class for complex pages | ⚠️ `MISSING-PAGE-OBJECT` - Inline locators |
| Locators as properties/getters | 💡 `MISSING-LOCATOR-PROPS` - Duplicated selectors |
| Actions as methods | 💡 `MISSING-ACTION-METHODS` - Repeated steps |
| No assertions in page objects | ⚠️ `MISSING-POM-SEPARATION` - Assertions in POM |

```typescript
// PRESENT: Proper Page Object
export class LoginPage {
  constructor(private page: Page) {}

  // Locators as getters
  get emailInput() {
    return this.page.getByRole('textbox', { name: 'Email' });
  }

  get passwordInput() {
    return this.page.getByRole('textbox', { name: 'Password' });
  }

  get submitButton() {
    return this.page.getByRole('button', { name: 'Sign in' });
  }

  // Actions as methods (no assertions!)
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}

// Test with assertions
test('login succeeds', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user@test.com', 'password');

  // Assertions in test, not POM
  await expect(page.getByText('Welcome')).toBeVisible();
});


// MISSING: Inline locators everywhere
test('login', async ({ page }) => {
  await page.locator('#email').fill('user@test.com');
  await page.locator('#password').fill('password');
  await page.locator('button[type="submit"]').click();
  // Repeated in every test that needs login!
});
```

### 5. Waiting Patterns

**Mnemonic:** **"AUTO-WAIT-TRUST"**

| Expected Pattern | If Missing |
|------------------|------------|
| Trust Playwright auto-wait | 🔴 `MISSING-AUTOWAIT-TRUST` - Manual waits |
| `waitForResponse` for API calls | ⚠️ `MISSING-RESPONSE-WAIT` - Timing issues |
| `waitForLoadState` for navigation | 💡 `MISSING-LOADSTATE` - Premature assertions |
| No `waitForTimeout` | 🔴 `MISSING-NO-TIMEOUT` - Hardcoded sleeps |

```typescript
// PRESENT: Proper waiting
// Auto-wait: Playwright waits for actionability
await page.getByRole('button', { name: 'Submit' }).click();

// Wait for API response
const [response] = await Promise.all([
  page.waitForResponse(r => r.url().includes('/api/submit')),
  page.getByRole('button', { name: 'Submit' }).click()
]);
expect(response.status()).toBe(200);

// Wait for navigation
await page.waitForURL('**/dashboard');


// MISSING: Hardcoded waits
await page.waitForTimeout(5000);  // ANTI-PATTERN!
await page.getByRole('button').click();
await page.waitForTimeout(2000);  // "Wait for animation"
```

### 6. Flaky Test Prevention

**Mnemonic:** **"STABLE-BY-DESIGN"**

| Expected Pattern | If Missing |
|------------------|------------|
| Auto-retrying assertions | 🔴 `MISSING-RETRY-ASSERT` - Race conditions |
| `toHaveCount()` before `all()` | 🔴 `MISSING-ALL-GUARD` - Empty array race |
| Independent tests | 🔴 `MISSING-INDEPENDENCE` - Order-dependent |
| No shared mutable state | 🔴 `MISSING-STATE-ISOLATION` - State contamination |
| Mock external dependencies | ⚠️ `MISSING-MOCK-EXTERNAL` - Third-party flakiness |
| Explicit environment config | ⚠️ `MISSING-EXPLICIT-ENV` - Environment assumptions |
| Animation handling | ⚠️ `MISSING-ANIMATION-HANDLING` - Visual instability |
| Deterministic assertions | 💡 `MISSING-DETERMINISTIC` - Non-deterministic values |

```typescript
// PRESENT: Stable test patterns

// 1. Auto-retrying assertions (not immediate fetchers)
await expect(page.locator('#status')).toHaveText('Complete');
// NOT: expect(await page.locator('#status').textContent()).toBe('Complete');

// 2. Guard locator.all() with count check
await expect(page.locator('.item')).toHaveCount(5);
const items = await page.locator('.item').all();

// 3. Independent tests with fixtures
const test = base.extend({
  testUser: async ({ request }, use) => {
    const user = await createUser(request);
    await use(user);
    await deleteUser(request, user.id);
  },
});

// 4. Mock external services
await page.route('**/api/external/**', route => route.fulfill({
  body: JSON.stringify({ data: 'mocked' })
}));

// 5. Explicit environment
test.use({ viewport: { width: 1280, height: 720 }, locale: 'en-US' });

// 6. Mock time for deterministic tests
await page.clock.install({ time: new Date('2024-01-15T10:30:00') });

// 7. Handle animations
await page.addStyleTag({
  content: '*, *::before, *::after { animation: none !important; }'
});


// MISSING: Flaky patterns

// Race condition - textContent() doesn't wait
const text = await page.locator('#status').textContent();
expect(text).toBe('Complete');  // Flaky!

// locator.all() without guard - may get empty array
const items = await page.locator('.item').all();  // Flaky!

// Order-dependent tests
test('test A', async () => { /* creates data */ });
test('test B', async () => { /* assumes test A ran */ });  // Flaky!

// Shared mutable state
let userId: string;  // Shared between tests - Flaky!

// Real external API
await page.goto('/oauth/google');  // Third-party - Flaky!

// Assumes environment
await expect(page.locator('.date')).toHaveText('01/15/2024');  // Locale-dependent - Flaky!
```

### 7. Debugging & CI Patterns

**Mnemonic:** **"TRACE-NOT-SLEEP"**

| Expected Pattern | If Missing |
|------------------|------------|
| Trace collection on failure | ⚠️ `MISSING-TRACE` - Hard to debug CI failures |
| Screenshots on failure | ⚠️ `MISSING-SCREENSHOT` - No visual context |
| `test.step()` for reports | 💡 `MISSING-STEPS` - Unclear failure point |
| Retries in CI | 💡 `MISSING-RETRIES` - Flaky test failures |

```typescript
// PRESENT: Good debugging setup
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
  retries: process.env.CI ? 2 : 0,
});

// Test with steps
test('checkout', async ({ page }) => {
  await test.step('Add to cart', async () => {
    await page.getByRole('button', { name: 'Add to Cart' }).click();
  });

  await test.step('Complete checkout', async () => {
    await page.getByRole('button', { name: 'Checkout' }).click();
    await expect(page.getByText('Order confirmed')).toBeVisible();
  });
});


// MISSING: No debugging aids
// playwright.config.ts
export default defineConfig({
  // No trace, no screenshots, no retries
  // When tests fail in CI, good luck debugging!
});
```

---

### 8. React-Specific Patterns

**Mnemonic:** **"REACT-AWARE-TESTING"**

| Expected Pattern | If Missing |
|------------------|------------|
| Wait for hydration before interaction | 🔴 `MISSING-HYDRATION-WAIT` - Clicks before handlers attached |
| Auto-retrying assertions for state updates | 🔴 `MISSING-STATE-WAIT` - Flaky async state tests |
| Page-level queries for portals | ⚠️ `MISSING-PORTAL-QUERY` - Modal/tooltip not found |
| Handle Suspense fallbacks | ⚠️ `MISSING-SUSPENSE-WAIT` - Lazy component assertions fail |
| Context providers in component tests | ⚠️ `MISSING-CONTEXT-SETUP` - Component crashes |
| API mocking for data fetching | ⚠️ `MISSING-API-MOCK` - Flaky real API calls |
| Component Object Model | 💡 `MISSING-COMPONENT-OBJECT` - Duplicated locators |

```typescript
// PRESENT: React-aware patterns

// Wait for hydration
await page.waitForSelector('[data-hydrated="true"]');
await page.getByRole('button', { name: 'Submit' }).click();

// Auto-retrying assertion for state
await expect(page.locator('.cart-count')).toHaveText('1');

// Portal query from page level
await expect(page.getByRole('dialog')).toBeVisible();

// Suspense handling
await expect(page.getByTestId('skeleton')).toBeHidden();
await expect(page.getByText('Content')).toBeVisible();

// API mocking
await page.route('**/api/user', route => route.fulfill({
  body: JSON.stringify({ name: 'Test User' })
}));

// Context providers via beforeMount hook
beforeMount(async ({ App, hooksConfig }) => (
  <ThemeProvider><App /></ThemeProvider>
));


// MISSING: React-unaware patterns

// No hydration wait - clicks fail in CI
await page.goto('/');
await page.getByRole('button', { name: 'Submit' }).click();  // Flaky!

// Immediate fetch - doesn't wait for React re-render
const text = await page.locator('.status').textContent();  // Flaky!

// Looking inside parent - portal renders elsewhere
await dashboard.getByRole('dialog').click();  // Not found!

// No mock - real API flakiness
await page.goto('/profile');  // Depends on API!
```

---

### Expected Patterns Summary Checklist

**When Reviewing, Verify Presence Of:**

🔴 **Critical (causes flaky or unreliable tests if missing):**
- [ ] `MISSING-ROLE-LOCATOR` - No getByRole for buttons, links, inputs
- [ ] `MISSING-WEBFIRST-ASSERT` - Manual isVisible() instead of toBeVisible()
- [ ] `MISSING-ISOLATION` - Tests share state or depend on order
- [ ] `MISSING-FRESH-CONTEXT` - State leaks between tests
- [ ] `MISSING-AUTOWAIT-TRUST` - Unnecessary manual waits
- [ ] `MISSING-NO-TIMEOUT` - waitForTimeout() present
- [ ] `MISSING-RETRY-ASSERT` - textContent()/innerText() instead of toHaveText()
- [ ] `MISSING-ALL-GUARD` - locator.all() without toHaveCount() guard
- [ ] `MISSING-INDEPENDENCE` - Tests depend on execution order
- [ ] `MISSING-STATE-ISOLATION` - Shared mutable state between tests
- [ ] `MISSING-HYDRATION-WAIT` - Interacting before React hydration (SSR)
- [ ] `MISSING-STATE-WAIT` - textContent() for async React state

⚠️ **Warning (significant reliability/maintainability impact):**
- [ ] `MISSING-TEXT-LOCATOR` - CSS classes instead of text content
- [ ] `MISSING-SPECIFIC-ASSERT` - Generic assertions
- [ ] `MISSING-LOCATOR-CHAIN` - Index-based selection (.nth(0))
- [ ] `MISSING-API-SETUP` - Slow UI-based test setup
- [ ] `MISSING-CLEANUP` - No data cleanup
- [ ] `MISSING-PAGE-OBJECT` - Inline locators in complex tests
- [ ] `MISSING-POM-SEPARATION` - Assertions in page objects
- [ ] `MISSING-RESPONSE-WAIT` - Not waiting for API responses
- [ ] `MISSING-TRACE` - No trace collection configured
- [ ] `MISSING-SCREENSHOT` - No failure screenshots
- [ ] `MISSING-MOCK-EXTERNAL` - Real calls to third-party APIs
- [ ] `MISSING-EXPLICIT-ENV` - Assumes viewport/locale/timezone
- [ ] `MISSING-ANIMATION-HANDLING` - No animation disabling
- [ ] `MISSING-PORTAL-QUERY` - Modal/tooltip queries scoped to parent (React)
- [ ] `MISSING-SUSPENSE-WAIT` - No wait for Suspense fallback (React)
- [ ] `MISSING-CONTEXT-SETUP` - Missing providers in component tests (React)
- [ ] `MISSING-API-MOCK` - No API mocking for useEffect/React Query (React)

💡 **Recommendation (best practices):**
- [ ] `MISSING-TESTID-FALLBACK` - No testid for complex scenarios
- [ ] `MISSING-NEGATIVE-ASSERT` - Only positive assertions
- [ ] `MISSING-SOFT-ASSERT` - No soft assertions for multi-check
- [ ] `MISSING-LOCATOR-PROPS` - Duplicated selectors
- [ ] `MISSING-ACTION-METHODS` - Repeated action sequences
- [ ] `MISSING-LOADSTATE` - Not waiting for page load
- [ ] `MISSING-STEPS` - No test.step for organization
- [ ] `MISSING-RETRIES` - No CI retries configured
- [ ] `MISSING-A11Y-TEST` - No accessibility testing
- [ ] `MISSING-VISUAL-TEST` - No visual regression tests
- [ ] `MISSING-DETERMINISTIC` - Assertions on random/time values
- [ ] `MISSING-COMPONENT-OBJECT` - No Component Object Model for reused React components

---

## Summary

High-quality Playwright tests follow these principles:

1. **User-Facing Locators** - getByRole > getByText > getByTestId > CSS
2. **Web-First Assertions** - toBeVisible(), toHaveText() with auto-retry
3. **Test Isolation** - Each test independent, fresh context, API setup
4. **Page Object Model** - Encapsulate locators and actions, not assertions
5. **No Hardcoded Waits** - Trust auto-wait, use waitForResponse when needed
6. **Flaky Test Prevention** - Auto-retrying assertions, guard locator.all(), mock externals
7. **Proper Debugging** - Traces, screenshots, test.step() for clarity
8. **Accessibility** - Integrate axe-core for a11y testing
9. **Visual Regression** - Screenshot comparison for UI stability
10. **React-Aware Testing** - Hydration, async state, portals, Suspense, context providers

---

*Based on Playwright official documentation, Better Stack guide, and E2E testing best practices*
*Guidelines compiled from Playwright team recommendations and community standards*

**Sources for Flaky Test Patterns:**
- [Better Stack - Flaky Tests](https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/)
- [Playwright Assertions - Race Conditions](https://dev.to/playwright/playwright-assertions-avoid-race-conditions-with-this-simple-fix-dm1)
- [Ray.run - Detecting Flaky Tests](https://ray.run/blog/detecting-and-handling-flaky-tests-in-playwright)
- [TestDino - Playwright Checklist](https://testdino.com/blog/playwright-automation-checklist/)
- [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)
- [Playwright Global Setup](https://playwright.dev/docs/test-global-setup-teardown)

**Sources for React-Specific Patterns:**
- [Playwright Component Testing](https://playwright.dev/docs/test-components)
- [Migrating from Testing Library](https://playwright.dev/docs/testing-library)
- [Next.js Playwright Testing](https://nextjs.org/docs/pages/guides/testing/playwright)
- [Playwright Hydration Issue](https://github.com/microsoft/playwright/issues/27759)
- [Next.js RSC Testing](https://github.com/kettanaito/nextjs-rsc-testing)
- [React createPortal](https://react.dev/reference/react-dom/createPortal)
