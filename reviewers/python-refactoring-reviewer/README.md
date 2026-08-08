# Python Refactoring Code Reviewer Skill

A Claude Code skill that reviews Python code for refactoring opportunities to improve readability, maintainability, testability, and performance using established refactoring patterns and best practices.

## What This Skill Does

This skill transforms Claude into a refactoring expert who:
- Identifies refactoring opportunities in Python code
- Detects code smells (Bloaters, Complexity, Coupling)
- Applies SOLID principles and DRY
- Suggests Pythonic patterns and idioms
- Provides concrete before/after refactoring examples
- References established refactoring catalogs (Refactoring Guru, clean-code-python)

## Installation

Use the [repository-wide installer](../../README.md#installation-and-use) and pass this reviewer directory name to `--skill`.

## How to Use

Simply ask Claude to review your Python code for refactoring:

```
"Refactor this code for better readability"
"Review this for code smells"
"How can I improve this code?"
"Apply SOLID principles to this class"
"Make this code more Pythonic"
"Improve maintainability of this function"
```

The skill will automatically activate based on keywords like:
- refactor, refactoring, improve
- code smell, clean code
- SOLID, DRY, maintainability
- readability, simplify

## What You'll Get

A structured refactoring review with:
- ✅ **Strengths** - What's well-designed (with mnemonic IDs)
- 🔨 **Refactoring Opportunities** - Issues with intent + mnemonic ID (e.g., **READABILITY: EXTRACT-METHOD**)
- **Before/After Code** - Concrete refactoring examples
- **Code Smell Addressed** - What problem is being fixed
- **Why This Matters** - Benefits explained

### Example Review

````markdown
## Refactoring Review: order_processor.py

### ✅ Strengths
- **MEANINGFUL-NAME**: Clear variable names throughout (order_total, customer_email)
- **DIP-VIOLATION**: Good use of dependency injection for database

### 🔨 Refactoring Opportunities

#### READABILITY: EXTRACT-METHOD - Complex order processing

**Current code:**
```python
def process_order(order):
    # Validation
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Negative total")

    # Tax calculation
    tax_rate = 0.08
    tax = order.subtotal * tax_rate

    # Discount
    if order.customer.is_premium:
        discount = order.subtotal * 0.1
    else:
        discount = 0

    # Total
    order.total = order.subtotal + tax - discount

    # Notification
    send_email(order.customer.email, f"Order: ${order.total}")
```

**Refactored code:**
```python
def process_order(order):
    validate_order(order)
    tax = calculate_tax(order.subtotal)
    discount = calculate_discount(order)
    order.total = calculate_final_total(order.subtotal, tax, discount)
    send_order_confirmation(order)

def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Negative total")

def calculate_tax(subtotal):
    TAX_RATE = 0.08
    return subtotal * TAX_RATE

def calculate_discount(order):
    PREMIUM_DISCOUNT_RATE = 0.1
    if order.customer.is_premium:
        return order.subtotal * PREMIUM_DISCOUNT_RATE
    return 0

def calculate_final_total(subtotal, tax, discount):
    return subtotal + tax - discount

def send_order_confirmation(order):
    message = f"Order confirmed: ${order.total}"
    send_email(order.customer.email, message)
```

**Why this matters:**
- Each function has single responsibility
- Easier to test individual components
- Self-documenting structure
- Reusable logic

**Code smell addressed:**
Long Method - broke down 30-line function into focused 5-line functions

---

#### MAINTAINABILITY: SRP-VIOLATION - Order class doing too much

**Current code:**
```python
class Order:
    def calculate_total(self):
        pass

    def save_to_database(self):
        pass

    def send_confirmation_email(self):
        pass
```

**Refactored code:**
```python
class Order:
    def calculate_total(self):
        pass

class OrderRepository:
    def save(self, order):
        pass

class OrderNotifier:
    def send_confirmation(self, order):
        pass
```

**Why this matters:**
- Single Responsibility Principle
- Each class has one reason to change
- Better separation of concerns
- Easier to test in isolation

**Code smell addressed:**
SRP Violation - Order had multiple responsibilities (calculation, persistence, notification)

### 💡 Refactoring Wisdom
> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand."
> — Martin Fowler, Refactoring
````

## The 70 Guidelines

### Organized by Intent

1. **Readability** (18 guidelines)
   - MEANINGFUL-NAME, PRONOUNCE-NAME, SEARCHABLE-NAME, AVOID-MENTAL-MAP
   - EXTRACT-METHOD, EXTRACT-VAR, DECOMPOSE-COND
   - LONG-FUNC, LONG-PARAM, MAGIC-NUM
   - COMMENT-WHY, COMMENT-SMELL, NESTED-DEEP
   - GUARD-CLAUSE, POSITIVE-COND, POLY-COND
   - RENAME-METHOD, SINGLE-PURPOSE, EXPLAIN-VAR

2. **Maintainability** (17 guidelines)
   - DRY-VIOLATION, EXTRACT-CLASS, DUPLICATE-CODE
   - SRP-VIOLATION, OCP-VIOLATION, LSP-VIOLATION, ISP-VIOLATION, DIP-VIOLATION
   - GOD-CLASS, DATA-CLASS, LAZY-CLASS
   - FEATURE-ENVY, MESSAGE-CHAIN, MIDDLE-MAN
   - SHOT-GUN, DIVERGENT-CHANGE, PARALLEL-HIER

3. **Testability** (8 guidelines)
   - PURE-FUNC, INJECT-DEP, SEPARATE-QUERY
   - HIDDEN-DEP, GLOBAL-STATE, TIGHTLY-COUPLED
   - EXTRACT-INTERFACE, FACTORY-METHOD

4. **Code Smells - Bloaters** (5 guidelines)
   - LONG-METHOD, LARGE-CLASS, LONG-PARAM-LIST
   - PRIMITIVE-OBS, DATA-CLUMP

5. **Code Smells - Complexity** (5 guidelines)
   - SWITCH-STMT, NESTED-COND, COMPLEX-BOOL
   - TEMP-FIELD, ALT-CLASSES

6. **Pythonic Patterns** (10 guidelines)
   - LIST-COMP, DICT-COMP, SET-COMP
   - GENERATOR-EXPR, CONTEXT-MGR, DECORATOR-USE
   - ENUMERATE-USE, ZIP-USE, UNPACK-USE, F-STRING

7. **Performance** (7 guidelines)
   - ALGO-COMPLEX, PREMATURE-OPT, CACHE-RESULT
   - GEN-NOT-LIST, SLOT-USE, LAZY-EVAL, AVOID-COPY

All 70 guidelines with complete code examples are embedded in SKILL.md.

## Intent Categories Explained

### Readability
Focus: Making code easier to understand
- Clear naming conventions
- Reduced complexity
- Self-documenting structure

### Maintainability
Focus: Making code easier to change
- DRY (Don't Repeat Yourself)
- SOLID principles
- Proper separation of concerns

### Testability
Focus: Making code easier to test
- Pure functions
- Dependency injection
- Isolated components

### Code Smells
Focus: Detecting problematic patterns
- Bloaters (too big)
- Complexity (too complex)
- Coupling (too dependent)

### Pythonic
Focus: Idiomatic Python
- Comprehensions
- Generators
- Context managers
- Built-in patterns

### Performance
Focus: Efficiency without premature optimization
- Algorithm choice
- Lazy evaluation
- Caching strategies

## Example Use Cases

### Readability Review
```
"Review this function for readability"
"Can you simplify this nested conditional?"
"How can I make this more self-documenting?"
```

### Maintainability Review
```
"Apply SOLID principles to this class"
"Is this code DRY?"
"Review for separation of concerns"
```

### Code Smell Detection
```
"Check for code smells"
"Is this a God class?"
"Detect long methods"
```

### Pythonic Patterns
```
"Make this more Pythonic"
"Can I use a comprehension here?"
"Should this be a generator?"
```

### Performance Review
```
"Optimize this algorithm"
"Is this efficient?"
"Should I cache this result?"
```

## Benefits

- ✅ **Comprehensive** - 70 refactoring guidelines across 7 categories
- ✅ **Actionable** - Concrete before/after code examples
- ✅ **Educational** - Explains why each refactoring matters
- ✅ **Practical** - Based on established refactoring catalogs
- ✅ **Balanced** - Considers readability, maintainability, and performance
- ✅ **Python-Focused** - Pythonic patterns and idioms

## Refactoring Process

The skill guides you through effective refactoring:

1. **Ensure Tests Exist** - Write tests if needed
2. **Small Steps** - One refactoring at a time
3. **Run Tests** - After each change
4. **Commit Frequently** - Track progress
5. **Review** - Is code better?

## Common Refactoring Techniques Covered

**Composing Methods**
- Extract Method, Inline Method
- Extract Variable, Replace Temp with Query

**Moving Features**
- Move Method, Extract Class

**Organizing Data**
- Replace Magic Number, Encapsulate Field
- Replace Primitives with Objects

**Simplifying Conditionals**
- Decompose Conditional, Guard Clauses
- Replace Conditional with Polymorphism

**Simplifying Method Calls**
- Rename Method, Introduce Parameter Object
- Separate Query from Modifier

**SOLID Principles**
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

## When to Use This Skill

- **Legacy Code** - Improving existing codebases
- **Code Reviews** - Systematic quality checks
- **Learning** - Understanding best practices
- **Refactoring Sessions** - Structured improvements
- **Team Standards** - Establishing coding guidelines

## Skill Philosophy

> "Refactoring is the process of changing a software system in such a way that it does not alter the external behavior of the code yet improves its internal structure."
> — Martin Fowler

This skill helps you:
- Preserve behavior while improving structure
- Make code easier to understand
- Make code cheaper to modify
- Apply proven patterns and principles

## Sources and Attribution

This skill is based on established refactoring catalogs and best practices:
- **Refactoring Guru** - Code smells and refactoring catalog
- **clean-code-python** (MIT License) - Clean Code principles for Python
- **Martin Fowler** - Refactoring concepts and patterns
- **SOLID Principles** - Object-oriented design principles
- **Python Best Practices** - PEP 8, Pythonic idioms

**📚 [View Complete Sources Documentation →](SOURCES.md)**

The SOURCES.md file provides detailed attribution for all 70 guidelines, including:
- Specific catalog mappings (Refactoring Guru, clean-code-python)
- License information
- Code example sources
- Refactoring technique origins

## License

This skill is licensed under MIT. The sources referenced (Refactoring Guru with attribution, clean-code-python under MIT, and public Python best practices) remain under their respective licenses.

---

**Write Better Code. Refactor with Confidence.** 🔨✨
