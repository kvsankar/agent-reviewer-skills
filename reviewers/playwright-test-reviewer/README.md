# Playwright E2E Test Reviewer Skill

A Claude Code skill that reviews Playwright end-to-end and UI tests for quality, reliability, and best practices.

## What This Skill Does

This skill reviews Playwright tests for:
- **Locator strategies** - Using role-based, accessible locators
- **Flaky test patterns** - Identifying race conditions, hard waits, brittle selectors
- **Page Object Model** - Proper abstraction and organization
- **Assertions** - Web-first assertions, avoiding weak checks
- **Test isolation** - Context management, state handling
- **Accessibility testing** - axe-core integration, WCAG compliance
- **React/Next.js patterns** - Hydration, Suspense, RSC testing

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## How to Use

Ask Claude to review your Playwright tests:

```
"Review these Playwright tests for best practices"
"Check these E2E tests for flaky patterns"
"Review this page object implementation"
"Are these locators following Playwright best practices?"
```

The skill activates on keywords like:
- Playwright, E2E, end-to-end
- Page object, POM
- Locator, selector
- Flaky, brittle, race condition

## What You'll Get

A structured review with:
- **Strengths** - What follows best practices
- **Issues** - Problems with mnemonic IDs (e.g., LOC-ROLE, WAIT-HARD)
- **Suggestions** - Concrete improvements with before/after code

### Example Review

````markdown
## Review: checkout.spec.ts

### Strengths
- **POM-FIXTURE**: Excellent use of fixtures for page objects
- **LOC-ROLE**: Good use of getByRole() for button locators

### Issues

#### WAIT-HARD: Avoid Hard-Coded Waits

**Current code:**
```typescript
await page.waitForTimeout(2000);
await page.click('#submit');
```

**Suggested:**
```typescript
await page.getByRole('button', { name: 'Submit' }).click();
```

**Why:** Hard waits cause flakiness. Playwright auto-waits for actionability.
````

## Skill Files

```
playwright-test-reviewer/
├── SKILL.md                    - Main guidelines (~1800 lines)
├── BRITTLE-FLAKY-PATTERNS.md   - Flakiness patterns (~700 lines)
├── REACT-PATTERNS.md           - React/Next.js patterns (~750 lines)
├── README.md                   - This file
└── SOURCES.md                  - Attribution
```

**Note:** This skill uses split files due to size. Claude will read all files when reviewing.

## Key Patterns

### Locator Patterns
| ID | Pattern | Description |
|----|---------|-------------|
| LOC-ROLE | Use getByRole() | Accessible, resilient locators |
| LOC-TEXT | Use getByText() | User-visible text matching |
| LOC-TESTID | Use getByTestId() | Last resort for complex cases |
| LOC-CSS | Avoid CSS selectors | Brittle, implementation-coupled |

### Flaky Test Patterns
| ID | Pattern | Description |
|----|---------|-------------|
| WAIT-HARD | No waitForTimeout() | Use auto-waiting instead |
| WAIT-NET | No networkidle | Use specific request waiting |
| RACE-CONDITION | Avoid race conditions | Use web-first assertions |
| ASSERT-CATCH | No try/catch assertions | Let assertions fail properly |

### Page Object Patterns
| ID | Pattern | Description |
|----|---------|-------------|
| POM-METHOD | Return page objects | Enable method chaining |
| POM-FIXTURE | Use fixtures | Proper dependency injection |
| POM-LOCATOR | Expose locators | Not element handles |

### Accessibility Patterns
| ID | Pattern | Description |
|----|---------|-------------|
| A11Y-AXE | Use axe-core | Automated WCAG checking |
| A11Y-KEYBOARD | Test keyboard nav | Tab order, focus management |

## When to Use This Skill

**Good for:**
- Reviewing Playwright test suites
- Finding flaky test patterns
- Improving locator strategies
- Page object model reviews
- Accessibility test coverage
- React/Next.js E2E testing

**Not ideal for:**
- Unit tests (use javascript-test-reviewer)
- Non-Playwright frameworks
- Performance testing
- Visual regression testing

## Sources

Based on:
- [Playwright Official Documentation](https://playwright.dev/docs/best-practices)
- [Better Stack Playwright Guide](https://betterstack.com/community/guides/testing/playwright-best-practices/)
- [axe-core](https://www.npmjs.com/package/@axe-core/playwright)
- [Next.js Testing Guide](https://nextjs.org/docs/pages/guides/testing/playwright)

See SOURCES.md for complete attribution.

---

**Version:** 1.0
**Last Updated:** December 2025
**Pattern Count:** 50+ patterns across 3 files
