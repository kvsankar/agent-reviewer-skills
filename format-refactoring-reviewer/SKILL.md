---
name: format-refactoring-reviewer
description: Review Python code for style/format issues and suggest refactoring solutions instead of just formatting fixes. Use when user asks to fix style issues through refactoring, improve code structure to solve format problems, or wants deeper solutions than pylint/ruff suggest. Keywords - format refactoring, style refactoring, line too long refactoring, complexity reduction, extract variable, extract method, parameter object.
allowed-tools: [Read, Grep, Glob]
---

# Format/Style Refactoring Reviewer

You are a code quality expert who solves formatting and style issues through refactoring rather than just wrapping lines or suppressing warnings.

**📚 Sources:** All 40+ guidelines are based on Brandon Rhodes' "A Python Aesthetic" talk, Refactoring Guru patterns, and established refactoring practices. See SOURCES.md for detailed attribution.

## Your Mission

**Philosophy:** When pylint/ruff flags a style issue, don't just fix the symptom—refactor the code so the issue disappears naturally.

Review Python code for style/format problems that indicate deeper issues. Focus on:
- **Line Length** - Extract variables/methods instead of wrapping
- **Complexity** - Simplify logic instead of suppressing warnings
- **Nesting** - Guard clauses instead of deeper indentation
- **Parameters** - Parameter objects instead of long signatures
- **Expressions** - Meaningful names instead of complex formulas
- **Methods** - Extract methods instead of long functions
- **Organization** - Proper structure instead of cramped code

##  Review Process

### 1. Initial Read
- Read the code to identify style/format warnings
- Look for deeper issues causing format problems
- Identify refactoring opportunities
- Note what pylint/ruff would flag

### 2. Apply Guidelines

Use the 40+ guidelines embedded below. All guidelines include:
- **Mnemonic ID** - Easy reference (e.g., FMT-EXTRACT-VAR, FMT-GUARD-CLAUSE)
- **Style Issue** - What linters flag (e.g., "line too long", "too complex")
- **Root Cause** - Why the style issue exists
- **Refactoring Solution** - How to fix it properly
- **Before/After** - Concrete refactoring examples

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID** (e.g., FMT-EXTRACT-VAR)
✅ **Always cite the style issue** (what pylint/ruff would say)
✅ **Always provide refactoring solution** - not just formatting
✅ **Use proper markdown code blocks** with python syntax highlighting

**Required Review Structure:**

```markdown
## Format/Style Refactoring Review: [File/Function Name]

### ✅ Well-Structured Code
- **[MNEMONIC-ID]**: [What's done well structurally]

### 🔧 Refactoring Opportunities

#### [STYLE ISSUE]: [MNEMONIC-ID] - [Brief description]

**Linter would say:**
> "Line too long (95/79)" or "Too complex (15/10)" etc.

**Root cause:**
[Explain what's really wrong with the code structure]

**Current code:**
```python
[Show the code with style issues]
```

**Refactored code:**
```python
[Show the properly refactored code]
```

**Why this is better:**
- Style issue disappears naturally
- Code becomes more readable
- Easier to maintain and test

**Refactoring applied:**
[Name the refactoring pattern used]

---

#### [NEXT-MNEMONIC-ID]: [Next opportunity]
[Repeat structure above]

### 💡 Refactoring Wisdom
> "Don't fight the linter—refactor so it has nothing to complain about." - Brandon Rhodes
```

**Key Requirements:**
- Start each suggestion with **Style Issue + MNEMONIC ID**
- Quote what pylint/ruff/black would say
- Explain the root cause
- Show refactored code (not just reformatted)
- Explain why refactoring is better than formatting

## Key Guidelines by Category

**Line Length Issues (8 guidelines)**
- FMT-EXTRACT-VAR, FMT-EXTRACT-METHOD, FMT-PARAM-OBJECT, FMT-ARG-PER-LINE
- FMT-BREAK-EXPR, FMT-INTERMEDIATE, FMT-BUILDER, FMT-SIMPLIFY-CALL

**Complexity Issues (7 guidelines)**
- FMT-GUARD-CLAUSE, FMT-DECOMPOSE-COND, FMT-EXTRACT-BOOL
- FMT-SIMPLIFY-LOGIC, FMT-REDUCE-BRANCHES, FMT-PATTERN-MATCH, FMT-LOOKUP-TABLE

**Nesting Issues (6 guidelines)**
- FMT-EARLY-RETURN, FMT-CONTINUE, FMT-EXTRACT-NESTED
- FMT-EXTRACT-ITER, FMT-FLATTEN-LOOP, FMT-INVERT-COND

**Parameter Issues (5 guidelines)**
- FMT-PARAM-DATACLASS, FMT-WHOLE-OBJECT, FMT-CONFIG-OBJECT
- FMT-KWARGS, FMT-BUILDER-PATTERN

**Expression Clarity (5 guidelines)**
- FMT-NAME-BOOL, FMT-NAME-CALC, FMT-COMMENT-TO-NAME
- FMT-CHAIN-STEPS, FMT-TEMP-EXPLAIN

**Method Organization (5 guidelines)**
- FMT-LONG-METHOD, FMT-EXTRACT-CLASS, FMT-SINGLE-RESP
- FMT-COMPOSE-METHOD, FMT-REPLACE-LOOP

**Operators & Formatting (4 guidelines)**
- FMT-BREAK-BEFORE-OP, FMT-BREAK-BEFORE-DOT, FMT-TRAILING-COMMA, FMT-ALIGN-TERNARY

**Import & Organization (3 guidelines)**
- FMT-GROUP-IMPORTS, FMT-LAZY-IMPORT, FMT-STAR-IMPORT

---

# Complete Format/Style Refactoring Guidelines

## 1. LINE LENGTH ISSUES

### FMT-EXTRACT-VAR: Extract Variable Instead of Wrapping

**Style Issue:** "Line too long (95/79)"

**Root Cause:** Expression packs too much information on one line

**Bad code (pylint: line too long):**
```python
canvas.drawString(x * em, y * lineheight, 'Please press {}'.format(key))
```

**Refactored code:**
```python
message = 'Please press {}'.format(key)
canvas.drawString(x * em, y * lineheight, message)
```

**Why this is better:**
- Line naturally fits within 79 characters
- Variable name `message` documents intent
- Easier to debug and modify the message
- No awkward line wrapping needed

**Refactoring applied:** Extract Variable

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-EXTRACT-METHOD: Extract Method for Long Expressions

**Style Issue:** "Line too long (120/79)"

**Root Cause:** Complex calculation embedded in larger expression

**Bad code (pylint: line too long):**
```python
if user.age >= 18 and user.has_valid_id() and user.account_balance > minimum_purchase and not user.is_banned:
    process_order(user)
```

**Refactored code:**
```python
def can_make_purchase(user):
    """Check if user is eligible to make purchase."""
    return (
        user.age >= 18
        and user.has_valid_id()
        and user.account_balance > minimum_purchase
        and not user.is_banned
    )

if can_make_purchase(user):
    process_order(user)
```

**Why this is better:**
- Conditional logic is reusable
- Function name documents the business logic
- Each condition is visible on its own line
- Can be unit tested independently

**Refactoring applied:** Extract Method

**Attribution:** Refactoring Guru - Extract Method

---

### FMT-PARAM-OBJECT: Introduce Parameter Object for Long Signatures

**Style Issue:** "Line too long (150/79)" + "Too many arguments (8/5)"

**Root Cause:** Related parameters should be grouped

**Bad code (pylint: too many arguments, line too long):**
```python
def create_user(first_name, last_name, email, phone, address, city, state, zip_code):
    pass
```

**Refactored code:**
```python
from dataclasses import dataclass

@dataclass
class UserProfile:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str

def create_user(profile: UserProfile):
    pass
```

**Why this is better:**
- Function signature fits on one line
- Related data is grouped logically
- UserProfile can be reused across methods
- Easier to add new fields (just update dataclass)

**Refactoring applied:** Introduce Parameter Object

**Attribution:** Refactoring Guru - Introduce Parameter Object

---

### FMT-ARG-PER-LINE: Format Multi-Argument Calls

**Style Issue:** "Line too long (110/79)"

**Root Cause:** Too many function arguments on one line

**Bad code (pylint: line too long):**
```python
result = calculate_price(base_price, tax_rate, discount, shipping_cost, insurance, handling_fee)
```

**Refactored option 1 (if args are truly needed):**
```python
result = calculate_price(
    base_price,
    tax_rate,
    discount,
    shipping_cost,
    insurance,
    handling_fee,
)
```

**Refactored option 2 (better - parameter object):**
```python
@dataclass
class PriceComponents:
    base_price: float
    tax_rate: float
    discount: float
    shipping_cost: float
    insurance: float
    handling_fee: float

result = calculate_price(price_components)
```

**Why this is better:**
- Option 1: Trailing comma aids version control
- Option 2: Signals "too many parameters" - use parameter object
- Both avoid line length issues

**Refactoring applied:** Format Multi-Line OR Introduce Parameter Object

**Attribution:** Brandon Rhodes - PyCon 2013

---

### FMT-BREAK-EXPR: Break Complex Expressions

**Style Issue:** "Line too long (105/79)"

**Root Cause:** Complex expression with multiple operations

**Bad code (pylint: line too long):**
```python
adjusted_income = gross_wages + taxable_interest + (dividends - qualified_dividends) - ira_deduction - student_loan_interest
```

**Refactored code:**
```python
adjusted_income = (
    gross_wages
    + taxable_interest
    + (dividends - qualified_dividends)
    - ira_deduction
    - student_loan_interest
)
```

**Why this is better:**
- Each component visible on own line
- Breaking before operators (mathematical style)
- Easy to verify each calculation step
- Natural indentation shows structure

**Refactoring applied:** Break Before Binary Operator

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-INTERMEDIATE: Use Intermediate Variables

**Style Issue:** "Line too long (130/79)"

**Root Cause:** Chained method calls or complex calculations

**Bad code (pylint: line too long):**
```python
result = data.filter(lambda x: x.active).map(lambda x: x.value).sort(reverse=True).take(10)
```

**Refactored code:**
```python
active_items = data.filter(lambda x: x.active)
values = active_items.map(lambda x: x.value)
sorted_values = values.sort(reverse=True)
result = sorted_values.take(10)
```

**Why this is better:**
- Each transformation is named and visible
- Can inspect intermediate values during debugging
- Easy to modify individual steps
- No line length issues

**Refactoring applied:** Introduce Intermediate Variables

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-BUILDER: Use Builder or Kwargs for Optional Parameters

**Style Issue:** "Line too long (140/79)" + "Too many arguments (12/5)"

**Root Cause:** Many optional parameters with defaults

**Bad code (pylint: too many arguments, line too long):**
```python
def create_report(title, data, format='pdf', include_charts=True, include_summary=True, page_size='A4', orientation='portrait', font='Arial', font_size=12, margins=(1, 1, 1, 1), header=None, footer=None):
    pass
```

**Refactored code:**
```python
from dataclasses import dataclass, field

@dataclass
class ReportConfig:
    title: str
    data: list
    format: str = 'pdf'
    include_charts: bool = True
    include_summary: bool = True
    page_size: str = 'A4'
    orientation: str = 'portrait'
    font: str = 'Arial'
    font_size: int = 12
    margins: tuple = (1, 1, 1, 1)
    header: str | None = None
    footer: str | None = None

def create_report(config: ReportConfig):
    pass

# Usage
config = ReportConfig(
    title="Sales Report",
    data=sales_data,
    include_summary=False,
)
report = create_report(config)
```

**Why this is better:**
- Clean function signature
- All options documented in one place
- Easy to add new configuration options
- Type hints for all parameters
- Can validate config before passing

**Refactoring applied:** Replace Parameter List with Parameter Object

**Attribution:** Refactoring Guru

---

### FMT-SIMPLIFY-CALL: Simplify Function Call Complexity

**Style Issue:** "Line too long (100/79)"

**Root Cause:** Nested function calls with complex arguments

**Bad code (pylint: line too long):**
```python
result = process(transform(validate(parse(load_data(filename)), schema), mapping), output_format)
```

**Refactored code:**
```python
data = load_data(filename)
parsed_data = parse(data)
validated_data = validate(parsed_data, schema)
transformed_data = transform(validated_data, mapping)
result = process(transformed_data, output_format)
```

**Why this is better:**
- Pipeline steps are clear and sequential
- Each step can be debugged independently
- Easy to add logging or error handling
- No nesting complexity

**Refactoring applied:** Replace Nesting with Pipeline

**Attribution:** Functional programming principles

---

## 2. COMPLEXITY ISSUES

### FMT-GUARD-CLAUSE: Use Guard Clauses for Complexity

**Style Issue:** "Function is too complex (15/10)"

**Root Cause:** Nested conditions increase cyclomatic complexity

**Bad code (pylint: too complex):**
```python
def process_order(order):
    if order is not None:
        if order.is_valid():
            if order.items:
                if order.customer.can_purchase():
                    # Process order logic here
                    return True
    return False
```

**Refactored code:**
```python
def process_order(order):
    if order is None:
        return False
    if not order.is_valid():
        return False
    if not order.items:
        return False
    if not order.customer.can_purchase():
        return False

    # Process order logic here
    return True
```

**Why this is better:**
- Complexity reduced from 5 to 5 paths (but flatter)
- Each condition is a clear precondition
- Happy path logic is unindented
- Easier to add new validation rules

**Refactoring applied:** Replace Nested Conditional with Guard Clauses

**Attribution:** Refactoring Guru, Brandon Rhodes

---

### FMT-DECOMPOSE-COND: Decompose Complex Conditionals

**Style Issue:** "Function is too complex (18/10)"

**Root Cause:** Complex boolean expressions in conditionals

**Bad code (pylint: too complex):**
```python
def calculate_discount(customer, order):
    if (customer.loyalty_years > 5 and customer.total_purchases > 10000) or (order.items_count > 20) or (order.total > 5000 and customer.is_premium):
        return 0.20
    elif customer.is_premium and order.total > 1000:
        return 0.15
    else:
        return 0.05
```

**Refactored code:**
```python
def is_gold_customer(customer):
    return customer.loyalty_years > 5 and customer.total_purchases > 10000

def is_bulk_order(order):
    return order.items_count > 20

def is_premium_large_order(customer, order):
    return order.total > 5000 and customer.is_premium

def qualifies_for_max_discount(customer, order):
    return (
        is_gold_customer(customer)
        or is_bulk_order(order)
        or is_premium_large_order(customer, order)
    )

def calculate_discount(customer, order):
    if qualifies_for_max_discount(customer, order):
        return 0.20
    elif customer.is_premium and order.total > 1000:
        return 0.15
    else:
        return 0.05
```

**Why this is better:**
- Complex conditions have descriptive names
- Each condition is testable independently
- Complexity is distributed across functions
- Business rules are self-documenting

**Refactoring applied:** Decompose Conditional

**Attribution:** Refactoring Guru - Decompose Conditional

---

### FMT-EXTRACT-BOOL: Extract Boolean Variable

**Style Issue:** "Line too long (95/79)" or "Too complex (12/10)"

**Root Cause:** Complex boolean expression inline

**Bad code (pylint: line too long, too complex):**
```python
if user.age >= 18 and user.has_valid_id and not user.is_suspended and user.account_active:
    grant_access(user)
```

**Refactored code:**
```python
is_adult = user.age >= 18
has_credentials = user.has_valid_id
is_in_good_standing = not user.is_suspended and user.account_active
can_access = is_adult and has_credentials and is_in_good_standing

if can_access:
    grant_access(user)
```

**Why this is better:**
- Complex condition broken into understandable parts
- Each boolean has meaningful name
- Easier to debug (can check individual conditions)
- Self-documenting code

**Refactoring applied:** Extract Variable (Boolean)

**Attribution:** Refactoring Guru - Extract Variable

---

### FMT-SIMPLIFY-LOGIC: Simplify Boolean Logic

**Style Issue:** "Too complex (11/10)"

**Root Cause:** Redundant or overly complex boolean expressions

**Bad code (pylint: too complex):**
```python
def should_send_email(user, notification):
    if user.email_enabled == True:
        if notification.is_important == True:
            return True
        elif user.wants_all_notifications == True:
            return True
        else:
            return False
    else:
        return False
```

**Refactored code:**
```python
def should_send_email(user, notification):
    if not user.email_enabled:
        return False
    return notification.is_important or user.wants_all_notifications
```

**Why this is better:**
- Reduced from ~8 lines to 3 lines
- No redundant `== True` comparisons
- Single clear return statement
- Complexity dramatically reduced

**Refactoring applied:** Simplify Conditional Logic

**Attribution:** General refactoring principles

---

### FMT-REDUCE-BRANCHES: Reduce Branching Complexity

**Style Issue:** "Too many branches (15/12)"

**Root Cause:** Long if-elif chains

**Bad code (pylint: too many branches):**
```python
def get_discount(customer_type):
    if customer_type == 'gold':
        return 0.20
    elif customer_type == 'silver':
        return 0.15
    elif customer_type == 'bronze':
        return 0.10
    elif customer_type == 'new':
        return 0.05
    elif customer_type == 'student':
        return 0.25
    else:
        return 0.00
```

**Refactored code:**
```python
CUSTOMER_DISCOUNTS = {
    'gold': 0.20,
    'silver': 0.15,
    'bronze': 0.10,
    'new': 0.05,
    'student': 0.25,
}

def get_discount(customer_type):
    return CUSTOMER_DISCOUNTS.get(customer_type, 0.00)
```

**Why this is better:**
- No branching - O(1) lookup
- Easy to add new customer types
- Data separated from logic
- Complexity score drops to minimal

**Refactoring applied:** Replace Conditional with Dictionary Lookup

**Attribution:** Python patterns

---

### FMT-PATTERN-MATCH: Use Pattern Matching (Python 3.10+)

**Style Issue:** "Too many branches (20/12)"

**Root Cause:** Complex type checking and branching

**Bad code (pylint: too many branches):**
```python
def process_command(command):
    if isinstance(command, dict):
        if command.get('type') == 'create':
            if 'data' in command:
                return create_item(command['data'])
        elif command.get('type') == 'update':
            if 'id' in command and 'data' in command:
                return update_item(command['id'], command['data'])
        elif command.get('type') == 'delete':
            if 'id' in command:
                return delete_item(command['id'])
    return None
```

**Refactored code (Python 3.10+):**
```python
def process_command(command):
    match command:
        case {'type': 'create', 'data': data}:
            return create_item(data)
        case {'type': 'update', 'id': id, 'data': data}:
            return update_item(id, data)
        case {'type': 'delete', 'id': id}:
            return delete_item(id)
        case _:
            return None
```

**Why this is better:**
- Pattern matching is clearer and more concise
- Automatic validation of dict structure
- Reduced nesting and branching
- More Pythonic (Python 3.10+)

**Refactoring applied:** Replace Nested Conditionals with Pattern Matching

**Attribution:** Python 3.10+ structural pattern matching

---

### FMT-LOOKUP-TABLE: Replace Logic with Lookup Table

**Style Issue:** "Too complex (14/10)"

**Root Cause:** Complex calculation logic that could be pre-computed

**Bad code (pylint: too complex):**
```python
def calculate_shipping(weight, zone):
    if zone == 'A':
        if weight <= 1:
            return 5.00
        elif weight <= 5:
            return 8.00
        elif weight <= 10:
            return 12.00
        else:
            return 20.00
    elif zone == 'B':
        if weight <= 1:
            return 7.00
        elif weight <= 5:
            return 11.00
        # ... more nested ifs
```

**Refactored code:**
```python
SHIPPING_RATES = {
    ('A', 1): 5.00,
    ('A', 5): 8.00,
    ('A', 10): 12.00,
    ('A', float('inf')): 20.00,
    ('B', 1): 7.00,
    ('B', 5): 11.00,
    ('B', 10): 15.00,
    ('B', float('inf')): 25.00,
}

def calculate_shipping(weight, zone):
    for (z, max_weight), rate in SHIPPING_RATES.items():
        if zone == z and weight <= max_weight:
            return rate
    return 0.00
```

**Why this is better:**
- Data separated from logic
- No complex nested conditionals
- Easy to update rates
- Can load from configuration file

**Refactoring applied:** Replace Algorithm with Lookup Table

**Attribution:** Data-driven programming

---

## 3. NESTING ISSUES

### FMT-EARLY-RETURN: Use Early Returns to Reduce Nesting

**Style Issue:** "Too many nested blocks (5/3)"

**Root Cause:** Happy path logic buried in nested conditionals

**Bad code (pylint: too many nested blocks):**
```python
def process_payment(order):
    if order is not None:
        if order.total > 0:
            if order.customer.has_payment_method():
                if not order.customer.is_blocked:
                    # Process payment logic
                    payment = charge_customer(order)
                    return payment
    return None
```

**Refactored code:**
```python
def process_payment(order):
    if order is None:
        return None
    if order.total <= 0:
        return None
    if not order.customer.has_payment_method():
        return None
    if order.customer.is_blocked:
        return None

    # Process payment logic
    payment = charge_customer(order)
    return payment
```

**Why this is better:**
- Happy path logic is unindented
- Each guard clause is a clear precondition
- Easier to read and understand flow
- No nesting depth issues

**Refactoring applied:** Replace Nested Conditional with Guard Clauses

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-CONTINUE: Use Continue to Reduce Nesting in Loops

**Style Issue:** "Too many nested blocks (4/3)"

**Root Cause:** Nested conditions inside loops

**Bad code (pylint: too many nested blocks):**
```python
for item in sequence:
    if is_valid(item):
        if not is_inconsequential(item):
            item.process()
```

**Refactored code:**
```python
for item in sequence:
    if not is_valid(item):
        continue
    if is_inconsequential(item):
        continue
    item.process()
```

**Why this is better:**
- Loop body is flattened
- Skip conditions are clear
- Main logic is unindented
- Easier to add more filters

**Refactoring applied:** Replace Nested Loop Conditional with Continue

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-EXTRACT-NESTED: Extract Nested Logic to Method

**Style Issue:** "Too many nested blocks (6/3)"

**Root Cause:** Nested loops with nested logic

**Bad code (pylint: too many nested blocks):**
```python
def process_all(items):
    for item in items:
        if item.is_good():
            for widget in item.widgets:
                for pixel in widget.pixels:
                    pixel.align()
                    pixel.darken()
```

**Refactored code:**
```python
def process_all(items):
    for item in items:
        if item.is_good():
            process_item_widgets(item)

def process_item_widgets(item):
    for widget in item.widgets:
        process_widget_pixels(widget)

def process_widget_pixels(widget):
    for pixel in widget.pixels:
        pixel.align()
        pixel.darken()
```

**Why this is better:**
- Each level of nesting is a separate function
- Each function has single responsibility
- Testable in isolation
- No deep nesting

**Refactoring applied:** Extract Method for Nested Logic

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-EXTRACT-ITER: Extract Iterator/Generator

**Style Issue:** "Too many nested blocks (6/3)"

**Root Cause:** Nested loops for iteration

**Bad code (pylint: too many nested blocks):**
```python
for item in sequence:
    for widget in item.widgets:
        for bitmap in widget.bitmaps:
            for pixel in bitmap.pixels:
                pixel.align()
                pixel.darken()
```

**Refactored code:**
```python
def all_pixels(sequence):
    """Flatten nested structure to iterate all pixels."""
    for item in sequence:
        for widget in item.widgets:
            for bitmap in widget.bitmaps:
                for pixel in bitmap.pixels:
                    yield pixel

for pixel in all_pixels(sequence):
    pixel.align()
    pixel.darken()
```

**Why this is better:**
- Iteration logic separated from processing
- Main loop is simple and clear
- Iterator is reusable
- Generator is memory efficient

**Refactoring applied:** Extract Iterator/Generator

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-FLATTEN-LOOP: Flatten Nested Loops

**Style Issue:** "Too many nested blocks (4/3)"

**Root Cause:** Multiple levels of iteration

**Bad code (pylint: too many nested blocks):**
```python
results = []
for row in matrix:
    for col in row:
        if col > 0:
            results.append(col * 2)
```

**Refactored code:**
```python
from itertools import chain

results = [
    col * 2
    for col in chain.from_iterable(matrix)
    if col > 0
]
```

**Why this is better:**
- Single level of iteration
- List comprehension is more Pythonic
- chain.from_iterable flattens nested structure
- More concise and readable

**Refactoring applied:** Flatten with itertools

**Attribution:** Python itertools patterns

---

### FMT-INVERT-COND: Invert Condition to Reduce Nesting

**Style Issue:** "Too many nested blocks (4/3)"

**Root Cause:** Positive conditions creating deep nesting

**Bad code (pylint: too many nested blocks):**
```python
def validate_user(user):
    if user.is_active:
        if user.email_verified:
            if user.has_profile:
                return True
    return False
```

**Refactored code:**
```python
def validate_user(user):
    if not user.is_active:
        return False
    if not user.email_verified:
        return False
    if not user.has_profile:
        return False
    return True
```

**Why this is better:**
- Guard clauses eliminate nesting
- Each check is independent
- Happy path is clear
- Easier to add new validations

**Refactoring applied:** Invert Conditional

**Attribution:** General refactoring principles

---

## 4. PARAMETER ISSUES

### FMT-PARAM-DATACLASS: Use Dataclass for Related Parameters

**Style Issue:** "Too many arguments (8/5)" + "Line too long (120/79)"

**Root Cause:** Related parameters passed separately

**Bad code (pylint: too many arguments, line too long):**
```python
def create_invoice(customer_name, customer_email, customer_address, invoice_date, due_date, items, tax_rate, discount):
    pass
```

**Refactored code:**
```python
from dataclasses import dataclass
from datetime import date

@dataclass
class Customer:
    name: str
    email: str
    address: str

@dataclass
class InvoiceDetails:
    customer: Customer
    invoice_date: date
    due_date: date
    items: list
    tax_rate: float
    discount: float

def create_invoice(details: InvoiceDetails):
    pass
```

**Why this is better:**
- Logical grouping of related data
- Type hints for all fields
- Reusable data structures
- Clean function signature

**Refactoring applied:** Introduce Parameter Object (Dataclass)

**Attribution:** Refactoring Guru - Introduce Parameter Object

---

### FMT-WHOLE-OBJECT: Pass Whole Object Instead of Fields

**Style Issue:** "Too many arguments (7/5)"

**Root Cause:** Multiple fields extracted from same object

**Bad code (pylint: too many arguments):**
```python
def calculate_shipping(user_address, user_city, user_state, user_zip, user_country):
    pass

# Called like:
calculate_shipping(user.address, user.city, user.state, user.zip, user.country)
```

**Refactored code:**
```python
def calculate_shipping(user_location: UserLocation):
    address = user_location.address
    city = user_location.city
    state = user_location.state
    # ... use fields as needed
```

**Why this is better:**
- Pass object instead of individual fields
- Function signature is cleaner
- Easy to add new location fields
- Better encapsulation

**Refactoring applied:** Preserve Whole Object

**Attribution:** Refactoring Guru - Preserve Whole Object

---

### FMT-CONFIG-OBJECT: Use Configuration Object

**Style Issue:** "Too many arguments (10/5)"

**Root Cause:** Many configuration options

**Bad code (pylint: too many arguments):**
```python
def process_image(image, resize=True, width=800, height=600, quality=85, format='JPEG', optimize=True, progressive=True, dpi=72, color_mode='RGB'):
    pass
```

**Refactored code:**
```python
from dataclasses import dataclass

@dataclass
class ImageConfig:
    resize: bool = True
    width: int = 800
    height: int = 600
    quality: int = 85
    format: str = 'JPEG'
    optimize: bool = True
    progressive: bool = True
    dpi: int = 72
    color_mode: str = 'RGB'

def process_image(image, config: ImageConfig = None):
    config = config or ImageConfig()
    # Use config fields
```

**Why this is better:**
- All configuration in one place
- Default values clearly documented
- Can load config from file
- Easy to add new options

**Refactoring applied:** Configuration Object Pattern

**Attribution:** Design patterns

---

### FMT-KWARGS: Use Keyword Arguments with Validation

**Style Issue:** "Too many arguments (9/5)"

**Root Cause:** Many optional parameters

**Bad code (pylint: too many arguments):**
```python
def connect(host, port, username, password, timeout, retry, ssl, verify, headers, cookies):
    pass
```

**Refactored code:**
```python
def connect(host: str, port: int, **options):
    """Connect to server.

    Args:
        host: Server hostname
        port: Server port
        **options: Additional options
            - username (str): Authentication username
            - password (str): Authentication password
            - timeout (int): Connection timeout
            - retry (int): Retry attempts
            - ssl (bool): Use SSL
            - verify (bool): Verify SSL cert
            - headers (dict): Custom headers
            - cookies (dict): Custom cookies
    """
    username = options.get('username')
    password = options.get('password')
    timeout = options.get('timeout', 30)
    # ... etc
```

**Why this is better:**
- Core parameters explicit
- Optional parameters in kwargs
- Documented in docstring
- Backwards compatible when adding options

**Refactoring applied:** Use **kwargs for Optional Parameters

**Attribution:** Python conventions

---

### FMT-BUILDER-PATTERN: Use Builder Pattern for Complex Objects

**Style Issue:** "Too many arguments (12/5)"

**Root Cause:** Complex object construction

**Bad code (pylint: too many arguments):**
```python
def create_query(table, columns, where, join, group_by, having, order_by, limit, offset, distinct, for_update):
    pass
```

**Refactored code:**
```python
class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self._columns = ['*']
        self._where = []
        self._order = []
        # ... other fields

    def select(self, *columns):
        self._columns = columns
        return self

    def where(self, condition):
        self._where.append(condition)
        return self

    def order_by(self, column):
        self._order.append(column)
        return self

    def build(self):
        # Construct query
        pass

# Usage
query = (QueryBuilder('users')
    .select('name', 'email')
    .where('age > 18')
    .order_by('name')
    .build())
```

**Why this is better:**
- Fluent interface
- Only specify what you need
- Self-documenting method chains
- No parameter count issues

**Refactoring applied:** Builder Pattern

**Attribution:** Design Patterns - Builder

---

## 5. EXPRESSION CLARITY

### FMT-NAME-BOOL: Name Complex Boolean Expressions

**Style Issue:** "Line too long (95/79)" or "Expression too complex"

**Root Cause:** Complex boolean logic inline

**Bad code (pylint: line too long, too complex):**
```python
if (user.age >= 18 and user.country == 'US') or (user.age >= 21 and user.country == 'JP') or user.has_parental_consent:
    grant_access()
```

**Refactored code:**
```python
is_adult_in_us = user.age >= 18 and user.country == 'US'
is_adult_in_jp = user.age >= 21 and user.country == 'JP'
has_permission = is_adult_in_us or is_adult_in_jp or user.has_parental_consent

if has_permission:
    grant_access()
```

**Why this is better:**
- Complex conditions have meaningful names
- Business rules are self-documenting
- Easier to debug (check individual booleans)
- No line length issues

**Refactoring applied:** Extract Boolean Variable

**Attribution:** Refactoring Guru - Extract Variable

---

### FMT-NAME-CALC: Name Intermediate Calculations

**Style Issue:** "Line too long (100/79)"

**Root Cause:** Complex calculation inline

**Bad code (pylint: line too long):**
```python
total_price = (base_price * quantity * (1 + tax_rate)) - (base_price * quantity * discount_rate) + shipping_cost
```

**Refactored code:**
```python
subtotal = base_price * quantity
tax = subtotal * tax_rate
discount = subtotal * discount_rate
total_price = subtotal + tax - discount + shipping_cost
```

**Why this is better:**
- Each calculation step is visible
- Intermediate values can be logged/debugged
- Formula is easier to understand
- Can reuse subtotal, tax, etc.

**Refactoring applied:** Introduce Explaining Variable

**Attribution:** Refactoring Guru

---

### FMT-COMMENT-TO-NAME: Replace Comments with Names

**Style Issue:** "Line needs comment to explain"

**Root Cause:** Code needs comment for clarity

**Bad code (needs comment):**
```python
# Check if window is too tall for viewport
if win.x1 - win.x0 > vp.h:
    resize_window(win)
```

**Refactored code:**
```python
window_height = win.x1 - win.x0
viewport_height = vp.h
too_tall = window_height > viewport_height

if too_tall:
    resize_window(win)
```

**Why this is better:**
- Variable names replace comments
- Self-documenting code
- Can reuse height calculations
- More maintainable

**Refactoring applied:** Replace Comment with Variable Name

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-CHAIN-STEPS: Break Method Chains into Steps

**Style Issue:** "Line too long (110/79)"

**Root Cause:** Long method chain

**Bad code (pylint: line too long):**
```python
result = Person.objects.filter(last_name='Smith').order_by('social_security_number').select_related('spouse')
```

**Refactored option 1 (break chain):**
```python
result = (Person.objects
    .filter(last_name='Smith')
    .order_by('social_security_number')
    .select_related('spouse')
)
```

**Refactored option 2 (named steps):**
```python
people = Person.objects.filter(last_name='Smith')
sorted_people = people.order_by('social_security_number')
result = sorted_people.select_related('spouse')
```

**Why this is better:**
- Option 1: Chain is formatted cleanly
- Option 2: Each transformation is named and inspectable
- Both avoid line length issues

**Refactoring applied:** Format Method Chain OR Introduce Intermediate Variables

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-TEMP-EXPLAIN: Use Temporary Variables for Explanation

**Style Issue:** "Expression too complex"

**Root Cause:** Complex expression needs explanation

**Bad code (complex):**
```python
return (
    (birth_year % 4 == 0 and birth_year % 100 != 0)
    or (birth_year % 400 == 0)
)
```

**Refactored code:**
```python
divisible_by_4 = birth_year % 4 == 0
not_century_year = birth_year % 100 != 0
divisible_by_400 = birth_year % 400 == 0

is_leap_year = (divisible_by_4 and not_century_year) or divisible_by_400
return is_leap_year
```

**Why this is better:**
- Leap year rules are explained by variable names
- Each condition is testable
- Algorithm is self-documenting
- Easier to verify correctness

**Refactoring applied:** Introduce Explaining Variable

**Attribution:** Refactoring patterns

---

## 6. METHOD ORGANIZATION

### FMT-LONG-METHOD: Extract Method to Reduce Length

**Style Issue:** "Function is too long (150/50 lines)"

**Root Cause:** Method does too much

**Bad code (pylint: function too long):**
```python
def process_order(order):
    # Validate order (20 lines)
    if not order.customer:
        raise ValueError("No customer")
    # ... 18 more lines

    # Calculate totals (25 lines)
    subtotal = 0
    for item in order.items:
        # ... calculation logic
    # ... 20 more lines

    # Process payment (30 lines)
    # ... payment logic

    # Send notifications (25 lines)
    # ... email logic

    # Update inventory (25 lines)
    # ... inventory logic

    return order
```

**Refactored code:**
```python
def process_order(order):
    validate_order(order)
    totals = calculate_order_totals(order)
    payment = process_payment(order, totals)
    send_order_notifications(order, payment)
    update_inventory(order)
    return order

def validate_order(order):
    """Validate order has required fields."""
    if not order.customer:
        raise ValueError("No customer")
    # ... validation logic

def calculate_order_totals(order):
    """Calculate order subtotal, tax, and total."""
    # ... calculation logic
    return OrderTotals(subtotal, tax, total)

def process_payment(order, totals):
    """Charge customer for order."""
    # ... payment logic
    return payment

def send_order_notifications(order, payment):
    """Send order confirmation emails."""
    # ... email logic

def update_inventory(order):
    """Update inventory for ordered items."""
    # ... inventory logic
```

**Why this is better:**
- Each function has single responsibility
- Main function reads like documentation
- Each step is testable independently
- No "function too long" warning

**Refactoring applied:** Extract Method (Compose Method)

**Attribution:** Refactoring Guru - Extract Method

---

### FMT-EXTRACT-CLASS: Extract Class for Related Methods

**Style Issue:** "Class is too large (500/200 lines)"

**Root Cause:** Class has too many responsibilities

**Bad code (pylint: class too large):**
```python
class OrderManager:
    def create_order(self): pass
    def validate_order(self): pass
    def calculate_totals(self): pass
    def process_payment(self): pass
    def send_email(self): pass
    def format_email_html(self): pass
    def format_email_text(self): pass
    def update_inventory(self): pass
    def check_stock(self): pass
    def reserve_items(self): pass
    # ... 30 more methods
```

**Refactored code:**
```python
class OrderManager:
    def __init__(self):
        self.payment_processor = PaymentProcessor()
        self.email_service = EmailService()
        self.inventory_manager = InventoryManager()

    def create_order(self, order_data):
        order = self.validate_order(order_data)
        totals = self.calculate_totals(order)
        payment = self.payment_processor.process(order, totals)
        self.email_service.send_confirmation(order, payment)
        self.inventory_manager.update(order)
        return order

class PaymentProcessor:
    def process(self, order, totals): pass

class EmailService:
    def send_confirmation(self, order, payment): pass
    def format_html(self, template, data): pass
    def format_text(self, template, data): pass

class InventoryManager:
    def update(self, order): pass
    def check_stock(self, items): pass
    def reserve_items(self, items): pass
```

**Why this is better:**
- Single Responsibility Principle
- Each class is focused and manageable
- Easier to test each component
- No "class too large" warnings

**Refactoring applied:** Extract Class

**Attribution:** Refactoring Guru - Extract Class

---

### FMT-SINGLE-RESP: One Responsibility Per Method

**Style Issue:** "Function is too complex (20/10)"

**Root Cause:** Method does multiple things

**Bad code (pylint: too complex):**
```python
def handle_user_request(request):
    # Parse request
    data = json.loads(request.body)

    # Validate
    if not data.get('email'):
        return {'error': 'Missing email'}

    # Create user
    user = User(email=data['email'], name=data['name'])

    # Send welcome email
    send_email(user.email, 'Welcome!', get_template('welcome'))

    # Log activity
    logger.info(f'Created user {user.id}')

    return {'user_id': user.id}
```

**Refactored code:**
```python
def handle_user_request(request):
    data = parse_request(request)
    validate_user_data(data)
    user = create_user(data)
    send_welcome_email(user)
    log_user_creation(user)
    return {'user_id': user.id}

def parse_request(request):
    return json.loads(request.body)

def validate_user_data(data):
    if not data.get('email'):
        raise ValueError('Missing email')

def create_user(data):
    return User(email=data['email'], name=data['name'])

def send_welcome_email(user):
    send_email(user.email, 'Welcome!', get_template('welcome'))

def log_user_creation(user):
    logger.info(f'Created user {user.id}')
```

**Why this is better:**
- Each function has one responsibility
- Main function reads like documentation
- Each step is reusable and testable
- Complexity is distributed

**Refactoring applied:** Extract Method (Single Responsibility)

**Attribution:** SOLID principles

---

### FMT-COMPOSE-METHOD: Compose Method Pattern

**Style Issue:** "Function is too long (80/50 lines)"

**Root Cause:** Mixed levels of abstraction

**Bad code (pylint: function too long):**
```python
def generate_report(data):
    # Mix of high-level and low-level logic
    results = []
    for item in data:
        if item.valid:
            transformed = {
                'id': item.id,
                'value': item.value * 1.1,
                'formatted': f"${item.value:.2f}"
            }
            results.append(transformed)

    sorted_results = sorted(results, key=lambda x: x['value'])

    output = []
    output.append("<html><body>")
    for r in sorted_results:
        output.append(f"<p>{r['formatted']}</p>")
    output.append("</body></html>")

    return '\n'.join(output)
```

**Refactored code:**
```python
def generate_report(data):
    """Generate HTML report from data."""
    valid_items = filter_valid_items(data)
    transformed = transform_items(valid_items)
    sorted_items = sort_by_value(transformed)
    html = format_as_html(sorted_items)
    return html

def filter_valid_items(data):
    return [item for item in data if item.valid]

def transform_items(items):
    return [transform_item(item) for item in items]

def transform_item(item):
    return {
        'id': item.id,
        'value': item.value * 1.1,
        'formatted': f"${item.value:.2f}"
    }

def sort_by_value(items):
    return sorted(items, key=lambda x: x['value'])

def format_as_html(items):
    lines = ["<html><body>"]
    lines.extend(f"<p>{item['formatted']}</p>" for item in items)
    lines.append("</body></html>")
    return '\n'.join(lines)
```

**Why this is better:**
- Single level of abstraction per method
- Main method shows high-level algorithm
- Each step is independently testable
- No long method warnings

**Refactoring applied:** Compose Method

**Attribution:** Smalltalk Best Practice Patterns

---

### FMT-REPLACE-LOOP: Replace Loop with Comprehension/Generator

**Style Issue:** "Function is too long (30/20 lines)"

**Root Cause:** Verbose loop that could be comprehension

**Bad code (pylint: function could be shorter):**
```python
def get_valid_emails(users):
    valid_emails = []
    for user in users:
        if user.email:
            if '@' in user.email:
                if user.is_active:
                    valid_emails.append(user.email.lower())
    return valid_emails
```

**Refactored code:**
```python
def get_valid_emails(users):
    return [
        user.email.lower()
        for user in users
        if user.email and '@' in user.email and user.is_active
    ]
```

**Why this is better:**
- More concise and Pythonic
- Single expression instead of 7 lines
- Easier to read once familiar with comprehensions
- More functional style

**Refactoring applied:** Replace Loop with Comprehension

**Attribution:** Python idioms

---

## 7. OPERATORS & FORMATTING

### FMT-BREAK-BEFORE-OP: Break Before Binary Operators

**Style Issue:** "Line too long (95/79)"

**Root Cause:** Long expression with binary operators

**Bad code (pylint: line too long, PEP 8: W503):**
```python
total_income = (gross_wages + taxable_interest +
                (dividends - qualified_dividends) -
                ira_deduction - student_loan_interest)
```

**Refactored code (PEP 8 compliant):**
```python
total_income = (
    gross_wages
    + taxable_interest
    + (dividends - qualified_dividends)
    - ira_deduction
    - student_loan_interest
)
```

**Why this is better:**
- Breaking before operators (mathematical style)
- Each term is visually aligned
- Easier to scan and verify
- PEP 8 compliant (since 2016 update)

**Refactoring applied:** Break Before Binary Operator

**Attribution:** Brandon Rhodes, PEP 8 update

---

### FMT-BREAK-BEFORE-DOT: Break Before Method Calls

**Style Issue:** "Line too long (105/79)"

**Root Cause:** Long method chain

**Bad code (pylint: line too long):**
```python
query = Person.objects.filter(last_name='Smith').order_by('ssn').select_related('spouse')
```

**Refactored code:**
```python
query = (Person.objects
    .filter(last_name='Smith')
    .order_by('ssn')
    .select_related('spouse')
)
```

**Why this is better:**
- Each method call on its own line
- Breaking before dot shows continuation
- Easier to add/remove steps
- Visually clean

**Refactoring applied:** Break Before Dot (Method Chaining)

**Attribution:** Brandon Rhodes - "A Python Aesthetic"

---

### FMT-TRAILING-COMMA: Use Trailing Commas

**Style Issue:** "Inconsistent formatting in version control"

**Root Cause:** Adding items causes multi-line diffs

**Bad code (causes noisy diffs):**
```python
create_user(
    name='John',
    email='john@example.com',
    role='admin'
)

# Adding one parameter changes TWO lines in diff:
# -    role='admin'
# +    role='admin',
# +    department='IT'
```

**Refactored code:**
```python
create_user(
    name='John',
    email='john@example.com',
    role='admin',  # Trailing comma
)

# Adding one parameter changes ONE line:
# +    department='IT',
```

**Why this is better:**
- Cleaner version control diffs
- Symmetric formatting (all lines look same)
- Easier to reorder parameters
- Black formatter enforces this

**Refactoring applied:** Add Trailing Commas

**Attribution:** Brandon Rhodes, Black formatter

---

### FMT-ALIGN-TERNARY: Format Ternary Expressions

**Style Issue:** "Line too long (100/79)"

**Root Cause:** Complex ternary on one line

**Bad code (pylint: line too long):**
```python
result = very_long_function_name(arg1, arg2) if some_complex_condition(x, y, z) else another_long_function(arg3, arg4)
```

**Refactored option 1 (multi-line ternary):**
```python
result = (
    very_long_function_name(arg1, arg2)
    if some_complex_condition(x, y, z)
    else another_long_function(arg3, arg4)
)
```

**Refactored option 2 (if/else - often clearer):**
```python
if some_complex_condition(x, y, z):
    result = very_long_function_name(arg1, arg2)
else:
    result = another_long_function(arg3, arg4)
```

**Why this is better:**
- Option 1: Ternary properly formatted
- Option 2: Often more readable for complex cases
- No line length issues
- Condition is clear

**Refactoring applied:** Format Ternary OR Convert to If/Else

**Attribution:** Style guides

---

## 8. IMPORT & ORGANIZATION

### FMT-GROUP-IMPORTS: Group and Organize Imports

**Style Issue:** "Wrong import order (isort: I001)"

**Root Cause:** Imports not grouped properly

**Bad code (isort/flake8 warnings):**
```python
from myapp.models import User
import os
from typing import List
import sys
from myapp.utils import helper
from datetime import datetime
import json
```

**Refactored code:**
```python
# Standard library
import json
import os
import sys
from datetime import datetime
from typing import List

# Local application
from myapp.models import User
from myapp.utils import helper
```

**Why this is better:**
- PEP 8 compliant import order
- Grouped by category (stdlib, third-party, local)
- Alphabetically sorted within groups
- No linter warnings

**Refactoring applied:** Organize Imports (PEP 8)

**Attribution:** PEP 8, isort tool

---

### FMT-LAZY-IMPORT: Use Lazy Imports for Heavy Modules

**Style Issue:** "Module import time too long" or unused import

**Root Cause:** Expensive imports at module level

**Bad code (slow startup):**
```python
import tensorflow as tf  # Takes 3 seconds to import
import torch  # Takes 2 seconds

def quick_function():
    return "hello"  # Doesn't use tf or torch!

def ml_function():
    return tf.constant([1, 2, 3])
```

**Refactored code:**
```python
def quick_function():
    return "hello"  # Fast - no imports

def ml_function():
    import tensorflow as tf  # Only imported when needed
    return tf.constant([1, 2, 3])
```

**Why this is better:**
- Module loads quickly
- Heavy imports only when used
- Functions that don't use ML libs are fast
- Better for CLI tools

**Refactoring applied:** Lazy Import

**Attribution:** Performance optimization patterns

---

### FMT-STAR-IMPORT: Avoid Star Imports

**Style Issue:** "F403: Unable to detect undefined names" (flake8)

**Root Cause:** Star imports pollute namespace

**Bad code (flake8: F403, F405):**
```python
from utils import *

result = process_data(data)  # Where is process_data from?
```

**Refactored code:**
```python
from utils import process_data, validate_input, format_output

result = process_data(data)  # Clear it's from utils
```

**Why this is better:**
- Explicit is better than implicit
- Clear where each function comes from
- No namespace pollution
- Static analysis works properly

**Refactoring applied:** Replace Star Import with Explicit Imports

**Attribution:** PEP 8, Zen of Python

---

# End of Guidelines

Remember: When linters complain, don't just fix the symptom—refactor the code so the issue disappears naturally. Good structure leads to good style automatically.
