# JavaScript/TypeScript Format Refactoring Reviewer Skill

A Claude Code skill that solves JavaScript/TypeScript ESLint/Prettier formatting issues through refactoring rather than just wrapping lines or disabling rules.

## What This Skill Does

This skill transforms Claude into a JavaScript/TypeScript format refactoring expert who:
- **Solves ESLint/Prettier issues through refactoring** - not just formatting
- **Goes beyond auto-fixers** - suggests structural improvements
- **Eliminates root causes** - not just symptoms
- **Applies industry best practices** - from Airbnb, React, and refactoring patterns
- **Provides refactoring patterns** - for each style issue
- **Shows before/after examples** - with proper refactoring

## Philosophy

> **"Don't fight ESLint—refactor so it has nothing to complain about."**

When ESLint says "line too long", don't just wrap it. Extract a function or variable so the line naturally fits.

When it says "too complex", don't raise the limit. Simplify the logic with extracted predicates or use a lookup object.

When it says "too many parameters", don't ignore it. Use destructuring or an options object.

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## How to Use

Simply ask Claude to review your JavaScript/TypeScript code for format refactoring:

```
"ESLint says this line is too long - how should I refactor it?"
"This function is too complex according to ESLint - help me refactor it"
"How can I fix this formatting issue structurally?"
"Refactor this to solve the ESLint warnings"
"This has too many parameters - what refactoring should I use?"
"Fix this JSX formatting through refactoring"
```

The skill will automatically activate based on keywords like:
- JavaScript format, TypeScript format
- ESLint, Prettier
- line too long, complexity
- refactoring, JSX formatting
- too many parameters

## What You'll Get

A structured refactoring review with:
- ✅ **Well-Structured Code** - What's already good structurally
- 🔧 **Refactoring Opportunities** - Style issues with root causes
- **ESLint Rules** - What ESLint would say
- **Root Cause Analysis** - Why the style issue exists
- **Refactored Code** - Proper structural fix (not just formatting)
- **Why Better** - Benefits beyond just passing linters

### Example Review

````markdown
## JavaScript Format Refactoring Review: userService.js

### ✅ Well-Structured Code
- **JS-PARAMS-DEFAULT**: Good use of default parameters in createUser() (line 15)

### 🔧 Refactoring Opportunities

#### max-len: JS-LONG-FUNC-PARAMS - Extract Parameter Object

**ESLint would say:**
> "Line exceeds 100 characters (max-len)"
> "Function has too many parameters (max-params)"

**Root cause:**
Function has 9 parameters making the signature too long and hard to call correctly. Parameters are related and should be grouped.

**Current code:**
```javascript
function createUser(firstName, lastName, email, age, address, phone, role, department, startDate) {
  // Implementation
}
```

**Refactored code:**
```javascript
function createUser({
  firstName,
  lastName,
  email,
  age,
  address,
  phone,
  role,
  department,
  startDate
}) {
  // Implementation
}

// Called like:
createUser({
  firstName: 'John',
  lastName: 'Doe',
  email: 'john@example.com',
  age: 30,
  address: '123 Main St',
  phone: '555-1234',
  role: 'admin',
  department: 'IT',
  startDate: new Date()
});
```

**Why this is better:**
- Fixes line length naturally
- Self-documenting parameter names
- Order doesn't matter
- Easy to add/remove parameters
- Can provide default values

**Refactoring applied:** Introduce Parameter Object

---

#### complexity: JS-COMPLEX-CONDITION - Simplify Complex Conditions

**ESLint would say:**
> "Function has too much complexity (complexity)"

**Root cause:**
Complex boolean expressions in conditionals increase cyclomatic complexity and make code hard to understand.

**Current code:**
```javascript
function calculateDiscount(customer, order) {
  if ((customer.loyaltyYears > 5 && customer.totalPurchases > 10000) || (order.itemsCount > 20) || (order.total > 5000 && customer.isPremium)) {
    return 0.20;
  }
  return 0.05;
}
```

**Refactored code:**
```javascript
function isGoldCustomer(customer) {
  return customer.loyaltyYears > 5 && customer.totalPurchases > 10000;
}

function isBulkOrder(order) {
  return order.itemsCount > 20;
}

function isPremiumLargeOrder(customer, order) {
  return order.total > 5000 && customer.isPremium;
}

function qualifiesForMaxDiscount(customer, order) {
  return (
    isGoldCustomer(customer) ||
    isBulkOrder(order) ||
    isPremiumLargeOrder(customer, order)
  );
}

function calculateDiscount(customer, order) {
  if (qualifiesForMaxDiscount(customer, order)) {
    return 0.20;
  }
  return 0.05;
}
```

**Why this is better:**
- Complex conditions have descriptive names
- Each predicate is testable independently
- Business rules are self-documenting
- Complexity is distributed across functions

**Refactoring applied:** Extract Predicate Function, Decompose Conditional

### 💡 Refactoring Wisdom
> "Good structure leads to good style automatically. Refactor for clarity, and ESLint compliance follows naturally."
````

## The 30+ Guidelines

### Line Length Issues (6 guidelines)
- **JS-LONG-FUNC-PARAMS** - Extract parameter object instead of long parameter list
- **JS-LONG-CHAIN** - Extract intermediate variables from chains
- **JS-LONG-CONDITION** - Extract predicate functions for complex conditions
- **JS-LONG-TEMPLATE** - Multi-line template literals for long strings
- **JS-LONG-ARRAY** - Multi-line array/object literals
- **JS-LONG-JSX** - Extract JSX components instead of cramming

### Complexity Issues (6 guidelines)
- **JS-COMPLEX-CONDITION** - Simplify complex conditions with predicates
- **JS-COMPLEX-FUNC** - Extract functions to reduce complexity
- **JS-COMPLEX-TERNARY** - Replace nested ternaries with if-else or lookup
- **JS-COMPLEX-SWITCH** - Use lookup objects or Maps instead of long switches
- **JS-COMPLEX-CALLBACK** - Use async/await instead of callback hell
- **JS-COMPLEX-NESTING** - Reduce nesting levels with guard clauses

### Function Parameters (4 guidelines)
- **JS-PARAMS-MANY** - Use destructuring or options object for many parameters
- **JS-PARAMS-ORDER** - Logical parameter order with named parameters
- **JS-PARAMS-BOOLEAN** - Avoid boolean parameters (use options object)
- **JS-PARAMS-DEFAULT** - Use default parameters properly

### React/JSX (6 guidelines)
- **JS-JSX-LONG** - Extract components instead of long JSX
- **JS-JSX-PROPS** - Extract props object or spread appropriately
- **JS-JSX-CONDITION** - Extract conditional rendering logic
- **JS-JSX-MAP** - Extract map callbacks into components
- **JS-JSX-INLINE** - Avoid inline functions when performance matters
- **JS-JSX-STYLE** - Extract style objects or use CSS-in-JS

### Array/Object (4 guidelines)
- **JS-OBJ-LONG** - Multi-line objects for readability
- **JS-ARRAY-LONG** - Multi-line arrays with trailing commas
- **JS-OBJ-COMPUTED** - Extract computed properties to variables
- **JS-SPREAD-LONG** - Multi-line spreads for clarity

### String/Template (4 guidelines)
- **JS-STRING-CONCAT** - Use template literals instead of concatenation
- **JS-TEMPLATE-LONG** - Multi-line templates for long strings
- **JS-TEMPLATE-COMPLEX** - Extract template parts to variables
- **JS-STRING-SPLIT** - Split long strings across lines

## Common ESLint Issues → Refactoring Solutions

| ESLint Says | Root Cause | Refactoring Solution |
|------------|------------|---------------------|
| Line exceeds max length (max-len) | Complex expression | Extract Variable / Extract Function |
| Too many parameters (max-params) | Related params separate | Introduce Parameter Object / Destructuring |
| Function too complex (complexity) | Nested conditions | Extract Predicate / Guard Clauses |
| Blocks nested too deeply (max-depth) | Deep nesting | Guard Clauses / Extract Iterator |
| Too many statements (max-statements) | Does too much | Extract Function |
| Too many nested callbacks (max-nested-callbacks) | Callback hell | Convert to Async/Await |
| Nested ternary (no-nested-ternary) | Unclear logic | If-Else or Lookup Object |
| Prefer template literals (prefer-template) | String concatenation | Use Template Literals |
| JSX nested too deeply (react/jsx-max-depth) | Complex JSX | Extract Component |
| Too many props per line (react/jsx-max-props-per-line) | Many props | Multi-line Props / Pass Object |

## Example Use Cases

### Refactoring for Line Length
- "This line is 120 chars - how do I refactor it?"
- "Extract parameter object to fix this long signature"
- "Too many function parameters causing long line"

### Refactoring for Complexity
- "ESLint says too complex (15/10) - help refactor"
- "Simplify this nested conditional"
- "Reduce cyclomatic complexity structurally"

### Refactoring React/JSX
- "This JSX is too long - extract components"
- "Too many props - how to refactor?"
- "Extract conditional rendering logic"
- "Performance issue with inline functions in map"

### Refactoring for Readability
- "Make this expression clearer through refactoring"
- "Extract function from this complex logic"
- "Flatten this deeply nested code"
- "Replace callback hell with async/await"

### Learning Refactoring Patterns
- "What refactoring fixes too many parameters in JavaScript?"
- "Show me async/await pattern for callbacks"
- "How to use options objects in TypeScript?"

## Benefits

- ✓ **Deeper than Prettier** - Structural improvements, not just cosmetic
- ✓ **Root cause fixes** - Solve problems, don't disable rules
- ✓ **Learn refactoring** - 30+ patterns with examples
- ✓ **Industry best practices** - Based on Airbnb, React patterns
- ✓ **Beyond auto-fixers** - Understand *why* ESLint complains
- ✓ **Better code** - More maintainable, testable, readable
- ✓ **Pattern-based** - Catalog of proven solutions
- ✓ **Educational** - Learn to think structurally
- ✓ **TypeScript ready** - Works for both JS and TS

## What Gets Checked

### Style Issues That Indicate Deeper Problems
- Lines too long → Extract functions/variables needed
- Functions too complex → Simplification needed
- Too many parameters → Parameter object needed
- Deep nesting → Guard clauses/extraction needed
- Complex expressions → Naming needed
- Long functions → Decomposition needed
- Callback hell → Async/await needed
- Long JSX → Component extraction needed

### Refactoring Solutions Applied
- Extract Variable - for clarity and line length
- Extract Function - for complexity and reuse
- Introduce Parameter Object - for parameter lists
- Guard Clauses - for nesting and complexity
- Extract Component - for React/JSX
- Decompose Conditional - for complex logic
- Replace Switch with Lookup - for branches
- Convert to Async/Await - for callbacks

## Supported Technologies

- **JavaScript (ES6+)** - All modern JavaScript features
- **TypeScript** - Full TypeScript support
- **React** - JSX and React-specific patterns
- **Node.js** - Backend JavaScript patterns
- **Modern frameworks** - Patterns apply to Vue, Angular, etc.

## ESLint Rules Covered

This skill helps refactor code for these common ESLint rules:

**Core:**
- max-len (line length)
- complexity (cyclomatic complexity)
- max-params (parameter count)
- max-statements (statement count)
- max-depth (nesting depth)
- max-nested-callbacks (callback nesting)
- no-nested-ternary (nested ternaries)
- prefer-template (template literals)
- default-param-last (default parameters)

**Objects/Arrays:**
- object-curly-newline
- object-property-newline
- array-element-newline

**React:**
- react/jsx-max-depth
- react/jsx-max-props-per-line
- react/jsx-no-bind

## Difference from Other Skills

| Skill | Focus |
|-------|-------|
| **javascript-format-refactoring-reviewer** | Solve JS/TS ESLint issues through refactoring |
| python-refactoring-reviewer | General code quality refactoring (Python) |
| javascript-functional-reviewer | Functional programming patterns in JS |
| python-format-refactoring-reviewer | Python format refactoring |

This skill specifically addresses **JavaScript/TypeScript formatting/style warnings by refactoring the structure**, not just reformatting.

## Sources and Attribution

All guidelines are based on:
- **Airbnb JavaScript Style Guide** - Industry-standard JavaScript conventions
- **ESLint Rules** - Official ESLint rule documentation
- **React Best Practices** - React documentation and community patterns
- **Refactoring Patterns** - Martin Fowler's refactoring catalog
- **Clean Code** - Robert C. Martin's principles
- **Modern JavaScript** - ES6+ features and patterns

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## License

This skill is licensed under MIT. It is based on public documentation, style guides, and established refactoring patterns.

---

**Refactor for structure, and ESLint compliance follows naturally.**
