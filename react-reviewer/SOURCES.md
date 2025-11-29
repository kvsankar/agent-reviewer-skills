# Sources and Attribution

This React Reviewer skill is based on official React documentation, community best practices, and authoritative sources from the React ecosystem.

## Primary Sources

### 1. React Official Documentation
**Source:** React Core Team  
**URL:** https://react.dev/  
**Relevance:** Official React documentation, core concepts, best practices

**Key resources:**
- **Learn React** - https://react.dev/learn
- **API Reference** - https://react.dev/reference
- **Rules of Hooks** - https://react.dev/reference/rules/rules-of-hooks
- **Thinking in React** - https://react.dev/learn/thinking-in-react

**Guidelines influenced:**
- HOOK-RULES - Rules of Hooks
- USE-EFFECT-DEPS - Synchronizing with Effects
- USE-EFFECT-CLEANUP - Lifecycle of Effects
- LIFTING-STATE - Sharing State Between Components
- DERIVED-STATE - Choosing the State Structure
- COMPOSITION - Passing Props to a Component

---

### 2. React Team Blog & Articles

#### "A Complete Guide to useEffect" by Dan Abramov
**URL:** https://overreacted.io/a-complete-guide-to-useeffect/  
**Relevance:** Comprehensive useEffect understanding

**Guidelines influenced:**
- USE-EFFECT-DEPS
- USE-EFFECT-CLEANUP
- STALE-CLOSURE
- AVOID-SYNC

#### "Before You memo()" by Dan Abramov
**URL:** https://overreacted.io/before-you-memo/  
**Relevance:** When memoization is actually needed

**Guidelines influenced:**
- OVER-MEMO
- MEMO-COMPONENT
- USE-CALLBACK
- STATE-COLOCATION

#### "Writing Resilient Components" by Dan Abramov
**URL:** https://overreacted.io/writing-resilient-components/  
**Relevance:** Component design principles

**Guidelines influenced:**
- SINGLE-RESPONSIBILITY
- DERIVED-STATE
- AVOID-SYNC

---

### 3. Kent C. Dodds - Testing Library & Best Practices
**URL:** https://kentcdodds.com/  
**Relevance:** Testing methodology, React patterns

**Key articles:**
- **Testing Implementation Details** - https://kentcdodds.com/blog/testing-implementation-details
- **Common Mistakes with React Testing Library** - https://kentcdodds.com/blog/common-mistakes-with-react-testing-library
- **AHA Testing** - https://kentcdodds.com/blog/aha-testing
- **Colocation** - https://kentcdodds.com/blog/colocation

**Guidelines influenced:**
- TEST-BEHAVIOR
- TEST-QUERIES
- MOCK-BOUNDARIES
- STATE-COLOCATION

---

### 4. React Testing Library
**Source:** Kent C. Dodds and contributors  
**URL:** https://testing-library.com/docs/react-testing-library/intro/  
**Relevance:** Testing best practices

**Key resources:**
- **Queries** - https://testing-library.com/docs/queries/about
- **Priority** - https://testing-library.com/docs/queries/about#priority
- **Async Utilities** - https://testing-library.com/docs/dom-testing-library/api-async

**Guidelines influenced:**
- TEST-QUERIES
- TEST-ASYNC
- TEST-ACCESSIBILITY

---

### 5. WAI-ARIA and Web Accessibility
**Sources:**
- **W3C WAI-ARIA** - https://www.w3.org/WAI/ARIA/
- **MDN Accessibility** - https://developer.mozilla.org/en-US/docs/Web/Accessibility
- **WebAIM** - https://webaim.org/
- **A11y Project** - https://www.a11yproject.com/

**Guidelines influenced:**
- SEMANTIC-HTML
- ARIA-LABELS
- KEYBOARD-NAV
- FOCUS-MANAGEMENT
- HEADING-ORDER
- SCREEN-READER
- COLOR-CONTRAST
- FOCUS-VISIBLE

---

### 6. React Patterns and Best Practices

#### Compound Components Pattern
**Sources:**
- React Training - https://reacttraining.com/
- Kent C. Dodds - Advanced React Patterns

**Guidelines influenced:**
- COMPOUND-COMPONENTS
- CHILDREN-PATTERN
- RENDER-PROPS

#### Context API Best Practices
**Source:** React Documentation  
**URL:** https://react.dev/learn/passing-data-deeply-with-context

**Guidelines influenced:**
- USE-CONTEXT
- CONTEXT-MODULE
- COMPOSITION

---

### 7. React Performance Documentation
**Source:** React Team  
**URL:** https://react.dev/reference/react/memo

**Key resources:**
- **React.memo** - https://react.dev/reference/react/memo
- **useMemo** - https://react.dev/reference/react/useMemo
- **useCallback** - https://react.dev/reference/react/useCallback
- **useTransition** - https://react.dev/reference/react/useTransition

**Guidelines influenced:**
- MEMO-COMPONENT
- USE-MEMO
- USE-CALLBACK
- TRANSITIONS
- LAZY-LOADING
- SUSPENSE

---

### 8. Error Boundaries Documentation
**Source:** React Documentation  
**URL:** https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary

**Related:**
- **react-error-boundary** - https://github.com/bvaughn/react-error-boundary

**Guidelines influenced:**
- ERROR-BOUNDARY
- ASYNC-ERROR

---

### 9. React Hook Form
**URL:** https://react-hook-form.com/  
**Relevance:** Form handling patterns

**Guidelines influenced:**
- CONTROLLED-VS-UNCONTROLLED
- FORM-VALIDATION

---

### 10. React Router
**URL:** https://reactrouter.com/  
**Relevance:** Routing patterns

**Guidelines influenced:**
- LAZY-LOADING
- CODE-SPLITTING

---

### 11. MSW (Mock Service Worker)
**URL:** https://mswjs.io/  
**Relevance:** API mocking for tests

**Guidelines influenced:**
- MOCK-BOUNDARIES
- TEST-ASYNC

---

### 12. Concurrent React Features
**Source:** React 18 Documentation  
**URL:** https://react.dev/blog/2022/03/29/react-v18

**Key features:**
- Suspense
- Transitions
- Automatic batching

**Guidelines influenced:**
- SUSPENSE
- TRANSITIONS
- LAZY-LOADING

---

### 13. ESLint Plugin React Hooks
**URL:** https://www.npmjs.com/package/eslint-plugin-react-hooks  
**Relevance:** Hook rules enforcement

**Guidelines influenced:**
- HOOK-RULES
- USE-EFFECT-DEPS

---

### 14. React DevTools
**URL:** https://react.dev/learn/react-developer-tools  
**Relevance:** Profiling and debugging

**Guidelines influenced:**
- MEMO-COMPONENT
- OVER-MEMO

---

### 15. Accessibility Testing Tools

#### jest-axe
**URL:** https://github.com/nickcolley/jest-axe  
**Relevance:** Automated accessibility testing

#### axe-core
**URL:** https://github.com/dequelabs/axe-core  
**Relevance:** Accessibility engine

**Guidelines influenced:**
- TEST-ACCESSIBILITY

---

## Books and Courses

### Books
- **Epic React** by Kent C. Dodds
- **Testing JavaScript** by Kent C. Dodds
- **Learning React** by Alex Banks and Eve Porcello

### Courses
- **React Documentation Tutorial** - react.dev/learn
- **Testing JavaScript** - testingjavascript.com
- **Epic React** - epicreact.dev

---

## Research Methodology

The guidelines in this skill were developed through:

1. **Documentation Review**
   - React official documentation
   - React RFC discussions
   - React team blog posts

2. **Community Best Practices**
   - Kent C. Dodds' articles and courses
   - Dan Abramov's blog posts
   - React community discussions

3. **Testing Validation**
   - Testing Library documentation
   - Real-world testing patterns
   - Accessibility testing tools

4. **Accessibility Standards**
   - WAI-ARIA specifications
   - WCAG guidelines
   - Screen reader testing

---

## Additional Resources

### Documentation
- React Docs - https://react.dev/
- Testing Library - https://testing-library.com/
- WAI-ARIA - https://www.w3.org/WAI/ARIA/

### Blogs
- Overreacted (Dan Abramov) - https://overreacted.io/
- Kent C. Dodds - https://kentcdodds.com/
- Josh W Comeau - https://www.joshwcomeau.com/

### Tools
- React DevTools - Chrome/Firefox extension
- ESLint Plugin React Hooks - npm package
- jest-axe - Accessibility testing

---

## Attribution Note

This skill synthesizes knowledge from official React documentation and respected community sources. All recommendations align with:
- React team's official guidance
- Testing Library philosophy
- WAI-ARIA accessibility standards
- Community-validated patterns

The examples are original implementations demonstrating principles from these sources, adapted for practical use with Claude Code.

## Version History

- **v1.0** (2025-01-19) - Initial release with 65+ React guidelines
  - Component Design (10 guidelines)
  - Hooks (12 guidelines)
  - Rendering & Performance (8 guidelines)
  - Patterns (8 guidelines)
  - Accessibility (8 guidelines)
  - Error Handling (5 guidelines)
  - Testing (6 guidelines)

---

**All sources are publicly available and represent industry-standard best practices for React development.**
