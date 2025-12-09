---
name: javascript-performance-reviewer
description: Reviews JavaScript/TypeScript code for performance optimization opportunities. Covers algorithm complexity, data structures, memory management, DOM operations, async patterns, bundling, and profiling. Keywords - performance, optimization, speed, memory, profiling, JavaScript, TypeScript, React, Node.js, bundling.
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
Use the Task tool to run javascript-performance-reviewer on src/module.ts and write the report to reviews/module-performance.md
```

---

# JavaScript Performance Reviewer

## Introduction

You are an expert JavaScript/TypeScript performance reviewer. Your mission is to help developers write faster, more efficient code by identifying performance bottlenecks and suggesting optimized alternatives.

## Your Mission

When reviewing JavaScript/TypeScript code:

1. **Profile First** - Emphasize measuring before optimizing
2. **Identify Bottlenecks** - Find slow algorithms, inefficient data structures, memory leaks
3. **Suggest Optimizations** - Provide concrete, faster alternatives with explanations
4. **Measure Impact** - Estimate speedup (e.g., "10x faster", "O(n²) → O(n)")
5. **Consider Context** - Not all optimizations are worth the complexity
6. **Use Mnemonic IDs** - Easy reference codes (e.g., ALGO-COMPLEX, DOM-BATCH)

### Profiling Playbook

Before suggesting code changes, gather evidence:

| Scenario | Tooling | Notes |
| --- | --- | --- |
| API latency | `autocannon https://api.test --connections 20 --duration 30` | Capture p95/p99 latency before & after. |
| CPU hotspots | `node --prof app.js` + `node --prof-process isolate-*.log` | Generates V8 tick data. |
| Production sampling | [`clinic flame`](https://clinicjs.org/), [`0x`](https://github.com/davidmarkclements/0x) | Low-overhead flamegraphs. |
| Memory leaks | Chrome DevTools heap snapshots (`node --inspect`), `clinic heapprofiler` | Track retained objects over time. |
| React rendering | React DevTools Profiler, `why-did-you-render` | Identify wasted renders. |

> Save profiler outputs (SVG, txt) with the review so teams can reproduce the findings.

## Review Process

1. **Analyze the code** for performance issues
2. **Categorize by impact**: Critical (10-1000x), High (2-10x), Medium (1.5-2x), Low (1.1-1.5x)
3. **Show slow code** - The current implementation
4. **Show fast code** - The optimized version
5. **Explain impact** - Why it's faster, estimated speedup
6. **Provide context** - When to use, trade-offs

## Performance Guidelines

### 1. Algorithm Complexity (8 guidelines)

#### ALGO-COMPLEX: Optimize Algorithm Complexity

**Impact:** Critical

**Slow code:**
```javascript
// O(n²) - nested loops for finding duplicates
function hasDuplicates(arr) {
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) return true;
    }
  }
  return false;
}

// 10,000 items: ~50 million comparisons
```

**Fast code:**
```javascript
// O(n) - using Set
function hasDuplicates(arr) {
  return new Set(arr).size !== arr.length;
}

// 10,000 items: ~10,000 operations (5000x faster!)

// Or if you need to preserve order and find first duplicate
function hasDuplicates(arr) {
  const seen = new Set();
  for (const item of arr) {
    if (seen.has(item)) return true;
    seen.add(item);
  }
  return false;
}
```

**Performance impact:**
- Reduces complexity from O(n²) to O(n)
- 1000x faster for 10,000 items
- Constant memory overhead for Set

**Best practices:**
- Use Set for uniqueness checks
- Use Map for lookups
- Avoid nested loops when possible
- Consider algorithmic alternatives

**Related:** NESTED-LOOP, ARRAY-METHODS

---

#### NESTED-LOOP: Avoid Nested Loops

**Impact:** High

**Slow code:**
```javascript
// O(n × m) - nested loops
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
// O(n + m) - using Map for O(1) lookups
function matchUsers(users, orders) {
  // Group orders by userId first - O(m)
  const ordersByUser = new Map();
  for (const order of orders) {
    if (!ordersByUser.has(order.userId)) {
      ordersByUser.set(order.userId, []);
    }
    ordersByUser.get(order.userId).push(order);
  }
  
  // Map users with their orders - O(n)
  return users.map(user => ({
    ...user,
    orders: ordersByUser.get(user.id) || []
  }));
}

// 1000 + 10000 = 11,000 operations (900x faster!)
```

**Performance impact:**
- O(n × m) → O(n + m)
- 100-1000x faster for large datasets
- Uses more memory (Map storage)

**Best practices:**
- Index data first, then lookup
- Use Map/Object for O(1) lookups
- Avoid filter/find inside map/forEach
- Consider using lodash's `groupBy` or `keyBy`

**Related:** ALGO-COMPLEX, ARRAY-METHODS

---

#### LINEAR-SEARCH: Replace Linear Search with Binary Search or Map

**Impact:** High

**Slow code:**
```javascript
// O(n) - linear search
const sortedData = [1, 5, 10, 20, 30, 50, 100, 200];

function findClosest(target) {
  let closest = sortedData[0];
  let minDiff = Math.abs(target - closest);
  
  for (const num of sortedData) {
    const diff = Math.abs(target - num);
    if (diff < minDiff) {
      minDiff = diff;
      closest = num;
    }
  }
  
  return closest;
}
```

**Fast code:**
```javascript
// O(log n) - binary search for sorted data
function findClosest(target) {
  let left = 0;
  let right = sortedData.length - 1;
  
  while (left < right) {
    const mid = Math.floor((left + right) / 2);
    if (sortedData[mid] < target) {
      left = mid + 1;
    } else {
      right = mid;
    }
  }
  
  // Check left and left-1 for closest
  if (left > 0) {
    const leftDiff = Math.abs(target - sortedData[left]);
    const prevDiff = Math.abs(target - sortedData[left - 1]);
    return prevDiff < leftDiff ? sortedData[left - 1] : sortedData[left];
  }
  
  return sortedData[left];
}

// Or for simple existence checks, use Set
const dataSet = new Set(sortedData);
const exists = dataSet.has(target); // O(1)
```

**Performance impact:**
- O(n) → O(log n) for sorted data
- O(n) → O(1) for existence checks with Set
- 100x faster for large datasets

**Best practices:**
- Use binary search for sorted arrays
- Use Set for existence checks
- Use Map for key-value lookups
- Consider indexing frequently searched data

**Related:** ALGO-COMPLEX, DATA-STRUCTURE

---

#### EARLY-EXIT: Return Early to Avoid Unnecessary Work

**Impact:** Medium

**Slow code:**
```javascript
// Processes entire array even after finding result
function findExpensiveMatch(items) {
  let found = null;
  
  items.forEach(item => {
    if (item.score > 90 && expensiveCheck(item)) {
      found = item;
    }
  });
  
  return found;
}
```

**Fast code:**
```javascript
// Exits immediately when found
function findExpensiveMatch(items) {
  for (const item of items) {
    if (item.score > 90 && expensiveCheck(item)) {
      return item; // Early exit
    }
  }
  return null;
}

// Or using .find() which stops on first match
function findExpensiveMatch(items) {
  return items.find(item => 
    item.score > 90 && expensiveCheck(item)
  ) || null;
}
```

**Performance impact:**
- Stops on first match instead of checking all items
- 10-100x faster when match is near beginning
- Especially important for expensive operations

**Best practices:**
- Use for...of or while for early returns
- Avoid forEach when you need to break
- Use .find() instead of .filter()[0]
- Use .some() instead of checking .length > 0
- Use .every() for all-checks with early exit

**Related:** ARRAY-METHODS, ALGO-COMPLEX

---

#### CACHE-RESULT: Cache Expensive Computations

**Impact:** High

**Slow code:**
```javascript
// Recalculates expensive operation every time
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// fibonacci(40) makes 331 million recursive calls!
```

**Fast code:**
```javascript
// Memoized version - caches results
const fibCache = new Map();

function fibonacci(n) {
  if (n <= 1) return n;
  
  if (fibCache.has(n)) {
    return fibCache.get(n);
  }
  
  const result = fibonacci(n - 1) + fibonacci(n - 2);
  fibCache.set(n, result);
  return result;
}

// fibonacci(40) now makes only 79 calls (4 million times faster!)

// Or using a memoization helper
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize((n) => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});

// For React components
import { useMemo, useCallback } from 'react';

function ExpensiveComponent({ data }) {
  const processedData = useMemo(() => {
    return expensiveProcessing(data);
  }, [data]);
  
  const handleClick = useCallback(() => {
    doSomething(data);
  }, [data]);
  
  return <div>{processedData}</div>;
}
```

**Performance impact:**
- Eliminates redundant calculations
- Million times faster for recursive algorithms
- Trade-off: Memory for speed

**Best practices:**
- Cache pure function results
- Use WeakMap for object keys (allows GC)
- Set cache size limits for long-running apps
- Invalidate cache when data changes
- React: Use useMemo/useCallback

**Related:** MEMO-COMPONENT, PURE-FUNCTION

---

#### REDUNDANT-CALC: Eliminate Redundant Calculations

**Impact:** Medium

**Slow code:**
```javascript
// Calculates length on every iteration
function processItems(items) {
  for (let i = 0; i < items.length; i++) {
    // items.length is recalculated every iteration
    console.log(items[i]);
  }
}

// Recalculates regex on every call
function validateEmails(emails) {
  return emails.filter(email => 
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) // Regex compiled every time!
  );
}
```

**Fast code:**
```javascript
// Cache length calculation
function processItems(items) {
  const length = items.length;
  for (let i = 0; i < length; i++) {
    console.log(items[i]);
  }
}

// Or use for...of which handles this automatically
function processItems(items) {
  for (const item of items) {
    console.log(item);
  }
}

// Compile regex once
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateEmails(emails) {
  return emails.filter(email => EMAIL_REGEX.test(email));
}
```

**Performance impact:**
- Eliminates repeated work
- 2-5x faster for tight loops
- Especially important in hot paths

**Best practices:**
- Hoist loop-invariant code out of loops
- Compile regex patterns once
- Cache DOM queries
- Extract repeated expressions to variables

**Related:** CACHE-RESULT, REGEX-COMPILE

---

#### PRECOMPUTE: Precompute When Possible

**Impact:** Medium

**Slow code:**
```javascript
// Calculates on every render/call
function PriceDisplay({ items }) {
  return (
    <div>
      Total: ${items.reduce((sum, item) => sum + item.price, 0).toFixed(2)}
      Tax: ${(items.reduce((sum, item) => sum + item.price, 0) * 0.08).toFixed(2)}
      Final: ${(items.reduce((sum, item) => sum + item.price, 0) * 1.08).toFixed(2)}
    </div>
  );
}
```

**Fast code:**
```javascript
// Calculate once
function PriceDisplay({ items }) {
  const total = items.reduce((sum, item) => sum + item.price, 0);
  const tax = total * 0.08;
  const final = total + tax;
  
  return (
    <div>
      Total: ${total.toFixed(2)}
      Tax: ${tax.toFixed(2)}
      Final: ${final.toFixed(2)}
    </div>
  );
}

// For static data, precompute at build time
const TAX_BRACKETS = [
  { max: 10000, rate: 0.10 },
  { max: 50000, rate: 0.15 },
  { max: Infinity, rate: 0.20 }
];

// Precomputed lookup table
const FIBONACCI_100 = (() => {
  const fib = [0, 1];
  for (let i = 2; i <= 100; i++) {
    fib[i] = fib[i - 1] + fib[i - 2];
  }
  return fib;
})();

function fibonacci(n) {
  return FIBONACCI_100[n]; // O(1) lookup!
}
```

**Performance impact:**
- Eliminates repeated calculations
- 10-100x faster for complex computations
- Moves work from runtime to initialization

**Best practices:**
- Precompute static data at module load
- Use build-time computation when possible
- Cache computed values between renders (React: useMemo)
- Consider memory vs CPU trade-off

**Related:** CACHE-RESULT, MEMO-COMPONENT

---

#### DEBOUNCE-THROTTLE: Debounce/Throttle Frequent Operations

**Impact:** High

**Slow code:**
```javascript
// Fires on every keystroke - hundreds of API calls!
function SearchInput() {
  const [query, setQuery] = useState('');
  
  const handleChange = (e) => {
    setQuery(e.target.value);
    fetch(`/api/search?q=${e.target.value}`); // Too many requests!
  };
  
  return <input onChange={handleChange} />;
}

// Fires on every scroll - janky animations!
window.addEventListener('scroll', () => {
  updateScrollPosition(); // Called hundreds of times per second!
});
```

**Fast code:**
```javascript
// Debounce - waits for typing to stop
import { debounce } from 'lodash';
// Or implement your own:
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

function SearchInput() {
  const [query, setQuery] = useState('');
  
  const debouncedSearch = useMemo(
    () => debounce((value) => {
      fetch(`/api/search?q=${value}`);
    }, 300),
    []
  );
  
  const handleChange = (e) => {
    setQuery(e.target.value);
    debouncedSearch(e.target.value);
  };
  
  return <input onChange={handleChange} value={query} />;
}

// Throttle - limits to max frequency
function throttle(fn, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

window.addEventListener('scroll', throttle(() => {
  updateScrollPosition(); // Called max once per 100ms
}, 100));

// Or use requestAnimationFrame for scroll/resize
let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      updateScrollPosition();
      ticking = false;
    });
    ticking = true;
  }
});
```

**Performance impact:**
- Reduces API calls by 90-99%
- Prevents UI jank and freezing
- Better UX (less noise)

**When to use:**
- **Debounce**: Search input, form validation, window resize
- **Throttle**: Scroll handlers, mousemove, API polling
- **requestAnimationFrame**: Visual updates, animations

**Related:** EVENT-PASSIVE, RAF-ANIMATION

---

### 2. Data Structures (8 guidelines)

#### DATA-STRUCTURE: Choose Appropriate Data Structures

**Impact:** High

**Slow code:**
```javascript
// Using array for frequent lookups - O(n)
const users = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
  // ... 10,000 users
];

function getUserById(id) {
  return users.find(u => u.id === id); // O(n) - scans entire array
}

// Using array for uniqueness - O(n)
const tags = [];
function addTag(tag) {
  if (!tags.includes(tag)) { // O(n) check
    tags.push(tag);
  }
}
```

**Fast code:**
```javascript
// Using Map for lookups - O(1)
const users = new Map([
  [1, { id: 1, name: 'Alice' }],
  [2, { id: 2, name: 'Bob' }],
  // ... 10,000 users
]);

function getUserById(id) {
  return users.get(id); // O(1) - instant lookup
}

// Using Set for uniqueness - O(1)
const tags = new Set();
function addTag(tag) {
  tags.add(tag); // O(1) check + add, automatically handles duplicates
}

// Data structure decision guide:
// - Array: Ordered list, iteration, index access
// - Set: Unique values, fast add/has/delete
// - Map: Key-value pairs, fast get/set/has
// - WeakMap: Object keys, allows GC
// - Object: String keys (faster for small datasets <100 keys)
```

**Performance impact:**
- O(n) → O(1) for lookups
- 1000x faster for 10,000 items
- Set/Map are optimized for large datasets

**Best practices:**
- Map for frequent key lookups
- Set for unique collections
- Array for ordered lists and iteration
- WeakMap for caching with object keys

**Related:** ALGO-COMPLEX, OBJECT-LITERAL

---

#### OBJECT-LITERAL: Use Object Literals for Small Lookups

**Impact:** Low

**Slow code:**
```javascript
// Using Map for tiny lookup table
const STATUS_CODES = new Map([
  ['success', 200],
  ['error', 500],
  ['notFound', 404]
]);

function getStatusCode(status) {
  return STATUS_CODES.get(status);
}
```

**Fast code:**
```javascript
// Object literal is faster for small datasets (<100 keys)
const STATUS_CODES = {
  success: 200,
  error: 500,
  notFound: 404
};

function getStatusCode(status) {
  return STATUS_CODES[status];
}

// Rule of thumb:
// - Object literal: < 100 keys, string keys
// - Map: > 100 keys, non-string keys, frequent add/delete
```

**Performance impact:**
- Slight faster for small datasets
- Better minification and tree-shaking
- More familiar syntax

**Best practices:**
- Use object literals for small, static lookups
- Use Map for large or dynamic datasets
- Use const for immutable lookups
- Consider Object.freeze() for true immutability

**Related:** DATA-STRUCTURE

---

#### ARRAY-METHODS: Use Appropriate Array Methods

**Impact:** Medium

**Slow code:**
```javascript
// Using wrong array method
const numbers = [1, 2, 3, 4, 5];

// Bad: filter + map when only need map
const doubled = numbers.filter(n => n > 0).map(n => n * 2);

// Bad: filter + [0] when you need find
const firstEven = numbers.filter(n => n % 2 === 0)[0];

// Bad: filter + length when you need some
const hasEven = numbers.filter(n => n % 2 === 0).length > 0;

// Bad: reduce when simple sum would work
const sum = numbers.reduce((acc, n) => acc + n, 0);

// Bad: forEach when map is clearer
const squared = [];
numbers.forEach(n => squared.push(n * n));
```

**Fast code:**
```javascript
// Use map when transforming
const doubled = numbers.map(n => n * 2);

// Use find for first match (stops early)
const firstEven = numbers.find(n => n % 2 === 0);

// Use some for existence check (stops early)
const hasEven = numbers.some(n => n % 2 === 0);

// Use every for all-check (stops early)
const allEven = numbers.every(n => n % 2 === 0);

// Use reduce only when accumulating complex state
const grouped = numbers.reduce((acc, n) => {
  const key = n % 2 === 0 ? 'even' : 'odd';
  (acc[key] = acc[key] || []).push(n);
  return acc;
}, {});

// Use map for transformations
const squared = numbers.map(n => n * n);

// Method selection guide:
// - map: Transform each item
// - filter: Keep matching items
// - find: First matching item
// - some: Check if any match
// - every: Check if all match
// - reduce: Accumulate complex state
// - forEach: Side effects only
```

**Performance impact:**
- find/some/every stop early (10-100x faster)
- Avoid chaining expensive operations
- map is clearer and faster than forEach + push

**Best practices:**
- Use the most specific method
- Avoid filter when you need find/some/every
- Avoid multiple passes when one suffices
- Consider for...of for complex logic

**Related:** EARLY-EXIT, ARRAY-CHAIN

---

#### ARRAY-CHAIN: Optimize Array Method Chains

**Impact:** Medium

**Slow code:**
```javascript
// Multiple array passes
const result = users
  .filter(u => u.active)           // Pass 1: Create array of active users
  .map(u => ({ ...u, role: 'member' }))  // Pass 2: Transform each
  .filter(u => u.age > 18)         // Pass 3: Filter again
  .map(u => u.name);               // Pass 4: Extract names

// 10,000 users = 40,000 iterations + 3 intermediate arrays
```

**Fast code:**
```javascript
// Single pass with for loop
const result = [];
for (const u of users) {
  if (u.active && u.age > 18) {
    result.push(u.name);
  }
}

// Or combine filters first
const result = users
  .filter(u => u.active && u.age > 18)  // Pass 1: Combined filter
  .map(u => u.name);                     // Pass 2: Extract names

// Or use reduce for single pass
const result = users.reduce((acc, u) => {
  if (u.active && u.age > 18) {
    acc.push(u.name);
  }
  return acc;
}, []);

// For large datasets, consider transducers (functional approach)
// Using ramda or transducers-js
import { transduce, compose, filter, map } from 'ramda';

const result = transduce(
  compose(
    filter(u => u.active),
    filter(u => u.age > 18),
    map(u => u.name)
  ),
  (acc, val) => (acc.push(val), acc),
  [],
  users
);
```

**Performance impact:**
- 4 passes → 1 pass
- 3 intermediate arrays eliminated
- 2-5x faster for large datasets

**Best practices:**
- Combine filters before mapping
- Use for...of for complex multi-step logic
- Avoid excessive chaining (>3 methods)
- Consider transducers for functional style without overhead

**Related:** ARRAY-METHODS, ALGO-COMPLEX

---

#### SPREAD-CLONE: Avoid Excessive Spreading

**Impact:** Medium

**Slow code:**
```javascript
// Spreading large objects repeatedly
function updateUser(user, updates) {
  return {
    ...user,  // Copies all properties
    ...updates
  };
}

// Spreading in loops - O(n × m)
let state = { items: [] };
for (let i = 0; i < 1000; i++) {
  state = {
    ...state,  // Copies everything on each iteration!
    items: [...state.items, i]  // Also copies entire array!
  };
}
```

**Fast code:**
```javascript
// Direct property assignment for large objects
function updateUser(user, updates) {
  return Object.assign({}, user, updates);
  // Or for very large objects, mutate if possible
  // Object.assign(user, updates);
}

// Mutate when building, freeze when done (immutability at boundaries)
function buildState() {
  const state = { items: [] };
  for (let i = 0; i < 1000; i++) {
    state.items.push(i);  // Mutate during construction
  }
  return Object.freeze(state);  // Immutable result
}

// For arrays, preallocate size
const items = new Array(1000);
for (let i = 0; i < 1000; i++) {
  items[i] = i;
}

// Immer for convenient immutability with mutation syntax
import produce from 'immer';

const nextState = produce(state, draft => {
  for (let i = 0; i < 1000; i++) {
    draft.items.push(i);  // Looks like mutation, produces immutable
  }
});
```

**Performance impact:**
- 100x faster for large objects/arrays in loops
- Reduces memory allocations
- Immer provides best of both worlds

**Best practices:**
- Avoid spreading in loops
- Use Object.assign for multiple updates
- Consider mutation for internal logic, immutability at API boundaries
- Use Immer for complex state updates

**Related:** IMMUTABLE-LIB, OBJECT-MUTATE

---

#### IMMUTABLE-LIB: Use Immutable Libraries for Complex State

**Impact:** Medium

**Slow code:**
```javascript
// Deep cloning on every update - very slow
function updateNestedState(state, path, value) {
  return JSON.parse(JSON.stringify({
    ...state,
    deeply: {
      ...state.deeply,
      nested: {
        ...state.deeply.nested,
        [path]: value
      }
    }
  }));
}
```

**Fast code:**
```javascript
// Using Immer - structural sharing
import produce from 'immer';

function updateNestedState(state, path, value) {
  return produce(state, draft => {
    draft.deeply.nested[path] = value;
  });
}

// Using Immutable.js - persistent data structures
import { Map } from 'immutable';

const state = Map({ count: 0, user: Map({ name: 'Alice' }) });
const next = state.setIn(['user', 'name'], 'Bob');  // Structural sharing

// Performance comparison for 10,000 updates:
// JSON clone: 5000ms
// Immer: 50ms (100x faster)
// Immutable.js: 20ms (250x faster)
```

**Performance impact:**
- 100-1000x faster than deep cloning
- Structural sharing reduces memory
- Better performance with nested updates

**Best practices:**
- Use Immer for occasional immutable updates
- Use Immutable.js for heavy immutable workloads
- Plain JS objects for simple, shallow updates
- Consider Zustand or Valtio for React state

**Related:** SPREAD-CLONE, MEMO-COMPONENT

---

#### WEAK-MAP: Use WeakMap for Object-Keyed Caches

**Impact:** Medium

**Slow code:**
```javascript
// Regular Map prevents garbage collection
const cache = new Map();

function getCachedData(obj) {
  if (cache.has(obj)) {
    return cache.get(obj);
  }
  const data = expensiveComputation(obj);
  cache.set(obj, data);
  return data;
}

// Problem: Objects are never garbage collected!
// Memory leak for long-running apps
```

**Fast code:**
```javascript
// WeakMap allows garbage collection
const cache = new WeakMap();

function getCachedData(obj) {
  if (cache.has(obj)) {
    return cache.get(obj);
  }
  const data = expensiveComputation(obj);
  cache.set(obj, data);
  return data;
}

// When obj is no longer referenced elsewhere,
// it and its cached data are garbage collected automatically

// Use cases for WeakMap:
// - Caching computed values for objects
// - Private data for objects
// - Metadata for DOM nodes
// - Memoization with object arguments

// React example: Private component state
const privateState = new WeakMap();

class Component {
  constructor() {
    privateState.set(this, { internalValue: 0 });
  }
  
  getState() {
    return privateState.get(this);
  }
}
```

**Performance impact:**
- Prevents memory leaks
- Automatic cleanup
- Same performance as Map for lookups

**Best practices:**
- Use WeakMap for object-keyed caches
- Use WeakSet for object collections
- Cannot iterate (keys are weak references)
- Keys must be objects (not primitives)

**Related:** CACHE-RESULT, MEMORY-LEAK

---

#### TYPED-ARRAYS: Use Typed Arrays for Numeric Data

**Impact:** High

**Slow code:**
```javascript
// Regular array for binary/numeric data
const pixels = [];
for (let i = 0; i < 1920 * 1080 * 4; i++) {
  pixels.push(Math.random() * 255);
}

// Memory: ~60MB (each number stored as 64-bit float)
// Processing: Slow due to dynamic typing
```

**Fast code:**
```javascript
// Typed array - 8-bit unsigned integers
const pixels = new Uint8ClampedArray(1920 * 1080 * 4);
for (let i = 0; i < pixels.length; i++) {
  pixels[i] = Math.random() * 255;
}

// Memory: ~8MB (8x smaller!)
// Processing: 2-10x faster

// Common typed arrays:
// - Int8Array, Uint8Array, Uint8ClampedArray (1 byte)
// - Int16Array, Uint16Array (2 bytes)
// - Int32Array, Uint32Array (4 bytes)
// - Float32Array, Float64Array (4/8 bytes)
// - BigInt64Array, BigUint64Array (8 bytes)

// Canvas example
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
const pixels = imageData.data; // Uint8ClampedArray

// Audio example
const audioContext = new AudioContext();
const buffer = audioContext.createBuffer(2, 44100, 44100);
const leftChannel = buffer.getChannelData(0); // Float32Array
const rightChannel = buffer.getChannelData(1); // Float32Array

// WebGL example
const vertices = new Float32Array([
  -1.0, -1.0, 0.0,
  1.0, -1.0, 0.0,
  0.0, 1.0, 0.0
]);
gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
```

**Performance impact:**
- 2-10x faster for numeric operations
- 2-8x less memory
- Required for WebGL, Canvas, Audio

**Best practices:**
- Use for pixel data, audio samples, binary protocols
- Choose appropriate size (Uint8 vs Uint16 vs Float32)
- Use Uint8ClampedArray for pixel values (auto-clamps 0-255)
- Share memory with ArrayBuffer for zero-copy

**Related:** WEB-WORKERS, ARRAY-BUFFER

---

### 3. Memory Management (6 guidelines)

#### MEMORY-LEAK: Avoid Memory Leaks

**Impact:** Critical

**Slow code:**
```javascript
// Forgotten event listeners
class Component {
  constructor() {
    window.addEventListener('resize', this.handleResize);
  }
  
  handleResize() {
    // ...
  }
  
  // Never removes listener - memory leak!
}

// Forgotten timers
function startPolling() {
  setInterval(() => {
    fetchData();
  }, 1000);
  // Never cleared - runs forever!
}

// Closures holding references
const cache = [];
function addToCache(largeObject) {
  cache.push(() => largeObject.data);  // Keeps largeObject in memory
}

// Forgotten global variables
function process() {
  tempData = largeArray;  // Forgot 'let' - global leak!
}
```

**Fast code:**
```javascript
// Clean up event listeners
class Component {
  constructor() {
    this.handleResize = this.handleResize.bind(this);
    window.addEventListener('resize', this.handleResize);
  }
  
  handleResize() {
    // ...
  }
  
  destroy() {
    window.removeEventListener('resize', this.handleResize);
  }
}

// React hooks pattern
useEffect(() => {
  const handleResize = () => { /* ... */ };
  window.addEventListener('resize', handleResize);
  
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);

// Clear timers
function startPolling() {
  const intervalId = setInterval(() => {
    fetchData();
  }, 1000);
  
  return () => clearInterval(intervalId);  // Cleanup function
}

// Avoid closures over large objects
const cache = [];
function addToCache(largeObject) {
  const data = largeObject.data;  // Extract only what's needed
  cache.push(() => data);
}

// Use strict mode to catch globals
'use strict';
function process() {
  const tempData = largeArray;  // Would error without 'const'
}

// Common leak sources:
// 1. Event listeners not removed
// 2. Timers not cleared
// 3. Closures holding large objects
// 4. Forgotten global variables
// 5. Circular references (less common in modern JS)
// 6. Detached DOM nodes
```

**Performance impact:**
- Prevents memory growth over time
- Avoids browser slowdown and crashes
- Critical for long-running SPAs

**Best practices:**
- Always clean up subscriptions, listeners, timers
- Use useEffect return for React cleanup
- Use WeakMap for object caches
- Avoid global variables
- Use browser DevTools memory profiler

**Related:** WEAK-MAP, EVENT-PASSIVE

---

#### CLOSURE-SCOPE: Be Mindful of Closure Scope

**Impact:** Medium

**Slow code:**
```javascript
// Closure captures entire scope
function createHandlers(largeData, users) {
  const handlers = [];
  
  for (let i = 0; i < 1000; i++) {
    handlers.push(() => {
      console.log(users[i].name);  // Captures largeData too!
    });
  }
  
  return handlers;
}

// Each closure holds reference to largeData unnecessarily
```

**Fast code:**
```javascript
// Extract only what's needed
function createHandlers(largeData, users) {
  const handlers = [];
  
  for (let i = 0; i < 1000; i++) {
    const name = users[i].name;  // Extract only name
    handlers.push(() => {
      console.log(name);  // Captures only name
    });
  }
  
  return handlers;
}

// Or pass parameters
function createHandlers(largeData, users) {
  const handlers = [];
  
  for (let i = 0; i < 1000; i++) {
    handlers.push(createHandler(users[i].name));
  }
  
  return handlers;
}

function createHandler(name) {
  return () => console.log(name);
}
```

**Performance impact:**
- Reduces memory per closure
- 10-100x less memory for large closures
- Faster garbage collection

**Best practices:**
- Extract only needed variables
- Avoid closures over large objects when possible
- Use parameters instead of closure scope
- Be aware of what your closures capture

**Related:** MEMORY-LEAK, PURE-FUNCTION

---

#### LAZY-INIT: Lazy Initialize Expensive Objects

**Impact:** Medium

**Slow code:**
```javascript
// Eager initialization - all loaded upfront
class Application {
  constructor() {
    this.database = new Database();  // 500ms
    this.cache = new Cache();        // 200ms
    this.logger = new Logger();      // 100ms
    this.analytics = new Analytics(); // 300ms
    // Total: 1100ms startup time, even if unused!
  }
}
```

**Fast code:**
```javascript
// Lazy initialization - only when needed
class Application {
  constructor() {
    this._database = null;
    this._cache = null;
    this._logger = null;
    this._analytics = null;
  }
  
  get database() {
    if (!this._database) {
      this._database = new Database();
    }
    return this._database;
  }
  
  get cache() {
    if (!this._cache) {
      this._cache = new Cache();
    }
    return this._cache;
  }
  
  // ...similar for other services
}

// Or using Proxy for automatic lazy loading
function lazyProxy(creator) {
  let instance = null;
  return new Proxy({}, {
    get(target, prop) {
      if (!instance) instance = creator();
      return instance[prop];
    }
  });
}

const database = lazyProxy(() => new Database());
database.query('...'); // Database created only now

// React lazy loading
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />  {/* Loaded only when rendered */}
    </Suspense>
  );
}
```

**Performance impact:**
- Faster startup (1100ms → 0ms)
- Lower initial memory
- Pay-as-you-go loading

**Best practices:**
- Lazy load expensive services
- Lazy load large components (React.lazy)
- Lazy load heavy libraries (dynamic import)
- Consider code splitting for route-based lazy loading

**Related:** CODE-SPLIT, DYNAMIC-IMPORT

---

#### GC-FRIENDLY: Write Garbage Collector Friendly Code

**Impact:** Low

**Slow code:**
```javascript
// Creates many short-lived objects
function processData(items) {
  return items.map(item => {
    const temp = { ...item };  // New object
    const result = transform(temp);  // New object
    return result;
  });
}

// Frequent object creation triggers GC pauses
```

**Fast code:**
```javascript
// Reuse objects when possible
function processData(items) {
  return items.map(item => transform(item));  // Direct transformation
}

// Object pooling for high-frequency allocations
class ObjectPool {
  constructor(factory, resetFn) {
    this.factory = factory;
    this.resetFn = resetFn;
    this.pool = [];
  }
  
  acquire() {
    return this.pool.pop() || this.factory();
  }
  
  release(obj) {
    this.resetFn(obj);
    this.pool.push(obj);
  }
}

// Example: Particle system
const particlePool = new ObjectPool(
  () => ({ x: 0, y: 0, vx: 0, vy: 0, life: 0 }),
  (p) => { p.x = p.y = p.vx = p.vy = p.life = 0; }
);

function createParticle(x, y) {
  const particle = particlePool.acquire();
  particle.x = x;
  particle.y = y;
  particle.life = 1.0;
  return particle;
}

function removeParticle(particle) {
  particlePool.release(particle);
}
```

**Performance impact:**
- Reduces GC frequency
- Smoother performance (no GC pauses)
- Important for games and real-time apps

**Best practices:**
- Avoid creating objects in hot loops
- Reuse objects when possible
- Use object pooling for high-frequency allocations
- Preallocate arrays when size is known

**Related:** CLOSURE-SCOPE, TYPED-ARRAYS

---

#### DETACHED-DOM: Avoid Detached DOM Nodes

**Impact:** Medium

**Slow code:**
```javascript
// Keeping references to removed DOM nodes
const cache = {};

function cacheElement(id) {
  cache[id] = document.getElementById(id);
}

// Later, element is removed from DOM
document.getElementById('my-div').remove();

// But cache still holds reference - memory leak!
```

**Fast code:**
```javascript
// Use WeakMap for DOM references
const cache = new WeakMap();

function cacheElement(element) {
  const data = computeData(element);
  cache.set(element, data);
}

// When element is removed, it can be garbage collected

// Or clear references explicitly
const cache = {};

function cacheElement(id) {
  const element = document.getElementById(id);
  cache[id] = { element, data: computeData(element) };
}

function clearCache(id) {
  delete cache[id];  // Removes reference
}

// React: Avoid storing DOM refs in state
// Bad
const [node, setNode] = useState(null);
useEffect(() => {
  setNode(document.getElementById('my-div'));
}, []);

// Good
const nodeRef = useRef(null);
useEffect(() => {
  nodeRef.current = document.getElementById('my-div');
}, []);
```

**Performance impact:**
- Prevents memory leaks
- Reduces memory usage
- Allows DOM nodes to be garbage collected

**Best practices:**
- Use WeakMap for DOM node caches
- Clear references when nodes are removed
- Use React refs, not state, for DOM nodes
- Use MutationObserver to detect removals

**Related:** MEMORY-LEAK, WEAK-MAP

---

#### MEMORY-MEASURE: Measure Memory Usage

**Impact:** Low (measurement tool, not optimization)

**Measurement techniques:**
```javascript
// Browser DevTools Memory Profiler
// 1. Open DevTools → Memory tab
// 2. Take heap snapshot
// 3. Perform action
// 4. Take another snapshot
// 5. Compare snapshots

// Performance.memory API (Chrome only)
if (performance.memory) {
  console.log('Used JS Heap:', performance.memory.usedJSHeapSize);
  console.log('Total JS Heap:', performance.memory.totalJSHeapSize);
  console.log('Heap Limit:', performance.memory.jsHeapSizeLimit);
}

// Memory pressure warning
if ('memory' in performance) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.name === 'memory') {
        console.warn('Memory pressure detected!', entry);
      }
    }
  });
  observer.observe({ entryTypes: ['memory'] });
}

// Measure object size (approximation)
function roughSizeOfObject(object) {
  const objectList = [];
  const stack = [object];
  let bytes = 0;

  while (stack.length) {
    const value = stack.pop();

    if (typeof value === 'boolean') {
      bytes += 4;
    } else if (typeof value === 'string') {
      bytes += value.length * 2;
    } else if (typeof value === 'number') {
      bytes += 8;
    } else if (typeof value === 'object' && value !== null) {
      if (objectList.indexOf(value) === -1) {
        objectList.push(value);
        for (const key in value) {
          stack.push(value[key]);
        }
      }
    }
  }

  return bytes;
}

console.log('Object size:', roughSizeOfObject(myObject), 'bytes');
```

**Best practices:**
- Use Chrome DevTools Memory Profiler regularly
- Look for "detached DOM nodes" and "retained size"
- Monitor performance.memory during development
- Set up memory budgets for production

**Related:** MEMORY-LEAK, WEAK-MAP

---

### 4. DOM Operations (7 guidelines)


#### DOM-BATCH: Batch DOM Operations

**Impact:** High

**Slow code:**
```javascript
// Triggering layout thrashing - 1000 reflows!
const container = document.getElementById('container');

for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  div.textContent = `Item ${i}`;
  container.appendChild(div);  // Reflow on each append!
  
  const height = div.offsetHeight;  // Forces layout calculation
  div.style.marginTop = height + 'px';  // Another reflow!
}
```

**Fast code:**
```javascript
// Batch DOM updates
const container = document.getElementById('container');
const fragment = document.createDocumentFragment();

for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  div.textContent = `Item ${i}`;
  fragment.appendChild(div);  // No reflow - not in DOM yet
}

container.appendChild(fragment);  // Single reflow

// Or use innerHTML for static content (faster)
const items = Array.from({ length: 1000 }, (_, i) => 
  `<div>Item ${i}</div>`
).join('');
container.innerHTML = items;  // Single reflow

// Or hide, modify, show
container.style.display = 'none';  // Remove from layout
for (let i = 0; i < 1000; i++) {
  const div = document.createElement('div');
  div.textContent = `Item ${i}`;
  container.appendChild(div);
}
container.style.display = '';  // Single reflow
```

**Performance impact:**
- 1000 reflows → 1 reflow
- 100-1000x faster
- Critical for list rendering

**Best practices:**
- Use DocumentFragment for multiple elements
- Use innerHTML for static content
- Hide element, modify, then show
- Batch style changes with cssText or classes

**Related:** VIRTUAL-SCROLL, LAYOUT-THRASH

---

#### LAYOUT-THRASH: Avoid Layout Thrashing

**Impact:** Critical

**Slow code:**
```javascript
// Reading layout, writing style, repeat - forces sync layout!
const elements = document.querySelectorAll('.item');

elements.forEach(el => {
  const height = el.offsetHeight;  // Read (forces layout)
  el.style.height = height + 10 + 'px';  // Write (invalidates layout)
  
  const width = el.offsetWidth;  // Read (forces layout AGAIN)
  el.style.width = width + 10 + 'px';  // Write (invalidates layout)
});

// Triggers layout calculation 2000 times for 1000 elements!
```

**Fast code:**
```javascript
// Batch reads, then batch writes
const elements = document.querySelectorAll('.item');

// Read phase
const dimensions = Array.from(elements).map(el => ({
  height: el.offsetHeight,
  width: el.offsetWidth
}));

// Write phase
elements.forEach((el, i) => {
  el.style.height = dimensions[i].height + 10 + 'px';
  el.style.width = dimensions[i].width + 10 + 'px';
});

// Or use FastDOM library to automatically batch
import fastdom from 'fastdom';

elements.forEach(el => {
  fastdom.measure(() => {
    const height = el.offsetHeight;
    const width = el.offsetWidth;
    
    fastdom.mutate(() => {
      el.style.height = height + 10 + 'px';
      el.style.width = width + 10 + 'px';
    });
  });
});

// Or use requestAnimationFrame for visual updates
const updates = [];

elements.forEach(el => {
  updates.push({
    el,
    height: el.offsetHeight,
    width: el.offsetWidth
  });
});

requestAnimationFrame(() => {
  updates.forEach(({ el, height, width }) => {
    el.style.height = height + 10 + 'px';
    el.style.width = width + 10 + 'px';
  });
});
```

**Performance impact:**
- 2000 layouts → 2 layouts
- 100-1000x faster
- Prevents jank and dropped frames

**Layout-triggering properties (read):**
- offsetHeight, offsetWidth, offsetTop, offsetLeft
- scrollHeight, scrollWidth, scrollTop, scrollLeft
- clientHeight, clientWidth, clientTop, clientLeft
- getBoundingClientRect(), getComputedStyle()

**Best practices:**
- Batch reads, then batch writes
- Use FastDOM or similar library
- Use requestAnimationFrame for visual updates
- Avoid reading layout in loops

**Related:** DOM-BATCH, RAF-ANIMATION

---

#### VIRTUAL-SCROLL: Use Virtual Scrolling for Long Lists

**Impact:** Critical

**Slow code:**
```javascript
// Rendering 100,000 DOM nodes
function renderList(items) {
  return items.map(item => `
    <div class="item">${item.text}</div>
  `).join('');
}

document.getElementById('list').innerHTML = renderList(items);

// 100,000 DOM nodes = slow rendering, sluggish scrolling
```

**Fast code:**
```javascript
// Virtual scrolling - render only visible items
class VirtualScroll {
  constructor(container, items, itemHeight, viewportHeight) {
    this.container = container;
    this.items = items;
    this.itemHeight = itemHeight;
    this.viewportHeight = viewportHeight;
    this.visibleCount = Math.ceil(viewportHeight / itemHeight);
    
    this.render();
    container.addEventListener('scroll', () => this.render());
  }
  
  render() {
    const scrollTop = this.container.scrollTop;
    const startIndex = Math.floor(scrollTop / this.itemHeight);
    const endIndex = startIndex + this.visibleCount;
    
    const visibleItems = this.items.slice(startIndex, endIndex);
    const offsetY = startIndex * this.itemHeight;
    
    this.container.innerHTML = `
      <div style="height: ${this.items.length * this.itemHeight}px">
        <div style="transform: translateY(${offsetY}px)">
          ${visibleItems.map(item => `
            <div class="item" style="height: ${this.itemHeight}px">
              ${item.text}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
}

// 100,000 items, render only ~20 at a time
new VirtualScroll(container, items, 50, 1000);

// Or use libraries:
// - react-window (React)
// - react-virtualized (React)
// - vue-virtual-scroller (Vue)
// - @angular/cdk/scrolling (Angular)

// React example
import { FixedSizeList } from 'react-window';

function App() {
  return (
    <FixedSizeList
      height={600}
      itemCount={100000}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>Item {index}</div>
      )}
    </FixedSizeList>
  );
}
```

**Performance impact:**
- 100,000 DOM nodes → 20 DOM nodes
- 1000x faster rendering
- Smooth scrolling regardless of list size

**Best practices:**
- Always use virtual scrolling for >1000 items
- Use libraries (react-window, react-virtualized)
- Consider dynamic item heights (trickier)
- Measure performance with realistic data

**Related:** DOM-BATCH, LAZY-RENDER

---

#### EVENT-PASSIVE: Use Passive Event Listeners

**Impact:** Medium

**Slow code:**
```javascript
// Non-passive listeners block scrolling
element.addEventListener('touchstart', (e) => {
  // Browser must wait to see if we call preventDefault()
  doSomething();
});

element.addEventListener('wheel', (e) => {
  // Blocks smooth scrolling
  handleWheel(e);
});
```

**Fast code:**
```javascript
// Passive listeners don't block scrolling
element.addEventListener('touchstart', (e) => {
  doSomething();
}, { passive: true });  // Tells browser we won't call preventDefault()

element.addEventListener('wheel', (e) => {
  handleWheel(e);
}, { passive: true });

// For scroll events, always use passive
window.addEventListener('scroll', () => {
  updateScrollPosition();
}, { passive: true });

// React: Passive listeners in useEffect
useEffect(() => {
  const handleScroll = () => updateScrollPosition();
  
  window.addEventListener('scroll', handleScroll, { passive: true });
  
  return () => {
    window.removeEventListener('scroll', handleScroll);
  };
}, []);
```

**Performance impact:**
- Eliminates scroll jank
- Smoother touch interactions
- Better perceived performance

**When to use passive:**
- scroll, wheel, touchstart, touchmove events
- When you never call preventDefault()
- Default for scroll/wheel in modern browsers

**When NOT to use passive:**
- When you need to call preventDefault()
- Form validation, drag-and-drop

**Related:** DEBOUNCE-THROTTLE, RAF-ANIMATION

---

#### EVENT-DELEGATE: Use Event Delegation

**Impact:** Medium

**Slow code:**
```javascript
// Adding listener to every item - 1000 listeners!
const items = document.querySelectorAll('.item');

items.forEach(item => {
  item.addEventListener('click', (e) => {
    handleClick(e.target);
  });
});

// Memory: 1000 listeners
// Dynamic items: Must re-attach listeners
```

**Fast code:**
```javascript
// Single listener on parent
const container = document.getElementById('container');

container.addEventListener('click', (e) => {
  // Find closest .item
  const item = e.target.closest('.item');
  if (item) {
    handleClick(item);
  }
});

// Memory: 1 listener
// Dynamic items: Automatically handled!

// React example
function List({ items }) {
  const handleClick = (e) => {
    const itemId = e.target.dataset.id;
    if (itemId) {
      console.log('Clicked item:', itemId);
    }
  };
  
  return (
    <div onClick={handleClick}>
      {items.map(item => (
        <div key={item.id} data-id={item.id} className="item">
          {item.text}
        </div>
      ))}
    </div>
  );
}
```

**Performance impact:**
- 1000 listeners → 1 listener
- Less memory
- Handles dynamic elements automatically

**Best practices:**
- Use delegation for lists
- Use for dynamically added elements
- Check event.target to identify clicked element
- Don't delegate for frequently firing events (mousemove)

**Related:** EVENT-PASSIVE, DOM-BATCH

---

#### CSS-CHANGES: Use CSS for Animations, Not JavaScript

**Impact:** High

**Slow code:**
```javascript
// JavaScript animation - runs on main thread
function animate(element) {
  let pos = 0;
  const id = setInterval(() => {
    if (pos >= 300) {
      clearInterval(id);
    } else {
      pos += 2;
      element.style.left = pos + 'px';  // Forces layout!
    }
  }, 10);
}
```

**Fast code:**
```javascript
// CSS animation - runs on compositor thread
element.classList.add('animate');

/* CSS */
.animate {
  animation: slide 1.5s ease-in-out forwards;
}

@keyframes slide {
  from { transform: translateX(0); }
  to { transform: translateX(300px); }
}

// Or CSS transitions
element.style.transition = 'transform 1.5s ease-in-out';
element.style.transform = 'translateX(300px)';

// For complex animations, use Web Animations API
element.animate([
  { transform: 'translateX(0)' },
  { transform: 'translateX(300px)' }
], {
  duration: 1500,
  easing: 'ease-in-out',
  fill: 'forwards'
});

// GPU-accelerated properties (use these):
// - transform (translate, rotate, scale)
// - opacity
// - filter (blur, brightness, etc.)

// Avoid animating (trigger layout):
// - left, top, width, height
// - margin, padding
// - Any layout-affecting property
```

**Performance impact:**
- 60fps vs 30fps or choppy
- Runs off main thread (compositor)
- GPU accelerated

**Best practices:**
- Use CSS animations/transitions
- Animate transform and opacity only
- Use will-change for complex animations
- Web Animations API for JS-controlled CSS anims

**Related:** RAF-ANIMATION, LAYOUT-THRASH

---

#### RAF-ANIMATION: Use requestAnimationFrame for JavaScript Animations

**Impact:** Medium

**Slow code:**
```javascript
// Using setInterval - not synced with display refresh
function animate() {
  setInterval(() => {
    element.style.left = pos++ + 'px';
  }, 16);  // Roughly 60fps, but not synced!
}

// setTimeout is similar
function animate() {
  setTimeout(() => {
    element.style.left = pos++ + 'px';
    animate();
  }, 16);
}
```

**Fast code:**
```javascript
// requestAnimationFrame - synced with display
function animate() {
  element.style.left = pos++ + 'px';
  
  if (pos < 300) {
    requestAnimationFrame(animate);
  }
}

requestAnimationFrame(animate);

// With delta time for smooth animation
let lastTime = 0;
function animate(currentTime) {
  const deltaTime = currentTime - lastTime;
  lastTime = currentTime;
  
  // Move based on time, not frames (handles variable frame rates)
  pos += speed * (deltaTime / 1000);
  element.style.left = pos + 'px';
  
  if (pos < 300) {
    requestAnimationFrame(animate);
  }
}

requestAnimationFrame(animate);

// Pause when tab is hidden (automatic with RAF)
let rafId;
function animate() {
  element.style.left = pos++ + 'px';
  
  if (pos < 300) {
    rafId = requestAnimationFrame(animate);
  }
}

// Start
rafId = requestAnimationFrame(animate);

// Stop
cancelAnimationFrame(rafId);
```

**Performance impact:**
- Synced with display refresh (60Hz, 120Hz, etc.)
- Automatic pause when tab hidden (saves battery)
- Smoother animations

**Best practices:**
- Always use RAF for JS animations
- Use delta time for frame-rate independence
- Cancel RAF when animation completes
- Consider CSS animations for simpler cases

**Related:** CSS-CHANGES, DEBOUNCE-THROTTLE

---

### 5. Async Operations (7 guidelines)

#### PROMISE-PARALLEL: Run Independent Promises in Parallel

**Impact:** High

**Slow code:**
```javascript
// Sequential - waits for each to complete
async function fetchData() {
  const users = await fetch('/api/users').then(r => r.json());  // 200ms
  const posts = await fetch('/api/posts').then(r => r.json());  // 300ms
  const comments = await fetch('/api/comments').then(r => r.json());  // 250ms
  
  return { users, posts, comments };
}

// Total: 750ms
```

**Fast code:**
```javascript
// Parallel - all requests at once
async function fetchData() {
  const [users, posts, comments] = await Promise.all([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/posts').then(r => r.json()),
    fetch('/api/comments').then(r => r.json())
  ]);
  
  return { users, posts, comments };
}

// Total: 300ms (longest request)

// Promise.allSettled for handling failures gracefully
async function fetchData() {
  const results = await Promise.allSettled([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/posts').then(r => r.json()),
    fetch('/api/comments').then(r => r.json())
  ]);
  
  const users = results[0].status === 'fulfilled' ? results[0].value : [];
  const posts = results[1].status === 'fulfilled' ? results[1].value : [];
  const comments = results[2].status === 'fulfilled' ? results[2].value : [];
  
  return { users, posts, comments };
}

// Promise.race for fastest response
async function fetchFastest() {
  return Promise.race([
    fetch('/api/cdn1/data'),
    fetch('/api/cdn2/data'),
    fetch('/api/cdn3/data')
  ]);
}
```

**Performance impact:**
- 2-5x faster for independent operations
- Reduces total wait time
- Better user experience

**Best practices:**
- Use Promise.all for independent async operations
- Use Promise.allSettled when some failures are OK
- Use Promise.race for redundant requests
- Don't parallelize dependent operations

**Related:** ASYNC-AWAIT, LAZY-LOAD

---

#### ASYNC-AWAIT: Use Async/Await Over Promises Chains

**Impact:** Low (readability, not performance)

**Slow code:**
```javascript
// Promise chains - harder to read and debug
function processUser(userId) {
  return fetchUser(userId)
    .then(user => {
      return validateUser(user);
    })
    .then(validUser => {
      return fetchUserPosts(validUser.id);
    })
    .then(posts => {
      return posts.map(p => processPost(p));
    })
    .then(processedPosts => {
      return { posts: processedPosts };
    })
    .catch(error => {
      console.error('Error:', error);
      throw error;
    });
}
```

**Fast code:**
```javascript
// Async/await - cleaner and easier to debug
async function processUser(userId) {
  try {
    const user = await fetchUser(userId);
    const validUser = await validateUser(user);
    const posts = await fetchUserPosts(validUser.id);
    const processedPosts = posts.map(p => processPost(p));
    
    return { posts: processedPosts };
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Parallel with async/await
async function fetchMultiple() {
  const [users, posts] = await Promise.all([
    fetchUsers(),
    fetchPosts()
  ]);
  
  return { users, posts };
}

// Top-level await (ES2022)
const data = await fetchData();
```

**Performance impact:**
- Same performance as Promise chains
- Easier to optimize (clearer control flow)
- Better debugging experience

**Best practices:**
- Use async/await for readability
- Remember to await Promise.all for parallel ops
- Use try/catch for error handling
- Avoid sequential awaits for independent ops

**Related:** PROMISE-PARALLEL

---

#### LAZY-LOAD: Lazy Load Heavy Resources

**Impact:** High

**Slow code:**
```javascript
// Loading everything upfront
import HeavyLibrary from 'heavy-library';  // 500KB!
import HeavyComponent from './HeavyComponent';  // 200KB

function App() {
  const [showHeavy, setShowHeavy] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShowHeavy(true)}>Show</button>
      {showHeavy && <HeavyComponent />}  {/* Loaded even if never shown */}
    </div>
  );
}
```

**Fast code:**
```javascript
// Lazy loading with dynamic imports
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  const [showHeavy, setShowHeavy] = useState(false);
  
  return (
    <div>
      <button onClick={() => setShowHeavy(true)}>Show</button>
      {showHeavy && (
        <Suspense fallback={<Loading />}>
          <HeavyComponent />  {/* Loaded only when shown */}
        </Suspense>
      )}
    </div>
  );
}

// Lazy load library when needed
let heavyLib = null;

async function processData(data) {
  if (!heavyLib) {
    heavyLib = await import('heavy-library');
  }
  return heavyLib.process(data);
}

// Prefetch on hover/interaction
function Button({ onClick }) {
  const [module, setModule] = useState(null);
  
  const handleMouseEnter = async () => {
    const mod = await import('./heavy-module');
    setModule(mod);
  };
  
  const handleClick = () => {
    if (module) {
      module.doSomething();
    }
    onClick();
  };
  
  return (
    <button 
      onMouseEnter={handleMouseEnter}
      onClick={handleClick}
    >
      Click Me
    </button>
  );
}
```

**Performance impact:**
- Faster initial load (500KB → 50KB)
- Lower bandwidth for users who don't use feature
- Better time-to-interactive

**Best practices:**
- Lazy load route components
- Lazy load modals, dialogs, heavy features
- Prefetch on hover/interaction
- Monitor bundle sizes with webpack-bundle-analyzer

**Related:** CODE-SPLIT, LAZY-INIT

---

#### WEB-WORKERS: Use Web Workers for Heavy Computation

**Impact:** High

**Slow code:**
```javascript
// Heavy computation on main thread - freezes UI
function processLargeDataset(data) {
  // 5 seconds of computation
  const result = data.map(item => {
    return expensiveCalculation(item);
  });
  
  updateUI(result);  // UI was frozen for 5 seconds!
}
```

**Fast code:**
```javascript
// Web Worker - runs on separate thread
// worker.js
self.addEventListener('message', (e) => {
  const data = e.data;
  
  const result = data.map(item => {
    return expensiveCalculation(item);
  });
  
  self.postMessage(result);
});

// main.js
const worker = new Worker('worker.js');

worker.addEventListener('message', (e) => {
  const result = e.data;
  updateUI(result);  // UI stayed responsive!
});

worker.postMessage(largeDataset);

// Using Comlink for easier API
// npm install comlink
// worker.js
import { expose } from 'comlink';

const api = {
  async processData(data) {
    return data.map(item => expensiveCalculation(item));
  }
};

expose(api);

// main.js
import { wrap } from 'comlink';

const worker = new Worker('worker.js');
const api = wrap(worker);

const result = await api.processData(largeDataset);
updateUI(result);

// React hook for Web Workers
function useWorker(workerFunction) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const run = useCallback((data) => {
    setLoading(true);
    
    const worker = new Worker(
      URL.createObjectURL(
        new Blob([`(${workerFunction.toString()})()`])
      )
    );
    
    worker.postMessage(data);
    worker.onmessage = (e) => {
      setResult(e.data);
      setLoading(false);
      worker.terminate();
    };
  }, [workerFunction]);
  
  return { result, loading, run };
}
```

**Performance impact:**
- UI stays responsive during heavy computation
- Uses multiple CPU cores
- 2-4x faster on multi-core devices

**Best practices:**
- Use for CPU-intensive tasks (>50ms)
- Image processing, data parsing, cryptography
- Cannot access DOM from worker
- Transfer typed arrays with transferable objects

**Related:** TYPED-ARRAYS, ASYNC-AWAIT

---

#### PRELOAD-PREFETCH: Use Resource Hints

**Impact:** Medium

**Slow code:**
```html
<!-- No resource hints - browser discovers late -->
<link rel="stylesheet" href="styles.css">
<script src="app.js"></script>

<!-- Later in page -->
<img src="hero.jpg">

<!-- User clicks, then fetches -->
<a href="/page2">Next Page</a>
```

**Fast code:**
```html
<!-- Preload critical resources early -->
<head>
  <!-- High priority, blocks render -->
  <link rel="preload" href="critical.css" as="style">
  <link rel="preload" href="font.woff2" as="font" crossorigin>
  <link rel="preload" href="hero.jpg" as="image">
  
  <!-- Medium priority, loads in background -->
  <link rel="prefetch" href="/page2">
  <link rel="prefetch" href="secondary.js">
  
  <!-- DNS lookup early -->
  <link rel="dns-prefetch" href="https://api.example.com">
  
  <!-- Connect early (DNS + TCP + TLS) -->
  <link rel="preconnect" href="https://cdn.example.com">
  
  <link rel="stylesheet" href="styles.css">
  <script src="app.js"></script>
</head>

<!-- In React/SPA -->
import { useEffect } from 'react';

function prefetchRoute(href) {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = href;
  document.head.appendChild(link);
}

function Link({ href, children }) {
  const handleMouseEnter = () => {
    prefetchRoute(href);
  };
  
  return <a href={href} onMouseEnter={handleMouseEnter}>{children}</a>;
}
```

**Resource hints:**
- **preload**: High priority, fetch ASAP (fonts, critical CSS/JS/images)
- **prefetch**: Low priority, fetch when idle (next page, secondary resources)
- **dns-prefetch**: Resolve DNS early (external domains)
- **preconnect**: DNS + TCP + TLS early (API servers, CDNs)
- **modulepreload**: Preload ES modules and dependencies

**Performance impact:**
- Reduces perceived load time
- Faster page transitions
- Better LCP (Largest Contentful Paint)

**Best practices:**
- Preload critical above-fold resources
- Prefetch likely next navigation
- Don't overuse (bandwidth cost)
- Measure with Lighthouse

**Related:** LAZY-LOAD, CODE-SPLIT

---

#### ABORT-REQUESTS: Cancel Unnecessary Requests

**Impact:** Medium

**Slow code:**
```javascript
// Old request continues even after new one starts
function SearchInput() {
  const [query, setQuery] = useState('');
  
  const search = (q) => {
    fetch(`/api/search?q=${q}`)
      .then(r => r.json())
      .then(results => setResults(results));
  };
  
  useEffect(() => {
    if (query) search(query);
  }, [query]);
  
  // User types "hello" quickly
  // Fires: /api/search?q=h, q=he, q=hel, q=hell, q=hello
  // All 5 requests complete, last write wins (might be wrong order!)
}
```

**Fast code:**
```javascript
// Abort previous request when new one starts
function SearchInput() {
  const [query, setQuery] = useState('');
  const abortControllerRef = useRef(null);
  
  const search = (q) => {
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // New abort controller
    const controller = new AbortController();
    abortControllerRef.current = controller;
    
    fetch(`/api/search?q=${q}`, { signal: controller.signal })
      .then(r => r.json())
      .then(results => setResults(results))
      .catch(err => {
        if (err.name === 'AbortError') {
          console.log('Request canceled');
        }
      });
  };
  
  useEffect(() => {
    if (query) search(query);
    
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [query]);
}

// Axios example
const CancelToken = axios.CancelToken;
let cancel;

axios.get('/api/data', {
  cancelToken: new CancelToken(c => cancel = c)
});

// Cancel
cancel('Request canceled');
```

**Performance impact:**
- Reduces unnecessary network traffic
- Prevents race conditions
- Lower server load

**Best practices:**
- Always use AbortController for fetch
- Cancel on component unmount
- Cancel previous search requests
- Cancel requests on navigation

**Related:** DEBOUNCE-THROTTLE, PROMISE-PARALLEL

---

#### STREAM-RESPONSE: Stream Large Responses

**Impact:** High

**Slow code:**
```javascript
// Waits for entire 100MB response
async function downloadLargeFile() {
  const response = await fetch('/api/large-data');
  const data = await response.json();  // Waits for all 100MB
  processData(data);
}
```

**Fast code:**
```javascript
// Stream and process incrementally
async function downloadLargeFile() {
  const response = await fetch('/api/large-data');
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  let buffer = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    
    // Process line by line
    const lines = buffer.split('\n');
    buffer = lines.pop();  // Keep incomplete line
    
    for (const line of lines) {
      processLine(JSON.parse(line));  // Process as data arrives
    }
  }
}

// Streaming JSON with ndjson (newline-delimited JSON)
async function streamNDJSON(url) {
  const response = await fetch(url);
  const reader = response.body
    .pipeThrough(new TextDecoderStream())
    .pipeThrough(new NDJSONStream())
    .getReader();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    processItem(value);
  }
}

// Server-Sent Events for real-time updates
const eventSource = new EventSource('/api/updates');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  processUpdate(data);
};

// Close when done
eventSource.close();
```

**Performance impact:**
- Start processing immediately (don't wait for all data)
- Lower memory usage
- Better perceived performance

**Best practices:**
- Stream large datasets (>1MB)
- Use ndjson for JSON streaming
- Use Server-Sent Events for real-time updates
- Use WebSockets for bidirectional communication

**Related:** LAZY-LOAD, WEB-WORKERS

---

### 6. Bundling & Loading (6 guidelines)

#### CODE-SPLIT: Split Code by Route

**Impact:** High

**Slow code:**
```javascript
// Single bundle - loads everything upfront
import Home from './pages/Home';
import About from './pages/About';
import Dashboard from './pages/Dashboard';  // Heavy!
import Admin from './pages/Admin';  // Heavy!

function App() {
  return (
    <Router>
      <Route path="/" component={Home} />
      <Route path="/about" component={About} />
      <Route path="/dashboard" component={Dashboard} />
      <Route path="/admin" component={Admin} />
    </Router>
  );
}

// Bundle: 2MB (all routes loaded for every user!)
```

**Fast code:**
```javascript
// Code splitting by route
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Admin = lazy(() => import('./pages/Admin'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Router>
        <Route path="/" component={Home} />
        <Route path="/about" component={About} />
        <Route path="/dashboard" component={Dashboard} />
        <Route path="/admin" component={Admin} />
      </Router>
    </Suspense>
  );
}

// Bundles:
// - main.js: 200KB (shared code)
// - home.js: 50KB
// - about.js: 30KB
// - dashboard.js: 500KB (loaded only when visited)
// - admin.js: 800KB (loaded only when visited)

// Next.js automatic code splitting
// pages/index.js
export default function Home() {
  return <div>Home</div>;
}

// pages/dashboard.js (automatically code split!)
export default function Dashboard() {
  return <div>Dashboard</div>;
}
```

**Performance impact:**
- Initial bundle: 2MB → 200KB (10x smaller)
- Faster time-to-interactive
- Only load code users actually visit

**Best practices:**
- Always split by route
- Split heavy features (charts, editors)
- Monitor bundle sizes
- Use webpack-bundle-analyzer

**Related:** LAZY-LOAD, TREE-SHAKE

---

#### TREE-SHAKE: Enable Tree Shaking

**Impact:** Medium

**Slow code:**
```javascript
// Imports entire library (1MB)
import _ from 'lodash';

function process(data) {
  return _.uniq(data);  // Only uses 1 function!
}

// Webpack includes ALL of lodash
```

**Fast code:**
```javascript
// Import only what you need
import uniq from 'lodash/uniq';

function process(data) {
  return uniq(data);
}

// Or use ES modules for automatic tree shaking
import { uniq } from 'lodash-es';  // .mjs enables tree shaking

// Date-fns example (tree-shake friendly)
import { format, parse } from 'date-fns';  // Only includes these 2 functions

// Ensure your library is tree-shakeable
// package.json
{
  "sideEffects": false,  // No side effects, safe to tree shake
  "module": "dist/index.esm.js"  // ES modules entry
}

// Or specify which files have side effects
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "src/polyfills.js"
  ]
}
```

**Performance impact:**
- 1MB → 10KB (100x smaller for single function)
- Faster parsing and execution
- Better caching (fewer files change)

**Best practices:**
- Use ES modules (import/export, not require)
- Import specific functions, not entire libraries
- Set "sideEffects": false in package.json
- Use modern libraries that support tree shaking

**Related:** CODE-SPLIT, BUNDLE-ANALYSIS

---

#### DYNAMIC-IMPORT: Use Dynamic Imports Strategically

**Impact:** Medium

**Slow code:**
```javascript
// Imports even if never used
import heavyLibrary from 'heavy-library';

function processSpecialCase(data) {
  if (data.type === 'special') {
    return heavyLibrary.process(data);
  }
  return simpleProcess(data);
}

// heavyLibrary loaded even if type is never 'special'
```

**Fast code:**
```javascript
// Load only when needed
async function processSpecialCase(data) {
  if (data.type === 'special') {
    const heavyLibrary = await import('heavy-library');
    return heavyLibrary.default.process(data);
  }
  return simpleProcess(data);
}

// Cache imported module
let heavyLibrary = null;

async function processSpecialCase(data) {
  if (data.type === 'special') {
    if (!heavyLibrary) {
      heavyLibrary = await import('heavy-library');
    }
    return heavyLibrary.default.process(data);
  }
  return simpleProcess(data);
}

// Prefetch on user interaction
button.addEventListener('mouseenter', () => {
  import('heavy-feature');  // Prefetch while user hovers
});

button.addEventListener('click', async () => {
  const module = await import('heavy-feature');  // Already loaded!
  module.doSomething();
});
```

**Performance impact:**
- Smaller initial bundle
- Faster startup
- Pay-as-you-go loading

**Best practices:**
- Dynamic import for conditional features
- Dynamic import for user-triggered features
- Cache imported modules
- Prefetch on user interaction

**Related:** LAZY-LOAD, CODE-SPLIT

---

#### COMPRESSION: Enable Compression

**Impact:** High

**Slow code:**
```javascript
// No compression configured
// Server sends 2MB JavaScript file uncompressed
```

**Fast code:**
```javascript
// Gzip compression (server config)
// Apache .htaccess
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript application/json
</IfModule>

// Nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
gzip_min_length 1000;

// Brotli (better compression)
// Nginx
brotli on;
brotli_types text/plain text/css application/json application/javascript;

// Express.js
const compression = require('compression');
app.use(compression());

// Or use Brotli
const shrinkRay = require('shrink-ray-current');
app.use(shrinkRay());

// Pre-compress at build time (best)
// webpack.config.js
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = {
  plugins: [
    new CompressionPlugin({
      algorithm: 'gzip',
      test: /\.(js|css|html|svg)$/,
    }),
    new CompressionPlugin({
      algorithm: 'brotliCompress',
      test: /\.(js|css|html|svg)$/,
      filename: '[path][base].br',
    })
  ]
};

// Serve pre-compressed files
// Nginx
location ~ \.(js|css|svg)$ {
  gzip_static on;
  brotli_static on;
}
```

**Performance impact:**
- 2MB → 500KB with gzip (4x smaller)
- 2MB → 400KB with Brotli (5x smaller)
- Faster downloads on slow connections

**Best practices:**
- Always enable compression in production
- Use Brotli over gzip (better compression)
- Pre-compress at build time (faster serving)
- Don't compress images/videos (already compressed)

**Related:** BUNDLE-SIZE, IMAGE-OPT

---

#### BUNDLE-ANALYSIS: Analyze Bundle Size

**Impact:** Low (analysis tool, not optimization)

**Analysis tools:**
```javascript
// webpack-bundle-analyzer
// npm install --save-dev webpack-bundle-analyzer

// webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin()
  ]
};

// Run: npm run build
// Opens interactive treemap in browser

// Source map explorer
// npm install --save-dev source-map-explorer

// package.json
{
  "scripts": {
    "analyze": "source-map-explorer 'build/static/js/*.js'"
  }
}

// bundlesize - CI checks
// npm install --save-dev bundlesize

// package.json
{
  "bundlesize": [
    {
      "path": "./dist/main.*.js",
      "maxSize": "200 kB"
    },
    {
      "path": "./dist/vendor.*.js",
      "maxSize": "500 kB"
    }
  ],
  "scripts": {
    "test": "bundlesize"
  }
}

// Next.js built-in
// next.config.js
module.exports = {
  webpack(config) {
    if (process.env.ANALYZE === 'true') {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(new BundleAnalyzerPlugin());
    }
    return config;
  }
};

// ANALYZE=true npm run build
```

**What to look for:**
- Duplicate dependencies
- Unused dependencies
- Large dependencies (>100KB)
- Opportunity for code splitting

**Best practices:**
- Analyze before every release
- Set bundle size budgets
- Monitor bundle size in CI
- Replace large libraries with smaller alternatives

**Related:** TREE-SHAKE, CODE-SPLIT

---

#### CDN-ASSETS: Serve Assets from CDN

**Impact:** Medium

**Slow code:**
```html
<!-- Serving from own server -->
<script src="/js/app.js"></script>
<link rel="stylesheet" href="/css/styles.css">
<img src="/images/hero.jpg">

<!-- Single server, no caching, slow for distant users -->
```

**Fast code:**
```html
<!-- Serve from CDN -->
<script src="https://cdn.example.com/js/app.v123.js"></script>
<link rel="stylesheet" href="https://cdn.example.com/css/styles.v123.css">
<img src="https://cdn.example.com/images/hero.jpg">

<!-- Benefits:
  - Geographically distributed (low latency)
  - Aggressive caching
  - Parallel downloads (different domain)
  - DDoS protection
-->

<!-- Popular CDNs:
  - Cloudflare (free tier)
  - AWS CloudFront
  - Fastly
  - Vercel Edge Network (automatic with Vercel)
-->

<!-- Webpack config for CDN -->
// webpack.config.js
module.exports = {
  output: {
    publicPath: 'https://cdn.example.com/'
  }
};

// Or environment-based
const publicPath = process.env.NODE_ENV === 'production'
  ? 'https://cdn.example.com/'
  : '/';

module.exports = {
  output: {
    publicPath
  }
};
```

**Performance impact:**
- 50-300ms lower latency (geographic distribution)
- Better caching (CDN edge servers)
- Parallel downloads (different domain)

**Best practices:**
- Use CDN for all static assets
- Use versioned filenames for cache busting
- Set long cache headers (1 year)
- Use multiple CDN domains for parallel downloads

**Related:** COMPRESSION, IMAGE-OPT

---

### 7. React-Specific (6 guidelines)

#### MEMO-COMPONENT: Memoize Components

**Impact:** Medium

**Slow code:**
```javascript
// Re-renders on every parent render
function ExpensiveChild({ data }) {
  // Expensive rendering logic
  return <div>{expensiveCalculation(data)}</div>;
}

function Parent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <ExpensiveChild data={staticData} />  {/* Re-renders even though data unchanged! */}
    </div>
  );
}
```

**Fast code:**
```javascript
// Memoize to prevent unnecessary re-renders
import { memo } from 'react';

const ExpensiveChild = memo(function ExpensiveChild({ data }) {
  return <div>{expensiveCalculation(data)}</div>;
});

// Or with custom comparison
const ExpensiveChild = memo(
  function ExpensiveChild({ data }) {
    return <div>{expensiveCalculation(data)}</div>;
  },
  (prevProps, nextProps) => {
    // Return true if props are equal (skip render)
    return prevProps.data.id === nextProps.data.id;
  }
);

// useMemo for expensive calculations
function Component({ items }) {
  const sortedItems = useMemo(() => {
    return items.sort((a, b) => b.score - a.score);
  }, [items]);
  
  return <List items={sortedItems} />;
}

// useCallback for stable function references
function Parent() {
  const [count, setCount] = useState(0);
  
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);  // Stable reference
  
  return <ExpensiveChild onClick={handleClick} />;
}
```

**Performance impact:**
- Skips expensive re-renders
- 2-10x faster for complex components
- Critical for lists and dashboards

**Best practices:**
- Memoize expensive components
- Memoize components that render often
- Don't memoize everything (overhead)
- Use React DevTools Profiler to identify

**Related:** PURE-COMPONENT, VIRTUAL-DOM

---

#### KEY-OPTIMIZATION: Use Stable Keys in Lists

**Impact:** High

**Slow code:**
```javascript
// Using index as key - causes re-renders on reorder
function List({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{item.text}</li>  // BAD: index changes on reorder
      ))}
    </ul>
  );
}

// When item moves from index 0 to 2:
// - React thinks item at 0 changed
// - Unnecessarily re-renders all items
```

**Fast code:**
```javascript
// Use stable, unique ID
function List({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.text}</li>  // GOOD: ID never changes
      ))}
    </ul>
  );
}

// If no ID, generate stable one
import { nanoid } from 'nanoid';

const items = data.map(item => ({
  ...item,
  id: item.id || nanoid()  // Add ID if missing
}));

// Or use index ONLY if:
// 1. List never reorders
// 2. List never filters
// 3. List never adds/removes items
```

**Performance impact:**
- Prevents unnecessary re-renders
- 10-100x faster for list operations
- Critical for drag-and-drop, filters, sorts

**Best practices:**
- Always use stable, unique ID as key
- Never use index as key (unless truly static)
- Generate IDs once, not on every render
- Use UUIDs or nanoid for client-generated IDs

**Related:** MEMO-COMPONENT, VIRTUAL-SCROLL

---

#### STATE-COLOCATION: Colocate State

**Impact:** Medium

**Slow code:**
```javascript
// State at top level causes wide re-renders
function App() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [editMode, setEditMode] = useState(false);  // Only used in UserEditor
  const [draft, setDraft] = useState('');  // Only used in UserEditor
  
  return (
    <div>
      <UserList users={users} onSelect={setSelectedUser} />
      <UserEditor 
        user={selectedUser}
        editMode={editMode}
        setEditMode={setEditMode}
        draft={draft}
        setDraft={setDraft}
      />
    </div>
  );
}

// Every edit triggers App re-render, which re-renders UserList too!
```

**Fast code:**
```javascript
// Move state closer to where it's used
function App() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  
  return (
    <div>
      <UserList users={users} onSelect={setSelectedUser} />
      <UserEditor user={selectedUser} />
    </div>
  );
}

// UserEditor manages its own state
function UserEditor({ user }) {
  const [editMode, setEditMode] = useState(false);
  const [draft, setDraft] = useState('');
  
  // Only UserEditor re-renders on edit, not entire App!
  
  return (
    <div>
      {editMode ? (
        <textarea value={draft} onChange={e => setDraft(e.target.value)} />
      ) : (
        <div>{user.bio}</div>
      )}
    </div>
  );
}
```

**Performance impact:**
- Reduces re-render scope
- 5-50x fewer re-renders
- Better component isolation

**Best practices:**
- State should live as close as possible to where it's used
- Lift state only when needed by multiple components
- Use composition over prop drilling
- Consider context for truly global state

**Related:** MEMO-COMPONENT, CONTEXT-SPLIT

---

#### CONTEXT-SPLIT: Split Contexts

**Impact:** High

**Slow code:**
```javascript
// Single context with all app state
const AppContext = createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState([]);
  
  const value = {
    user, setUser,
    theme, setTheme,
    notifications, setNotifications
  };
  
  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

// ANY state change causes ALL consumers to re-render!
function ThemeToggle() {
  const { theme, setTheme } = useContext(AppContext);  // Re-renders on user/notification changes!
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>Toggle</button>;
}
```

**Fast code:**
```javascript
// Split into separate contexts
const UserContext = createContext();
const ThemeContext = createContext();
const NotificationsContext = createContext();

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState([]);
  
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <ThemeContext.Provider value={{ theme, setTheme }}>
        <NotificationsContext.Provider value={{ notifications, setNotifications }}>
          {children}
        </NotificationsContext.Provider>
      </ThemeContext.Provider>
    </UserContext.Provider>
  );
}

function ThemeToggle() {
  const { theme, setTheme } = useContext(ThemeContext);  // Only re-renders on theme changes!
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>Toggle</button>;
}

// Or use separate providers pattern
function AppProvider({ children }) {
  return (
    <UserProvider>
      <ThemeProvider>
        <NotificationsProvider>
          {children}
        </NotificationsProvider>
      </ThemeProvider>
    </UserProvider>
  );
}

// Advanced: Context with selector
function createSelectableContext() {
  const Context = createContext(null);
  
  function Provider({ value, children }) {
    const valueRef = useRef(value);
    valueRef.current = value;
    const [subscribers] = useState(() => new Set());
    
    const contextValue = useMemo(() => ({
      value: valueRef,
      subscribe: (callback) => {
        subscribers.add(callback);
        return () => subscribers.delete(callback);
      }
    }), []);
    
    useEffect(() => {
      subscribers.forEach(callback => callback());
    }, [value]);
    
    return <Context.Provider value={contextValue}>{children}</Context.Provider>;
  }
  
  function useSelector(selector) {
    const context = useContext(Context);
    const [, forceUpdate] = useReducer(x => x + 1, 0);
    
    useEffect(() => {
      return context.subscribe(forceUpdate);
    }, [context]);
    
    return selector(context.value.current);
  }
  
  return { Provider, useSelector };
}
```

**Performance impact:**
- Prevents unnecessary re-renders
- 10-100x fewer re-renders
- Critical for large apps

**Best practices:**
- Split contexts by concern
- Never put all state in one context
- Consider Zustand/Jotai for fine-grained reactivity
- Use context selectors (react-tracked, use-context-selector)

**Related:** STATE-COLOCATION, MEMO-COMPONENT

---

#### VIRTUALIZE-LISTS: Virtualize Long Lists

**Impact:** Critical

(See VIRTUAL-SCROLL in DOM Operations section)

---

#### LAZY-COMPONENT: Lazy Load Components

**Impact:** High

(See LAZY-LOAD in Async Operations section)

---

### 8. Profiling & Measurement (5 guidelines)

#### PROFILE-FIRST: Profile Before Optimizing

**Impact:** Critical (measurement, not optimization)

**Measurement tools:**
```javascript
// Chrome DevTools Performance tab
// 1. Open DevTools → Performance
// 2. Click Record
// 3. Perform slow action
// 4. Click Stop
// 5. Analyze flame chart

// Console timing
console.time('operation');
expensiveOperation();
console.timeEnd('operation');  // operation: 1523.456ms

// Performance API
const start = performance.now();
expensiveOperation();
const end = performance.now();
console.log(`Took ${end - start}ms`);

// React Profiler
import { Profiler } from 'react';

function onRenderCallback(
  id, // Component ID
  phase, // "mount" or "update"
  actualDuration, // Time spent rendering
  baseDuration, // Estimated time without memo
  startTime,
  commitTime,
  interactions
) {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>

// Lighthouse (Chrome DevTools)
// Audits → Performance
// Gives scores and recommendations

// Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);  // Cumulative Layout Shift
getFID(console.log);  // First Input Delay
getFCP(console.log);  // First Contentful Paint
getLCP(console.log);  // Largest Contentful Paint
getTTFB(console.log); // Time to First Byte
```

**Best practices:**
- Always profile before optimizing
- Use Lighthouse for overall performance audit
- Use Performance tab for detailed analysis
- Monitor Web Vitals in production

**Related:** All performance guidelines

---

#### MEASURE-IMPACT: Measure Optimization Impact

**Impact:** Low (measurement)

**Before/after benchmarks:**
```javascript
// Benchmark helper
function benchmark(fn, iterations = 1000) {
  const start = performance.now();
  for (let i = 0; i < iterations; i++) {
    fn();
  }
  const end = performance.now();
  return (end - start) / iterations;
}

// Test slow vs fast
const slowTime = benchmark(() => slowFunction(data));
const fastTime = benchmark(() => fastFunction(data));

console.log(`Slow: ${slowTime.toFixed(3)}ms`);
console.log(`Fast: ${fastTime.toFixed(3)}ms`);
console.log(`Speedup: ${(slowTime / fastTime).toFixed(1)}x`);

// jsPerf-style comparison
function compare(fns, iterations = 10000) {
  const results = {};
  
  for (const [name, fn] of Object.entries(fns)) {
    const times = [];
    
    // Warm-up
    for (let i = 0; i < 100; i++) fn();
    
    // Measure
    for (let i = 0; i < 10; i++) {
      const start = performance.now();
      for (let j = 0; j < iterations; j++) fn();
      times.push(performance.now() - start);
    }
    
    results[name] = times.reduce((a, b) => a + b) / times.length;
  }
  
  // Find fastest
  const sorted = Object.entries(results).sort((a, b) => a[1] - b[1]);
  const fastest = sorted[0];
  
  console.log('Results:');
  for (const [name, time] of sorted) {
    const relative = time / fastest[1];
    console.log(`  ${name}: ${time.toFixed(2)}ms (${relative.toFixed(2)}x)`);
  }
}

compare({
  'Array.push': () => {
    const arr = [];
    for (let i = 0; i < 100; i++) arr.push(i);
  },
  'Array[i]': () => {
    const arr = new Array(100);
    for (let i = 0; i < 100; i++) arr[i] = i;
  },
  'Array.from': () => {
    const arr = Array.from({ length: 100 }, (_, i) => i);
  }
});
```

**Best practices:**
- Measure before and after optimization
- Run multiple iterations for accuracy
- Test with realistic data sizes
- Use statistical analysis (mean, median, std dev)

**Related:** PROFILE-FIRST

---

#### REAL-USER-MONITORING: Monitor Production Performance

**Impact:** Low (monitoring)

**RUM implementation:**
```javascript
// Google Analytics with Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics({ name, delta, id }) {
  gtag('event', name, {
    event_category: 'Web Vitals',
    value: Math.round(name === 'CLS' ? delta * 1000 : delta),
    event_label: id,
    non_interaction: true,
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);

// Performance Observer
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.entryType === 'navigation') {
      console.log('DNS:', entry.domainLookupEnd - entry.domainLookupStart);
      console.log('TCP:', entry.connectEnd - entry.connectStart);
      console.log('TTFB:', entry.responseStart - entry.requestStart);
      console.log('Download:', entry.responseEnd - entry.responseStart);
      console.log('DOM Interactive:', entry.domInteractive - entry.fetchStart);
      console.log('DOM Complete:', entry.domComplete - entry.fetchStart);
      console.log('Load Complete:', entry.loadEventEnd - entry.fetchStart);
      
      // Send to analytics
      sendToAnalytics('navigation', entry);
    }
  }
});

observer.observe({ entryTypes: ['navigation'] });

// Long tasks monitoring
const longTaskObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.warn('Long task detected:', entry.duration, 'ms');
    // Send to error tracking (Sentry, etc.)
  }
});

longTaskObserver.observe({ entryTypes: ['longtask'] });

// SaaS RUM tools:
// - Datadog RUM
// - New Relic Browser
// - SpeedCurve
// - Calibre
// - DebugBear
```

**Best practices:**
- Monitor Web Vitals in production
- Set up alerts for performance regressions
- Track performance by geography, device, browser
- Monitor long tasks and jank

**Related:** PROFILE-FIRST, WEB-VITALS

---

#### PERFORMANCE-BUDGET: Set Performance Budgets

**Impact:** Low (process, not optimization)

**Budget configuration:**
```javascript
// Lighthouse CI
// lighthouserc.json
{
  "ci": {
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["error", { "maxNumericValue": 300 }],
        "interactive": ["error", { "maxNumericValue": 3500 }]
      }
    }
  }
}

// Bundlesize budgets
// package.json
{
  "bundlesize": [
    {
      "path": "./dist/main.*.js",
      "maxSize": "200 kB"
    },
    {
      "path": "./dist/vendor.*.js",
      "maxSize": "500 kB"
    },
    {
      "path": "./dist/*.css",
      "maxSize": "50 kB"
    }
  ]
}

// Webpack performance hints
// webpack.config.js
module.exports = {
  performance: {
    maxAssetSize: 250000, // 250 KB
    maxEntrypointSize: 250000,
    hints: 'error'
  }
};

// Next.js bundle analysis
// next.config.js
module.exports = {
  // Errors if page bundle > 128 KB
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
  },
  // Custom size limits
  experimental: {
    modern: true,
    granularChunks: true,
  }
};
```

**Best practices:**
- Set budgets based on user needs (connection speed)
- Monitor in CI/CD
- Fail builds that exceed budgets
- Review budgets quarterly

**Related:** BUNDLE-ANALYSIS, LIGHTHOUSE

---

#### LIGHTHOUSE-CI: Automate Performance Testing

**Impact:** Low (automation)

**CI setup:**
```yaml
# GitHub Actions
name: Lighthouse CI
on: [push]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm run build
      - run: npm install -g @lhci/cli
      - run: lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

**Best practices:**
- Run Lighthouse in CI on every PR
- Compare performance vs main branch
- Block PRs that regress performance
- Track performance over time

**Related:** PERFORMANCE-BUDGET

---

## Expected Good Patterns (Check for Absence)

> **Sources:** [web.dev V8 Performance Tips](https://web.dev/articles/speed-v8), [Node.js Event Loop Guide](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop), [React memo docs](https://react.dev/reference/react/memo), [MDN Performance](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/JavaScript)

This section identifies the **absence of good patterns** (not just presence of anti-patterns). Use `MISSING-*` IDs for tracking.

### 1. Profiling & Measurement Patterns

**Mnemonic:** **"MEASURE-BEFORE-OPTIMIZE"**

| Expected Pattern | If Missing |
|------------------|------------|
| Performance profiling before optimization | 🔴 `MISSING-PROFILE-FIRST` - Optimizing without data |
| Lighthouse/DevTools measurements | ⚠️ `MISSING-MEASURE-BASELINE` - No baseline for comparison |
| Production monitoring (RUM) | ⚠️ `MISSING-RUM` - No real-world performance data |
| Performance budgets | 💡 `MISSING-PERF-BUDGET` - No guardrails against regression |

```javascript
// PRESENT: Profiling-guided optimization
// 1. Run lighthouse before changes
// npx lighthouse http://localhost:3000 --output json > baseline.json

// 2. Add console timing for suspect code
console.time('dataProcessing');
const result = processLargeDataset(data);
console.timeEnd('dataProcessing');
// → "dataProcessing: 1234.56ms"

// 3. Use Performance API for precise measurement
const start = performance.now();
await heavyOperation();
const duration = performance.now() - start;
console.log(`Operation took ${duration.toFixed(2)}ms`);

// 4. Profile in React DevTools for render times
// React.Profiler wrapper for component timing

// MISSING: Optimizing based on gut feeling
function processData(items) {
  // "I think this is slow, let me optimize..."
  // No measurements, no profiling, just guessing!
}
```

### 2. V8 Engine Optimization Patterns

**Mnemonic:** **"HIDDEN-CLASSES-MATTER"** (Initialize consistent object shapes)

| Expected Pattern | If Missing |
|------------------|------------|
| Consistent object shapes (same properties, same order) | 🔴 `MISSING-HIDDEN-CLASS` - V8 deoptimization |
| Monomorphic function calls (same argument types) | ⚠️ `MISSING-MONOMORPHIC` - Inline cache misses |
| Properties initialized in constructor | ⚠️ `MISSING-CTOR-INIT` - Hidden class transitions |
| Avoid property deletion (`delete obj.prop`) | 💡 `MISSING-NO-DELETE` - Forces slow mode |

```javascript
// PRESENT: V8-friendly object construction
class User {
  constructor(name, age, email) {
    // Always initialize ALL properties in constructor
    // Always in the SAME ORDER
    this.name = name;
    this.age = age;
    this.email = email;
    this.role = null;        // Initialize even if null
    this.lastLogin = null;   // Consistent shape
  }
}

// All instances share same hidden class = optimized
const user1 = new User('Alice', 30, 'alice@example.com');
const user2 = new User('Bob', 25, 'bob@example.com');

// MISSING: V8 deoptimization traps
function createUser(name) {
  const user = { name }; // Only name
  if (Math.random() > 0.5) {
    user.age = 30;       // Sometimes age - different hidden class!
  }
  user.email = 'a@b.com'; // Added later - another hidden class!
  return user;
}

// Different argument types = polymorphic = slow
function add(a, b) { return a + b; }
add(1, 2);       // Numbers - optimized
add('a', 'b');   // Strings - deoptimized! Now polymorphic.

// Property deletion forces slow mode
delete user.role;  // BAD: Forces dictionary mode
user.role = null;  // GOOD: Preserves hidden class
```

### 3. Event Loop Protection (Node.js)

**Mnemonic:** **"NEVER-BLOCK-THE-LOOP"**

| Expected Pattern | If Missing |
|------------------|------------|
| Async file/crypto/compression APIs | 🔴 `MISSING-ASYNC-IO` - Blocks event loop |
| Partitioned long computations | 🔴 `MISSING-PARTITION` - Starves other requests |
| `setImmediate`/`setTimeout` for chunking | ⚠️ `MISSING-YIELD-LOOP` - No yielding to event loop |
| Web Workers / worker_threads for CPU work | ⚠️ `MISSING-WORKER-OFFLOAD` - CPU blocks main thread |
| Safe regex (no nested quantifiers) | 🔴 `MISSING-SAFE-REGEX` - ReDoS vulnerability |

```javascript
// PRESENT: Non-blocking file operations
import { readFile } from 'fs/promises';

async function loadConfig() {
  const data = await readFile('config.json', 'utf8');
  return JSON.parse(data);
}

// PRESENT: Partitioned computation with setImmediate
function processLargeArray(items, callback) {
  const results = [];
  let index = 0;

  function processChunk() {
    const chunkEnd = Math.min(index + 1000, items.length);

    while (index < chunkEnd) {
      results.push(expensiveOperation(items[index]));
      index++;
    }

    if (index < items.length) {
      // Yield to event loop, then continue
      setImmediate(processChunk);
    } else {
      callback(results);
    }
  }

  processChunk();
}

// PRESENT: Worker thread for CPU-intensive work
import { Worker } from 'worker_threads';

function runHeavyTask(data) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./heavy-task.js', { workerData: data });
    worker.on('message', resolve);
    worker.on('error', reject);
  });
}

// MISSING: Blocking synchronous operations
import { readFileSync } from 'fs';

function loadConfigBlocking() {
  // BLOCKS entire event loop while reading!
  const data = readFileSync('config.json', 'utf8');
  return JSON.parse(data);
}

// MISSING: Unpartitioned heavy computation
function processAllItems(items) {
  // Blocks for SECONDS with large arrays!
  return items.map(item => veryExpensiveOperation(item));
}

// MISSING: Vulnerable regex (ReDoS)
const VULNERABLE_REGEX = /(\w+)+$/;  // Nested quantifiers!
// Input: "aaaaaaaaaaaaaaaaaaaaaaaaaaaa!" takes SECONDS
```

### 4. React Memoization Patterns

**Mnemonic:** **"MEMO-WHERE-MEASURED"** (Not premature, but where profiled)

| Expected Pattern | If Missing |
|------------------|------------|
| `React.memo()` for expensive child components | ⚠️ `MISSING-MEMO-COMPONENT` - Unnecessary re-renders |
| `useMemo` for expensive calculations | ⚠️ `MISSING-USEMEMO` - Recalculates every render |
| `useCallback` for callbacks passed to memoized children | ⚠️ `MISSING-USECALLBACK` - Breaks child memoization |
| Stable object/array references in deps | 🔴 `MISSING-STABLE-REFS` - Always re-renders |

```javascript
// PRESENT: Proper React memoization
import { memo, useMemo, useCallback } from 'react';

// Memoized expensive child
const ExpensiveList = memo(function ExpensiveList({ items, onItemClick }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id} onClick={() => onItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
});

function Parent({ data }) {
  // useMemo for expensive computation
  const processedItems = useMemo(() => {
    return data.map(item => ({
      ...item,
      displayName: computeExpensiveDisplayName(item)
    }));
  }, [data]);

  // useCallback to maintain stable reference for memoized child
  const handleItemClick = useCallback((id) => {
    console.log('Clicked:', id);
  }, []); // Stable reference

  return <ExpensiveList items={processedItems} onItemClick={handleItemClick} />;
}

// MISSING: Broken memoization
function Parent({ data }) {
  // Creates new array every render - processedItems always different!
  const processedItems = data.map(item => ({ ...item }));

  // Creates new function every render - child always re-renders!
  const handleClick = (id) => console.log(id);

  // ExpensiveList re-renders EVERY TIME even with React.memo!
  return <ExpensiveList items={processedItems} onItemClick={handleClick} />;
}

// MISSING: Object literals in JSX props
function Parent() {
  return (
    // New object reference every render!
    <Child style={{ color: 'red' }} />  // BAD
    <Child data={{ id: 1 }} />          // BAD
  );
}

// PRESENT: Stable object references
const RED_STYLE = { color: 'red' };

function Parent() {
  return <Child style={RED_STYLE} />;  // Stable reference
}
```

### 5. Async & Promise Patterns

**Mnemonic:** **"PARALLEL-NOT-SERIAL"**

| Expected Pattern | If Missing |
|------------------|------------|
| `Promise.all()` for independent async ops | 🔴 `MISSING-PARALLEL-ASYNC` - Serial when could be parallel |
| `Promise.allSettled()` when some failures OK | ⚠️ `MISSING-ALLSETTLED` - All-or-nothing when partial OK |
| Abort controllers for cancellation | ⚠️ `MISSING-ABORT-CONTROLLER` - Wasted resources |
| Error boundaries for promise chains | 💡 `MISSING-ASYNC-ERROR` - Silent failures |

```javascript
// PRESENT: Parallel independent operations
async function loadDashboard(userId) {
  // Run ALL independent fetches in parallel
  const [user, orders, recommendations] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchRecommendations(userId)
  ]);

  return { user, orders, recommendations };
}
// Total time: max(userTime, ordersTime, recommendationsTime)

// PRESENT: Partial success with allSettled
async function loadOptionalData(ids) {
  const results = await Promise.allSettled(
    ids.map(id => fetchData(id))
  );

  return results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);
}

// PRESENT: Cancellable fetch
async function searchWithCancel(query, signal) {
  const response = await fetch(`/api/search?q=${query}`, { signal });
  return response.json();
}

// In component:
useEffect(() => {
  const controller = new AbortController();
  searchWithCancel(query, controller.signal).then(setResults);

  return () => controller.abort(); // Cancel on cleanup
}, [query]);

// MISSING: Sequential when could be parallel
async function loadDashboardSlow(userId) {
  // Each waits for previous - SLOW!
  const user = await fetchUser(userId);           // 200ms
  const orders = await fetchOrders(userId);       // 300ms
  const recommendations = await fetchRecommendations(userId); // 150ms

  return { user, orders, recommendations };
}
// Total time: 200 + 300 + 150 = 650ms (should be 300ms!)
```

### 6. DOM & Rendering Patterns

**Mnemonic:** **"BATCH-READS-WRITES"**

| Expected Pattern | If Missing |
|------------------|------------|
| Batched DOM reads, then writes | 🔴 `MISSING-DOM-BATCH` - Layout thrashing |
| DocumentFragment for multiple insertions | ⚠️ `MISSING-FRAGMENT` - Multiple reflows |
| `requestAnimationFrame` for visual updates | ⚠️ `MISSING-RAF` - Janky animations |
| Passive event listeners for scroll/touch | ⚠️ `MISSING-PASSIVE-LISTENER` - Scroll jank |
| Virtual scrolling for long lists | 🔴 `MISSING-VIRTUAL-SCROLL` - Thousands of DOM nodes |

```javascript
// PRESENT: Batched DOM operations
function updateElements(elements, newData) {
  // BATCH 1: Read all measurements first
  const measurements = elements.map(el => ({
    width: el.offsetWidth,
    height: el.offsetHeight
  }));

  // BATCH 2: Then write all changes
  elements.forEach((el, i) => {
    el.style.transform = `scale(${newData[i].scale})`;
  });
}

// PRESENT: DocumentFragment for insertions
function addManyItems(container, items) {
  const fragment = document.createDocumentFragment();

  items.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item.name;
    fragment.appendChild(li);
  });

  container.appendChild(fragment); // Single reflow!
}

// PRESENT: requestAnimationFrame for animations
function smoothScroll(element, target) {
  const start = element.scrollTop;
  const distance = target - start;
  let startTime = null;

  function step(currentTime) {
    if (!startTime) startTime = currentTime;
    const progress = Math.min((currentTime - startTime) / 500, 1);

    element.scrollTop = start + distance * easeOutCubic(progress);

    if (progress < 1) {
      requestAnimationFrame(step);
    }
  }

  requestAnimationFrame(step);
}

// PRESENT: Passive event listener
window.addEventListener('scroll', handleScroll, { passive: true });
window.addEventListener('touchstart', handleTouch, { passive: true });

// MISSING: Layout thrashing
function thrashingUpdate(elements) {
  elements.forEach(el => {
    // Read-write-read-write interleaved = LAYOUT THRASH!
    const width = el.offsetWidth;    // Forces layout
    el.style.width = width + 10 + 'px';  // Invalidates layout
    const height = el.offsetHeight;  // Forces layout AGAIN!
    el.style.height = height + 10 + 'px';  // Invalidates AGAIN!
  });
}
```

### 7. Bundle & Loading Patterns

**Mnemonic:** **"SPLIT-LAZY-COMPRESS"**

| Expected Pattern | If Missing |
|------------------|------------|
| Code splitting by route | ⚠️ `MISSING-CODE-SPLIT` - Loads everything upfront |
| Dynamic imports for heavy features | ⚠️ `MISSING-DYNAMIC-IMPORT` - Blocks initial load |
| Tree shaking enabled | ⚠️ `MISSING-TREE-SHAKE` - Dead code in bundle |
| Gzip/Brotli compression | 🔴 `MISSING-COMPRESSION` - 60-80% larger transfers |
| Preload/prefetch hints | 💡 `MISSING-RESOURCE-HINTS` - Suboptimal loading |

```javascript
// PRESENT: Route-based code splitting (React)
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));
const Analytics = lazy(() => import('./Analytics'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </Suspense>
  );
}

// PRESENT: Dynamic import for heavy feature
async function loadChartLibrary() {
  const { Chart } = await import('chart.js');
  return Chart;
}

// Only load Chart.js when user needs charts
button.addEventListener('click', async () => {
  const Chart = await loadChartLibrary();
  new Chart(canvas, config);
});

// PRESENT: Resource hints in HTML
// <link rel="preload" href="/fonts/main.woff2" as="font" crossorigin>
// <link rel="prefetch" href="/js/dashboard.js">
// <link rel="preconnect" href="https://api.example.com">

// MISSING: Single monolithic bundle
import Dashboard from './Dashboard';
import Settings from './Settings';
import Analytics from './Analytics';
import HugeChartLibrary from 'huge-chart-library';
import MassiveDataGrid from 'massive-data-grid';
// Everything loaded upfront, even if user never uses it!
```

### 8. Data Structure Selection

**Mnemonic:** **"RIGHT-STRUCTURE-FOR-JOB"**

| Expected Pattern | If Missing |
|------------------|------------|
| `Set` for unique value collections | ⚠️ `MISSING-SET-USAGE` - O(n) uniqueness checks |
| `Map` for key-value lookups | ⚠️ `MISSING-MAP-USAGE` - O(n) array finds |
| Object literals for small, static lookups | 💡 `MISSING-OBJECT-LOOKUP` - Overhead for simple cases |
| Typed arrays for numeric data | 💡 `MISSING-TYPED-ARRAY` - Slower numeric operations |

```javascript
// PRESENT: Set for unique values
const uniqueTags = new Set();

function addTag(tag) {
  uniqueTags.add(tag);  // O(1) - handles duplicates automatically
}

function hasTag(tag) {
  return uniqueTags.has(tag);  // O(1) lookup
}

// PRESENT: Map for key-value lookups
const usersById = new Map();

function addUser(user) {
  usersById.set(user.id, user);  // O(1)
}

function getUser(id) {
  return usersById.get(id);  // O(1) lookup
}

// PRESENT: Object for small static lookups
const HTTP_STATUS = {
  OK: 200,
  NOT_FOUND: 404,
  SERVER_ERROR: 500
};

// PRESENT: Typed array for numeric processing
const audioData = new Float32Array(44100);
const pixelData = new Uint8ClampedArray(width * height * 4);

// MISSING: Array for uniqueness (O(n))
const tags = [];

function addTagSlow(tag) {
  if (!tags.includes(tag)) {  // O(n) check!
    tags.push(tag);
  }
}

// MISSING: Array for lookups (O(n))
const users = [];

function getUserSlow(id) {
  return users.find(u => u.id === id);  // O(n) scan!
}
```

---

### Expected Patterns Summary Checklist

**When Reviewing, Verify Presence Of:**

🔴 **Critical (causes major performance issues if missing):**
- [ ] `MISSING-PROFILE-FIRST` - No profiling before optimization
- [ ] `MISSING-HIDDEN-CLASS` - Inconsistent object shapes
- [ ] `MISSING-ASYNC-IO` - Sync file/crypto in Node.js
- [ ] `MISSING-PARTITION` - Unpartitioned heavy computation
- [ ] `MISSING-SAFE-REGEX` - Vulnerable regex patterns
- [ ] `MISSING-PARALLEL-ASYNC` - Serial awaits for independent ops
- [ ] `MISSING-DOM-BATCH` - Interleaved DOM reads/writes
- [ ] `MISSING-VIRTUAL-SCROLL` - Thousands of DOM nodes
- [ ] `MISSING-COMPRESSION` - No Gzip/Brotli

⚠️ **Warning (significant impact):**
- [ ] `MISSING-MONOMORPHIC` - Polymorphic function calls
- [ ] `MISSING-CTOR-INIT` - Properties added after construction
- [ ] `MISSING-YIELD-LOOP` - No yielding in long loops
- [ ] `MISSING-WORKER-OFFLOAD` - CPU work on main thread
- [ ] `MISSING-MEMO-COMPONENT` - Expensive components not memoized
- [ ] `MISSING-USEMEMO` - Expensive calculations every render
- [ ] `MISSING-USECALLBACK` - Callbacks breaking child memo
- [ ] `MISSING-STABLE-REFS` - New objects/arrays in render
- [ ] `MISSING-ALLSETTLED` - Promise.all when partial OK
- [ ] `MISSING-ABORT-CONTROLLER` - No fetch cancellation
- [ ] `MISSING-FRAGMENT` - Multiple DOM insertions
- [ ] `MISSING-RAF` - JS animations without RAF
- [ ] `MISSING-PASSIVE-LISTENER` - Non-passive scroll/touch
- [ ] `MISSING-CODE-SPLIT` - Monolithic bundles
- [ ] `MISSING-DYNAMIC-IMPORT` - Heavy libs loaded upfront
- [ ] `MISSING-TREE-SHAKE` - Dead code in bundle
- [ ] `MISSING-SET-USAGE` - Arrays for uniqueness
- [ ] `MISSING-MAP-USAGE` - Arrays for lookups

💡 **Recommendation (good practice):**
- [ ] `MISSING-MEASURE-BASELINE` - No baseline metrics
- [ ] `MISSING-RUM` - No production monitoring
- [ ] `MISSING-PERF-BUDGET` - No performance budgets
- [ ] `MISSING-NO-DELETE` - Property deletion in hot paths
- [ ] `MISSING-ASYNC-ERROR` - Silent async failures
- [ ] `MISSING-RESOURCE-HINTS` - No preload/prefetch
- [ ] `MISSING-OBJECT-LOOKUP` - Map for tiny static lookups
- [ ] `MISSING-TYPED-ARRAY` - Regular arrays for numeric data

---

## Performance Wisdom

> **"Premature optimization is the root of all evil."** - Donald Knuth

> **"Make it work, make it right, make it fast."** - Kent Beck

> **"Measure, don't guess."** - Performance Engineering Principle

### The Performance Optimization Process

1. **Profile First** - Use Chrome DevTools, Lighthouse
2. **Identify Bottlenecks** - Find the 20% causing 80% slowness
3. **Optimize** - Apply appropriate guideline
4. **Measure Again** - Verify improvement
5. **Repeat** - Until performance is acceptable

### When to Optimize

✅ **DO optimize when:**
- You've profiled and identified real bottlenecks
- Performance impacts user experience
- You have clear performance requirements
- The optimization is simple and maintains readability

❌ **DON'T optimize when:**
- You haven't measured (guessing)
- Code is fast enough for requirements
- Optimization hurts readability significantly
- You're in early development (premature)

---

## Quick Reference

### By Performance Impact

**Critical (10-1000x speedup):**
- ALGO-COMPLEX - O(n²) → O(n)
- NESTED-LOOP - O(n × m) → O(n + m)
- LAYOUT-THRASH - Batch read/writes
- VIRTUAL-SCROLL - Render only visible items
- MEMORY-LEAK - Fix leaks

**High (2-10x speedup):**
- DATA-STRUCTURE - Array → Set/Map
- CACHE-RESULT - Memoize expensive calls
- DEBOUNCE-THROTTLE - Reduce event frequency
- DOM-BATCH - Batch DOM updates
- PROMISE-PARALLEL - Parallel async ops
- WEB-WORKERS - Offload heavy computation
- LAZY-LOAD - Lazy load routes/features
- CODE-SPLIT - Split bundles
- COMPRESSION - Enable gzip/Brotli
- KEY-OPTIMIZATION - Stable list keys
- CONTEXT-SPLIT - Split React contexts

**Medium (1.5-2x speedup):**
- ARRAY-METHODS - Use appropriate methods
- ARRAY-CHAIN - Reduce array passes
- SPREAD-CLONE - Avoid excessive spreading
- EVENT-PASSIVE - Passive scroll listeners
- CSS-CHANGES - CSS animations over JS
- TREE-SHAKE - Remove unused code
- MEMO-COMPONENT - Memoize React components
- STATE-COLOCATION - Move state closer

**Low (1.1-1.5x speedup):**
- OBJECT-LITERAL - Objects for small lookups
- EARLY-EXIT - Return early
- REDUNDANT-CALC - Hoist loop-invariant code

### Node.js Runtime & Streams

#### EVENT-LOOP-BLOCK
- Identify synchronous hotspots (`fs.readFileSync`, crypto loops) with `clinic flame` or `node --prof`.
- Move CPU-bound work to `worker_threads` pools (Piscina, workerpool) or external services.

#### WORKER-THREAD
- Reuse workers to avoid startup cost, pass data via `Transferable` objects for large buffers.
- Guard with health checks so stuck workers get replaced.

#### STREAM-BACKPRESSURE
- Prefer `stream.pipeline` / `Readable.fromWeb` / `AsyncGenerator` to automatically manage backpressure.
- Avoid manual `data` listeners that ignore `stream.pause()`—they cause OOM when producers outpace consumers.

#### CLUSTER-STRATEGY
- Use process managers (PM2, systemd, Kubernetes) to spawn one worker per vCPU.
- Ensure sticky sessions (ingress affinity, `socket.io-redis`) for WebSockets or stateful protocols.

#### KEEPALIVE-TUNING
- Configure HTTP/HTTPS agents with `keepAlive: true`, `maxSockets`, `maxFreeSockets`.
- Adjust `server.keepAliveTimeout`/`headersTimeout` to prevent slowloris attacks while keeping sockets reusable.

#### OBSERVE-EVENTLOOP
- Monitor event-loop lag via `perf_hooks.monitorEventLoopDelay()` and export metrics (Prometheus, StatsD).
- Alert when p95 lag exceeds ~100ms; it signals blocking synchronous work.

### By Use Case

**Slow Algorithms:**
ALGO-COMPLEX, NESTED-LOOP, LINEAR-SEARCH, CACHE-RESULT

**Data Structure:**
DATA-STRUCTURE, OBJECT-LITERAL, ARRAY-METHODS, WEAK-MAP

**Memory:**
MEMORY-LEAK, CLOSURE-SCOPE, LAZY-INIT, GC-FRIENDLY, DETACHED-DOM

**DOM:**
DOM-BATCH, LAYOUT-THRASH, VIRTUAL-SCROLL, EVENT-DELEGATE

**Async:**
PROMISE-PARALLEL, WEB-WORKERS, LAZY-LOAD, ABORT-REQUESTS

**Bundling:**
CODE-SPLIT, TREE-SHAKE, COMPRESSION, CDN-ASSETS

**React:**
MEMO-COMPONENT, KEY-OPTIMIZATION, STATE-COLOCATION, CONTEXT-SPLIT

---

**Remember: Profile first, optimize what matters, measure improvement.**
