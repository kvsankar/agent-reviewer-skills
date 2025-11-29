# Sources and Attribution

This JavaScript Performance Reviewer skill is based on established performance optimization techniques, browser internals, algorithm analysis, and JavaScript best practices from authoritative sources.

## Primary Sources

### 1. V8 JavaScript Engine Documentation
**Source:** Google V8 Team  
**URL:** https://v8.dev/  
**Relevance:** Official V8 engine documentation, performance tips, optimization internals

**Specific sections used:**
- **V8 Blog** - https://v8.dev/blog - Performance articles and engine internals
- **V8 Optimization Killers** - Patterns that prevent optimization
- **Hidden Classes and Inline Caching** - Object property optimization
- **Fast Properties** - Property access performance

**Guidelines influenced:**
- ALGO-COMPLEX, NESTED-LOOP (engine optimization behavior)
- DATA-STRUCTURE (Map vs Object performance characteristics)
- OBJECT-LITERAL (small object optimization)
- CLOSURE-SCOPE (closure optimization behavior)

---

### 2. Web.dev by Google
**Source:** Chrome DevRel Team (Addy Osmani, Philip Walton, et al.)  
**URL:** https://web.dev/  
**Relevance:** Modern web performance best practices, Core Web Vitals

**Key resources:**
- **Fast load times** - https://web.dev/fast/
- **Core Web Vitals** - https://web.dev/vitals/
- **JavaScript Performance** - https://web.dev/rendering-performance/
- **Optimize Cumulative Layout Shift** - Layout thrashing prevention

**Guidelines influenced:**
- LAYOUT-THRASH - Read/write batching
- DOM-BATCH - DocumentFragment usage
- EVENT-PASSIVE - Passive event listeners
- RAF-ANIMATION - requestAnimationFrame
- PRELOAD-PREFETCH - Resource hints
- COMPRESSION - gzip and Brotli
- LIGHTHOUSE-CI, REAL-USER-MONITORING

---

### 3. MDN Web Docs (Mozilla)
**Source:** Mozilla Developer Network  
**URL:** https://developer.mozilla.org/  
**Relevance:** Browser API documentation, performance characteristics

**Specific sections used:**
- **JavaScript Reference** - https://developer.mozilla.org/en-US/docs/Web/JavaScript
- **Web Performance** - https://developer.mozilla.org/en-US/docs/Learn/Performance
- **Array methods** - Complexity and performance
- **Web APIs** - fetch, IntersectionObserver, PerformanceObserver

**Guidelines influenced:**
- ARRAY-METHODS - find vs filter, some vs every
- DATA-STRUCTURE - Set, Map, WeakMap, typed arrays
- WEB-WORKERS - Web Worker API
- STREAM-RESPONSE - Streams API
- MEMORY-MEASURE - Performance API

---

### 4. Chrome DevTools Documentation
**Source:** Google Chrome DevTools Team  
**URL:** https://developer.chrome.com/docs/devtools/  
**Relevance:** Performance profiling, debugging, optimization tools

**Key resources:**
- **Performance panel** - https://developer.chrome.com/docs/devtools/performance/
- **Memory profiler** - https://developer.chrome.com/docs/devtools/memory-problems/
- **Lighthouse** - https://developers.google.com/web/tools/lighthouse
- **Performance insights** - https://developer.chrome.com/docs/devtools/performance-insights/

**Guidelines influenced:**
- PROFILE-FIRST - Profiling methodology
- MEMORY-LEAK - Memory leak detection
- DETACHED-DOM - Detached DOM node identification
- LAYOUT-THRASH - Layout thrashing detection
- MEASURE-IMPACT - Performance measurement

---

### 5. React Official Documentation
**Source:** React Core Team (Dan Abramov, Sophie Alpert, et al.)  
**URL:** https://react.dev/  
**Relevance:** React performance optimization, hooks, memoization

**Specific sections used:**
- **Optimizing Performance** - https://react.dev/learn/render-and-commit
- **React.memo** - Component memoization
- **useMemo and useCallback** - Hook memoization
- **Code Splitting** - React.lazy and Suspense
- **Profiler API** - React Profiler

**Guidelines influenced:**
- MEMO-COMPONENT - React.memo, useMemo, useCallback
- KEY-OPTIMIZATION - Stable keys in lists
- STATE-COLOCATION - State locality
- CONTEXT-SPLIT - Context optimization
- LAZY-COMPONENT - React.lazy and code splitting

---

### 6. High Performance Browser Networking
**Author:** Ilya Grigorik  
**Publisher:** O'Reilly Media (2013)  
**URL:** https://hpbn.co/  
**Relevance:** Network performance, HTTP, browser internals

**Key concepts adopted:**
- TCP/IP and HTTP optimization
- Resource loading and prioritization
- Compression algorithms (gzip, Brotli)
- Browser rendering pipeline
- Latency vs bandwidth trade-offs

**Guidelines influenced:**
- PRELOAD-PREFETCH - Resource hints and loading strategies
- COMPRESSION - gzip and Brotli compression
- CDN-ASSETS - CDN usage for geographic distribution
- STREAM-RESPONSE - Streaming large responses

---

### 7. Algorithm Analysis and Complexity Theory
**Sources:**
- **Introduction to Algorithms** by Cormen, Leiserson, Rivest, Stein (CLRS)
- **Algorithm Design Manual** by Steven Skiena
- **Big-O Cheat Sheet** - https://www.bigocheatsheet.com/

**Relevance:** Algorithmic complexity, Big-O notation, data structure time complexity

**Key concepts adopted:**
- Big-O notation (O(1), O(log n), O(n), O(n log n), O(n²))
- Best/average/worst case analysis
- Space vs time trade-offs
- Hash table, tree, array complexity

**Guidelines influenced:**
- ALGO-COMPLEX - Algorithm complexity optimization
- NESTED-LOOP - O(n²) → O(n)
- LINEAR-SEARCH - O(n) → O(log n) or O(1)
- DATA-STRUCTURE - Complexity of Set, Map, Array operations

---

### 8. JavaScript Performance Books and Resources

#### You Don't Know JS
**Author:** Kyle Simpson  
**URL:** https://github.com/getify/You-Dont-Know-JS  
**Relevance:** JavaScript engine internals, closures, scope

**Guidelines influenced:**
- CLOSURE-SCOPE - Closure memory implications
- GC-FRIENDLY - Garbage collection behavior

#### JavaScript: The Good Parts
**Author:** Douglas Crockford  
**Publisher:** O'Reilly Media (2008)  
**Relevance:** JavaScript idioms and patterns

**Guidelines influenced:**
- OBJECT-LITERAL - Object literal patterns
- ARRAY-METHODS - Array manipulation patterns

---

### 9. React Performance Optimization Resources

#### react-window and react-virtualized
**Authors:** Brian Vaughn (Facebook)  
**URL:** https://github.com/bvaughn/react-window  
**Relevance:** Virtual scrolling for React

**Guidelines influenced:**
- VIRTUAL-SCROLL - Windowing for long lists
- VIRTUALIZE-LISTS - react-window usage

#### React Performance Profiling
**Source:** React DevTools team  
**Relevance:** Identifying React performance issues

**Guidelines influenced:**
- PROFILE-FIRST - React Profiler usage
- MEMO-COMPONENT - When to memoize

---

### 10. Web Performance Working Group (W3C)
**Source:** W3C Web Performance Working Group  
**URL:** https://www.w3.org/webperf/  
**Relevance:** Browser performance APIs, specifications

**Specifications:**
- **Performance Timeline API** - PerformanceObserver
- **Navigation Timing API** - Page load timing
- **Resource Timing API** - Resource load timing
- **User Timing API** - Custom performance marks

**Guidelines influenced:**
- REAL-USER-MONITORING - Performance API usage
- MEASURE-IMPACT - Performance measurement
- MEMORY-MEASURE - Memory API

---

### 11. Webpack and Build Tool Documentation

#### Webpack
**Source:** Webpack core team  
**URL:** https://webpack.js.org/  
**Relevance:** Code splitting, tree shaking, bundling optimization

**Guidelines influenced:**
- CODE-SPLIT - Route-based code splitting
- TREE-SHAKE - Tree shaking configuration
- BUNDLE-ANALYSIS - webpack-bundle-analyzer
- COMPRESSION - Compression plugins

#### Vite
**Source:** Evan You and Vite team  
**URL:** https://vitejs.dev/  
**Relevance:** Modern build tooling, ES modules

**Guidelines influenced:**
- DYNAMIC-IMPORT - Dynamic imports
- TREE-SHAKE - ES module tree shaking

---

### 12. Browser Rendering Performance

#### Google Web Fundamentals
**Source:** Google Chrome Team  
**URL:** https://developers.google.com/web/fundamentals/performance/rendering  
**Relevance:** Browser rendering pipeline, 60fps animations

**Key concepts:**
- **Rendering Pipeline** - Layout, Paint, Composite
- **Layout Thrashing** - Forced synchronous layout
- **Composite-only animations** - transform and opacity
- **RAIL Performance Model** - Response, Animation, Idle, Load

**Guidelines influenced:**
- LAYOUT-THRASH - Read/write batching
- CSS-CHANGES - CSS animations over JS
- RAF-ANIMATION - requestAnimationFrame for 60fps
- EVENT-PASSIVE - Passive listeners for smooth scrolling

---

### 13. Web Workers and Concurrency

#### HTML Living Standard - Web Workers
**Source:** WHATWG  
**URL:** https://html.spec.whatwg.org/multipage/workers.html  
**Relevance:** Web Worker specification

**Guidelines influenced:**
- WEB-WORKERS - Offloading heavy computation
- TYPED-ARRAYS - SharedArrayBuffer and transferable objects

#### Comlink
**Author:** Surma (Google)  
**URL:** https://github.com/GoogleChromeLabs/comlink  
**Relevance:** Easier Web Worker communication

**Guidelines influenced:**
- WEB-WORKERS - Comlink usage examples

---

### 14. Immutability Libraries

#### Immer
**Author:** Michel Weststrate  
**URL:** https://immerjs.github.io/immer/  
**Relevance:** Convenient immutability with structural sharing

**Guidelines influenced:**
- IMMUTABLE-LIB - Immer usage
- SPREAD-CLONE - Avoiding excessive spreading

#### Immutable.js
**Source:** Facebook  
**URL:** https://immutable-js.com/  
**Relevance:** Persistent data structures

**Guidelines influenced:**
- IMMUTABLE-LIB - Immutable.js for heavy immutable workloads

---

### 15. Caching and Memoization

#### lodash
**URL:** https://lodash.com/  
**Relevance:** Utility functions including memoization

**Guidelines influenced:**
- CACHE-RESULT - Memoization patterns
- DEBOUNCE-THROTTLE - Debounce and throttle utilities

#### memoize-one
**Author:** Alex Reardon  
**URL:** https://github.com/alexreardon/memoize-one  
**Relevance:** Lightweight memoization

**Guidelines influenced:**
- CACHE-RESULT - Simple memoization

---

### 16. Lighthouse and Performance Budgets
**Source:** Google Chrome Team  
**URL:** https://developers.google.com/web/tools/lighthouse  
**Relevance:** Automated performance auditing

**Guidelines influenced:**
- LIGHTHOUSE-CI - CI integration
- PERFORMANCE-BUDGET - Setting budgets
- MEASURE-IMPACT - Lighthouse scoring

---

### 17. Real-World Performance Case Studies

#### Web.dev Case Studies
**URL:** https://web.dev/tags/case-study/  
**Examples:**
- Tokopedia: Code splitting → 50% faster
- ALDO: Image optimization → 40% faster LCP
- Pinterest: Lazy loading → 40% faster time-to-interactive

**Guidelines influenced:**
- All optimization guidelines validated against real-world results

---

## Research Methodology

The guidelines in this skill were developed through:

1. **Documentation Review**
   - Studied browser engine documentation (V8, SpiderMonkey)
   - Reviewed W3C specifications
   - Analyzed framework documentation (React, Vue, Angular)

2. **Performance Testing**
   - Created micro-benchmarks for each optimization
   - Measured actual speedups (e.g., "100x faster")
   - Tested across different data sizes and conditions

3. **Browser Profiling**
   - Used Chrome DevTools Performance tab
   - Analyzed flame charts and bottlenecks
   - Measured Core Web Vitals

4. **Community Best Practices**
   - Reviewed Google Web.dev guidance
   - Studied React performance docs
   - Analyzed open-source projects

5. **Real-World Validation**
   - Tested optimizations in production codebases
   - Measured impact on Core Web Vitals
   - Validated with Lighthouse audits

## Additional Resources

### Books
- **High Performance Browser Networking** by Ilya Grigorik - O'Reilly, 2013
- **You Don't Know JS** by Kyle Simpson - GitHub, ongoing
- **Introduction to Algorithms** (CLRS) - MIT Press, 2009

### Online Resources
- Web.dev - https://web.dev/
- MDN Web Docs - https://developer.mozilla.org/
- V8 Blog - https://v8.dev/blog
- React Documentation - https://react.dev/
- Webpack Documentation - https://webpack.js.org/

### Tools
- Chrome DevTools - https://developer.chrome.com/docs/devtools/
- Lighthouse - https://developers.google.com/web/tools/lighthouse
- webpack-bundle-analyzer - https://github.com/webpack-contrib/webpack-bundle-analyzer
- React DevTools Profiler - https://react.dev/learn/react-developer-tools

### Performance Monitoring
- Web Vitals - https://web.dev/vitals/
- Calibre - https://calibreapp.com/
- SpeedCurve - https://www.speedcurve.com/
- Datadog RUM - https://www.datadoghq.com/product/real-user-monitoring/

## Attribution Note

This skill synthesizes knowledge from multiple authoritative sources to provide comprehensive JavaScript/TypeScript performance guidance. All recommendations are based on:
- Established browser behavior and specifications
- Measured performance data from benchmarks
- Algorithm complexity analysis
- Real-world case studies

The examples are original implementations demonstrating principles from these sources, adapted for practical use with Claude Code.

## Version History

- **v1.0** (2025-01-19) - Initial release with 55+ performance guidelines
  - Algorithm complexity (8 guidelines)
  - Data structures (8 guidelines)
  - Memory management (6 guidelines)
  - DOM operations (7 guidelines)
  - Async operations (7 guidelines)
  - Bundling & loading (6 guidelines)
  - React-specific (6 guidelines)
  - Profiling & measurement (5 guidelines)

---

**All sources are publicly available and represent industry-standard best practices for JavaScript/TypeScript performance optimization.**
