# Sources and Attribution

This skill is built upon the collective wisdom of the JavaScript functional programming community. All guidelines are derived from publicly available resources, documentation, and educational materials.

## Primary Sources

### 1. Eric Elliott - Composing Software Series

**Source:** Medium - "Composing Software" series
**Author:** Eric Elliott
**URL:** https://medium.com/javascript-scene/composing-software-the-book-f31c77fc3ddc

**Key Contributions:**
- Pure function definitions and benefits
- Function composition patterns
- Higher-order functions
- Functors and functional patterns
- "Functional programming is about writing pure functions, removing hidden inputs and outputs"

**Guidelines Derived:**
- PURE-FUNC: Pure Functions Return Same Output for Same Input
- NO-SIDE-EFFECT: Avoid Side Effects in Functions
- COMPOSE-FUNC: Compose Small Functions
- FUNCTOR-MAP: Use Functor Pattern
- HOF-PATTERN: Functions as First-Class Citizens

---

### 2. Kyle Simpson - Functional-Light JavaScript

**Source:** "Functional-Light JavaScript" book
**Author:** Kyle Simpson (@getify)
**URL:** https://github.com/getify/Functional-Light-JS

**Key Contributions:**
- Pragmatic approach to FP in JavaScript
- Function purity and side effects
- Closure patterns
- Currying and partial application
- Point-free style
- Recursion patterns

**Guidelines Derived:**
- CLOSURE-ENCAP: Use Closures for Encapsulation
- CURRY-PATTERN: Curry for Reusable Functions
- PARTIAL-APP: Partial Application for Specialization
- POINT-FREE: Point-Free Style Where Clear
- RECURSION-BASE: Use Recursion for Recursive Problems
- TAIL-RECURSION: Note JavaScript Tail Call Limitations

---

### 3. Brian Lonsdorf - Professor Frisby's Mostly Adequate Guide to FP

**Source:** "Professor Frisby's Mostly Adequate Guide to Functional Programming"
**Author:** Brian Lonsdorf (DrBoolean)
**URL:** https://github.com/MostlyAdequate/mostly-adequate-guide

**Key Contributions:**
- Composition and pipelines
- Currying patterns
- Functors, applicatives, and monads
- Point-free programming
- Maybe and Either patterns

**Guidelines Derived:**
- PIPE-PATTERN: Use Pipe for Left-to-Right Composition
- MAYBE-PATTERN: Handle Null/Undefined Safely
- EITHER-PATTERN: Functional Error Handling
- UNARY-WRAP: Wrap Functions to Control Arity

---

### 4. MDN Web Docs - JavaScript Reference

**Source:** Mozilla Developer Network
**Organization:** Mozilla Foundation
**URL:** https://developer.mozilla.org/en-US/docs/Web/JavaScript

**Key Contributions:**
- Array method documentation (map, filter, reduce, etc.)
- ES6+ feature documentation
- Arrow functions and lexical this
- Destructuring and spread syntax
- Optional chaining and nullish coalescing
- Generator functions

**Guidelines Derived:**
- ARR-MAP: Use map() for Transformations
- ARR-FILTER: Use filter() for Selection
- ARR-REDUCE: Use reduce() for Accumulation
- ARR-FLATMAP: Use flatMap() for Mapping + Flattening
- ARR-FIND: Use find/findIndex for Searching
- ARR-SOME-EVERY: Use some/every for Boolean Tests
- ARR-FROM: Use Array.from for Conversions
- ARR-SLICE: Use slice() for Safe Copying
- ARROW-SIMPLE: Use Arrows for Simple Functions
- ARROW-LEXICAL: Leverage Lexical this Binding
- DESTRUCTURE: Use Destructuring for Clarity
- SPREAD-REST: Use Spread/Rest Operators
- DEFAULT-PARAMS: Default Parameters Over Conditionals
- OPTIONAL-CHAIN: Optional Chaining for Safe Access
- NULLISH-COALESCE: Nullish Coalescing for Defaults
- LAZY-EVAL: Lazy Evaluation Patterns

---

### 5. JavaScript.info - The Modern JavaScript Tutorial

**Source:** JavaScript.info
**Authors:** Ilya Kantor and contributors
**URL:** https://javascript.info/

**Key Contributions:**
- Modern JavaScript features
- Immutability patterns
- Arrow functions best practices
- Recursion and iteration
- Closures and scope

**Guidelines Derived:**
- USE-CONST: Prefer const Over let
- IMMUT-COPY: Copy Objects/Arrays Instead of Mutating
- SPREAD-COPY: Use Spread Operator for Shallow Copies
- AVOID-ARROW-COMPLEX: Use Regular Functions for Complex Logic

---

### 6. Airbnb JavaScript Style Guide

**Source:** Airbnb JavaScript Style Guide
**Organization:** Airbnb
**URL:** https://github.com/airbnb/javascript

**Key Contributions:**
- Prefer const over let
- Avoid mutating variables
- Use array spreads and methods
- Arrow function best practices
- Destructuring patterns

**Guidelines Derived:**
- USE-CONST: Prefer const Over let
- AVOID-PUSH-POP: Use Immutable Array Methods
- ARR-CHAINING: Chain Array Methods
- AVOID-FOR-LOOP: Replace Imperative Loops

---

### 7. Functional Programming Resources

**Various Community Resources:**

#### Ramda Documentation
**URL:** https://ramdajs.com/
**Contributions:** Curry patterns, composition, point-free style

#### Lodash/FP Documentation
**URL:** https://github.com/lodash/lodash/wiki/FP-Guide
**Contributions:** Functional programming patterns in JavaScript

#### "JavaScript Allongé" by Reg Braithwaite
**URL:** https://leanpub.com/javascriptallongesix
**Contributions:** Function composition, closures, combinators

---

## Concept Sources

### Pure Functions
**Principle:** "A pure function is a function that, given the same input, will always return the same output and does not have any observable side effects."
**Sources:** Eric Elliott, Kyle Simpson, functional programming fundamentals

### Immutability
**Principle:** Prefer immutable data structures and avoid mutations
**Sources:** Redux documentation, React best practices, functional programming principles

### Function Composition
**Principle:** "The essence of software development is composition" - building complex from simple
**Sources:** Eric Elliott, Brian Lonsdorf, functional programming theory

### Declarative Programming
**Principle:** Express what to do, not how to do it
**Sources:** React philosophy, functional programming paradigm

### Higher-Order Functions
**Principle:** Functions as first-class citizens - can be passed as arguments and returned
**Sources:** JavaScript language design, functional programming fundamentals

---

## ES6+ Feature Sources

### Arrow Functions
**Specification:** ECMAScript 2015 (ES6)
**Documentation:** MDN Web Docs, TC39 proposals

### Destructuring
**Specification:** ECMAScript 2015 (ES6)
**Documentation:** MDN Web Docs

### Spread/Rest Operators
**Specification:** ECMAScript 2015 (ES6) and ES2018 (object spread)
**Documentation:** MDN Web Docs

### Optional Chaining
**Specification:** ECMAScript 2020 (ES11)
**Documentation:** MDN Web Docs, TC39 proposal

### Nullish Coalescing
**Specification:** ECMAScript 2020 (ES11)
**Documentation:** MDN Web Docs, TC39 proposal

---

## Pattern Sources

### Maybe Monad
**Sources:**
- Haskell Maybe type
- Brian Lonsdorf - "Professor Frisby's Guide"
- Folktale library documentation

### Either Monad
**Sources:**
- Haskell Either type
- Functional programming theory
- Railway-oriented programming (Scott Wlaschin)

### Functor Pattern
**Sources:**
- Category theory
- Brian Lonsdorf - Functors in JavaScript
- Functional programming fundamentals

### Memoization
**Sources:**
- Dynamic programming techniques
- Lodash memoize implementation
- React useMemo documentation

---

## Additional References

### Books
1. **"Eloquent JavaScript"** by Marijn Haverbeke - Array methods, functional patterns
2. **"You Don't Know JS"** by Kyle Simpson - Closures, scope, this binding
3. **"JavaScript: The Good Parts"** by Douglas Crockford - Functional features of JS

### Articles & Blogs
1. **JavaScript Scene** (Eric Elliott) - Functional programming in JavaScript
2. **2ality** (Dr. Axel Rauschmayer) - ES6+ features and functional patterns
3. **Reginald Braithwaite's Blog** - Advanced functional JavaScript

### Specifications
1. **ECMAScript Language Specification** - Official JavaScript spec
2. **TC39 Proposals** - Upcoming JavaScript features

---

## Guideline Mapping

Each guideline in this skill can be traced to one or more of the above sources:

### Pure Functions & Side Effects
- PURE-FUNC → Eric Elliott, Kyle Simpson
- NO-SIDE-EFFECT → Eric Elliott, FP fundamentals
- NO-MUTATE-ARGS → FP best practices, Airbnb guide

### Immutability
- USE-CONST → Airbnb guide, MDN, modern JS practices
- IMMUT-COPY → React docs, Redux patterns
- SPREAD-COPY → MDN, ES6 spec
- OBJECT-FREEZE → MDN, immutability patterns
- AVOID-PUSH-POP → Airbnb guide, functional patterns
- IMMUT-PATTERN → Redux docs, React best practices

### Array Methods
- ARR-MAP, ARR-FILTER, ARR-REDUCE → MDN, Array.prototype spec
- ARR-FLATMAP → ES2019 spec, MDN
- ARR-FIND → ES2015 spec, MDN
- ARR-SOME-EVERY → MDN, Array methods
- ARR-CHAINING → Functional patterns, Lodash
- AVOID-FOR-LOOP → Airbnb guide, functional style
- ARR-FROM → ES2015 spec, MDN
- ARR-SLICE → MDN, immutability patterns

### Higher-Order Functions
- HOF-PATTERN → Eric Elliott, FP fundamentals
- FUNC-RETURN → Kyle Simpson, closures
- CALLBACK-PATTERN → JavaScript design patterns
- CLOSURE-ENCAP → Kyle Simpson, "You Don't Know JS"

### Composition
- COMPOSE-FUNC → Eric Elliott, Ramda docs
- PIPE-PATTERN → Brian Lonsdorf, Ramda
- POINT-FREE → Kyle Simpson, Brian Lonsdorf
- SINGLE-RESPONSIBILITY → Clean Code principles, SOLID

### Currying & Partial Application
- CURRY-PATTERN → Kyle Simpson, Ramda docs
- PARTIAL-APP → Kyle Simpson, FP patterns
- UNARY-WRAP → Brian Lonsdorf, Ramda

### Arrow Functions
- ARROW-SIMPLE → ES2015 spec, MDN
- ARROW-LEXICAL → ES2015 spec, MDN
- AVOID-ARROW-COMPLEX → Airbnb guide, best practices

### ES6+ Features
- DESTRUCTURE → ES2015 spec, MDN
- SPREAD-REST → ES2015/ES2018 spec, MDN
- DEFAULT-PARAMS → ES2015 spec, MDN
- OPTIONAL-CHAIN → ES2020 spec, MDN
- NULLISH-COALESCE → ES2020 spec, MDN

### Recursion
- RECURSION-BASE → FP fundamentals, Kyle Simpson
- TAIL-RECURSION → FP theory, JavaScript limitations

### Functional Patterns
- MAYBE-PATTERN → Haskell, Brian Lonsdorf
- EITHER-PATTERN → Haskell, Railway-oriented programming
- FUNCTOR-MAP → Category theory, Brian Lonsdorf
- LAZY-EVAL → Generator functions, FP patterns
- MEMOIZATION → Dynamic programming, optimization patterns

---

## Acknowledgments

This skill exists thanks to the JavaScript community's commitment to sharing knowledge:

- **Eric Elliott** - For "Composing Software" and extensive FP education
- **Kyle Simpson** - For "Functional-Light JavaScript" and pragmatic FP
- **Brian Lonsdorf** - For making category theory accessible to JavaScript developers
- **Mozilla Foundation** - For comprehensive MDN documentation
- **TC39 Committee** - For evolving JavaScript with functional features
- **Airbnb** - For codifying JavaScript best practices
- **Open source community** - For libraries like Ramda, Lodash/FP, and Folktale

---

## Usage and Attribution

This skill compiles and synthesizes information from the sources listed above. When using insights from this skill:

1. **Credit the original authors** when sharing specific concepts
2. **Link to source materials** for deeper learning
3. **Respect licenses** of original works
4. **Contribute back** improvements to the community

---

## Disclaimer

This skill is an educational tool based on publicly available resources. It represents community best practices as of its creation date. JavaScript and functional programming patterns continue to evolve.

For authoritative information, always refer to:
- Official ECMAScript specification
- MDN Web Docs for current standards
- Original author's works for in-depth understanding

---

**Last Updated:** November 2025
**Skill Version:** 1.0

*This skill stands on the shoulders of giants in the JavaScript functional programming community.*
