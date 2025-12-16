# Sources and Attribution

## Primary Sources

### Playwright Official Documentation

The core guidelines in this skill are based on Playwright's official best practices and documentation.

- **Best Practices:** https://playwright.dev/docs/best-practices
- **Locators:** https://playwright.dev/docs/locators
- **Assertions:** https://playwright.dev/docs/test-assertions
- **Test Isolation:** https://playwright.dev/docs/browser-contexts
- **Page Object Model:** https://playwright.dev/docs/pom
- **Accessibility Testing:** https://playwright.dev/docs/accessibility-testing
- **Trace Viewer:** https://playwright.dev/docs/trace-viewer
- **Test Fixtures:** https://playwright.dev/docs/test-fixtures
- **Global Setup/Teardown:** https://playwright.dev/docs/test-global-setup-teardown
- **Component Testing:** https://playwright.dev/docs/test-components
- **Migrating from Testing Library:** https://playwright.dev/docs/testing-library

### Better Stack Guides

Comprehensive guides on Playwright best practices and avoiding flaky tests.

- **Playwright Best Practices:** https://betterstack.com/community/guides/testing/playwright-best-practices/
- **Avoiding Flaky Tests:** https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/

### Accessibility Testing

- **axe-core/playwright:** https://www.npmjs.com/package/@axe-core/playwright
- Deque Systems axe-core accessibility engine

### Flaky Test Patterns

Additional resources for identifying and fixing flaky tests:

- **dev.to - Playwright Assertions:** https://dev.to/playwright/playwright-assertions-avoid-race-conditions-with-this-simple-fix-dm1
- **Ray.run - Detecting Flaky Tests:** https://ray.run/blog/detecting-and-handling-flaky-tests-in-playwright
- **TestDino - Playwright Checklist:** https://testdino.com/blog/playwright-automation-checklist/

### React/Next.js Testing

Resources for testing React and Next.js applications:

- **Next.js Playwright Testing:** https://nextjs.org/docs/pages/guides/testing/playwright
- **Playwright Hydration Issues:** https://github.com/microsoft/playwright/issues/27759
- **Next.js RSC Testing:** https://github.com/kettanaito/nextjs-rsc-testing
- **React createPortal:** https://react.dev/reference/react-dom/createPortal

## Guideline Categories

### Core Patterns (from Playwright docs)
- LOC-ROLE, LOC-TEXT, LOC-TESTID - Locator strategies
- ASSERT-WEB, ASSERT-EXPECT - Web-first assertions
- POM-METHOD, POM-FIXTURE - Page Object Model patterns
- ISO-CONTEXT, ISO-STORAGE - Test isolation

### Flaky Test Patterns (from Better Stack, dev.to, Ray.run)
- WAIT-HARD, WAIT-NET - Timing anti-patterns
- RACE-CONDITION, RACE-NETWORK - Race condition patterns
- ASSERT-CATCH, ASSERT-WEAK - Assertion anti-patterns

### Accessibility Patterns (from axe-core)
- A11Y-AXE, A11Y-KEYBOARD, A11Y-FOCUS - Accessibility testing

### React Patterns (from Next.js docs, Playwright component testing)
- REACT-HYDRATION, REACT-SUSPENSE - React-specific patterns
- NEXT-RSC, NEXT-ROUTER - Next.js patterns

## Copyright Notice

- **Playwright Documentation** - MIT License, Microsoft Corporation
- **Better Stack Guides** - Used with attribution
- **axe-core** - Mozilla Public License 2.0, Deque Systems
- **Next.js Documentation** - MIT License, Vercel

## Contributing

When adding new patterns to this skill:
1. Cite the authoritative source
2. Link to official documentation where possible
3. Prefer Playwright official docs over third-party sources
4. Test patterns against real Playwright test suites
