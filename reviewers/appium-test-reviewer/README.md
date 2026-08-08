# Appium Mobile Test Reviewer Skill

A Claude Code skill that reviews Appium mobile automation tests for reliability, maintainability, and cross-platform best practices.

## What This Skill Does

This skill reviews Appium tests for:

- **Locator strategies** - Accessibility ID vs XPath, platform-specific selectors
- **Wait strategies** - Explicit waits vs Thread.sleep(), custom conditions
- **Page Object Model** - Mobile-specific page object design patterns
- **Cross-platform design** - Code reuse between iOS and Android
- **Gesture handling** - Swipe, scroll, tap, and complex gesture implementation
- **Test reliability** - Flakiness prevention, state management, retry patterns
- **Capabilities configuration** - Correct Appium 2.0 driver setup
- **Parallel execution** - Multi-device testing considerations

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## How to Use

Ask Claude to review your Appium tests:

```text
"Review these Appium tests for mobile best practices"
"Check these mobile E2E tests for flaky patterns"
"Review this mobile page object implementation"
"Are these locators following Appium best practices?"
"Review the wait strategies in these mobile tests"
```

The skill activates on keywords like:

- Appium, mobile testing, mobile automation
- iOS automation, Android automation
- XCUITest, UIAutomator2
- Accessibility ID, mobile locators
- Mobile gestures, swipe, scroll
- Page object model for mobile

## What You'll Get

A structured review with:

- **Strengths** - What follows best practices
- **Issues** - Problems with mnemonic IDs (e.g., LOC-ACCESS-ID, WAIT-EXPLICIT)
- **Suggestions** - Concrete improvements with before/after code

### Example Review

````markdown
## Appium Test Review: LoginTests.spec.js

### Strengths
- **POM-STRUCTURE**: Good use of Page Object Model with separate LoginPage class
- **ORG-NAMING**: Descriptive test names that explain expected behavior

### Critical Issues (Must Fix)

#### LOC-ACCESS-ID: Using XPath instead of Accessibility ID

**Current code:**
```javascript
const loginButton = await driver.$('//android.widget.Button[@text="Login"]');
```

**Recommended:**
```javascript
const loginButton = await driver.$('~loginButton');
```

**Why:** XPath is 10-50x slower and breaks when UI changes. Accessibility IDs
are cross-platform and stable.

#### WAIT-EXPLICIT: Using Thread.sleep instead of explicit waits

**Current code:**
```javascript
await driver.pause(3000);
const element = await driver.$('~welcomeMessage');
```

**Recommended:**
```javascript
const element = await driver.$('~welcomeMessage');
await element.waitForDisplayed({ timeout: 10000 });
```

**Why:** Thread.sleep always waits full duration. Explicit waits return
immediately when condition is met, making tests faster and more reliable.
````

## Key Patterns

### Locator Strategy Patterns

| ID | Pattern | Description |
|----|---------|-------------|
| LOC-ACCESS-ID | Use accessibility IDs | Fastest, cross-platform, stable |
| LOC-RESOURCE-ID | Use resource-id (Android) | When accessibility ID unavailable |
| LOC-PLATFORM-SELECTOR | Platform-specific selectors | UIAutomator, iOS predicates |
| LOC-AVOID-XPATH | Avoid XPath | Slow, brittle, last resort only |
| LOC-REQUEST-IDS | Request IDs from dev | Work with developers to add IDs |

### Wait Strategy Patterns

| ID | Pattern | Description |
|----|---------|-------------|
| WAIT-EXPLICIT | Use explicit waits | WebDriverWait, waitForDisplayed |
| WAIT-CUSTOM-CONDITIONS | Custom wait conditions | App-specific state checks |
| WAIT-ACTIVITY | Wait for activities | Screen transition handling |
| WAIT-NO-IMPLICIT | Avoid implicit waits | Or use carefully with low timeout |

### Page Object Patterns

| ID | Pattern | Description |
|----|---------|-------------|
| POM-STRUCTURE | Page Object Model | Separate locators from tests |
| POM-CROSS-PLATFORM | Cross-platform design | Reuse across iOS/Android |
| POM-NO-ASSERTIONS | Assertions in tests | Not in page objects |

### Gesture Patterns

| ID | Pattern | Description |
|----|---------|-------------|
| GESTURE-MOBILE-CMD | Use mobile: commands | Not deprecated TouchAction |
| GESTURE-SWIPE-HELPER | Reusable swipe helpers | Common gesture utilities |
| GESTURE-LONG-PRESS | Proper long press | Platform-specific commands |

### Reliability Patterns

| ID | Pattern | Description |
|----|---------|-------------|
| RELIABLE-APP-STATE | Reset app state | Clean state between tests |
| RELIABLE-NO-ORDER-DEPENDENCY | Independent tests | No test order dependencies |
| RELIABLE-RETRY-LOGIC | Smart retry | For inherently flaky operations |
| RELIABLE-SCREENSHOT | Screenshot on failure | Debugging artifacts |

### Configuration Patterns

| ID | Pattern | Description |
|----|---------|-------------|
| CAP-REQUIRED | Required capabilities | Essential driver configuration |
| CAP-PARALLEL | Parallel configuration | Multi-device test setup |

## Coverage Summary

The skill covers these key areas:

1. **Locator Strategies** (5 patterns)
   - Accessibility ID as primary strategy
   - Platform-specific selectors (UIAutomator, iOS predicates)
   - XPath avoidance and when to use it
   - Working with development teams on IDs

2. **Wait Strategies** (4 patterns)
   - Explicit waits vs Thread.sleep
   - Custom wait conditions
   - Activity/screen transition waits
   - Implicit wait considerations

3. **Page Object Model** (3 patterns)
   - Mobile-specific POM structure
   - Cross-platform page objects
   - Separation of concerns

4. **Mobile Gestures** (3 patterns)
   - Modern mobile: commands
   - Swipe, scroll, tap helpers
   - Long press and complex gestures

5. **Test Reliability** (4 patterns)
   - App state management
   - Test independence
   - Retry strategies
   - Screenshot capture

6. **Configuration** (2 patterns)
   - Appium 2.0 capabilities
   - Parallel execution setup

7. **Test Organization** (2 patterns)
   - Naming conventions
   - Test tagging

8. **Error Handling** (2 patterns)
   - Meaningful error messages
   - Recovery strategies

## When to Use This Skill

**Good for:**

- Reviewing Appium test suites (JavaScript/TypeScript, Python)
- Finding flaky test patterns in mobile automation
- Improving mobile locator strategies
- Page object model reviews for mobile
- Cross-platform test architecture
- Appium 2.0 migration reviews

**Not ideal for:**

- Unit tests (use javascript-test-reviewer or python-test-reviewer)
- Non-Appium mobile frameworks (Detox, Espresso, XCUITest directly)
- Web E2E tests (use playwright-test-reviewer)
- API testing

## Philosophy

This skill is built on these principles:

1. **Reliability over speed** - A slow, stable test is better than a fast, flaky one
2. **Cross-platform where possible** - Design for reuse between iOS and Android
3. **Explicit over implicit** - Be explicit about waits, locators, and state
4. **Collaboration with dev teams** - Request accessibility IDs rather than hack around missing identifiers
5. **Modern patterns** - Use Appium 2.0 features and mobile: commands

### Key Philosophy Points

**"Most test flakiness comes from synchronization issues and brittle selectors, not Appium itself"** - Jonathan Lipps, Appium Project Architect

**Locator Priority:**
1. Accessibility ID (cross-platform, fast, stable)
2. Resource ID / Name (platform-specific but stable)
3. Platform-specific selectors (UIAutomator, iOS predicates)
4. XPath (last resort only)

**Wait Priority:**
1. Explicit waits with conditions
2. Custom wait functions
3. Short implicit waits (2 seconds max)
4. Never: Thread.sleep() or hard-coded delays

## Sources

Based on:

- [Appium 2.0 Official Documentation](https://appium.io/docs/en/2.0/)
- [BrowserStack Appium Best Practices](https://www.browserstack.com/guide/appium-best-practices)
- [HeadSpin Appium Guides](https://www.headspin.io/blog/making-your-appium-tests-fast-and-reliable-part-1-test-flakiness)
- [Appium Pro Tips](https://appiumpro.com/)

See SOURCES.md for complete attribution.

---

**Version:** 1.0
**Last Updated:** January 2026
**Pattern Count:** 25+ patterns across 8 categories
