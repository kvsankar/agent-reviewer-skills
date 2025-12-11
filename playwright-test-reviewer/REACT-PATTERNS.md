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
