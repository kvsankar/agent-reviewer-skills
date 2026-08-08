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
