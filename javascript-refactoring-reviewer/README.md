# JavaScript Refactoring Reviewer Skill

A Claude Code skill that reviews JavaScript/TypeScript code for refactoring opportunities to improve readability, maintainability, testability, and performance. **Clean code through systematic refactoring** - shows detailed approaches for code smells, SOLID principles, and modern JavaScript patterns.

## What This Skill Does

This skill transforms Claude into a JavaScript refactoring expert who:
- **Identifies code smells** - Long functions, god classes, duplicated code, tight coupling
- **Applies SOLID principles** - SRP, OCP, LSP, ISP, DIP
- **Suggests modern JavaScript patterns** - ES6+, async/await, functional programming
- **Provides before/after examples** - Concrete refactoring demonstrations
- **Explains trade-offs** - When and why to apply each refactoring
- **Improves testability** - Dependency injection, pure functions, loose coupling

## Philosophy

> **"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."** - Martin Fowler

> **"Make it work, make it right, make it fast."** - Kent Beck

This skill focuses on the "make it right" phase - transforming working code into maintainable, testable, and performant code through systematic refactoring.

## Installation

### Personal Installation (Available in All Projects)

Copy the entire skill folder to your personal Claude directory:

```bash
# Linux/Mac
cp -r javascript-refactoring-reviewer ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse "javascript-refactoring-reviewer" "$env:USERPROFILE\.claude\skills\"
```

After this, the skill works in **any project** you open with Claude Code.

### Project Installation (For Teams)

Copy the skill to your project:

```bash
# Copy to another project
cp -r javascript-refactoring-reviewer /path/to/your-project/.claude/skills/

# Then commit it
cd /path/to/your-project
git add .claude/skills/javascript-refactoring-reviewer
git commit -m "Add JavaScript Refactoring Reviewer skill"
```

**✅ Self-Contained:** All 50+ guidelines are embedded directly in SKILL.md - no external file references needed!

## How to Use

Simply ask Claude to review your code or suggest refactoring opportunities:

```
"Review this JavaScript code for refactoring opportunities"
"How can I improve this code's maintainability?"
"Identify code smells in this function"
"Refactor this to follow SOLID principles"
"Make this code more testable"
"Suggest modern JavaScript patterns for this"
```

The skill will automatically activate based on keywords like:
- refactor, refactoring, code smell
- clean code, improve, simplify
- SOLID, DRY, maintainability, readability
- JavaScript, TypeScript

## What You'll Get

A comprehensive refactoring review with:
- **Code Smells Identified** - What problems exist in the current code
- **Before/After Examples** - Concrete refactoring demonstrations
- **Intent Classification** - Readability, Maintainability, Testability, Performance
- **Why It Matters** - Benefits of each refactoring
- **Mnemonic IDs** - Easy reference (e.g., EXTRACT-FUNC, DRY-VIOLATION)

### Example Review

````markdown
## Refactoring Review: OrderProcessor

### ✅ Strengths
- **CONST-LET**: Properly using const for immutable values
- **ASYNC-AWAIT**: Modern async handling instead of callbacks

### 🔨 Refactoring Opportunities

#### READABILITY: LONG-FUNC - Break down long processOrder function

**Current code:**
```javascript
function processOrder(order) {
    // Validate order
    if (!order.items || order.items.length === 0) {
        throw new Error("Empty order");
    }

    // Calculate tax
    const taxRate = 0.08;
    const tax = order.subtotal * taxRate;

    // Apply discount
    let discount = 0;
    if (order.customer.isPremium) {
        discount = order.subtotal * 0.1;
    }

    // Calculate final total
    order.total = order.subtotal + tax - discount;

    // Send confirmation
    const email = `Order confirmed: $${order.total}`;
    sendEmail(order.customer.email, email);
}
```

**Refactored code:**
```javascript
function processOrder(order) {
    validateOrder(order);
    const tax = calculateTax(order.subtotal);
    const discount = calculateDiscount(order);
    order.total = calculateFinalTotal(order.subtotal, tax, discount);
    sendOrderConfirmation(order);
}

function validateOrder(order) {
    if (!order.items || order.items.length === 0) {
        throw new Error("Empty order");
    }
}

function calculateTax(subtotal) {
    const TAX_RATE = 0.08;
    return subtotal * TAX_RATE;
}

function calculateDiscount(order) {
    return order.customer.isPremium ? order.subtotal * 0.1 : 0;
}

function calculateFinalTotal(subtotal, tax, discount) {
    return subtotal + tax - discount;
}

function sendOrderConfirmation(order) {
    const email = `Order confirmed: $${order.total}`;
    sendEmail(order.customer.email, email);
}
```

**Why this matters:**
- Each function has single responsibility
- Easier to test individual pieces
- Improves reusability
- Self-documenting through function names

**Code smell addressed:** Long Method
````

## The 50+ Guidelines

### Readability (12 guidelines)
- **MEANINGFUL-NAME** - Use meaningful variable names
- **PRONOUNCE-NAME** - Use pronounceable names
- **SEARCHABLE-NAME** - Use searchable names
- **AVOID-MENTAL-MAP** - Avoid mental mapping
- **EXTRACT-FUNC** - Extract long functions
- **EXTRACT-VAR** - Introduce explaining variable
- **DECOMPOSE-COND** - Decompose conditional
- **LONG-FUNC** - Shorten long functions
- **LONG-PARAM** - Reduce long parameter lists
- **MAGIC-NUM** - Replace magic numbers with named constants
- **ARROW-FUNC** - Use arrow functions for callbacks
- **TEMPLATE-LIT** - Use template literals

### Maintainability (15 guidelines)
- **DRY-VIOLATION** - Don't Repeat Yourself
- **EXTRACT-CLASS** - Extract class
- **DUPLICATE-CODE** - Remove duplicate code
- **SRP-VIOLATION** - Single Responsibility Principle
- **OCP-VIOLATION** - Open/Closed Principle
- **LSP-VIOLATION** - Liskov Substitution Principle
- **DIP-VIOLATION** - Dependency Inversion Principle
- **GOD-CLASS** - Break down god classes
- **DATA-CLASS** - Enrich data classes
- **FEATURE-ENVY** - Move method to appropriate class
- **MESSAGE-CHAIN** - Hide delegate
- **MIDDLE-MAN** - Remove middle man
- **SHOT-GUN** - Consolidate shotgun surgery
- **DIVERGENT-CHANGE** - Separate divergent changes
- **PARALLEL-HIER** - Collapse parallel hierarchies

### Testability (7 guidelines)
- **PURE-FUNC** - Prefer pure functions
- **INJECT-DEP** - Use dependency injection
- **SEPARATE-QUERY** - Separate query from command
- **HIDDEN-DEP** - Expose hidden dependencies
- **GLOBAL-STATE** - Avoid global state
- **TIGHTLY-COUPLED** - Reduce tight coupling
- **FACTORY-PATTERN** - Use factory for object creation

### Code Smells - Bloaters (5 guidelines)
- **LONG-METHOD** - Break down long methods
- **LARGE-CLASS** - Split large classes
- **LONG-PARAM-LIST** - Use parameter object
- **PRIMITIVE-OBS** - Replace primitives with objects
- **DATA-CLUMP** - Group related data

### Code Smells - Complexity (4 guidelines)
- **SWITCH-STMT** - Replace switch with polymorphism
- **NESTED-COND** - Reduce nested conditionals
- **COMPLEX-BOOL** - Simplify complex boolean logic
- **CALLBACK-HELL** - Flatten callback hell

### Modern JavaScript (8 guidelines)
- **DESTRUCTURE** - Use destructuring
- **SPREAD-REST** - Use spread and rest operators
- **OPT-CHAIN** - Use optional chaining
- **NULLISH-COAL** - Use nullish coalescing
- **ASYNC-AWAIT** - Use async/await
- **ARRAY-METHODS** - Use array methods (map, filter, reduce)
- **CONST-LET** - Use const and let
- **DEFAULT-PARAM** - Use default parameters

### Performance (5 guidelines)
- **ALGO-COMPLEX** - Optimize algorithm complexity
- **MEMO-RESULT** - Memoize expensive computations
- **LAZY-EVAL** - Use lazy evaluation
- **AVOID-CLOSURE-LOOP** - Fix closure issues in loops
- **DEBOUNCE-THROTTLE** - Debounce/throttle frequent events

## Key Differentiators

### SOLID Principles Coverage

Full coverage of SOLID principles with concrete JavaScript/TypeScript examples:
- **Single Responsibility Principle** - One reason to change
- **Open/Closed Principle** - Open for extension, closed for modification
- **Liskov Substitution Principle** - Subtypes must be substitutable
- **Dependency Inversion Principle** - Depend on abstractions

### Modern JavaScript Focus

Emphasizes ES6+ features and patterns:
- Arrow functions, template literals
- Destructuring, spread/rest operators
- Optional chaining, nullish coalescing
- async/await instead of callbacks
- Array methods (map, filter, reduce)
- const/let instead of var

### Testability Emphasis

Strong focus on making code testable:
- Dependency injection
- Pure functions
- Separation of concerns
- Avoiding global state
- Loose coupling

### Before/After Examples

Every guideline includes:
- Concrete "bad code" example showing the problem
- Refactored "good code" showing the solution
- Explanation of why it matters
- Code smell being addressed

## Common Patterns This Skill Teaches

### ✅ Do This
```javascript
// Pure function - easy to test
function calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### ❌ Not This
```javascript
// Impure function - uses external state
let total = 0;
function addToTotal(price) {
    total += price; // Side effect
}
```

### ✅ Do This
```javascript
// Dependency injection
class UserService {
    constructor(database, emailService) {
        this.db = database;
        this.emailer = emailService;
    }
}
```

### ❌ Not This
```javascript
// Hard-coded dependencies
class UserService {
    constructor() {
        this.db = new Database(); // Hard to test
        this.emailer = new EmailService(); // Hard to test
    }
}
```

### ✅ Do This
```javascript
// Modern async/await
async function fetchUser(id) {
    const response = await fetch(`/api/users/${id}`);
    return response.json();
}
```

### ❌ Not This
```javascript
// Callback hell
function fetchUser(id, callback) {
    fetch(`/api/users/${id}`, (err, response) => {
        if (err) {
            callback(err);
        } else {
            response.json((err, data) => {
                callback(err, data);
            });
        }
    });
}
```

## Example Use Cases

### Code Review
- "Review this pull request for code smells"
- "Check if this code follows SOLID principles"
- "Identify refactoring opportunities in this module"

### Legacy Code Improvement
- "Help me refactor this legacy callback-based code to async/await"
- "This function is 200 lines long - how should I break it down?"
- "Improve the testability of this tightly-coupled code"

### Learning Best Practices
- "Show me how to apply the Single Responsibility Principle"
- "What are the code smells in this class?"
- "How can I make this more maintainable?"

### Performance Optimization
- "This algorithm is slow - how can I optimize it?"
- "Should I memoize this expensive calculation?"
- "How can I reduce unnecessary re-renders?"

## Benefits

- ✓ **Identify code smells** - Long functions, god classes, duplication
- ✓ **Apply SOLID principles** - Better OOP design
- ✓ **Write testable code** - Dependency injection, pure functions
- ✓ **Use modern JavaScript** - ES6+, async/await, functional patterns
- ✓ **Improve performance** - Algorithm optimization, memoization
- ✓ **Learn refactoring** - Concrete before/after examples
- ✓ **Maintain quality** - Readable, maintainable, testable code

## What Gets Checked

### Code Smells
- Long functions/methods (>20 lines)
- God classes (doing too much)
- Duplicate code (DRY violations)
- Magic numbers
- Complex conditionals
- Long parameter lists
- Callback hell
- Tight coupling

### SOLID Principles
- Single Responsibility violations
- Open/Closed violations
- Liskov Substitution violations
- Dependency Inversion violations
- Interface Segregation (when applicable)

### Modern JavaScript
- Using var instead of const/let
- String concatenation instead of template literals
- Callbacks instead of async/await
- Manual loops instead of array methods
- Missing destructuring opportunities
- Missing optional chaining

### Testability
- Hard-coded dependencies
- Global state usage
- Side effects in functions
- Hidden dependencies
- Tight coupling

### Performance
- Inefficient algorithms (O(n²) when O(n) possible)
- Missing memoization opportunities
- Unnecessary computations
- Closure issues in loops
- Unthrottled event handlers

## Supported Languages

- **JavaScript** (ES6+)
- **TypeScript**
- **Node.js**
- **React** (component refactoring)
- **Vue** (component refactoring)
- **Express** (backend refactoring)

## Sources and Attribution

All guidelines are based on:
- **Refactoring Guru** - Comprehensive refactoring catalog
- **clean-code-javascript** - JavaScript adaptation of Clean Code
- **SOLID Principles** - Object-oriented design principles
- **Martin Fowler** - Refactoring: Improving the Design of Existing Code
- **Kent Beck** - Extreme Programming
- **Modern JavaScript Best Practices** - ES6+ patterns

See [SOURCES.md](./SOURCES.md) for detailed attribution and references.

## Refactoring Philosophy

### Make It Work, Make It Right, Make It Fast

1. **Make it work** - Get the functionality right first
2. **Make it right** - Refactor for readability and maintainability (this skill)
3. **Make it fast** - Optimize performance when needed

### The Boy Scout Rule

> "Always leave the code better than you found it."

### Refactoring vs. Rewriting

This skill focuses on **incremental refactoring** - small, safe steps that improve code quality without changing behavior. Not complete rewrites.

### When to Refactor

- Before adding new features (make room)
- When you understand code better (clarify intent)
- During code review (improve quality)
- When fixing bugs (prevent future bugs)
- When tests are hard to write (improve testability)

### When NOT to Refactor

- When the code works and is clear enough
- When the abstraction cost exceeds the benefit
- When you're on a deadline (technical debt is sometimes OK)
- When the code will be deleted soon

## Tips for Getting the Most Out of This Skill

1. **Paste your code**: Include the actual code you want reviewed
2. **Specify concerns**: "Focus on testability" or "Check for SOLID violations"
3. **Ask about trade-offs**: "When should I apply this refactoring?"
4. **Request specific patterns**: "Show me how to use dependency injection here"
5. **Iterate**: Apply one refactoring, then ask for another review

## Quick Reference

When you see these code smells:
- **100+ line functions** → Extract smaller functions
- **Class with 20+ methods** → Extract classes, apply SRP
- **Repeated code blocks** → DRY principle, extract common logic
- **if/else chains** → Polymorphism, strategy pattern
- **Callbacks 3+ levels deep** → async/await
- **Hard to test** → Dependency injection, pure functions
- **var keyword** → Use const/let
- **|| for defaults with 0** → Use nullish coalescing (??)

## License

This skill is licensed under MIT. It is based on public refactoring catalogs, design principles, and JavaScript best practices.

---

**Make it work. Make it right. Make it fast. This skill helps with "make it right".**
