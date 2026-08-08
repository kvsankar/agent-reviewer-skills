# JavaScript Performance Reviewer Skill

A Claude Code skill that reviews JavaScript/TypeScript code for performance optimization opportunities. **Comprehensive performance analysis** - covers algorithm complexity, data structures, memory management, DOM operations, async patterns, bundling, and React-specific optimizations.

## What This Skill Does

This skill transforms Claude into a JavaScript/TypeScript performance expert who:
- **Identifies performance bottlenecks** - Slow algorithms, inefficient data structures, memory leaks, layout thrashing
- **Suggests optimized alternatives** - Faster algorithms, better data structures, efficient patterns
- **Provides concrete examples** - Before/after code with performance measurements
- **Explains performance impact** - Big-O analysis, speedup estimates, frame rate improvements
- **Recommends profiling tools** - Chrome DevTools, Lighthouse, React Profiler
- **Categorizes by impact** - Critical, High, Medium, Low

## Philosophy

> **"Premature optimization is the root of all evil."** - Donald Knuth

> **"Make it work, make it right, make it fast."** - Kent Beck

> **"Measure, don't guess."** - Performance Engineering Principle

This skill emphasizes **profile-driven optimization** - always measure before optimizing, focus on real bottlenecks, and verify improvements.

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r javascript-performance-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "javascript-performance-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r javascript-performance-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/javascript-performance-reviewer
git commit -m "Add JavaScript Performance Reviewer skill"
```

**✅ Self-Contained:** All 55+ guidelines are embedded directly in SKILL.md - no external file references needed!

## How to Use

Simply ask Claude to review your code for performance:

```
"Review this code for performance issues"
"Find performance bottlenecks in this function"
"How can I make this faster?"
"This React component is slow - optimize it"
"Review this loop for performance"
"Check for inefficient algorithms"
"Optimize this event handler"
"Find memory leaks in this code"
"Why is this animation janky?"
```

The skill will automatically activate based on keywords like:
- performance, optimize, slow, fast, bottleneck
- speed, efficiency, memory, CPU, fps, jank
- algorithm, complexity, O(n), Big-O
- profile, benchmark, React performance

## What You'll Get

A comprehensive performance review with:
- **Impact Classification** - Critical (10-1000x), High (2-10x), Medium (1.5-2x), Low (1.1-1.5x)
- **Slow Code** - Shows the performance issue
- **Fast Code** - Shows the optimized version
- **Performance Impact** - Speedup estimates, Big-O analysis, FPS improvements
- **Best Practices** - When to use, pitfalls to avoid
- **Mnemonic IDs** - Easy reference (e.g., ALGO-COMPLEX, DOM-BATCH, MEMO-COMPONENT)

### Example Review

````markdown
## Performance Review: UserList.jsx

### 🐌 Performance Issues

#### CRITICAL: NESTED-LOOP - O(n × m) Nested Loops

**Slow code:**
```javascript
function matchUsers(users, orders) {
  return users.map(user => ({
    ...user,
    orders: orders.filter(order => order.userId === user.id)
  }));
}
// 1000 users × 10000 orders = 10 million comparisons
```

**Fast code:**
```javascript
function matchUsers(users, orders) {
  const ordersByUser = new Map();
  for (const order of orders) {
    if (!ordersByUser.has(order.userId)) {
      ordersByUser.set(order.userId, []);
    }
    ordersByUser.get(order.userId).push(order);
  }
  
  return users.map(user => ({
    ...user,
    orders: ordersByUser.get(user.id) || []
  }));
}
// 1000 + 10000 = 11,000 operations (900x faster!)
```

**Performance impact:**
- O(n × m) → O(n + m)
- 900x faster for large datasets

**Related:** ALGO-COMPLEX, DATA-STRUCTURE
````

## The 55+ Performance Guidelines

### Algorithm Complexity (8 guidelines)
- **ALGO-COMPLEX** - Optimize algorithm complexity (O(n²) → O(n))
- **NESTED-LOOP** - Avoid nested loops when possible
- **LINEAR-SEARCH** - Use binary search or Map for lookups
- **EARLY-EXIT** - Return early to avoid unnecessary work
- **CACHE-RESULT** - Cache expensive computations (memoization)
- **REDUNDANT-CALC** - Eliminate redundant calculations
- **PRECOMPUTE** - Precompute values when possible
- **DEBOUNCE-THROTTLE** - Debounce/throttle frequent operations

### Data Structures (8 guidelines)
- **DATA-STRUCTURE** - Choose appropriate data structures (Set, Map, Array)
- **OBJECT-LITERAL** - Use object literals for small lookups
- **ARRAY-METHODS** - Use appropriate array methods (find vs filter)
- **ARRAY-CHAIN** - Optimize array method chains (reduce passes)
- **SPREAD-CLONE** - Avoid excessive spreading
- **IMMUTABLE-LIB** - Use immutable libraries (Immer)
- **WEAK-MAP** - Use WeakMap for object-keyed caches
- **TYPED-ARRAYS** - Use typed arrays for numeric data

### Memory Management (6 guidelines)
- **MEMORY-LEAK** - Avoid memory leaks (listeners, timers, closures)
- **CLOSURE-SCOPE** - Be mindful of closure scope
- **LAZY-INIT** - Lazy initialize expensive objects
- **GC-FRIENDLY** - Write garbage collector friendly code
- **DETACHED-DOM** - Avoid detached DOM nodes
- **MEMORY-MEASURE** - Measure memory usage

### DOM Operations (7 guidelines)
- **DOM-BATCH** - Batch DOM operations (DocumentFragment)
- **LAYOUT-THRASH** - Avoid layout thrashing (batch reads/writes)
- **VIRTUAL-SCROLL** - Use virtual scrolling for long lists
- **EVENT-PASSIVE** - Use passive event listeners
- **EVENT-DELEGATE** - Use event delegation
- **CSS-CHANGES** - Use CSS for animations, not JavaScript
- **RAF-ANIMATION** - Use requestAnimationFrame for JS animations

### Async Operations (7 guidelines)
- **PROMISE-PARALLEL** - Run independent promises in parallel
- **ASYNC-AWAIT** - Use async/await over promise chains
- **LAZY-LOAD** - Lazy load heavy resources
- **WEB-WORKERS** - Use Web Workers for heavy computation
- **PRELOAD-PREFETCH** - Use resource hints (preload, prefetch)
- **ABORT-REQUESTS** - Cancel unnecessary requests
- **STREAM-RESPONSE** - Stream large responses

### Bundling & Loading (6 guidelines)
- **CODE-SPLIT** - Split code by route
- **TREE-SHAKE** - Enable tree shaking
- **DYNAMIC-IMPORT** - Use dynamic imports strategically
- **COMPRESSION** - Enable compression (gzip, Brotli)
- **BUNDLE-ANALYSIS** - Analyze bundle size
- **CDN-ASSETS** - Serve assets from CDN

### React-Specific (6 guidelines)
- **MEMO-COMPONENT** - Memoize components (React.memo, useMemo)
- **KEY-OPTIMIZATION** - Use stable keys in lists
- **STATE-COLOCATION** - Colocate state
- **CONTEXT-SPLIT** - Split contexts
- **VIRTUALIZE-LISTS** - Virtualize long lists (react-window)
- **LAZY-COMPONENT** - Lazy load components

### Profiling & Measurement (5 guidelines)
- **PROFILE-FIRST** - Profile before optimizing
- **MEASURE-IMPACT** - Measure optimization impact
- **REAL-USER-MONITORING** - Monitor production performance
- **PERFORMANCE-BUDGET** - Set performance budgets
- **LIGHTHOUSE-CI** - Automate performance testing

## Key Differentiators

### Profile-Driven Optimization

Emphasizes the critical importance of profiling:
- **Measure first** - Use Chrome DevTools, Lighthouse, React Profiler
- **Identify bottlenecks** - Find the 20% causing 80% of slowness
- **Verify results** - Measure before and after optimization
- **Focus effort** - Optimize what actually matters

### Real Performance Impact

Every guideline includes:
- Estimated speedup (e.g., "100x faster", "900x faster")
- Big-O complexity analysis (e.g., "O(n²) → O(n)")
- Memory impact (e.g., "Prevents memory leaks")
- When the optimization matters (data size, frequency)

### Practical Examples

Examples identify the runtime—browser, Node.js, or React—and pair the change
with an appropriate measurement such as a DevTools trace, benchmark, render
count, or bundle-size comparison. They explain both the gain and the added
complexity.

### Platform-Specific

Covers JavaScript/TypeScript ecosystems:
- **Browser APIs** - DOM, fetch, Web Workers, Storage
- **React** - Hooks, memoization, context, virtualization
- **Modern JS** - ES6+, async/await, modules
- **Build tools** - Webpack, Vite, bundling, code splitting
- **Frameworks** - React, Vue, Angular patterns

## Common Patterns This Skill Teaches

### ✅ Do This

```javascript
// Use Set for membership testing
const items = new Set(data);
if (items.has(value)) { ... }  // O(1)

// Batch DOM operations
const fragment = document.createDocumentFragment();
for (const item of items) {
  fragment.appendChild(createDiv(item));
}
container.appendChild(fragment);  // Single reflow

// Parallel async operations
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);

// Memoize React components
const ExpensiveList = React.memo(({ items }) => {
  return items.map(item => <Item key={item.id} {...item} />);
});

// Lazy load routes
const Dashboard = lazy(() => import('./Dashboard'));

// Use appropriate data structure
const ordersByUser = new Map();  // O(1) lookups

// Debounce search
const debouncedSearch = debounce(search, 300);
```

### ❌ Not This

```javascript
// Linear search in array
const items = [/* 10000 items */];
if (items.includes(value)) { ... }  // O(n)

// Individual DOM appends
for (const item of items) {
  container.appendChild(createDiv(item));  // 1000 reflows!
}

// Sequential async operations
const users = await fetchUsers();  // Wait
const posts = await fetchPosts();  // Then wait again

// Missing memoization
function ExpensiveList({ items }) {
  // Re-renders on every parent render
  return items.map(item => <Item {...item} />);
}

// Eager loading
import Dashboard from './Dashboard';  // 500KB loaded upfront

// Wrong data structure
const orders = [];  // O(n) for every lookup

// No debouncing
input.addEventListener('input', (e) => {
  search(e.target.value);  // Fires 100x per second!
});
```

## Example Use Cases

### Algorithm Optimization
- "This nested loop is slow - how can I optimize it?"
- "Find O(n²) algorithms and make them O(n)"
- "Optimize this search function"

### Memory Optimization
- "This page leaks memory after navigation"
- "Find memory leaks in this code"
- "Why does memory keep growing?"

### DOM Performance
- "This list is slow to render"
- "Animation is janky - why?"
- "Scrolling lags with 10,000 items"

### React Performance
- "This React component re-renders too much"
- "Why is my React app slow?"
- "Optimize this useEffect"

### Bundle Optimization
- "Our bundle is 5MB - help reduce it"
- "How can we split our bundle?"
- "Initial load is too slow"

### Pre-Production Review
- "Performance review before launch"
- "Find all performance issues"
- "Audit for Core Web Vitals"

## Benefits

- ✓ **Find bottlenecks** - Identify slow code before production
- ✓ **Concrete speedups** - See exact improvements (e.g., "100x faster")
- ✓ **Big-O analysis** - Understand algorithmic complexity
- ✓ **Memory optimization** - Reduce usage and prevent leaks
- ✓ **DOM mastery** - Eliminate layout thrashing and jank
- ✓ **React expertise** - Optimize components and hooks
- ✓ **Bundle optimization** - Reduce and split bundles
- ✓ **Profiling guidance** - Learn Chrome DevTools, Lighthouse
- ✓ **Impact classification** - Prioritize fixes (Critical/High/Medium/Low)
- ✓ **Real examples** - Copy-paste ready optimizations

## What Gets Checked

### Algorithms
- Nested loops
- Linear searches
- Inefficient sorting
- Missing caching
- Redundant calculations

### Data Structures
- Array when Set/Map needed
- Wrong method choices
- Excessive spreading
- Array chaining

### Memory
- Event listener leaks
- Timer leaks
- Closure leaks
- Detached DOM nodes
- Large objects in closures

### DOM
- Layout thrashing
- Individual DOM mutations
- Missing virtualization
- Non-passive listeners
- Missing event delegation

### Async
- Sequential when could be parallel
- Missing lazy loading
- No request cancellation
- Heavy computation on main thread

### Bundling
- Missing code splitting
- No tree shaking
- Large bundles
- Missing compression

### React
- Missing memoization
- Unstable list keys
- Wide re-render scope
- Single monolithic context

### Profiling
- No profiling data
- Guessing bottlenecks
- Missing benchmarks

## Supported Technologies

- **JavaScript/TypeScript:** ES6+, modern syntax
- **Frameworks:** React, Vue, Angular, Svelte
- **Build Tools:** Webpack, Vite, Rollup, esbuild
- **Testing:** Jest, Vitest, Playwright
- **Bundling:** Code splitting, tree shaking, lazy loading
- **Profiling:** Chrome DevTools, Lighthouse, React Profiler
- **Browser APIs:** DOM, fetch, Web Workers, Storage APIs

## Sources and Attribution

All guidelines are based on:
- **V8 JavaScript Engine** - Performance tips and internals
- **Chrome DevTools** - Performance profiling documentation
- **Web.dev** - Performance best practices from Google
- **React Documentation** - Official React performance docs
- **High Performance Browser Networking** - Book by Ilya Grigorik
- **Algorithm Analysis** - Big-O complexity theory
- **MDN Web Docs** - Browser API performance characteristics
- **Lighthouse** - Performance auditing tool from Google

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## Performance Philosophy

### Profile First

Never optimize without profiling:
1. Use Chrome DevTools Performance tab
2. Use Lighthouse for overall audit
3. Use React Profiler for React apps
4. Measure before and after optimization

### Focus on Impact

Prioritize JavaScript hot paths confirmed by a browser or Node.js profile.
Large algorithmic, network, rendering, and bundle improvements deserve action;
small micro-benchmark gains rarely justify harder-to-read application code.

### Optimize What Matters

80/20 rule:
- 20% of code causes 80% of slowness
- Focus on that 20%
- Don't optimize cold paths
- Profile to identify hot paths

### Keep It Readable

Avoid premature optimization:
- Readability > Performance for cold paths
- Performance > Readability for hot paths
- Profile to know which is which
- Document non-obvious optimizations

## Tips for Getting the Most Out of This Skill

1. **Provide context**: "This renders 10,000 items" or "This runs on every scroll"
2. **Share profiling data**: "DevTools shows this function takes 80% of time"
3. **Specify constraints**: "Need 60fps" or "Must load in <3s"
4. **Include data sizes**: "Processing 1M rows" or "10,000 DOM nodes"
5. **Ask about trade-offs**: "Is this optimization worth the complexity?"

## License

This skill is licensed under MIT. It is based on public performance best practices, browser specifications, and established algorithms.

---

**Fast code is good code. But first, make it work. Then make it right. Then make it fast.**
