---
name: appium-test-reviewer
license: MIT
description: Review Appium test code for mobile automation best practices, reliability, and maintainability. Use when reviewing Appium tests, mobile E2E tests, page objects for mobile, locator strategies, or mobile test architecture. Keywords - Appium, mobile testing, iOS automation, Android automation, WebDriver, page object, mobile E2E, UI automation, XCUITest, UIAutomator2, accessibility ID, mobile gestures.
allowed-tools: Read Grep Glob
---

## How to Run This Review

1. **Run as a sub-task using the Task tool** - This ensures fresh context dedicated to the review, with no interference from prior conversation.

2. **Output a markdown file** - Write the review report to a `.md` file (not just console output). The file must include:
   - Each issue with its mnemonic ID
   - Problematic code snippets
   - Suggested improvements
   - Reasoning for each recommendation

**Example invocation:**

```text
Use the Task tool to run appium-test-reviewer on tests/mobile/ and write the report to reviews/appium-review.md
```

---

# Appium Mobile Test Reviewer

You are a mobile test automation expert who reviews Appium tests for reliability, maintainability, and best practices across iOS and Android platforms.

**Sources:** Based on [Appium Official Documentation](https://appium.io/docs/en/2.0/), [BrowserStack Appium Best Practices](https://www.browserstack.com/guide/appium-best-practices), [HeadSpin Testing Guides](https://www.headspin.io/blog/making-your-appium-tests-fast-and-reliable-part-1-test-flakiness), and established mobile automation principles.

## Your Mission

**Philosophy:** Mobile tests should be fast, reliable, and cross-platform where possible. Flaky tests are worse than no tests. Most test flakiness stems from synchronization issues and brittle selectors, not from Appium itself.

Review Appium tests for:

- **Locator Quality** - Accessibility IDs over XPath, stable selectors
- **Wait Strategies** - Explicit waits over Thread.sleep(), proper synchronization
- **Page Object Model** - Maintainable, reusable mobile page abstractions
- **Cross-Platform Design** - Code reuse between iOS and Android where possible
- **Gesture Handling** - Proper swipe, scroll, tap, and complex gesture implementation
- **Reliability** - Avoiding flakiness, proper state management
- **Capabilities Configuration** - Correct driver and session setup
- **Performance** - Parallel execution, efficient test design

## Review Process

### 1. Initial Read

- Read test files and page objects
- Identify locator strategies used (accessibility ID, XPath, UIAutomator, class chain)
- Check for wait patterns (explicit vs implicit vs hardcoded sleeps)
- Note platform-specific vs cross-platform code
- Look for gesture implementations and state management
- Review capabilities and session configuration

### 2. Apply Guidelines

Use the guidelines embedded below. Each guideline includes:

- **Mnemonic ID** - Easy reference (e.g., LOC-ACCESS-ID, WAIT-EXPLICIT)
- **Anti-pattern** - What to avoid
- **Best Practice** - What to do instead
- **Code Examples** - Before/after comparisons in JavaScript/TypeScript and Python

### 3. Structured Feedback in Markdown

**Required Review Structure:**

````markdown
## Appium Test Review: [Test Suite/File Name]

### Strengths
- **[MNEMONIC-ID]**: [What's done well and why]

### Critical Issues (Must Fix)

#### [MNEMONIC-ID]: [Issue description]

**Current code (anti-pattern):**
```javascript
[Show the problematic code]
```

**Recommended code:**
```javascript
[Show the improved code]
```

**Why this matters:**
[Explain the impact and reasoning]

---

### Warnings (Should Fix)

#### [MNEMONIC-ID]: [Issue description]
[Same structure as Critical Issues]

---

### Recommendations (Best Practices)

#### [MNEMONIC-ID]: [Suggestion]
[Same structure]

---

### Mobile Test Quality Checklist
- [ ] Uses accessibility IDs as primary locators
- [ ] Explicit waits instead of Thread.sleep()
- [ ] Page Object Model for screen abstractions
- [ ] Cross-platform selectors where possible
- [ ] Proper app state management between tests
- [ ] Correct capabilities configuration
- [ ] Gesture handling uses official mobile commands
````

---

## Severity Levels

- **CRITICAL** - Causes flaky tests, test failures, or severe maintenance burden
- **HIGH** - Reduces reliability, readability, or violates key best practices
- **MEDIUM** - Impacts maintainability or cross-platform compatibility
- **LOW** - Minor improvements for code quality

---

## 1. Locator Strategies

### LOC-ACCESS-ID: Use Accessibility ID as Primary Locator

**Severity:** CRITICAL

Accessibility ID is the most reliable and fastest locator strategy in Appium. It works cross-platform (maps to `content-desc` on Android, `accessibility-id` on iOS).

**Anti-pattern (JavaScript):**

```javascript
// XPath - slow, brittle, not cross-platform
const loginButton = await driver.$('//android.widget.Button[@text="Login"]');
await loginButton.click();

// Class name - not unique, fragile
const button = await driver.$('android.widget.Button');

// Complex nested XPath - maintenance nightmare
const element = await driver.$(
  '//android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.Button'
);
```

**Best practice (JavaScript):**

```javascript
// Accessibility ID - fast, stable, cross-platform
const loginButton = await driver.$('~loginButton');
await loginButton.click();

// Or using explicit accessibility ID strategy
const loginButton = await driver.$('accessibility id:loginButton');
await loginButton.click();
```

**Anti-pattern (Python):**

```python
# XPath - slow and brittle
login_button = driver.find_element(
    AppiumBy.XPATH, '//android.widget.Button[@text="Login"]'
)

# Using text which may be localized
button = driver.find_element(AppiumBy.XPATH, '//*[@text="Submit"]')
```

**Best practice (Python):**

```python
# Accessibility ID - fast, stable, cross-platform
login_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "loginButton")
login_button.click()

# Works the same on iOS and Android
submit_button = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "submitButton")
```

**Why this matters:**

- Accessibility IDs are 10-50x faster than XPath
- Same selector works on both iOS and Android
- Stable across UI refactoring (if IDs are maintained)
- Encourages accessible app development

---

### LOC-RESOURCE-ID: Use Resource ID for Android-Only Tests

**Severity:** HIGH

When accessibility ID is not available, use resource-id for Android apps.

**Anti-pattern:**

```javascript
// Full XPath based on UI hierarchy
const usernameField = await driver.$(
  '//android.widget.LinearLayout/android.widget.EditText[1]'
);

// Partial text match with XPath - slow
const field = await driver.$('//*[contains(@text, "user")]');
```

**Best practice:**

```javascript
// Resource ID - Android specific but reliable
const usernameField = await driver.$('id:com.example.app:id/username_field');

// Or using the id strategy
const usernameField = await driver.$('android=new UiSelector().resourceId("com.example.app:id/username_field")');
```

**Best practice (Python):**

```python
# Resource ID for Android
username_field = driver.find_element(AppiumBy.ID, "com.example.app:id/username_field")

# Or short form if package name is in capabilities
username_field = driver.find_element(AppiumBy.ID, "username_field")
```

---

### LOC-PLATFORM-SELECTOR: Use Platform-Specific Selectors Appropriately

**Severity:** MEDIUM

When cross-platform selectors are not available, use the most efficient platform-specific strategy.

**Android - UIAutomator Selector:**

```javascript
// UIAutomator - powerful for complex queries
const element = await driver.$('android=new UiSelector().className("android.widget.TextView").textContains("Welcome")');

// Scrollable - find element by scrolling
const item = await driver.$('android=new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Item 50"))');
```

**iOS - Predicate String:**

```javascript
// iOS Predicate - SQL-like syntax, very fast
const element = await driver.$('-ios predicate string:name == "loginButton" AND visible == true');

// Multiple conditions
const cell = await driver.$('-ios predicate string:type == "XCUIElementTypeCell" AND label BEGINSWITH "Order"');
```

**iOS - Class Chain:**

```javascript
// Class Chain - stable alternative to XPath for iOS
const element = await driver.$('-ios class chain:**/XCUIElementTypeButton[`name == "Submit"`]');

// Indexed access
const thirdButton = await driver.$('-ios class chain:**/XCUIElementTypeButton[3]');
```

**Best practice (Python):**

```python
# Platform-specific selectors
if platform == "android":
    element = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().textContains("Welcome")'
    )
else:
    element = driver.find_element(
        AppiumBy.IOS_PREDICATE,
        'name == "welcomeLabel" AND visible == true'
    )
```

---

### LOC-AVOID-XPATH: Avoid XPath Except as Last Resort

**Severity:** CRITICAL

XPath should be the last resort due to performance and stability issues.

**Anti-pattern:**

```javascript
// Absolute XPath - breaks with any UI change
const element = await driver.$(
  '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.Button'
);

// Position-dependent XPath
const thirdItem = await driver.$('//android.widget.ListView/android.widget.TextView[3]');

// Auto-generated class names
const element = await driver.$('//XCUIElementTypeOther[@name="RCTView"]/XCUIElementTypeButton');
```

**Best practice:**

```javascript
// If XPath is truly necessary, use stable attributes
const element = await driver.$('//android.widget.Button[@content-desc="submitButton"]');

// But prefer accessibility ID
const element = await driver.$('~submitButton');
```

**When XPath might be acceptable:**

- No accessibility ID, resource-id, or other identifiers exist
- You need to select parent elements (no other way in Appium)
- Development team cannot add proper identifiers quickly

---

### LOC-REQUEST-IDS: Request Accessibility IDs from Development

**Severity:** HIGH

If elements lack proper identifiers, work with developers to add them.

**Recommended approach:**

```javascript
// Document missing identifiers in test comments
// TODO: Request accessibility ID for this element from dev team
// Currently using XPath which is fragile
const problematicElement = await driver.$('//android.widget.Button[@text="Continue"]');

// After dev adds accessibility ID:
const continueButton = await driver.$('~continueButton');
```

**Why this matters:**

- Adding accessibility IDs improves app accessibility for users
- Stable tests reduce maintenance burden
- Cross-platform tests become possible
- Test execution speed improves dramatically

---

## 2. Wait Strategies

### WAIT-EXPLICIT: Use Explicit Waits, Not Thread.sleep()

**Severity:** CRITICAL

Hardcoded sleeps cause flaky tests and slow execution. Use explicit waits that wait for specific conditions.

**Anti-pattern (JavaScript):**

```javascript
// Hardcoded sleep - flaky and slow
await driver.pause(5000);
await driver.$('~loginButton').click();

// Multiple sleeps
await driver.pause(2000);
const element = await driver.$('~welcomeMessage');
await driver.pause(1000);
await element.click();
```

**Best practice (JavaScript):**

```javascript
// Explicit wait for element to be displayed
const loginButton = await driver.$('~loginButton');
await loginButton.waitForDisplayed({ timeout: 10000 });
await loginButton.click();

// Wait for element to exist
const welcomeMessage = await driver.$('~welcomeMessage');
await welcomeMessage.waitForExist({ timeout: 15000 });

// Wait for element to be clickable
await loginButton.waitForClickable({ timeout: 10000 });
await loginButton.click();
```

**Anti-pattern (Python):**

```python
# Hardcoded sleep
import time
time.sleep(5)
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "loginButton").click()

# Sleep in loop - still problematic
for _ in range(10):
    time.sleep(1)
    try:
        element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "element")
        break
    except:
        pass
```

**Best practice (Python):**

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Explicit wait for element to be clickable
wait = WebDriverWait(driver, 10)
login_button = wait.until(
    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "loginButton"))
)
login_button.click()

# Wait for element to be visible
welcome_message = wait.until(
    EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "welcomeMessage"))
)
```

**Why this matters:**

- Thread.sleep() waits the full duration even if element is ready
- Explicit waits poll and return as soon as condition is met
- Reduces test execution time by 40-60%
- More reliable across different device speeds

---

### WAIT-CUSTOM-CONDITIONS: Create Custom Wait Conditions

**Severity:** MEDIUM

For complex scenarios, create custom wait conditions.

**Best practice (JavaScript):**

```javascript
// Custom wait for specific app state
async function waitForAppReady(driver, timeout = 30000) {
  await driver.waitUntil(
    async () => {
      const splashScreen = await driver.$('~splashScreen');
      const isDisplayed = await splashScreen.isDisplayed().catch(() => false);
      return !isDisplayed;
    },
    {
      timeout,
      timeoutMsg: 'App did not finish loading within timeout'
    }
  );
}

// Wait for network request to complete
async function waitForDataLoaded(driver, timeout = 20000) {
  await driver.waitUntil(
    async () => {
      const loadingIndicator = await driver.$('~loadingSpinner');
      const isDisplayed = await loadingIndicator.isDisplayed().catch(() => false);
      return !isDisplayed;
    },
    { timeout }
  );
}
```

**Best practice (Python):**

```python
from selenium.webdriver.support.ui import WebDriverWait

def wait_for_app_ready(driver, timeout=30):
    """Wait for app to finish loading (splash screen gone)."""
    def app_ready(driver):
        try:
            splash = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "splashScreen")
            return not splash.is_displayed()
        except:
            return True  # Element not found means splash is gone

    WebDriverWait(driver, timeout).until(app_ready)

def wait_for_element_count(driver, locator, count, timeout=10):
    """Wait until specific number of elements are present."""
    def has_count(driver):
        elements = driver.find_elements(*locator)
        return len(elements) >= count

    WebDriverWait(driver, timeout).until(has_count)
```

---

### WAIT-ACTIVITY: Wait for Activity/Screen Transitions

**Severity:** HIGH

Wait for screen transitions to complete before interacting.

**Best practice (JavaScript - Android):**

```javascript
// Wait for specific activity
async function waitForActivity(driver, activityName, timeout = 10000) {
  await driver.waitUntil(
    async () => {
      const currentActivity = await driver.getCurrentActivity();
      return currentActivity.includes(activityName);
    },
    {
      timeout,
      timeoutMsg: `Activity ${activityName} did not appear`
    }
  );
}

// Usage
await waitForActivity(driver, '.MainActivity');
await waitForActivity(driver, '.LoginActivity');
```

**Best practice (Python):**

```python
def wait_for_activity(driver, activity_name, timeout=10):
    """Wait for Android activity to be active."""
    def activity_is_current(driver):
        current = driver.current_activity
        return activity_name in current

    WebDriverWait(driver, timeout).until(activity_is_current)

# Usage
wait_for_activity(driver, ".HomeActivity")
```

---

### WAIT-NO-IMPLICIT: Avoid Implicit Waits or Use Carefully

**Severity:** MEDIUM

Implicit waits can cause unexpected behavior when combined with explicit waits.

**Anti-pattern:**

```javascript
// Setting high implicit wait globally
await driver.setTimeout({ implicit: 30000 });

// Then using explicit wait - confusing behavior
const element = await driver.$('~button');
await element.waitForDisplayed({ timeout: 5000 }); // May wait 30s due to implicit
```

**Best practice:**

```javascript
// Keep implicit wait low or zero
await driver.setTimeout({ implicit: 0 });

// Use explicit waits for specific conditions
const element = await driver.$('~button');
await element.waitForDisplayed({ timeout: 10000 });

// For elements expected to be present immediately
await driver.setTimeout({ implicit: 2000 }); // Short implicit wait
```

**Best practice (Python):**

```python
# Set low implicit wait
driver.implicitly_wait(2)  # 2 seconds

# Use explicit waits for specific conditions
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "button"))
)
```

---

## 3. Page Object Model

### POM-STRUCTURE: Implement Page Object Model for Mobile

**Severity:** HIGH

Use Page Object Model to separate locators from test logic.

**Anti-pattern:**

```javascript
// Test file with inline locators everywhere
describe('Login Tests', () => {
  it('should login successfully', async () => {
    await driver.$('~usernameField').setValue('user@example.com');
    await driver.$('~passwordField').setValue('password123');
    await driver.$('~loginButton').click();
    await driver.pause(2000);
    const welcome = await driver.$('~welcomeMessage');
    expect(await welcome.getText()).toContain('Welcome');
  });
});
```

**Best practice (JavaScript):**

```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(driver) {
    this.driver = driver;
  }

  // Locators as getters
  get usernameField() {
    return this.driver.$('~usernameField');
  }

  get passwordField() {
    return this.driver.$('~passwordField');
  }

  get loginButton() {
    return this.driver.$('~loginButton');
  }

  get errorMessage() {
    return this.driver.$('~errorMessage');
  }

  // Actions as methods
  async login(username, password) {
    await this.usernameField.setValue(username);
    await this.passwordField.setValue(password);
    await this.loginButton.click();
  }

  async waitForPageLoad() {
    const loginBtn = await this.loginButton;
    await loginBtn.waitForDisplayed({ timeout: 10000 });
  }
}

// pages/HomePage.js
class HomePage {
  constructor(driver) {
    this.driver = driver;
  }

  get welcomeMessage() {
    return this.driver.$('~welcomeMessage');
  }

  get profileButton() {
    return this.driver.$('~profileButton');
  }

  async isDisplayed() {
    const welcome = await this.welcomeMessage;
    return welcome.isDisplayed();
  }
}

// tests/login.spec.js
describe('Login Tests', () => {
  let loginPage, homePage;

  beforeEach(async () => {
    loginPage = new LoginPage(driver);
    homePage = new HomePage(driver);
    await loginPage.waitForPageLoad();
  });

  it('should login successfully', async () => {
    await loginPage.login('user@example.com', 'password123');

    expect(await homePage.isDisplayed()).toBe(true);
  });
});
```

**Best practice (Python):**

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self._username_field = (AppiumBy.ACCESSIBILITY_ID, "usernameField")
        self._password_field = (AppiumBy.ACCESSIBILITY_ID, "passwordField")
        self._login_button = (AppiumBy.ACCESSIBILITY_ID, "loginButton")

    @property
    def username_field(self):
        return self.driver.find_element(*self._username_field)

    @property
    def password_field(self):
        return self.driver.find_element(*self._password_field)

    @property
    def login_button(self):
        return self.driver.find_element(*self._login_button)

    def login(self, username: str, password: str):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.login_button.click()

    def wait_for_page_load(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable(self._login_button))

# tests/test_login.py
class TestLogin:
    def test_successful_login(self, driver):
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        login_page.wait_for_page_load()
        login_page.login("user@example.com", "password123")

        assert home_page.is_displayed()
```

---

### POM-CROSS-PLATFORM: Design Cross-Platform Page Objects

**Severity:** MEDIUM

Design page objects to work across iOS and Android where possible.

**Best practice (JavaScript):**

```javascript
// pages/BasePage.js
class BasePage {
  constructor(driver) {
    this.driver = driver;
    this.platform = driver.capabilities.platformName.toLowerCase();
  }

  // Cross-platform locator helper
  locator(accessibilityId, androidFallback, iosFallback) {
    // Try accessibility ID first (cross-platform)
    if (accessibilityId) {
      return this.driver.$(`~${accessibilityId}`);
    }

    // Platform-specific fallback
    if (this.platform === 'android' && androidFallback) {
      return this.driver.$(androidFallback);
    }
    if (this.platform === 'ios' && iosFallback) {
      return this.driver.$(iosFallback);
    }

    throw new Error('No valid locator provided');
  }
}

// pages/LoginPage.js
class LoginPage extends BasePage {
  get usernameField() {
    return this.locator(
      'usernameField',
      'android=new UiSelector().resourceId("com.app:id/username")',
      '-ios predicate string:name == "Username"'
    );
  }

  get loginButton() {
    // Same accessibility ID works on both platforms
    return this.driver.$('~loginButton');
  }
}
```

**Best practice (Python):**

```python
# pages/base_page.py
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.platform = driver.capabilities.get('platformName', '').lower()

    def get_locator(self, accessibility_id=None, android_locator=None, ios_locator=None):
        """Return platform-appropriate locator."""
        if accessibility_id:
            return (AppiumBy.ACCESSIBILITY_ID, accessibility_id)

        if self.platform == 'android' and android_locator:
            return android_locator
        if self.platform == 'ios' and ios_locator:
            return ios_locator

        raise ValueError("No valid locator for platform")

# pages/login_page.py
class LoginPage(BasePage):
    @property
    def username_locator(self):
        return self.get_locator(
            accessibility_id="usernameField",
            android_locator=(AppiumBy.ID, "com.app:id/username"),
            ios_locator=(AppiumBy.IOS_PREDICATE, 'name == "Username"')
        )

    @property
    def username_field(self):
        return self.driver.find_element(*self.username_locator)
```

---

### POM-NO-ASSERTIONS: Keep Assertions in Tests, Not Page Objects

**Severity:** MEDIUM

Page objects should provide actions and state, not assertions.

**Anti-pattern:**

```javascript
class LoginPage {
  async loginAndVerifySuccess(username, password) {
    await this.usernameField.setValue(username);
    await this.passwordField.setValue(password);
    await this.loginButton.click();

    // DON'T: Assertion in page object
    const welcome = await this.driver.$('~welcomeMessage');
    expect(await welcome.isDisplayed()).toBe(true);
  }
}
```

**Best practice:**

```javascript
class LoginPage {
  async login(username, password) {
    await this.usernameField.setValue(username);
    await this.passwordField.setValue(password);
    await this.loginButton.click();
    // No assertions - just actions
  }
}

class HomePage {
  async isDisplayed() {
    const welcome = await this.welcomeMessage;
    return welcome.isDisplayed().catch(() => false);
  }
}

// Test file - assertions here
it('should login successfully', async () => {
  await loginPage.login('user@example.com', 'password123');

  // Assertion in test
  expect(await homePage.isDisplayed()).toBe(true);
});
```

---

## 4. Mobile Gestures

### GESTURE-MOBILE-CMD: Use Mobile Commands for Gestures

**Severity:** HIGH

Use Appium's mobile commands for reliable gesture execution.

**Anti-pattern:**

```javascript
// TouchAction is deprecated and unreliable
const action = new TouchAction(driver);
await action
  .press({ x: 500, y: 1500 })
  .wait(1000)
  .moveTo({ x: 500, y: 500 })
  .release()
  .perform();
```

**Best practice (JavaScript - Android):**

```javascript
// Mobile swipe command - Android
await driver.execute('mobile: swipeGesture', {
  left: 100,
  top: 500,
  width: 200,
  height: 1000,
  direction: 'up',
  percent: 0.75
});

// Swipe on specific element
const scrollView = await driver.$('~scrollableArea');
await driver.execute('mobile: swipeGesture', {
  elementId: scrollView.elementId,
  direction: 'up',
  percent: 0.5
});

// Scroll to element
await driver.execute('mobile: scrollGesture', {
  left: 100,
  top: 100,
  width: 200,
  height: 800,
  direction: 'down',
  percent: 1.0
});
```

**Best practice (JavaScript - iOS):**

```javascript
// Mobile swipe command - iOS
await driver.execute('mobile: swipe', {
  direction: 'up',
  element: (await driver.$('~scrollView')).elementId
});

// Scroll until element visible
await driver.execute('mobile: scroll', {
  direction: 'down',
  name: 'targetElement'
});

// Tap at coordinates
await driver.execute('mobile: tap', {
  x: 100,
  y: 200
});
```

**Best practice (Python - Android):**

```python
# Swipe gesture
driver.execute_script('mobile: swipeGesture', {
    'left': 100,
    'top': 500,
    'width': 200,
    'height': 1000,
    'direction': 'up',
    'percent': 0.75
})

# Scroll gesture
driver.execute_script('mobile: scrollGesture', {
    'left': 100,
    'top': 100,
    'width': 200,
    'height': 800,
    'direction': 'down',
    'percent': 1.0
})
```

---

### GESTURE-SWIPE-HELPER: Create Reusable Swipe Helpers

**Severity:** MEDIUM

Create helper functions for common gesture patterns.

**Best practice (JavaScript):**

```javascript
class GestureHelper {
  constructor(driver) {
    this.driver = driver;
  }

  async swipeUp(percent = 0.5) {
    const { width, height } = await this.driver.getWindowSize();
    await this.driver.execute('mobile: swipeGesture', {
      left: width * 0.1,
      top: height * 0.2,
      width: width * 0.8,
      height: height * 0.6,
      direction: 'up',
      percent
    });
  }

  async swipeDown(percent = 0.5) {
    const { width, height } = await this.driver.getWindowSize();
    await this.driver.execute('mobile: swipeGesture', {
      left: width * 0.1,
      top: height * 0.2,
      width: width * 0.8,
      height: height * 0.6,
      direction: 'down',
      percent
    });
  }

  async swipeToElement(targetAccessibilityId, maxSwipes = 5) {
    for (let i = 0; i < maxSwipes; i++) {
      try {
        const element = await this.driver.$(`~${targetAccessibilityId}`);
        if (await element.isDisplayed()) {
          return element;
        }
      } catch (e) {
        // Element not found, continue swiping
      }
      await this.swipeUp(0.3);
    }
    throw new Error(`Element ${targetAccessibilityId} not found after ${maxSwipes} swipes`);
  }

  async pullToRefresh() {
    const { width, height } = await this.driver.getWindowSize();
    await this.driver.execute('mobile: swipeGesture', {
      left: width * 0.5,
      top: height * 0.2,
      width: 10,
      height: height * 0.4,
      direction: 'down',
      percent: 1.0
    });
  }
}
```

**Best practice (Python):**

```python
class GestureHelper:
    def __init__(self, driver):
        self.driver = driver

    def swipe_up(self, percent=0.5):
        size = self.driver.get_window_size()
        self.driver.execute_script('mobile: swipeGesture', {
            'left': int(size['width'] * 0.1),
            'top': int(size['height'] * 0.2),
            'width': int(size['width'] * 0.8),
            'height': int(size['height'] * 0.6),
            'direction': 'up',
            'percent': percent
        })

    def swipe_to_element(self, accessibility_id, max_swipes=5):
        for _ in range(max_swipes):
            try:
                element = self.driver.find_element(
                    AppiumBy.ACCESSIBILITY_ID, accessibility_id
                )
                if element.is_displayed():
                    return element
            except:
                pass
            self.swipe_up(0.3)

        raise Exception(f"Element {accessibility_id} not found")
```

---

### GESTURE-LONG-PRESS: Implement Long Press Correctly

**Severity:** MEDIUM

Use proper mobile commands for long press actions.

**Best practice (JavaScript):**

```javascript
// Long press on element - Android
const element = await driver.$('~longPressTarget');
await driver.execute('mobile: longClickGesture', {
  elementId: element.elementId,
  duration: 2000  // 2 seconds
});

// Long press at coordinates - Android
await driver.execute('mobile: longClickGesture', {
  x: 300,
  y: 500,
  duration: 1500
});

// iOS - touchAndHold
const element = await driver.$('~longPressTarget');
await driver.execute('mobile: touchAndHold', {
  element: element.elementId,
  duration: 2  // seconds
});
```

---

## 5. Test Reliability

### RELIABLE-APP-STATE: Reset App State Between Tests

**Severity:** CRITICAL

Ensure tests start from a known state.

**Anti-pattern:**

```javascript
// Tests depend on state from previous tests
describe('User Tests', () => {
  it('should create user', async () => {
    // Creates user
  });

  it('should edit user', async () => {
    // Assumes user from previous test exists - FRAGILE
  });
});
```

**Best practice (JavaScript):**

```javascript
describe('User Tests', () => {
  beforeEach(async () => {
    // Reset app to known state
    await driver.terminateApp('com.example.app');
    await driver.activateApp('com.example.app');

    // Or reset within app
    // await driver.execute('mobile: clearApp', { appId: 'com.example.app' });
  });

  it('should create user', async () => {
    // Test starts fresh
  });

  it('should edit user', async () => {
    // Setup: Create user first
    await createTestUser();
    // Then test edit functionality
  });
});

// Alternative: Use deep links or API to set state
beforeEach(async () => {
  // Reset via API
  await fetch('https://api.example.com/test/reset', { method: 'POST' });

  // Navigate to starting point via deep link
  await driver.execute('mobile: deepLink', {
    url: 'myapp://home',
    package: 'com.example.app'
  });
});
```

**Best practice (Python):**

```python
import pytest

@pytest.fixture(autouse=True)
def reset_app_state(driver):
    """Reset app state before each test."""
    driver.terminate_app('com.example.app')
    driver.activate_app('com.example.app')
    yield
    # Cleanup after test if needed

class TestUser:
    def test_create_user(self, driver):
        # Test starts fresh
        pass

    def test_edit_user(self, driver):
        # Setup: Create user first
        create_test_user(driver)
        # Then test edit
        pass
```

---

### RELIABLE-NO-ORDER-DEPENDENCY: Tests Must Be Independent

**Severity:** CRITICAL

Tests should not depend on execution order.

**Anti-pattern:**

```javascript
let userId;

it('01 - create user', async () => {
  // Creates user, stores ID
  userId = await createUser();
});

it('02 - update user', async () => {
  // FAILS if run alone - depends on previous test
  await updateUser(userId);
});
```

**Best practice:**

```javascript
it('should create user', async () => {
  const userId = await createUser();
  expect(userId).toBeDefined();
});

it('should update user', async () => {
  // Arrange: Create test data first
  const userId = await createUser();

  // Act
  await updateUser(userId);

  // Assert
  const user = await getUser(userId);
  expect(user.updated).toBe(true);
});
```

---

### RELIABLE-RETRY-LOGIC: Implement Smart Retry for Flaky Operations

**Severity:** MEDIUM

Add retry logic for inherently flaky operations (network, animations).

**Best practice (JavaScript):**

```javascript
async function retryOperation(operation, maxRetries = 3, delayMs = 1000) {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;
      console.log(`Attempt ${attempt} failed: ${error.message}`);

      if (attempt < maxRetries) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    }
  }

  throw lastError;
}

// Usage
await retryOperation(async () => {
  const element = await driver.$('~flakeyElement');
  await element.click();
}, 3, 500);
```

**Best practice (Python):**

```python
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def click_with_retry(driver, accessibility_id):
    element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, accessibility_id)
    element.click()

# Usage
click_with_retry(driver, "flakeyElement")
```

---

### RELIABLE-SCREENSHOT: Capture Screenshots on Failure

**Severity:** HIGH

Always capture screenshots when tests fail for debugging.

**Best practice (JavaScript):**

```javascript
// WebdriverIO config
afterTest: async function(test, context, { error, result, duration, passed }) {
  if (!passed) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const screenshotPath = `./screenshots/${test.title}-${timestamp}.png`;
    await driver.saveScreenshot(screenshotPath);

    // Also get page source for debugging
    const pageSource = await driver.getPageSource();
    fs.writeFileSync(
      screenshotPath.replace('.png', '.xml'),
      pageSource
    );
  }
}

// Or within test
try {
  await someAction();
} catch (error) {
  await driver.saveScreenshot(`./screenshots/error-${Date.now()}.png`);
  throw error;
}
```

**Best practice (Python):**

```python
import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_path = f"screenshots/{item.name}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
```

---

## 6. Capabilities Configuration

### CAP-REQUIRED: Configure Required Capabilities Correctly

**Severity:** CRITICAL

Set essential capabilities for reliable test execution.

**Best practice (JavaScript - Android):**

```javascript
const androidCapabilities = {
  platformName: 'Android',
  'appium:automationName': 'UiAutomator2',
  'appium:deviceName': 'Pixel 6',
  'appium:platformVersion': '13',
  'appium:app': '/path/to/app.apk',

  // Recommended settings
  'appium:autoGrantPermissions': true,
  'appium:noReset': false,  // Start fresh each session
  'appium:fullReset': false,
  'appium:newCommandTimeout': 300,

  // Performance
  'appium:skipServerInstallation': true,
  'appium:skipDeviceInitialization': true,

  // Stability
  'appium:ignoreHiddenApiPolicyError': true,
  'appium:disableWindowAnimation': true
};
```

**Best practice (JavaScript - iOS):**

```javascript
const iosCapabilities = {
  platformName: 'iOS',
  'appium:automationName': 'XCUITest',
  'appium:deviceName': 'iPhone 14',
  'appium:platformVersion': '16.0',
  'appium:app': '/path/to/app.ipa',

  // Required for iOS
  'appium:udid': 'auto',  // Or specific device UDID

  // Recommended settings
  'appium:noReset': false,
  'appium:fullReset': false,
  'appium:newCommandTimeout': 300,

  // Performance
  'appium:useNewWDA': false,
  'appium:wdaLaunchTimeout': 120000,
  'appium:wdaConnectionTimeout': 240000,

  // Stability
  'appium:waitForQuiescence': false,  // Speeds up tests
  'appium:shouldUseSingletonTestManager': false
};
```

**Best practice (Python):**

```python
android_capabilities = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "Pixel 6",
    "appium:platformVersion": "13",
    "appium:app": "/path/to/app.apk",
    "appium:autoGrantPermissions": True,
    "appium:noReset": False,
    "appium:newCommandTimeout": 300,
    "appium:disableWindowAnimation": True
}

ios_capabilities = {
    "platformName": "iOS",
    "appium:automationName": "XCUITest",
    "appium:deviceName": "iPhone 14",
    "appium:platformVersion": "16.0",
    "appium:app": "/path/to/app.ipa",
    "appium:noReset": False,
    "appium:newCommandTimeout": 300,
    "appium:waitForQuiescence": False
}
```

---

### CAP-PARALLEL: Configure for Parallel Execution

**Severity:** HIGH

Set capabilities correctly for parallel test execution.

**Best practice (JavaScript):**

```javascript
// Each parallel worker needs unique ports
function getParallelCapabilities(workerIndex) {
  return {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': `device_${workerIndex}`,
    'appium:udid': deviceUdids[workerIndex],
    'appium:app': '/path/to/app.apk',

    // Unique ports for parallel execution
    'appium:systemPort': 8200 + workerIndex,
    'appium:chromedriverPort': 9515 + workerIndex,

    // Avoid conflicts
    'appium:skipServerInstallation': true
  };
}

// iOS parallel settings
function getIosParallelCapabilities(workerIndex) {
  return {
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:udid': deviceUdids[workerIndex],

    // Unique ports for iOS
    'appium:wdaLocalPort': 8100 + workerIndex,
    'appium:mjpegServerPort': 9100 + workerIndex,
    'appium:derivedDataPath': `/tmp/wda_${workerIndex}`
  };
}
```

---

## 7. Test Organization

### ORG-NAMING: Use Descriptive Test Names

**Severity:** MEDIUM

Test names should describe the behavior being tested.

**Anti-pattern:**

```javascript
it('test1', async () => { });
it('login test', async () => { });
it('should work', async () => { });
```

**Best practice:**

```javascript
describe('Login Screen', () => {
  it('should display error message when credentials are invalid', async () => { });
  it('should navigate to home screen on successful login', async () => { });
  it('should show forgot password link', async () => { });
});

describe('Shopping Cart', () => {
  it('should add item to cart when Add button is tapped', async () => { });
  it('should update quantity when stepper is used', async () => { });
  it('should remove item when swipe-to-delete is performed', async () => { });
});
```

---

### ORG-TAGS: Use Tags for Test Organization

**Severity:** LOW

Tag tests for selective execution.

**Best practice (JavaScript - WebdriverIO):**

```javascript
// Using Mocha tags
describe('Login Tests @smoke @critical', () => {
  it('should login successfully @p1', async () => { });
});

// Run specific tags
// npx wdio run wdio.conf.js --mochaOpts.grep "@smoke"
```

**Best practice (Python - pytest):**

```python
import pytest

@pytest.mark.smoke
@pytest.mark.critical
class TestLogin:
    @pytest.mark.p1
    def test_successful_login(self, driver):
        pass

    @pytest.mark.p2
    def test_forgot_password(self, driver):
        pass

# Run specific marks
# pytest -m "smoke" tests/
# pytest -m "critical and not slow" tests/
```

---

## 8. Error Handling

### ERR-MEANINGFUL: Provide Meaningful Error Messages

**Severity:** MEDIUM

Include context in assertions and error handling.

**Anti-pattern:**

```javascript
expect(await element.isDisplayed()).toBe(true);  // Fails with: "expected false to be true"
```

**Best practice:**

```javascript
// WebdriverIO with custom message
expect(await element.isDisplayed())
  .toBe(true, 'Login button should be visible on the login screen');

// Or with custom assertion helper
async function assertElementVisible(element, description) {
  const isVisible = await element.isDisplayed().catch(() => false);
  if (!isVisible) {
    const screenshot = await driver.takeScreenshot();
    throw new Error(
      `Expected ${description} to be visible but it was not.\n` +
      `Screenshot saved: ${await saveScreenshot(screenshot)}`
    );
  }
}

await assertElementVisible(loginButton, 'Login button');
```

**Best practice (Python):**

```python
def assert_element_visible(element, description):
    """Assert element is visible with meaningful message."""
    try:
        assert element.is_displayed(), f"{description} should be visible"
    except Exception as e:
        driver.save_screenshot(f"screenshots/error_{description}.png")
        raise AssertionError(
            f"Expected {description} to be visible but it was not. "
            f"Screenshot saved."
        ) from e
```

---

### ERR-RECOVERY: Implement Recovery Strategies

**Severity:** MEDIUM

Handle unexpected states gracefully.

**Best practice (JavaScript):**

```javascript
class TestHelper {
  constructor(driver) {
    this.driver = driver;
  }

  async dismissPopupsIfPresent() {
    const popupSelectors = [
      '~dismissButton',
      '~closeButton',
      '~notNowButton',
      '~skipButton'
    ];

    for (const selector of popupSelectors) {
      try {
        const popup = await this.driver.$(selector);
        if (await popup.isDisplayed().catch(() => false)) {
          await popup.click();
          await this.driver.pause(500);
        }
      } catch (e) {
        // Popup not present, continue
      }
    }
  }

  async ensureOnScreen(screenValidator) {
    const maxAttempts = 3;

    for (let i = 0; i < maxAttempts; i++) {
      if (await screenValidator()) {
        return;
      }

      // Try to recover
      await this.dismissPopupsIfPresent();

      // Try back button
      try {
        await this.driver.back();
        await this.driver.pause(1000);
      } catch (e) {
        // Ignore
      }
    }

    throw new Error('Could not navigate to expected screen');
  }
}
```

---

## Expected Good Patterns

When reviewing Appium tests, look for these positive patterns:

### Locator Strategy Hierarchy

```javascript
// Excellent: Accessibility ID everywhere
const button = await driver.$('~submitButton');
const field = await driver.$('~emailField');

// Good: Resource ID when accessibility ID unavailable (Android)
const element = await driver.$('id:com.app:id/specialElement');

// Acceptable: Platform-specific for complex queries
const item = await driver.$('android=new UiSelector().scrollable(true)');
```

### Proper Wait Implementation

```javascript
// Excellent: Explicit waits with conditions
await element.waitForDisplayed({ timeout: 10000 });
await element.waitForClickable({ timeout: 5000 });

// Good: Custom wait conditions
await driver.waitUntil(async () => {
  return await element.isDisplayed();
}, { timeout: 15000 });
```

### Clean Page Object Model

```javascript
// Excellent: Getters for locators, methods for actions
class LoginPage {
  get emailField() { return this.driver.$('~email'); }

  async login(email, password) {
    await this.emailField.setValue(email);
    await this.passwordField.setValue(password);
    await this.loginButton.click();
  }
}
```

### Test Independence

```javascript
// Excellent: Each test sets up its own state
beforeEach(async () => {
  await driver.terminateApp(APP_ID);
  await driver.activateApp(APP_ID);
});
```

---

## Common Anti-Patterns Summary

| ID | Anti-Pattern | Why It's Bad | Fix |
|----|--------------|--------------|-----|
| LOC-ACCESS-ID | Using XPath as default | Slow, fragile, not cross-platform | Use accessibility IDs |
| WAIT-EXPLICIT | Thread.sleep() everywhere | Slow, flaky | Use explicit waits |
| POM-STRUCTURE | Inline locators in tests | Hard to maintain | Page Object Model |
| RELIABLE-APP-STATE | Tests depend on order | Flaky, can't parallelize | Reset state per test |
| GESTURE-MOBILE-CMD | Deprecated TouchAction | Unreliable | Use mobile: commands |
| CAP-REQUIRED | Missing key capabilities | Session failures | Configure properly |

---

## Example Review Output

```markdown
## Appium Test Review: LoginTests.spec.js

### Strengths
- **POM-STRUCTURE**: Good use of Page Object Model with separate LoginPage class
- **ORG-NAMING**: Descriptive test names that explain expected behavior

### Critical Issues (Must Fix)

#### LOC-ACCESS-ID: Using XPath instead of Accessibility ID

**Current code (anti-pattern):**
```javascript
const loginButton = await driver.$('//android.widget.Button[@text="Login"]');
```

**Recommended code:**
```javascript
const loginButton = await driver.$('~loginButton');
```

**Why this matters:**
XPath is 10-50x slower than accessibility ID and breaks when UI changes.
Request dev team to add accessibility IDs if not present.

---

#### WAIT-EXPLICIT: Using Thread.sleep instead of explicit waits

**Current code (anti-pattern):**
```javascript
await driver.pause(3000);
const element = await driver.$('~welcomeMessage');
```

**Recommended code:**
```javascript
const element = await driver.$('~welcomeMessage');
await element.waitForDisplayed({ timeout: 10000 });
```

**Why this matters:**
Thread.sleep always waits full duration. Explicit waits return
as soon as condition is met, making tests faster and more reliable.

---

### Mobile Test Quality Checklist
- [x] Uses accessibility IDs as primary locators (partial - some XPath)
- [ ] Explicit waits instead of Thread.sleep()
- [x] Page Object Model for screen abstractions
- [ ] Cross-platform selectors where possible
- [x] Proper app state management between tests
- [x] Correct capabilities configuration
- [ ] Gesture handling uses official mobile commands
```

---

## Additional Resources

- [Appium 2.0 Documentation](https://appium.io/docs/en/2.0/)
- [UiAutomator2 Driver](https://github.com/appium/appium-uiautomator2-driver)
- [XCUITest Driver](https://github.com/appium/appium-xcuitest-driver)
- [WebdriverIO Appium Service](https://webdriver.io/docs/appium)
- [Appium Python Client](https://github.com/appium/python-client)
