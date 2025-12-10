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

## 6. Test Organization

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

### 6. Debugging & CI Patterns

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

### Expected Patterns Summary Checklist

**When Reviewing, Verify Presence Of:**

🔴 **Critical (causes flaky or unreliable tests if missing):**
- [ ] `MISSING-ROLE-LOCATOR` - No getByRole for buttons, links, inputs
- [ ] `MISSING-WEBFIRST-ASSERT` - Manual isVisible() instead of toBeVisible()
- [ ] `MISSING-ISOLATION` - Tests share state or depend on order
- [ ] `MISSING-FRESH-CONTEXT` - State leaks between tests
- [ ] `MISSING-AUTOWAIT-TRUST` - Unnecessary manual waits
- [ ] `MISSING-NO-TIMEOUT` - waitForTimeout() present

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

---

## Summary

High-quality Playwright tests follow these principles:

1. **User-Facing Locators** - getByRole > getByText > getByTestId > CSS
2. **Web-First Assertions** - toBeVisible(), toHaveText() with auto-retry
3. **Test Isolation** - Each test independent, fresh context, API setup
4. **Page Object Model** - Encapsulate locators and actions, not assertions
5. **No Hardcoded Waits** - Trust auto-wait, use waitForResponse when needed
6. **Proper Debugging** - Traces, screenshots, test.step() for clarity
7. **Accessibility** - Integrate axe-core for a11y testing
8. **Visual Regression** - Screenshot comparison for UI stability

---

*Based on Playwright official documentation, Better Stack guide, and E2E testing best practices*
*Guidelines compiled from Playwright team recommendations and community standards*
