# Functional JavaScript Reviewer

A comprehensive Claude Code skill for reviewing JavaScript code through the lens of functional programming principles and modern ES6+ best practices.

## 🎯 What This Skill Reviews

This skill analyzes JavaScript code for:

### Pure Functions & Side Effects
- Pure function patterns (same input → same output)
- Side effect isolation
- Avoiding argument mutation
- Global state dependencies

### Immutability
- Proper use of `const` over `let`
- Immutable update patterns with spread operator
- Avoiding array mutations (push, pop, splice)
- Object.freeze for true immutability
- Copy-on-write patterns

### Array Methods & Iteration
- Declarative array methods (map, filter, reduce)
- Method chaining for transformation pipelines
- flatMap, find, some, every usage
- Replacing imperative loops with functional alternatives
- Safe array copying with slice

### Function Composition
- Building complex operations from simple functions
- Compose and pipe patterns
- Point-free style where appropriate
- Single responsibility principle

### Higher-Order Functions
- Functions as first-class citizens
- Returning functions from functions
- Closures for encapsulation
- Callback patterns

### Currying & Partial Application
- Currying for reusable specialized functions
- Partial application patterns
- Controlling function arity

### Modern ES6+ Features
- Destructuring for clarity
- Spread/rest operators
- Arrow functions and lexical `this`
- Default parameters
- Optional chaining (`?.`)
- Nullish coalescing (`??`)

### Functional Patterns
- Maybe pattern for null safety
- Either pattern for error handling
- Functor pattern
- Lazy evaluation with generators
- Memoization for performance

## 📋 Example Review Output

````markdown
## Review: userService.js

### ✅ Strengths
- **ARR-MAP**: Good use of map() for transforming user data (line 15)
- **USE-CONST**: Properly using const for immutable bindings throughout
- **ARROW-LEXICAL**: Clean use of arrow functions in callbacks

### ⚠️ Suggestions

#### AVOID-FOR-LOOP: Using imperative loop instead of array methods

**Current code:**
```javascript
const activeUsers = [];
for (let i = 0; i < users.length; i++) {
  if (users[i].isActive) {
    activeUsers.push(users[i]);
  }
}
```

**Suggested refactoring:**
```javascript
const activeUsers = users.filter(user => user.isActive);
```

**Why this matters:**
Array methods like filter are declarative, expressing *what* you want rather than *how* to get it. They're easier to read, less error-prone, and can be optimized by the engine.

**FP principle:**
Replace imperative iteration with declarative array methods for clearer intent and fewer bugs.

---

#### IMMUT-COPY: Mutating object instead of creating new one

**Current code:**
```javascript
function updateUserEmail(user, email) {
  user.email = email;
  return user;
}
```

**Suggested refactoring:**
```javascript
function updateUserEmail(user, email) {
  return { ...user, email };
}
```

**Why this matters:**
Mutating arguments causes unexpected behavior in calling code. Creating new objects preserves immutability and prevents bugs from shared references.

**FP principle:**
Never mutate function arguments - always return new objects with the desired changes.

### 💡 Functional Programming Wisdom
> "Functional programming is about writing pure functions, removing hidden inputs and outputs, so that as much of our code as possible just describes a relationship between inputs and outputs."
````

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## 💡 How to Use

Once installed, the skill activates automatically when you request functional programming reviews:

```
"Review this JavaScript code for functional programming issues"
"Check this code for immutability violations"
"Make this code more functional"
"Review these functions for side effects"
"Suggest functional alternatives to these loops"
"Check for proper use of array methods"
```

Or invoke directly:

```
"Use the functional JavaScript reviewer on this file"
"Apply functional programming patterns here"
```

## 📚 What You'll Learn

This skill is educational - it doesn't just point out issues, it teaches:

✅ **Why functional patterns matter** - Real-world benefits explained
✅ **Concrete code examples** - Before/after transformations
✅ **Modern JavaScript** - ES6+ features for functional style
✅ **Best practices** - Industry-standard patterns and idioms
✅ **Trade-offs** - When to use functional vs imperative approaches

## 🎓 Skill Coverage

### 45+ Guidelines Organized by Category

1. **Pure Functions (3)** - PURE-FUNC, NO-SIDE-EFFECT, NO-MUTATE-ARGS
2. **Immutability (6)** - USE-CONST, IMMUT-COPY, SPREAD-COPY, OBJECT-FREEZE, AVOID-PUSH-POP, IMMUT-PATTERN
3. **Array Methods (10)** - ARR-MAP, ARR-FILTER, ARR-REDUCE, ARR-FLATMAP, ARR-FIND, ARR-SOME-EVERY, ARR-CHAINING, AVOID-FOR-LOOP, ARR-FROM, ARR-SLICE
4. **Higher-Order Functions (4)** - HOF-PATTERN, FUNC-RETURN, CALLBACK-PATTERN, CLOSURE-ENCAP
5. **Composition (4)** - COMPOSE-FUNC, PIPE-PATTERN, POINT-FREE, SINGLE-RESPONSIBILITY
6. **Currying (3)** - CURRY-PATTERN, PARTIAL-APP, UNARY-WRAP
7. **Arrow Functions (3)** - ARROW-SIMPLE, ARROW-LEXICAL, AVOID-ARROW-COMPLEX
8. **ES6+ Features (5)** - DESTRUCTURE, SPREAD-REST, DEFAULT-PARAMS, OPTIONAL-CHAIN, NULLISH-COALESCE
9. **Recursion (2)** - RECURSION-BASE, TAIL-RECURSION
10. **Patterns (5)** - MAYBE-PATTERN, EITHER-PATTERN, FUNCTOR-MAP, LAZY-EVAL, MEMOIZATION

Each guideline includes:
- Clear principle statement
- Concrete code examples (good/bad)
- Explanation of benefits
- Real-world context

## 🔍 When to Use This Skill

**Perfect for:**
- ✅ Adopting functional programming patterns in JavaScript
- ✅ Code reviews focused on immutability and pure functions
- ✅ Modernizing code to use ES6+ functional features
- ✅ Learning functional JavaScript best practices
- ✅ Reducing bugs from mutable state and side effects
- ✅ Improving code testability and maintainability

**Not ideal for:**
- ❌ Performance-critical code requiring imperative optimizations
- ❌ Code that's already highly functional
- ❌ Projects explicitly using object-oriented patterns
- ❌ Quick scripts where FP adds unnecessary complexity

## 🎯 Philosophy

This skill embraces JavaScript's multi-paradigm nature:

> **Pragmatic, not dogmatic** - Functional when beneficial, imperative when clearer
>
> **Modern JavaScript** - Leverages ES6+ features for cleaner functional code
>
> **Education-focused** - Teaches principles, not just rules
>
> **Real-world** - Patterns you'll actually use in production code

## 🤝 Works Great With

Combine with other skills for comprehensive reviews:
- **Security reviewer** - Functional patterns + security checks
- **Performance reviewer** - Balance FP with performance needs
- **Test reviewer** - Pure functions are easier to test
- **Refactoring reviewer** - Functional refactoring opportunities

## 📖 Based On

This skill is based on established JavaScript functional programming resources:

- **Eric Elliott** - "Composing Software" series
- **Kyle Simpson** - "Functional-Light JavaScript"
- **Brian Lonsdorf** - "Professor Frisby's Mostly Adequate Guide to FP"
- **MDN Web Docs** - JavaScript language reference
- **JavaScript community standards** - Modern best practices

## 🔧 Customization

The skill uses these tools (configurable in SKILL.md frontmatter):
- `Read` - Reads code files
- `Grep` - Searches for patterns
- `Glob` - Finds files by pattern

## 📊 Review Quality

Each review provides:
- **Mnemonic IDs** - Easy reference (e.g., ARR-MAP, PURE-FUNC)
- **Structured format** - Strengths, suggestions, wisdom
- **Code examples** - Current vs. suggested code
- **Explanations** - Why it matters and underlying principles
- **Actionable feedback** - Clear steps to improve

## 💬 Feedback & Contributions

Found an issue or have a suggestion?
- Open an issue on the repository
- Suggest new guidelines or patterns
- Share how you're using the skill

## 📄 License

This skill is licensed under MIT. See SOURCES.md for detailed attribution to functional programming resources and authors.

---

**Write clearer, more maintainable JavaScript with functional programming patterns.**
