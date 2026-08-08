# React Reviewer Skill

A Claude Code skill that reviews React code for best practices, patterns, performance, accessibility, and common pitfalls. **Comprehensive React analysis** - covers components, hooks, state management, rendering optimization, patterns, accessibility, error handling, and testing.

## What This Skill Does

This skill transforms Claude into a React expert who:
- **Identifies React anti-patterns** - Improper hook usage, state management issues, stale closures
- **Suggests best practices** - Modern patterns, correct hook dependencies, proper composition
- **Optimizes performance** - Memoization, virtualization, lazy loading
- **Ensures accessibility** - ARIA, keyboard navigation, screen reader support
- **Improves testing** - Testing Library queries, behavior testing, async handling
- **Categorizes by severity** - Critical, Warning, Info

## Philosophy

> **"Don't optimize prematurely"** - React Team

> **"Lift state up only when you need to"** - React Docs

> **"Test behavior, not implementation"** - Testing Library

This skill emphasizes **React's declarative model** - keep components simple, derive values when possible, and let React handle the rendering.

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## How to Use

Simply ask Claude to review your React code:

```
"Review this React component"
"Check my hooks for issues"
"Is this component accessible?"
"How can I optimize this React app?"
"Review this useEffect for problems"
"Check for React anti-patterns"
"Make this component more maintainable"
```

## What You'll Get

A comprehensive React review with:
- **Severity Classification** - Critical, Warning, Info
- **Problematic Code** - Shows the issue
- **Improved Code** - Shows the fix
- **Explanation** - Why it matters
- **Mnemonic IDs** - Easy reference (e.g., USE-EFFECT-DEPS, MEMO-COMPONENT)

### Example Review

````markdown
## React Review: UserProfile.jsx

### 🔴 Critical Issues

#### USE-EFFECT-DEPS: Missing Hook Dependencies

**Problematic code:**
```jsx
useEffect(() => {
  fetchUser(userId).then(setUser);
}, []);  // Missing 'userId' dependency!
```

**Improved code:**
```jsx
useEffect(() => {
  fetchUser(userId).then(setUser);
}, [userId]);  // Runs when userId changes
```

**Why:** Without userId in dependencies, the effect only runs once and uses stale userId value.
````

## The 65+ React Guidelines

### Component Design (10 guidelines)
- **SINGLE-RESPONSIBILITY** - Components should do one thing
- **COMPOSITION** - Prefer composition over prop drilling
- **PROP-TYPES** - Define clear component interfaces
- **CONTROLLED-VS-UNCONTROLLED** - Choose appropriate form strategy
- **LIFTING-STATE** - Lift state to common ancestor
- **STATE-COLOCATION** - Keep state close to where it's used
- **DERIVED-STATE** - Avoid redundant state
- **AVOID-SYNC** - Don't sync state with useEffect
- **CHILDREN-PATTERN** - Use children for flexible composition
- **COMPONENT-NAMING** - Use clear naming conventions

### Hooks (12 guidelines)
- **USE-EFFECT-DEPS** - Correct useEffect dependencies
- **USE-EFFECT-CLEANUP** - Always clean up side effects
- **CUSTOM-HOOKS** - Extract reusable logic into custom hooks
- **HOOK-RULES** - Follow the Rules of Hooks
- **USE-CALLBACK** - Stabilize function references
- **USE-MEMO** - Memoize expensive calculations
- **STALE-CLOSURE** - Avoid stale closures
- **USE-REF** - Use refs appropriately
- **USE-REDUCER** - Use useReducer for complex state
- **USE-CONTEXT** - Use context effectively
- **USE-LAYOUT-EFFECT** - Know when to use useLayoutEffect
- **OVER-MEMO** - Don't over-memoize

### Rendering & Performance (8 guidelines)
- **MEMO-COMPONENT** - Memoize components appropriately
- **KEY-PROP** - Use keys correctly
- **LIST-RENDER** - Optimize list rendering
- **CONDITIONAL-RENDER** - Handle conditional rendering properly
- **AVOID-INLINE-OBJECTS** - Avoid creating objects in JSX
- **LAZY-LOADING** - Lazy load components
- **SUSPENSE** - Use Suspense for loading states
- **TRANSITIONS** - Use transitions for non-urgent updates

### Patterns (8 guidelines)
- **COMPOUND-COMPONENTS** - Use compound components pattern
- **RENDER-PROPS** - Use render props for flexible rendering
- **HIGHER-ORDER-COMPONENTS** - Use HOCs sparingly
- **CONTROLLED-COMPONENTS** - Build controlled components
- **CONTAINER-PRESENTATIONAL** - Separate logic from presentation
- **FORWARD-REF** - Forward refs to DOM elements
- **PORTALS** - Use portals for modals and tooltips
- **CONTEXT-MODULE** - Organize context with module pattern

### Accessibility (8 guidelines)
- **SEMANTIC-HTML** - Use semantic HTML elements
- **ARIA-LABELS** - Use ARIA attributes correctly
- **KEYBOARD-NAV** - Ensure keyboard navigation
- **FOCUS-MANAGEMENT** - Manage focus properly
- **HEADING-ORDER** - Use correct heading hierarchy
- **SCREEN-READER** - Consider screen reader experience
- **COLOR-CONTRAST** - Ensure sufficient color contrast
- **FOCUS-VISIBLE** - Style focus states

### Error Handling (5 guidelines)
- **ERROR-BOUNDARY** - Use error boundaries
- **ASYNC-ERROR** - Handle async errors properly
- **LOADING-STATE** - Handle loading states
- **FORM-VALIDATION** - Provide clear validation feedback
- **NULL-CHECK** - Handle null/undefined safely

### Testing (6 guidelines)
- **TEST-BEHAVIOR** - Test behavior, not implementation
- **TEST-QUERIES** - Use correct Testing Library queries
- **MOCK-BOUNDARIES** - Mock at system boundaries
- **TEST-ASYNC** - Handle async operations in tests
- **TEST-HOOK** - Test custom hooks
- **TEST-ACCESSIBILITY** - Test accessibility

## Common Patterns This Skill Teaches

### ✅ Do This

```jsx
// Derive values during render
function ProductList({ products, filter }) {
  const filtered = products.filter(p => p.category === filter);
  return <List items={filtered} />;
}

// Correct hook dependencies
useEffect(() => {
  fetchData(id).then(setData);
}, [id]);

// Functional state updates
setCount(prev => prev + 1);

// Clean up side effects
useEffect(() => {
  const sub = subscribe(id);
  return () => sub.unsubscribe();
}, [id]);

// Use semantic HTML
<nav aria-label="Main">
  <ul>{/* links */}</ul>
</nav>

// Test behavior
expect(screen.getByRole('button', { name: /submit/i })).toBeEnabled();
```

### ❌ Not This

```jsx
// Syncing state (anti-pattern)
const [filtered, setFiltered] = useState([]);
useEffect(() => {
  setFiltered(products.filter(p => p.category === filter));
}, [products, filter]);

// Missing dependencies
useEffect(() => {
  fetchData(id).then(setData);
}, []);  // id missing!

// Stale closure
setCount(count + 1);  // May be stale in async contexts

// No cleanup
useEffect(() => {
  const sub = subscribe(id);
  // Memory leak!
}, [id]);

// Div soup
<div className="nav">
  <div className="link">Home</div>
</div>

// Testing implementation
expect(component.state.isOpen).toBe(true);
```

## Benefits

- ✓ **Find anti-patterns** - Identify common React mistakes
- ✓ **Correct hook usage** - Proper dependencies, cleanup, rules
- ✓ **Better state management** - Avoid derived state, sync issues
- ✓ **Performance optimization** - Memoization, virtualization
- ✓ **Accessibility** - ARIA, keyboard nav, screen readers
- ✓ **Testing guidance** - Behavior testing, async handling
- ✓ **Modern patterns** - Compound components, custom hooks
- ✓ **Severity classification** - Prioritize fixes

## What Gets Checked

### Hooks
- Missing/incorrect dependencies
- Stale closures
- Missing cleanup
- Rules of hooks violations
- Over-memoization

### Components
- Single responsibility
- Prop drilling
- State colocation
- Derived vs synced state
- Composition patterns

### Performance
- Unnecessary re-renders
- Missing memoization (where needed)
- List rendering issues
- Lazy loading opportunities

### Accessibility
- Semantic HTML
- ARIA usage
- Keyboard navigation
- Focus management
- Screen reader support

### Testing
- Implementation vs behavior testing
- Query selection
- Async handling
- Accessibility testing

## Supported Technologies

- **React:** 16.8+ (Hooks), 17, 18
- **TypeScript:** Full support
- **Testing:** React Testing Library, Jest
- **State:** Context, Redux, Zustand
- **Routing:** React Router
- **Forms:** React Hook Form, Formik

## Sources and Attribution

All guidelines are based on:
- **React Official Documentation** - react.dev
- **React Team Blog Posts** - Thinking in React, Rules of Hooks
- **Kent C. Dodds** - Testing Library, Epic React
- **Dan Abramov** - Overreacted blog, useEffect guide
- **A11y Resources** - WAI-ARIA, WebAIM

See [SOURCES.md](./SOURCES.md) for detailed attribution.

## Tips for Best Results

1. **Provide context**: "This is a form component" or "This handles authentication"
2. **Share related code**: Include custom hooks or context providers
3. **Mention issues**: "Users report it's slow" or "Accessibility audit failed"
4. **Ask specific questions**: "Is this hook correct?" or "How can I test this?"

## License

This skill is licensed under MIT. It is based on official React documentation and community best practices.

---

**React is about building UIs that are predictable, composable, and maintainable.**
