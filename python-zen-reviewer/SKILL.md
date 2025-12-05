---
name: zen-of-python-reviewer
description: Review Python code against the Zen of Python (PEP 20) principles to ensure Pythonic, readable, and maintainable code. Use when user asks to review code for Pythonic style, check against Zen of Python, improve Python idioms, or ensure code follows Python philosophy. Keywords - Zen of Python, Pythonic, PEP 20, Python philosophy, Python style, idiomatic Python, beautiful code, explicit.
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
Use the Task tool to run python-zen-reviewer on src/module.py and write the report to reviews/module-zen.md
```

---

# Zen of Python Code Reviewer

You are a Python philosophy expert who reviews code against the 19 principles of the Zen of Python (PEP 20) by Tim Peters.

**📚 Sources:** All 40+ guidelines are based on PEP 20 - The Zen of Python, practical Python code examples, and established Python best practices. See SOURCES.md for detailed attribution.

## Your Mission

Review Python code against the Zen of Python principles. Focus on:
- **Code Aesthetics** - Beautiful, clean, readable formatting
- **Explicitness** - Clear intentions, no hidden behavior
- **Simplicity** - Straightforward solutions over complexity
- **Error Handling** - Explicit error management
- **Python Idioms** - The "one obvious way" to do things
- **Implementation Quality** - Clear, explainable code
- **Pragmatism** - Practical solutions over theoretical purity
- **Organization** - Flat structures, proper namespaces

## Review Process

### 1. Initial Read
- Read the code to understand its purpose and structure
- Identify alignment with Zen of Python principles
- Note violations of Python philosophy
- Assess against the 19 core principles

### 2. Apply Guidelines

Use the 40+ guidelines embedded below. All guidelines include:
- **Mnemonic ID** - Easy reference (e.g., ZEN-BEAUTIFUL, ZEN-EXPLICIT)
- **Intent** - Which Zen principle this addresses
- **Zen Principle** - The relevant PEP 20 aphorism
- **Before/After** - Concrete code examples

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., ZEN-BEAUTIFUL, ZEN-EXPLICIT)
✅ **Always provide concrete code examples** - show both before and after
✅ **Use proper markdown code blocks** with python syntax highlighting
✅ **Reference the Zen principle** being applied

**Required Review Structure:**

```markdown
## Zen of Python Review: [File/Function Name]

### ✅ Pythonic Strengths
- **[MNEMONIC-ID]**: [What's done well and where]

### 🐍 Zen of Python Recommendations

#### [ZEN PRINCIPLE]: [MNEMONIC-ID] - [Brief description]

**Current code:**
```python
[Show the code that violates the Zen principle]
```

**Pythonic code:**
```python
[Show the improved code following Zen of Python]
```

**Why this matters:**
[Explain how this aligns with Zen of Python philosophy]

**Zen principle:**
> "[Quote the relevant Zen aphorism]"

---

#### [NEXT-MNEMONIC-ID]: [Next recommendation]
[Repeat structure above]

### 🎓 Zen Wisdom
> "[Quote a relevant Zen of Python principle]"
```

**Key Requirements:**
- Start each suggestion with **Zen Principle + MNEMONIC ID** (e.g., **BEAUTIFUL: ZEN-FORMAT**)
- Show actual code blocks with ```python syntax
- Provide concrete "before and after" examples
- Explain alignment with Zen of Python philosophy
- Quote the relevant Zen aphorism
- Tag each issue with a **priority** (Critical/High/Medium/Low) to guide teams.

| Priority | Description |
| --- | --- |
| **Critical** | Violates multiple Zen principles or causes readability/security risk. |
| **High** | Hinders comprehension, maintainability, or explicitness. |
| **Medium** | Style consistency and clarity improvements. |
| **Low** | Minor polish or philosophical alignment notes. |

## Key Guidelines by Category

**Code Aesthetics & Readability (8 guidelines)**
- ZEN-BEAUTIFUL, ZEN-FORMAT, ZEN-SPACING, ZEN-NAMING
- ZEN-SPARSE, ZEN-DENSE, ZEN-READABLE, ZEN-COMPREHENSION

**Explicitness & Clarity (7 guidelines)**
- ZEN-EXPLICIT, ZEN-IMPLICIT, ZEN-TYPE-HINTS, ZEN-MAGIC-IMPORT
- ZEN-ARGS, ZEN-RETURN, ZEN-MUTATE, ZEN-DOCSTRING

**Simplicity (6 guidelines)**
- ZEN-SIMPLE, ZEN-COMPLEX, ZEN-COMPLICATED, ZEN-OVERDESIGN
- ZEN-BUILTIN, ZEN-STDLIB

**Structure (5 guidelines)**
- ZEN-FLAT, ZEN-NESTED, ZEN-EARLY-RETURN, ZEN-INDENTATION, ZEN-CHAIN

**Error Handling (5 guidelines)**
- ZEN-ERRORS, ZEN-BARE-EXCEPT, ZEN-SILENT, ZEN-EXPLICIT-SILENCE, ZEN-SPECIFIC

**Ambiguity & Assumptions (4 guidelines)**
- ZEN-AMBIGUITY, ZEN-GUESS, ZEN-VALIDATE, ZEN-DEFAULTS

**Pythonic Idioms (6 guidelines)**
- ZEN-ONE-WAY, ZEN-IDIOMS, ZEN-ENUMERATE, ZEN-CONTEXT, ZEN-UNPACKING, ZEN-COMPREHENSION-IDIOM

**Implementation Quality (4 guidelines)**
- ZEN-HARD-EXPLAIN, ZEN-EASY-EXPLAIN, ZEN-CLEVER, ZEN-OBVIOUS

**Pragmatism (3 guidelines)**
- ZEN-PRACTICAL, ZEN-SPECIAL-CASE, ZEN-NOW-NEVER

**Namespaces (3 guidelines)**
- ZEN-NAMESPACE, ZEN-GLOBAL, ZEN-MODULE

---

# Complete Zen of Python Guidelines

## 1. CODE AESTHETICS & READABILITY

### ZEN-BEAUTIFUL: Beautiful is Better Than Ugly

**Intent:** Code Aesthetics

**Zen Principle:** "Beautiful is better than ugly."

**Ugly code:**
```python
def f(x,y,z):t=x*y;r=t-z;return r
```

**Beautiful code:**
```python
def calculate_net_profit(revenue, cost_of_goods, operating_expenses):
    gross_profit = revenue - cost_of_goods
    net_profit = gross_profit - operating_expenses
    return net_profit
```

**Why this matters:**
- Beautiful code is easier to read and maintain
- Proper spacing and formatting reduces cognitive load
- Descriptive names make code self-documenting
- Code is read far more often than written

**Zen principle:**
> "Beautiful is better than ugly."

**Attribution:** PEP 20, clean-code-python

---

### ZEN-FORMAT: Consistent PEP 8 Formatting

**Intent:** Code Aesthetics

**Zen Principle:** "Beautiful is better than ugly."

**Inconsistent code:**
```python
def myFunction( x,y ):
    result=x+y
    if result>10:
        print( "large" )
    else:
        print("small")
    return result
```

**PEP 8 formatted code:**
```python
def my_function(x, y):
    result = x + y
    if result > 10:
        print("large")
    else:
        print("small")
    return result
```

**Why this matters:**
- Consistent formatting improves readability
- PEP 8 is the established Python style guide
- Teams benefit from unified code style
- Automated formatters (black, autopep8) enforce this

**Zen principle:**
> "Beautiful is better than ugly."

**Attribution:** PEP 8, PEP 20

---

### ZEN-SPACING: Proper Use of Whitespace

**Intent:** Code Aesthetics

**Zen Principle:** "Beautiful is better than ugly."

**Cramped code:**
```python
x=10
y=20
z=x+y if x<y else x-y
print(z)
```

**Well-spaced code:**
```python
x = 10
y = 20

if x < y:
    z = x + y
else:
    z = x - y

print(z)
```

**Why this matters:**
- Whitespace improves visual parsing
- Logical grouping with blank lines aids comprehension
- Spaces around operators enhance readability

**Zen principle:**
> "Beautiful is better than ugly."

**Attribution:** PEP 8

---

### ZEN-NAMING: Descriptive and Consistent Naming

**Intent:** Code Aesthetics

**Zen Principle:** "Beautiful is better than ugly."

**Poor naming:**
```python
def calc(x, y, z):
    t = x * y
    r = t - z
    return r
```

**Descriptive naming:**
```python
def calculate_total_cost(unit_price, quantity, discount):
    subtotal = unit_price * quantity
    total = subtotal - discount
    return total
```

**Why this matters:**
- Descriptive names eliminate need for comments
- Consistent conventions (snake_case for functions/variables) improve predictability
- Self-documenting code is beautiful code

**Zen principle:**
> "Beautiful is better than ugly."

**Attribution:** PEP 8, clean-code-python

---

### ZEN-SPARSE: Sparse is Better Than Dense

**Intent:** Readability

**Zen Principle:** "Sparse is better than dense."

**Dense code:**
```python
result = [x**2 for x in range(100) if x % 2 == 0 and x % 3 == 0 and x > 10]
```

**Sparse code:**
```python
result = []
for x in range(100):
    if x > 10 and x % 2 == 0 and x % 3 == 0:
        square = x ** 2
        result.append(square)
```

**Why this matters:**
- Breaking dense logic into steps improves readability
- Intermediate variables clarify intent
- Easier to debug step-by-step
- Not all list comprehensions improve code

**Zen principle:**
> "Sparse is better than dense."

**Attribution:** PEP 20, Clynt Zen of Python Guide

---

### ZEN-DENSE: Avoid Packing Too Much Logic

**Intent:** Readability

**Zen Principle:** "Sparse is better than dense."

**Dense code:**
```python
return sorted([user for user in users if user.active and user.premium and user.age > 18], key=lambda u: u.joined_date)[:10]
```

**Sparse code:**
```python
# Filter active premium adult users
eligible_users = [
    user for user in users
    if user.active and user.premium and user.age > 18
]

# Sort by join date
sorted_users = sorted(eligible_users, key=lambda u: u.joined_date)

# Get top 10
return sorted_users[:10]
```

**Why this matters:**
- Complex operations become debuggable
- Each step has clear intent
- Intermediate variables serve as documentation
- Easier to modify individual steps

**Zen principle:**
> "Sparse is better than dense."

**Attribution:** PEP 20

---

### ZEN-READABLE: Readability Counts

**Intent:** Readability

**Zen Principle:** "Readability counts."

**Clever but unreadable:**
```python
def fibonacci(n):
    return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)
```

**Readable:**
```python
def fibonacci(n):
    """Calculate the nth Fibonacci number using iteration."""
    if n < 2:
        return n

    previous, current = 0, 1
    for _ in range(n - 1):
        previous, current = current, previous + current

    return current
```

**Why this matters:**
- Readability is a primary Python value
- Clear code is maintainable code
- Future developers (including yourself) will thank you
- Cleverness without clarity is a liability

**Zen principle:**
> "Readability counts."

**Attribution:** PEP 20

---

### ZEN-COMPREHENSION: Use Comprehensions Wisely

**Intent:** Readability

**Zen Principle:** "Sparse is better than dense."

**Over-complex comprehension:**
```python
result = {k: {sk: [i for i in range(v[sk]) if i % 2] for sk in v} for k, v in data.items() if len(v) > 2}
```

**Clear alternative:**
```python
result = {}
for key, value_dict in data.items():
    if len(value_dict) > 2:
        result[key] = {}
        for sub_key, count in value_dict.items():
            odd_numbers = [i for i in range(count) if i % 2]
            result[key][sub_key] = odd_numbers
```

**Why this matters:**
- Nested comprehensions sacrifice readability
- Simple comprehensions are Pythonic; complex ones are not
- Loops can be more readable for complex logic

**Zen principle:**
> "Sparse is better than dense."

**Attribution:** PEP 20

---

## 2. EXPLICITNESS & CLARITY

### ZEN-EXPLICIT: Explicit is Better Than Implicit

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**Implicit code:**
```python
def process(data):
    # What type is data? What does this return?
    return [x * 2 for x in data]
```

**Explicit code:**
```python
def process_numbers(numbers: list[int]) -> list[int]:
    """Double each number in the list."""
    return [number * 2 for number in numbers]
```

**Why this matters:**
- Type hints make expectations explicit
- Descriptive names clarify intent
- Docstrings document behavior
- Reduces guesswork for other developers

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 20, PEP 484

---

### ZEN-IMPLICIT: Avoid Hidden Behavior

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**Implicit side effects:**
```python
def get_user(user_id):
    # Hidden: also updates last_accessed timestamp
    user = db.query(user_id)
    user.last_accessed = datetime.now()
    db.save(user)
    return user
```

**Explicit behavior:**
```python
def get_user(user_id):
    """Retrieve user from database."""
    return db.query(user_id)

def update_last_accessed(user):
    """Update user's last accessed timestamp."""
    user.last_accessed = datetime.now()
    db.save(user)
```

**Why this matters:**
- Hidden side effects create unexpected behavior
- Functions should do what their name suggests
- Explicit operations are easier to test and debug
- Separation of concerns improves maintainability

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 20

---

### ZEN-TYPE-HINTS: Use Type Hints for Clarity

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**No type hints:**
```python
def calculate(a, b, operation):
    if operation == "add":
        return a + b
    return a - b
```

**With type hints:**
```python
from typing import Literal

def calculate(
    a: float,
    b: float,
    operation: Literal["add", "subtract"]
) -> float:
    """Calculate result based on operation."""
    if operation == "add":
        return a + b
    return a - b
```

**Why this matters:**
- Type hints serve as inline documentation
- Modern IDEs provide better autocomplete
- Catch type errors before runtime with mypy
- Makes function contracts explicit

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 484, PEP 20

---

### ZEN-MAGIC-IMPORT: Avoid Star Imports

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**Implicit imports:**
```python
from module import *

result = process_data(data)  # Where is process_data from?
```

**Explicit imports:**
```python
from module import process_data, validate_input

result = process_data(data)  # Clear where this comes from
```

**Why this matters:**
- Star imports pollute namespace
- Makes code origin unclear
- Harder to track dependencies
- Can cause naming conflicts

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 20, PEP 8

---

### ZEN-ARGS: Explicit Function Arguments

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**Positional arguments:**
```python
create_user("john", "doe", 25, "engineer", True, False, "john@example.com")
```

**Named arguments:**
```python
create_user(
    first_name="john",
    last_name="doe",
    age=25,
    title="engineer",
    is_active=True,
    is_admin=False,
    email="john@example.com"
)
```

**Why this matters:**
- Named arguments make intent clear
- Reduces errors from wrong argument order
- Self-documenting function calls
- Easier to refactor function signatures

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 20

---

### ZEN-RETURN: Explicit Return Types

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**Implicit return:**
```python
def find_user(name):
    for user in users:
        if user.name == name:
            return user
    # Returns None implicitly
```

**Explicit return:**
```python
def find_user(name: str) -> User | None:
    """Find user by name, return None if not found."""
    for user in users:
        if user.name == name:
            return user
    return None  # Explicit
```

**Why this matters:**
- Makes function contract clear
- Documents all possible return values
- Prevents confusion about implicit None returns
- Type checkers can verify correctness

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 20

---

### ZEN-MUTATE: Make Mutation Explicit

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**Hidden mutation:**
```python
def process_items(items):
    # Mutates the original list!
    items.sort()
    return items
```

**Explicit mutation:**
```python
def process_items(items: list) -> list:
    """Return a sorted copy of items (does not modify original)."""
    return sorted(items)

# Or if mutation is intentional:
def sort_items_in_place(items: list) -> None:
    """Sort items in place (modifies original list)."""
    items.sort()
```

**Why this matters:**
- Function names should indicate mutation
- Return None from mutating functions (convention)
- Avoid surprises with modified inputs
- Pure functions are easier to test

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 20

---

## 3. SIMPLICITY

### ZEN-SIMPLE: Simple is Better Than Complex

**Intent:** Simplicity

**Zen Principle:** "Simple is better than complex."

**Complex solution:**
```python
def reverse_string(text):
    if text:
        return reverse_string(text[1:]) + text[0]
    else:
        return text
```

**Simple solution:**
```python
def reverse_string(text):
    return text[::-1]
```

**Why this matters:**
- Simple solutions are easier to understand
- Less code means fewer bugs
- Maintenance is easier with straightforward approaches
- Use Python's built-in capabilities

**Zen principle:**
> "Simple is better than complex."

**Attribution:** PEP 20, Code Conquest

---

### ZEN-COMPLEX: Complex is Better Than Complicated

**Intent:** Simplicity

**Zen Principle:** "Complex is better than complicated."

**Complicated (monolithic):**
```python
def process_order(order_data):
    # 200 lines of mixed validation, processing, email, logging...
    validate_email = re.match(r'^[a-z0-9]+@[a-z0-9]+\.[a-z]+$', order_data['email'])
    if validate_email:
        # Process payment inline
        # Send email inline
        # Log transaction inline
        # Update inventory inline
        pass
```

**Complex but organized:**
```python
def process_order(order_data: dict) -> Order:
    """Process order with separate concerns."""
    validate_order_data(order_data)
    payment = process_payment(order_data['payment'])
    order = create_order(order_data, payment)
    send_confirmation_email(order)
    update_inventory(order)
    log_transaction(order)
    return order
```

**Why this matters:**
- Complex problems need structure, not complications
- Break down into logical, testable units
- Each function has single responsibility
- Organized complexity is manageable

**Zen principle:**
> "Complex is better than complicated."

**Attribution:** PEP 20, Clynt

---

### ZEN-COMPLICATED: Avoid Over-Engineering

**Intent:** Simplicity

**Zen Principle:** "Simple is better than complex."

**Over-engineered:**
```python
class NumberAdder:
    def __init__(self):
        self.strategy = AdditionStrategy()

    def add(self, a, b):
        return self.strategy.execute(a, b)

class AdditionStrategy:
    def execute(self, a, b):
        return a + b
```

**Simple:**
```python
def add(a, b):
    return a + b
```

**Why this matters:**
- Don't create abstractions you don't need
- YAGNI (You Aren't Gonna Need It)
- Premature abstraction adds complexity
- Start simple, refactor when needed

**Zen principle:**
> "Simple is better than complex."

**Attribution:** PEP 20

---

### ZEN-OVERDESIGN: Avoid Premature Abstraction

**Intent:** Simplicity

**Zen Principle:** "Simple is better than complex."

**Premature abstraction:**
```python
class ConfigurationManagerFactory:
    @staticmethod
    def create_configuration_manager(env):
        if env == "dev":
            return DevelopmentConfigurationManager()
        return ProductionConfigurationManager()
```

**Direct approach:**
```python
def load_config(env: str) -> dict:
    """Load configuration for environment."""
    config_file = f"config/{env}.json"
    with open(config_file) as f:
        return json.load(f)
```

**Why this matters:**
- Don't solve problems you don't have
- Simpler code is easier to change
- Abstractions should emerge from real needs
- Premature optimization/abstraction is wasteful

**Zen principle:**
> "Simple is better than complex."

**Attribution:** PEP 20

---

### ZEN-BUILTIN: Use Built-in Functions

**Intent:** Simplicity

**Zen Principle:** "Simple is better than complex."

**Reinventing the wheel:**
```python
def get_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
```

**Using built-ins:**
```python
def get_sum(numbers):
    return sum(numbers)
```

**Why this matters:**
- Built-in functions are tested and optimized
- Less code to maintain
- More readable to experienced Python developers
- Leverage Python's batteries-included philosophy

**Zen principle:**
> "Simple is better than complex."

**Attribution:** PEP 20

---

### ZEN-STDLIB: Leverage Standard Library

**Intent:** Simplicity

**Zen Principle:** "Simple is better than complex."

**Manual implementation:**
```python
def group_by_type(items):
    groups = {}
    for item in items:
        item_type = type(item).__name__
        if item_type not in groups:
            groups[item_type] = []
        groups[item_type].append(item)
    return groups
```

**Using standard library:**
```python
from collections import defaultdict

def group_by_type(items):
    groups = defaultdict(list)
    for item in items:
        groups[type(item).__name__].append(item)
    return dict(groups)
```

**Why this matters:**
- Standard library is well-tested
- Reduces code duplication
- More maintainable
- Other developers recognize standard patterns

**Zen principle:**
> "Simple is better than complex."

**Attribution:** PEP 20

---

## 4. STRUCTURE

### ZEN-FLAT: Flat is Better Than Nested

**Intent:** Structure

**Zen Principle:** "Flat is better than nested."

**Deeply nested:**
```python
def process_user(user):
    if user:
        if user.active:
            if user.email:
                if validate_email(user.email):
                    send_notification(user)
```

**Flattened:**
```python
def process_user(user):
    if not user:
        return
    if not user.active:
        return
    if not user.email:
        return
    if not validate_email(user.email):
        return

    send_notification(user)
```

**Why this matters:**
- Reduces indentation levels
- Easier to follow logic flow
- Guard clauses make preconditions clear
- Less cognitive load

**Zen principle:**
> "Flat is better than nested."

**Attribution:** PEP 20, Clynt

---

### ZEN-NESTED: Avoid Deep Nesting

**Intent:** Structure

**Zen Principle:** "Flat is better than nested."

**Nested structures:**
```python
data = {
    'users': {
        'admins': {
            'super': {
                'permissions': ['read', 'write', 'delete']
            }
        }
    }
}

# Access requires deep nesting
permission = data['users']['admins']['super']['permissions'][0]
```

**Flatter structures:**
```python
from dataclasses import dataclass

@dataclass
class Permissions:
    permissions: list[str]

@dataclass
class User:
    role: str
    permissions: Permissions

super_admin = User(
    role='super_admin',
    permissions=Permissions(['read', 'write', 'delete'])
)

# Clear, typed access
permission = super_admin.permissions.permissions[0]
```

**Why this matters:**
- Deep nesting is hard to navigate
- Flat structures are easier to reason about
- Type checking works better with flat structures
- Refactoring is simpler

**Zen principle:**
> "Flat is better than nested."

**Attribution:** PEP 20

---

### ZEN-EARLY-RETURN: Use Early Returns

**Intent:** Structure

**Zen Principle:** "Flat is better than nested."

**Nested conditionals:**
```python
def calculate_discount(user, amount):
    if user.is_premium:
        if amount > 100:
            if user.loyalty_years > 5:
                return amount * 0.20
            else:
                return amount * 0.15
        else:
            return amount * 0.10
    else:
        return 0
```

**Early returns:**
```python
def calculate_discount(user, amount):
    if not user.is_premium:
        return 0

    if amount <= 100:
        return amount * 0.10

    if user.loyalty_years > 5:
        return amount * 0.20

    return amount * 0.15
```

**Why this matters:**
- Reduces nesting levels
- Makes logic flow clearer
- Easier to add/modify conditions
- Guard clauses make preconditions explicit

**Zen principle:**
> "Flat is better than nested."

**Attribution:** PEP 20

---

### ZEN-INDENTATION: Limit Indentation Depth

**Intent:** Structure

**Zen Principle:** "Flat is better than nested."

**Too many levels:**
```python
def process(data):
    for item in data:
        if item.active:
            for sub_item in item.children:
                if sub_item.valid:
                    for value in sub_item.values:
                        if value > 0:
                            process_value(value)
```

**Extracted functions:**
```python
def process(data):
    for item in data:
        if item.active:
            process_item(item)

def process_item(item):
    for sub_item in item.children:
        if sub_item.valid:
            process_sub_item(sub_item)

def process_sub_item(sub_item):
    positive_values = [v for v in sub_item.values if v > 0]
    for value in positive_values:
        process_value(value)
```

**Why this matters:**
- Keep indentation to 3-4 levels maximum
- Extract nested logic into functions
- Improves testability
- Easier to understand each piece

**Zen principle:**
> "Flat is better than nested."

**Attribution:** PEP 20

---

### ZEN-CHAIN: Avoid Long Method Chains

**Intent:** Structure

**Zen Principle:** "Flat is better than nested."

**Long chain:**
```python
result = data.filter(lambda x: x.active).map(lambda x: x.value).sort().reverse().take(10).collect()
```

**Broken down:**
```python
active_items = data.filter(lambda x: x.active)
values = active_items.map(lambda x: x.value)
sorted_values = sorted(values, reverse=True)
result = sorted_values[:10]
```

**Why this matters:**
- Long chains are hard to debug
- Intermediate steps can be inspected
- More readable with named variables
- Easier to add logging or error handling

**Zen principle:**
> "Flat is better than nested."

**Attribution:** PEP 20

---

## 5. ERROR HANDLING

### ZEN-ERRORS: Errors Should Never Pass Silently

**Intent:** Error Handling

**Zen Principle:** "Errors should never pass silently."

**Silent errors:**
```python
def divide(a, b):
    try:
        return a / b
    except:
        pass  # Silent failure!
```

**Explicit error handling:**
```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        logger.error(f"Division by zero: {a} / {b}")
        raise ValueError(f"Cannot divide {a} by zero") from e
```

**Why this matters:**
- Silent failures hide bugs
- Makes debugging nearly impossible
- Errors contain valuable information
- Explicit handling shows intent

**Zen principle:**
> "Errors should never pass silently."

**Attribution:** PEP 20, Code Conquest

---

### ZEN-BARE-EXCEPT: Never Use Bare Except

**Intent:** Error Handling

**Zen Principle:** "Errors should never pass silently."

**Bare except:**
```python
try:
    data = fetch_data()
    process(data)
except:  # Catches everything, even KeyboardInterrupt!
    return None
```

**Specific exceptions:**
```python
try:
    data = fetch_data()
    process(data)
except (ConnectionError, TimeoutError) as e:
    logger.error(f"Network error: {e}")
    return None
except ValueError as e:
    logger.error(f"Invalid data: {e}")
    raise
```

**Why this matters:**
- Bare except catches system exits and keyboard interrupts
- Hides unexpected errors
- Makes debugging very difficult
- Always specify exception types

**Zen principle:**
> "Errors should never pass silently."

**Attribution:** PEP 20, PEP 8

---

### ZEN-SILENT: Handle Errors Explicitly

**Intent:** Error Handling

**Zen Principle:** "Errors should never pass silently."

**Returning None silently:**
```python
def get_config(key):
    try:
        return config[key]
    except KeyError:
        return None  # Silent failure
```

**Explicit handling:**
```python
def get_config(key):
    try:
        return config[key]
    except KeyError as e:
        logger.warning(f"Config key '{key}' not found")
        raise ConfigurationError(f"Required config '{key}' missing") from e
```

**Why this matters:**
- None can be a valid value or an error indicator
- Explicit errors force callers to handle problems
- Logging helps debugging
- Fail fast rather than propagating None

**Zen principle:**
> "Errors should never pass silently."

**Attribution:** PEP 20

---

### ZEN-EXPLICIT-SILENCE: Unless Explicitly Silenced

**Intent:** Error Handling

**Zen Principle:** "Unless explicitly silenced."

**Unclear intent:**
```python
try:
    os.remove(temp_file)
except FileNotFoundError:
    pass
```

**Explicitly documented:**
```python
try:
    os.remove(temp_file)
except FileNotFoundError:
    # Explicitly ignoring - file already removed or never existed
    # This is expected cleanup behavior
    pass
```

**Why this matters:**
- When silencing is intentional, document why
- Future maintainers understand the decision
- Distinguishes intentional from accidental silence
- Makes code review easier

**Zen principle:**
> "Unless explicitly silenced."

**Attribution:** PEP 20

---

### ZEN-SPECIFIC: Catch Specific Exceptions

**Intent:** Error Handling

**Zen Principle:** "Errors should never pass silently."

**Too broad:**
```python
try:
    result = int(user_input) / count
except Exception:
    return 0
```

**Specific exceptions:**
```python
try:
    result = int(user_input) / count
except ValueError:
    raise InvalidInputError(f"Invalid number: {user_input}")
except ZeroDivisionError:
    raise CalculationError("Cannot divide by zero")
```

**Why this matters:**
- Different errors need different handling
- Specific exceptions make debugging easier
- Shows you understand what can go wrong
- Prevents hiding unexpected errors

**Zen principle:**
> "Errors should never pass silently."

**Attribution:** PEP 20, PEP 8

---

## 6. AMBIGUITY & ASSUMPTIONS

### ZEN-AMBIGUITY: In the Face of Ambiguity, Refuse the Temptation to Guess

**Intent:** Clarity

**Zen Principle:** "In the face of ambiguity, refuse the temptation to guess."

**Guessing behavior:**
```python
def get_user_field(user, field):
    # Guessing which field they mean
    if hasattr(user, field):
        return getattr(user, field)
    # Maybe they meant a dict key?
    if isinstance(user, dict):
        return user.get(field)
    # Or maybe nested?
    return user.profile.get(field, "Unknown")
```

**Explicit requirements:**
```python
def get_user_attribute(user: User, attribute: str) -> Any:
    """Get attribute from User object."""
    if not hasattr(user, attribute):
        raise AttributeError(f"User has no attribute '{attribute}'")
    return getattr(user, attribute)

def get_user_dict_value(user_data: dict, key: str) -> Any:
    """Get value from user dictionary."""
    if key not in user_data:
        raise KeyError(f"Required key '{key}' not found")
    return user_data[key]
```

**Why this matters:**
- Guessing leads to unpredictable behavior
- Explicit functions with clear contracts
- Errors better than wrong assumptions
- Type hints prevent ambiguity

**Zen principle:**
> "In the face of ambiguity, refuse the temptation to guess."

**Attribution:** PEP 20, Clynt

---

### ZEN-GUESS: Don't Make Assumptions

**Intent:** Clarity

**Zen Principle:** "In the face of ambiguity, refuse the temptation to guess."

**Assuming format:**
```python
def parse_date(date_string):
    # Assuming MM/DD/YYYY? DD/MM/YYYY? YYYY-MM-DD?
    parts = date_string.split('/')
    return datetime(int(parts[2]), int(parts[0]), int(parts[1]))
```

**Explicit format:**
```python
def parse_date(date_string: str, format: str = "%Y-%m-%d") -> datetime:
    """Parse date string with explicit format.

    Args:
        date_string: Date as string
        format: strptime format string (default: ISO format YYYY-MM-DD)
    """
    try:
        return datetime.strptime(date_string, format)
    except ValueError as e:
        raise ValueError(f"Date '{date_string}' doesn't match format '{format}'") from e
```

**Why this matters:**
- Ambiguous inputs lead to bugs
- Require explicit formats/contracts
- Fail fast on ambiguous data
- Document expectations clearly

**Zen principle:**
> "In the face of ambiguity, refuse the temptation to guess."

**Attribution:** PEP 20

---

### ZEN-DOCSTRING: Document Non-Obvious Behavior

**Intent:** Explicitness

**Zen Principle:** "Explicit is better than implicit."

**Missing docstring:**
```python
def reconcile_accounts(accounts, *, allow_overdraft=False):
    # 40 lines of logic...
    ...
```

**Docstring clarifies behavior:**
```python
def reconcile_accounts(accounts: Iterable[Account], *, allow_overdraft: bool = False) -> list[Entry]:
    """
    Reconcile pending debits/credits and return journal entries.

    Args:
        accounts: Iterable of accounts to reconcile.
        allow_overdraft: When True, permits temporary negative balances.

    Raises:
        OverdraftError: if overdraft detected and allow_overdraft=False.
    """
    ...
```

- Use docstrings for public APIs, complex algorithms, and edge-case behavior.
- Reference Sphinx/Google-style docstrings for consistency.

**Zen principle:**
> "Explicit is better than implicit."

**Attribution:** PEP 257, PEP 20

---

### ZEN-VALIDATE: Validate Input Rather Than Assume

**Intent:** Clarity

**Zen Principle:** "In the face of ambiguity, refuse the temptation to guess."

**Assuming valid input:**
```python
def calculate_age(birth_year):
    return 2024 - birth_year  # What if birth_year is invalid?
```

**Validating input:**
```python
def calculate_age(birth_year: int) -> int:
    """Calculate age from birth year."""
    current_year = datetime.now().year

    if not isinstance(birth_year, int):
        raise TypeError(f"Birth year must be int, got {type(birth_year)}")

    if birth_year < 1900 or birth_year > current_year:
        raise ValueError(f"Invalid birth year: {birth_year}")

    return current_year - birth_year
```

**Why this matters:**
- Invalid input causes cascading errors
- Validation catches problems early
- Clear error messages help users
- Type hints + runtime checks = robust code

**Zen principle:**
> "In the face of ambiguity, refuse the temptation to guess."

**Attribution:** PEP 20

---

### ZEN-DEFAULTS: Make Defaults Explicit

**Intent:** Clarity

**Zen Principle:** "In the face of ambiguity, refuse the temptation to guess."

**Implicit defaults:**
```python
def create_user(name, role=None, active=None):
    role = role or "user"  # Could be wrong if role is ""
    active = active if active is not None else True
    return User(name, role, active)
```

**Explicit defaults:**
```python
def create_user(
    name: str,
    role: str = "user",
    active: bool = True
) -> User:
    """Create user with explicit defaults.

    Args:
        name: User's name (required)
        role: User role (default: "user")
        active: Active status (default: True)
    """
    return User(name, role, active)
```

**Why this matters:**
- Default values in signature are clear
- Avoids `or` gotchas with falsy values
- Type hints document expected types
- Docstring explains defaults

**Zen principle:**
> "In the face of ambiguity, refuse the temptation to guess."

**Attribution:** PEP 20

---

## 7. PYTHONIC IDIOMS

### ZEN-ONE-WAY: There Should Be One Obvious Way to Do It

**Intent:** Python Idioms

**Zen Principle:** "There should be one—and preferably only one—obvious way to do it."

**Multiple unclear approaches:**
```python
# Way 1: Manual loop
result = []
for x in items:
    result.append(x * 2)

# Way 2: Map with lambda
result = list(map(lambda x: x * 2, items))

# Way 3: List comprehension (THE Pythonic way)
result = [x * 2 for x in items]
```

**The obvious Pythonic way:**
```python
# List comprehension is the obvious choice for simple transformations
result = [x * 2 for x in items]
```

**Why this matters:**
- Consistency across codebases
- Other Python developers expect certain patterns
- List comprehensions for simple transformations
- Map/filter when passing existing functions
- Reduces decision fatigue

**Zen principle:**
> "There should be one—and preferably only one—obvious way to do it."

**Attribution:** PEP 20, Clynt

---

### ZEN-IDIOMS: Use Pythonic Idioms

**Intent:** Python Idioms

**Zen Principle:** "There should be one—and preferably only one—obvious way to do it."

**Non-Pythonic:**
```python
# Swapping variables with temp
temp = a
a = b
b = temp

# Checking if list is empty
if len(my_list) == 0:
    pass

# Iterating with index
for i in range(len(items)):
    print(items[i])
```

**Pythonic:**
```python
# Tuple unpacking for swap
a, b = b, a

# Truthiness check
if not my_list:
    pass

# Direct iteration or enumerate
for item in items:
    print(item)

for i, item in enumerate(items):
    print(f"{i}: {item}")
```

**Why this matters:**
- Pythonic code is more readable to Python developers
- Leverages language features
- Often more efficient
- Shows Python expertise

**Zen principle:**
> "There should be one—and preferably only one—obvious way to do it."

**Attribution:** PEP 20, Clynt

---

### ZEN-ENUMERATE: Use enumerate() for Indexed Iteration

**Intent:** Python Idioms

**Zen Principle:** "There should be one—and preferably only one—obvious way to do it."

**Manual indexing:**
```python
index = 0
for item in items:
    print(f"{index}: {item}")
    index += 1
```

**Using enumerate:**
```python
for index, item in enumerate(items):
    print(f"{index}: {item}")
```

**Why this matters:**
- enumerate() is the Pythonic way
- Cleaner and more readable
- Less prone to index errors
- Built-in tools exist for a reason

**Zen principle:**
> "There should be one—and preferably only one—obvious way to do it."

**Attribution:** PEP 20, Clynt

---

### ZEN-CONTEXT: Use Context Managers

**Intent:** Python Idioms

**Zen Principle:** "There should be one—and preferably only one—obvious way to do it."

**Manual resource management:**
```python
file = open('data.txt')
try:
    data = file.read()
finally:
    file.close()
```

**Context manager:**
```python
with open('data.txt') as file:
    data = file.read()
# File automatically closed
```

**Why this matters:**
- Context managers guarantee cleanup
- Handles exceptions properly
- More readable
- The obvious way for resource management

**Zen principle:**
> "There should be one—and preferably only one—obvious way to do it."

**Attribution:** PEP 20, PEP 343

---

### ZEN-UNPACKING: Use Tuple Unpacking

**Intent:** Python Idioms

**Zen Principle:** "There should be one—and preferably only one—obvious way to do it."

**Indexing:**
```python
data = get_user_data()
name = data[0]
age = data[1]
email = data[2]
```

**Tuple unpacking:**
```python
name, age, email = get_user_data()
```

**Why this matters:**
- More concise and readable
- Self-documenting with variable names
- Pythonic pattern
- Less error-prone than indexing

**Zen principle:**
> "There should be one—and preferably only one—obvious way to do it."

**Attribution:** PEP 20

---

### ZEN-COMPREHENSION-IDIOM: Prefer Comprehensions Over map/filter

**Intent:** Python Idioms

**Zen Principle:** "There should be one—and preferably only one—obvious way to do it."

**Using map/filter:**
```python
result = list(filter(lambda x: x > 0, map(lambda x: x * 2, numbers)))
```

**List comprehension:**
```python
result = [x * 2 for x in numbers if x * 2 > 0]
```

**Why this matters:**
- List comprehensions are more readable
- No lambda needed for simple operations
- More Pythonic for transformations
- map/filter are functional but less common in modern Python

**Zen principle:**
> "There should be one—and preferably only one—obvious way to do it."

**Attribution:** PEP 20

---

## 8. IMPLEMENTATION QUALITY

### ZEN-HARD-EXPLAIN: If the Implementation is Hard to Explain, It's a Bad Idea

**Intent:** Implementation Quality

**Zen Principle:** "If the implementation is hard to explain, it's a bad idea."

**Hard to explain:**
```python
result = reduce(lambda a, b: {**a, **{k: a.get(k, 0) + b.get(k, 0) for k in set(a) | set(b)}}, data, {})
```

**Easy to explain:**
```python
def merge_counters(data: list[dict]) -> dict:
    """Merge list of dicts, summing values for matching keys."""
    result = {}
    for counter in data:
        for key, value in counter.items():
            result[key] = result.get(key, 0) + value
    return result

result = merge_counters(data)
```

**Why this matters:**
- If you can't explain it simply, simplify it
- Complex implementations hide bugs
- Team members need to understand code
- Maintainability requires clarity

**Zen principle:**
> "If the implementation is hard to explain, it's a bad idea."

**Attribution:** PEP 20, Clynt

---

### ZEN-EASY-EXPLAIN: If the Implementation is Easy to Explain, It May Be a Good Idea

**Intent:** Implementation Quality

**Zen Principle:** "If the implementation is easy to explain, it may be a good idea."

**Clear implementation:**
```python
def calculate_total_price(items: list[Item], tax_rate: float) -> float:
    """Calculate total price including tax.

    Args:
        items: List of items to price
        tax_rate: Tax rate (e.g., 0.08 for 8%)

    Returns:
        Total price including tax
    """
    subtotal = sum(item.price for item in items)
    tax = subtotal * tax_rate
    total = subtotal + tax
    return round(total, 2)
```

**Why this matters:**
- Simple explanation = good design
- Clear steps are testable
- Easy to review and maintain
- Documentation writes itself

**Zen principle:**
> "If the implementation is easy to explain, it may be a good idea."

**Attribution:** PEP 20

---

### ZEN-CLEVER: Avoid Clever Code

**Intent:** Implementation Quality

**Zen Principle:** "If the implementation is hard to explain, it's a bad idea."

**Clever (obscure):**
```python
# FizzBuzz one-liner
print('\n'.join('FizzBuzz'[i%-3&-4:i%-5&8^12] or str(i) for i in range(1, 101)))
```

**Clear:**
```python
def fizzbuzz(n: int) -> str:
    """Return FizzBuzz result for number n."""
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)

for i in range(1, 101):
    print(fizzbuzz(i))
```

**Why this matters:**
- Clever code is hard to maintain
- Readability beats brevity
- Future you will thank present you
- Code is written once, read many times

**Zen principle:**
> "If the implementation is hard to explain, it's a bad idea."

**Attribution:** PEP 20

---

### ZEN-OBVIOUS: Make Code Self-Documenting

**Intent:** Implementation Quality

**Zen Principle:** "If the implementation is easy to explain, it may be a good idea."

**Needs comments:**
```python
def f(x):
    # Check if x is divisible by 4 and not by 100, or divisible by 400
    return (x % 4 == 0 and x % 100 != 0) or (x % 400 == 0)
```

**Self-documenting:**
```python
def is_leap_year(year: int) -> bool:
    """Check if year is a leap year."""
    divisible_by_4 = year % 4 == 0
    not_century_year = year % 100 != 0
    divisible_by_400 = year % 400 == 0

    return (divisible_by_4 and not_century_year) or divisible_by_400
```

**Why this matters:**
- Good names eliminate need for comments
- Breaking down logic clarifies intent
- Easy to understand = easy to maintain
- Self-documenting code is a good idea

**Zen principle:**
> "If the implementation is easy to explain, it may be a good idea."

**Attribution:** PEP 20

---

## 9. PRAGMATISM

### ZEN-PRACTICAL: Practicality Beats Purity

**Intent:** Pragmatism

**Zen Principle:** "Although practicality beats purity."

**Purist approach:**
```python
# Never mutate, always return new objects (pure functional)
def add_item_pure(shopping_list: list, item: str) -> list:
    return shopping_list + [item]

# This creates many intermediate lists, wasting memory
for item in new_items:
    shopping_list = add_item_pure(shopping_list, item)
```

**Pragmatic approach:**
```python
# Mutation is practical here
def add_item(shopping_list: list, item: str) -> None:
    """Add item to shopping list in place."""
    shopping_list.append(item)

for item in new_items:
    add_item(shopping_list, item)
```

**Why this matters:**
- Perfect is the enemy of good
- Sometimes practicality matters more than theory
- Python allows mutation for good reason
- Don't dogmatically follow paradigms

**Zen principle:**
> "Although practicality beats purity."

**Attribution:** PEP 20, Clynt

---

### ZEN-SPECIAL-CASE: Special Cases Aren't Special Enough to Break the Rules

**Intent:** Consistency

**Zen Principle:** "Special cases aren't special enough to break the rules."

**Inconsistent naming:**
```python
def calculate_total_price(items):
    pass

def CalcUserAge(birth_date):  # Different convention!
    pass

def get_order_status(order_id):
    pass
```

**Consistent naming:**
```python
def calculate_total_price(items):
    pass

def calculate_user_age(birth_date):  # Consistent!
    pass

def get_order_status(order_id):
    pass
```

**Why this matters:**
- Consistency aids readability
- No function is special enough to break conventions
- Follow PEP 8 everywhere
- Team standards apply to everyone

**Zen principle:**
> "Special cases aren't special enough to break the rules."

**Attribution:** PEP 20

---

### ZEN-NOW-NEVER: Now is Better Than Never (Although Never is Often Better Than Right Now)

**Intent:** Pragmatism

**Zen Principle:** "Now is better than never. Although never is often better than right now."

**Hasty implementation:**
```python
def process_payment(amount):
    # TODO: Add validation
    # TODO: Add error handling
    # TODO: Add logging
    # Ship it now, fix later!
    return charge_card(amount)
```

**Balanced approach:**
```python
def process_payment(amount: float) -> PaymentResult:
    """Process payment with essential safeguards.

    Args:
        amount: Payment amount (must be positive)

    Returns:
        PaymentResult with status and transaction ID

    Raises:
        ValueError: If amount is invalid
        PaymentError: If payment processing fails
    """
    # Implement now: critical validations
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}")

    # Implement now: error handling
    try:
        result = charge_card(amount)
        logger.info(f"Payment processed: {amount}")
        return result
    except Exception as e:
        logger.error(f"Payment failed: {e}")
        raise PaymentError("Payment processing failed") from e

    # Can wait: Advanced fraud detection, retry logic
```

**Why this matters:**
- Don't rush broken code
- Implement critical features now
- Nice-to-haves can wait
- Balance speed with quality

**Zen principle:**
> "Now is better than never. Although never is often better than right now."

**Attribution:** PEP 20

---

## 10. NAMESPACES

### ZEN-NAMESPACE: Namespaces Are One Honking Great Idea

**Intent:** Organization

**Zen Principle:** "Namespaces are one honking great idea—let's do more of those!"

**Global namespace pollution:**
```python
# utils.py
def format_date(date):
    pass

def format_currency(amount):
    pass

def validate_email(email):
    pass

def validate_phone(phone):
    pass

# Hard to organize, everything in one namespace
from utils import *
```

**Organized namespaces:**
```python
# formatters.py
def format_date(date):
    pass

def format_currency(amount):
    pass

# validators.py
def validate_email(email):
    pass

def validate_phone(phone):
    pass

# Clear organization
from formatters import format_date, format_currency
from validators import validate_email, validate_phone
```

**Why this matters:**
- Namespaces prevent naming conflicts
- Organize related functionality
- Clear where functions come from
- Scalable code organization

**Zen principle:**
> "Namespaces are one honking great idea—let's do more of those!"

**Attribution:** PEP 20, Clynt

---

### ZEN-GLOBAL: Avoid Global Variables

**Intent:** Organization

**Zen Principle:** "Namespaces are one honking great idea—let's do more of those!"

**Global state:**
```python
# Global mutable state
counter = 0

def increment():
    global counter
    counter += 1

def get_count():
    return counter
```

**Encapsulated state:**
```python
class Counter:
    """Encapsulate counter state in namespace."""

    def __init__(self):
        self._count = 0

    def increment(self):
        self._count += 1

    def get_count(self) -> int:
        return self._count

# Or use a module-level namespace
# counter_module.py with private _counter
```

**Why this matters:**
- Global variables create hidden dependencies
- Hard to test code with global state
- Namespaces (classes, modules) contain state
- Explicit is better than implicit

**Zen principle:**
> "Namespaces are one honking great idea—let's do more of those!"

**Attribution:** PEP 20

---

### ZEN-MODULE: Organize Code into Modules

**Intent:** Organization

**Zen Principle:** "Namespaces are one honking great idea—let's do more of those!"

**Everything in one file:**
```python
# app.py (5000 lines)
class User:
    pass

class Order:
    pass

class Payment:
    pass

def validate_user():
    pass

def process_order():
    pass

def charge_card():
    pass
# ... 4900 more lines
```

**Organized modules:**
```python
# models/user.py
class User:
    pass

# models/order.py
class Order:
    pass

# models/payment.py
class Payment:
    pass

# services/user_service.py
def validate_user():
    pass

# services/order_service.py
def process_order():
    pass

# services/payment_service.py
def charge_card():
    pass
```

**Why this matters:**
- Modules are namespaces
- Organize by domain/responsibility
- Easier to navigate
- Supports team collaboration

**Zen principle:**
> "Namespaces are one honking great idea—let's do more of those!"

**Attribution:** PEP 20

---

# End of Guidelines

Remember: The Zen of Python is not just philosophy—it's practical guidance for writing better Python code. When reviewing code, always ask: "Is this Pythonic?" and reference these principles.
