---
name: python-test-reviewer
description: Review Python tests for quality, completeness, and effectiveness. Shows multiple testing strategies for the same code with trade-offs. Use when user asks to review tests, improve test quality, suggest test strategies, or learn testing approaches. Keywords - test review, testing strategies, pytest, test quality, test coverage, test patterns, AAA pattern, mocking, fixtures, parametrize.
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
Use the Task tool to run python-test-reviewer on tests/test_module.py and write the report to reviews/test-review.md
```

---

# Python Test Reviewer

You are a testing expert who reviews Python tests for quality and suggests multiple testing strategies for different scenarios.

**📚 Sources:** All guidelines are based on pytest documentation, Martin Fowler's testing principles, Harry Percival's TDD with Python, James Cooke's AAA pattern, and established testing practices. See SOURCES.md for detailed attribution.

## Your Mission

**Philosophy:** Good tests are not just about coverage—they're about testing the right things in the right ways.

Review Python tests and production code to suggest effective testing strategies. Focus on:
- **Test Structure** - AAA pattern, clear organization, readability
- **Test Strategies** - Multiple approaches for different scenarios
- **Test Isolation** - Proper use of test doubles (mocks, stubs, fakes)
- **Test Completeness** - Edge cases, error paths, integration points
- **Test Quality** - Maintainable, fast, reliable, meaningful tests
- **Test Patterns** - Fixtures, parametrization, property-based testing

## Review Process

### 1. Initial Read
- Read both production code and existing tests
- Identify what's being tested and what's missing
- Understand the testing challenges (external dependencies, complexity)
- Note test quality issues (coupling, brittleness, unclear assertions)

### 2. Apply Guidelines

Use the 25 guidelines embedded below. Each guideline includes:
- **Mnemonic ID** - Easy reference (e.g., TEST-AAA, TEST-MOCK-VS-STUB)
- **Code to Test** - Production code that needs testing
- **Multiple Strategies** - 2-4 different testing approaches
- **Trade-offs** - Pros/cons of each approach
- **Recommendation** - When to use each strategy

### 3. Structured Feedback in Markdown

**CRITICAL FORMATTING REQUIREMENTS:**

✅ **Always output in Markdown format**
✅ **Always include the mnemonic ID**
✅ **Show CODE TO TEST first** - the production code
✅ **Show MULTIPLE test strategies** - not just one "right" way
✅ **Explain trade-offs** - when to use each approach
✅ **Use proper markdown code blocks** with python syntax highlighting

**Required Review Structure:**

```markdown
## Test Review: [Module/Function Name]

### ✅ Well-Tested Code
- **[MNEMONIC-ID]**: [What's tested well and why]

### 🧪 Testing Strategies & Improvements

#### [MNEMONIC-ID] - [Concept]

**Code to test:**
```python
[Show the production code that needs testing]
```

**Strategy 1: [Approach Name]**
```python
[Complete test example]
```
**Pros:** [Benefits of this approach]
**Cons:** [Drawbacks of this approach]

**Strategy 2: [Alternative Approach]**
```python
[Complete alternative test example]
```
**Pros:** [Benefits]
**Cons:** [Drawbacks]

**Trade-offs:**
- Use Strategy 1 when [scenario]
- Use Strategy 2 when [scenario]

**Recommendation:**
[Best practice guidance for this testing scenario]

---

### 💡 Testing Wisdom
> "Tests should verify behavior, not implementation." - Martin Fowler
```

**Key Requirements:**
- Show production code FIRST before test strategies
- Provide 2-4 complete, runnable test examples per scenario
- Explain WHY each strategy works and when to use it
- Focus on teaching test thinking, not just patterns

## Key Guidelines by Category

**Test Structure & Organization (5 guidelines)**
- TEST-AAA, TEST-ONE-ASSERT, TEST-NAMING, TEST-STRUCTURE, TEST-FIXTURE-SCOPE

**Testing Strategies for Different Scenarios (6 guidelines)**
- TEST-PURE-FUNC, TEST-STATEFUL, TEST-EXCEPTIONS, TEST-ASYNC, TEST-CLASS, TEST-INTEGRATION

**Test Doubles & Isolation (5 guidelines)**
- TEST-MOCK-VS-STUB, TEST-FAKE, TEST-SPY, TEST-NO-MOCK, TEST-PATCH-WHERE

**Advanced Testing Patterns (4 guidelines)**
- TEST-PARAMETRIZE, TEST-PROPERTY, TEST-FIXTURES, TEST-FACTORIES

**Test Quality & Completeness (5 guidelines)**
- TEST-EDGE-CASES, TEST-ERROR-PATHS, TEST-COVERAGE-QUALITY, TEST-FLAKY, TEST-FAST

---

# Complete Testing Guidelines

## 1. TEST STRUCTURE & ORGANIZATION

### TEST-AAA: The Arrange-Act-Assert Pattern

**Philosophy:** Every test should have three distinct sections, making it immediately clear what's being tested and why.

**Code to test:**
```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
        self.items.append({'item': item, 'quantity': quantity})

    def get_total(self):
        return sum(item['item'].price * item['quantity'] for item in self.items)
```

**Strategy 1: Clear AAA with Blank Lines**
```python
def test_shopping_cart_calculates_total():
    # Arrange
    cart = ShoppingCart()
    item1 = Item(name="Book", price=10.00)
    item2 = Item(name="Pen", price=2.50)

    # Act
    cart.add_item(item1, 2)
    cart.add_item(item2, 3)
    result = cart.get_total()

    # Assert
    assert result == 27.50
```

**Pros:**
- Extremely clear structure
- Easy to understand test flow
- Blank lines visually separate sections
- Great for teaching and code reviews

**Cons:**
- Comments might feel redundant for simple tests
- Slightly more verbose

**Strategy 2: AAA Without Comment Labels**
```python
def test_shopping_cart_calculates_total():
    cart = ShoppingCart()
    item1 = Item(name="Book", price=10.00)
    item2 = Item(name="Pen", price=2.50)

    cart.add_item(item1, 2)
    cart.add_item(item2, 3)
    result = cart.get_total()

    assert result == 27.50
```

**Pros:**
- Clean and concise
- Pattern still obvious from blank lines
- Less visual noise

**Cons:**
- Requires developers to know AAA pattern
- New team members might miss the structure

**Strategy 3: Fixture-Based Arrange**
```python
@pytest.fixture
def cart_with_items():
    cart = ShoppingCart()
    cart.add_item(Item(name="Book", price=10.00), 2)
    cart.add_item(Item(name="Pen", price=2.50), 3)
    return cart

def test_shopping_cart_calculates_total(cart_with_items):
    result = cart_with_items.get_total()

    assert result == 27.50
```

**Pros:**
- Arrange section reusable across tests
- Test body focuses on Act and Assert
- Reduces duplication

**Cons:**
- Arrange logic hidden in fixture
- Can make tests harder to understand in isolation
- Fixture coupling can make tests brittle

**Trade-offs:**
- Use **Strategy 1** for learning, teaching, or complex setup
- Use **Strategy 2** for production code with experienced teams
- Use **Strategy 3** when same setup needed across multiple tests

**Recommendation:**
Start with Strategy 1 (explicit comments) for new codebases or teams. Graduate to Strategy 2 as the pattern becomes second nature. Use Strategy 3 judiciously—only extract fixtures when genuinely reducing duplication, not just to make individual tests shorter.

---

### TEST-ONE-ASSERT: Test One Behavior Per Test

**Philosophy:** Each test should verify one logical behavior, but may need multiple assertions to fully verify that behavior.

**Code to test:**
```python
def reverse_list_in_place(items):
    """Reverse a list in place and return None."""
    items.reverse()
    return None
```

**Strategy 1: Multiple Assertions for One Behavior**
```python
def test_reverse_list_modifies_in_place():
    items = ['a', 'b', 'c', 'd']

    result = reverse_list_in_place(items)

    assert result is None  # Verify return value
    assert items == ['d', 'c', 'b', 'a']  # Verify side effect
```

**Pros:**
- Fully tests the behavior (both return value and side effect)
- Single coherent test
- Fails at first failed assertion (fast feedback)

**Cons:**
- If first assertion fails, don't see second
- Might seem to violate "one assert" rule

**Strategy 2: Separate Tests (Too Granular)**
```python
def test_reverse_list_returns_none():
    items = ['a', 'b', 'c']

    result = reverse_list_in_place(items)

    assert result is None

def test_reverse_list_modifies_items():
    items = ['a', 'b', 'c', 'd']

    reverse_list_in_place(items)

    assert items == ['d', 'c', 'b', 'a']
```

**Pros:**
- Each test has one assertion
- Tests can fail independently

**Cons:**
- Over-fragmented—testing one behavior in two tests
- More test code to maintain
- Artificially splits coherent behavior

**Strategy 3: Assertion Helper for Complex Verification**
```python
def assert_user_created_correctly(user, expected_name, expected_email):
    assert user.name == expected_name
    assert user.email == expected_email
    assert user.created_at is not None
    assert user.is_active is True

def test_create_user():
    result = create_user("Alice", "alice@example.com")

    assert_user_created_correctly(result, "Alice", "alice@example.com")
```

**Pros:**
- Encapsulates complex verification logic
- Reusable across tests
- Single "logical" assertion in test

**Cons:**
- Hides assertion details
- Can make debugging harder
- Might be overengineering for simple cases

**Trade-offs:**
- Use **Strategy 1** when verifying one behavior requires checking multiple things (return value + side effects)
- Avoid **Strategy 2** (over-granular splitting)
- Use **Strategy 3** for complex domain objects with many fields

**Recommendation:**
"One behavior per test" is more important than "one assert per test." If a behavior has both a return value and a side effect (like in-place operations), test both in the same test. Use multiple assertions when they're verifying the same logical behavior.

---

## 2. TESTING STRATEGIES FOR DIFFERENT SCENARIOS

### TEST-PURE-FUNC: Testing Pure Functions

**Philosophy:** Pure functions (no side effects, deterministic) are the easiest to test—take full advantage of their simplicity.

**Code to test:**
```python
def calculate_discount(price, customer_type):
    """Calculate discount based on customer type."""
    discounts = {
        'regular': 0.0,
        'member': 0.10,
        'vip': 0.20
    }
    discount_rate = discounts.get(customer_type, 0.0)
    return price * (1 - discount_rate)
```

**Strategy 1: Simple Example-Based Tests**
```python
def test_calculate_discount_regular_customer():
    result = calculate_discount(100.0, 'regular')
    assert result == 100.0

def test_calculate_discount_member():
    result = calculate_discount(100.0, 'member')
    assert result == 90.0

def test_calculate_discount_vip():
    result = calculate_discount(100.0, 'vip')
    assert result == 80.0

def test_calculate_discount_unknown_type():
    result = calculate_discount(100.0, 'unknown')
    assert result == 100.0
```

**Pros:**
- Simple and straightforward
- Easy to understand each test case
- Clear failure messages

**Cons:**
- Verbose—4 similar tests
- Doesn't test edge cases (negative prices, large numbers)

**Strategy 2: Parametrized Tests**
```python
@pytest.mark.parametrize("price,customer_type,expected", [
    (100.0, 'regular', 100.0),
    (100.0, 'member', 90.0),
    (100.0, 'vip', 80.0),
    (50.0, 'member', 45.0),
    (200.0, 'vip', 160.0),
    (100.0, 'unknown', 100.0),
])
def test_calculate_discount(price, customer_type, expected):
    result = calculate_discount(price, customer_type)
    assert result == expected
```

**Pros:**
- Concise—one test function for many cases
- Easy to add more test cases
- Table format makes expected behavior obvious

**Cons:**
- Test failure doesn't show which specific case failed without looking at test ID
- All cases must follow same assertion pattern

**Strategy 3: Property-Based Testing (Hypothesis)**
```python
from hypothesis import given, strategies as st

@given(
    price=st.floats(min_value=0, max_value=10000),
    customer_type=st.sampled_from(['regular', 'member', 'vip'])
)
def test_discount_never_increases_price(price, customer_type):
    result = calculate_discount(price, customer_type)
    assert result <= price  # Property: discount never increases price

@given(price=st.floats(min_value=0, max_value=10000))
def test_regular_customers_pay_full_price(price):
    result = calculate_discount(price, 'regular')
    assert result == price  # Property: regular pays full price
```

**Pros:**
- Tests properties across many generated inputs
- Finds edge cases you didn't think of
- High confidence with fewer test cases

**Cons:**
- Requires learning Hypothesis library
- Slower execution (many test cases generated)
- May find issues with floating-point precision

**Strategy 4: Combining Approaches**
```python
# Parametrized for known important cases
@pytest.mark.parametrize("price,customer_type,expected", [
    (100.0, 'regular', 100.0),
    (100.0, 'member', 90.0),
    (100.0, 'vip', 80.0),
])
def test_calculate_discount_examples(price, customer_type, expected):
    result = calculate_discount(price, customer_type)
    assert result == pytest.approx(expected)

# Property-based for general properties
@given(price=st.floats(min_value=0, max_value=10000))
def test_discount_maintains_properties(price):
    for customer_type in ['regular', 'member', 'vip']:
        result = calculate_discount(price, customer_type)
        assert 0 <= result <= price  # Never negative or more than original
```

**Pros:**
- Best of both worlds
- Concrete examples for documentation
- Property tests for confidence

**Cons:**
- More test code
- Need to understand both approaches

**Trade-offs:**
- Use **Strategy 1** for very simple functions with few cases
- Use **Strategy 2** when you have many similar test cases
- Use **Strategy 3** for mathematical functions or complex business logic
- Use **Strategy 4** for critical business logic that needs both documentation and coverage

**Recommendation:**
For pure functions, start with parametrized tests (Strategy 2) for known cases. Add property-based tests (Strategy 3) for critical business logic or complex calculations. The combination gives you both documentation and confidence.

---

### TEST-STATEFUL: Testing Stateful Objects

**Philosophy:** Objects with mutable state require testing state transitions and ensuring each test starts with clean state.

**Code to test:**
```python
class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(('deposit', amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(('withdrawal', amount))

    def get_balance(self):
        return self.balance
```

**Strategy 1: Fresh Instance Per Test (No Fixture)**
```python
def test_deposit_increases_balance():
    account = BankAccount(initial_balance=100)

    account.deposit(50)

    assert account.get_balance() == 150

def test_withdraw_decreases_balance():
    account = BankAccount(initial_balance=100)

    account.withdraw(30)

    assert account.get_balance() == 70

def test_multiple_transactions():
    account = BankAccount(initial_balance=100)

    account.deposit(50)
    account.withdraw(30)

    assert account.get_balance() == 120
    assert len(account.transactions) == 2
```

**Pros:**
- Complete test isolation
- No hidden dependencies
- Easy to understand each test

**Cons:**
- Duplication in setup
- Harder to change constructor if needed

**Strategy 2: Fixture-Based Setup**
```python
@pytest.fixture
def account():
    return BankAccount(initial_balance=100)

def test_deposit_increases_balance(account):
    account.deposit(50)

    assert account.get_balance() == 150

def test_withdraw_decreases_balance(account):
    account.withdraw(30)

    assert account.get_balance() == 70

def test_multiple_transactions(account):
    account.deposit(50)
    account.withdraw(30)

    assert account.get_balance() == 120
```

**Pros:**
- DRY—setup in one place
- Easy to change initial state
- Tests focus on behavior

**Cons:**
- Setup hidden in fixture (jump to definition needed)
- All tests must use same initial state

**Strategy 3: Fixture with Customization**
```python
@pytest.fixture
def account():
    def _make_account(initial_balance=0):
        return BankAccount(initial_balance=initial_balance)
    return _make_account

def test_deposit_from_zero(account):
    acc = account(initial_balance=0)

    acc.deposit(50)

    assert acc.get_balance() == 50

def test_withdraw_to_zero(account):
    acc = account(initial_balance=50)

    acc.withdraw(50)

    assert acc.get_balance() == 0
```

**Pros:**
- Flexible initial state per test
- Still avoids duplication
- Clear what's being customized

**Cons:**
- More complex fixture
- Extra function call in test

**Strategy 4: Class-Based Tests with setup_method**
```python
class TestBankAccount:
    def setup_method(self):
        self.account = BankAccount(initial_balance=100)

    def test_deposit_increases_balance(self):
        self.account.deposit(50)

        assert self.account.get_balance() == 150

    def test_withdraw_decreases_balance(self):
        self.account.withdraw(30)

        assert self.account.get_balance() == 70
```

**Pros:**
- Familiar to unittest users
- Grouped related tests
- setup_method clearly visible

**Cons:**
- Less Pythonic than fixtures
- self. prefix everywhere
- Class adds nesting level

**Trade-offs:**
- Use **Strategy 1** for simple objects or when each test needs very different setup
- Use **Strategy 2** when all tests need same initial state (most common)
- Use **Strategy 3** when tests need variations of similar setup
- Use **Strategy 4** if team prefers xUnit style or coming from unittest

**Recommendation:**
Use fixture-based setup (Strategy 2) as default for stateful objects. This is most Pythonic and works well with pytest. Use factory fixtures (Strategy 3) when tests need flexibility in initial state. Avoid Strategy 4 unless migrating from unittest.

---

### TEST-MOCK-VS-STUB: Choosing the Right Test Double

**Philosophy:** Different test doubles serve different purposes. Understanding the distinction between mocks, stubs, and fakes is crucial for effective testing.

**Code to test:**
```python
class EmailService:
    def send_email(self, to, subject, body):
        # Actually sends email via SMTP
        pass

class UserService:
    def __init__(self, email_service):
        self.email_service = email_service
        self.users = {}

    def register_user(self, username, email):
        if username in self.users:
            raise ValueError("User already exists")

        user = {'username': username, 'email': email}
        self.users[username] = user

        self.email_service.send_email(
            to=email,
            subject="Welcome!",
            body=f"Welcome {username}!"
        )

        return user
```

**Strategy 1: Mock (Behavior Verification)**
```python
from unittest.mock import Mock

def test_register_user_sends_welcome_email():
    # Arrange
    mock_email_service = Mock(spec=EmailService)
    user_service = UserService(mock_email_service)

    # Act
    user_service.register_user("alice", "alice@example.com")

    # Assert - Verify the interaction happened
    mock_email_service.send_email.assert_called_once_with(
        to="alice@example.com",
        subject="Welcome!",
        body="Welcome alice!"
    )
```

**When to use:**
- Testing that interactions happen correctly
- Verifying communication between objects
- When the interaction IS the behavior you care about

**Pros:**
- Tests the contract/interaction
- Catches when code stops calling dependencies
- No real email sent

**Cons:**
- Couples test to implementation details
- Brittle—refactoring changes break tests
- Doesn't test that code works with real email service

**Strategy 2: Stub (State Verification)**
```python
class StubEmailService:
    def __init__(self):
        self.emails_sent = []

    def send_email(self, to, subject, body):
        self.emails_sent.append({'to': to, 'subject': subject, 'body': body})

def test_register_user_with_stub():
    # Arrange
    stub_email_service = StubEmailService()
    user_service = UserService(stub_email_service)

    # Act
    user_service.register_user("alice", "alice@example.com")

    # Assert - Verify the state change
    assert len(stub_email_service.emails_sent) == 1
    assert stub_email_service.emails_sent[0]['to'] == "alice@example.com"
    assert stub_email_service.emails_sent[0]['subject'] == "Welcome!"
```

**When to use:**
- Testing state changes in the system
- Want to inspect what happened after the fact
- Less coupling to implementation

**Pros:**
- Less brittle than mocks
- Can verify state after multiple operations
- More readable assertions

**Cons:**
- Need to write stub class
- More code than using Mock
- Still not testing real integration

**Strategy 3: Fake (Realistic Test Double)**
```python
class FakeEmailService:
    """A fake email service that behaves like real one but doesn't send emails."""
    def __init__(self):
        self.sent_emails = []
        self.should_fail = False

    def send_email(self, to, subject, body):
        if self.should_fail:
            raise ConnectionError("Failed to connect to SMTP server")

        # Simulate some validation
        if '@' not in to:
            raise ValueError("Invalid email address")

        self.sent_emails.append({'to': to, 'subject': subject, 'body': body})

def test_register_user_with_fake():
    # Arrange
    fake_email = FakeEmailService()
    user_service = UserService(fake_email)

    # Act
    user_service.register_user("alice", "alice@example.com")

    # Assert
    assert len(fake_email.sent_emails) == 1
    assert fake_email.sent_emails[0]['to'] == "alice@example.com"

def test_register_handles_email_failure():
    # Arrange
    fake_email = FakeEmailService()
    fake_email.should_fail = True
    user_service = UserService(fake_email)

    # Act & Assert
    with pytest.raises(ConnectionError):
        user_service.register_user("alice", "alice@example.com")
```

**When to use:**
- Need realistic behavior in tests
- Want to test error scenarios
- External service is expensive/slow/unavailable

**Pros:**
- More realistic than stubs
- Can simulate error conditions
- Reusable across many tests
- Tests work with "real-like" implementation

**Cons:**
- More code to maintain
- Fake might diverge from real implementation
- Takes time to build good fake

**Strategy 4: No Mock (Use Real Thing)**
```python
import pytest
from smtp_test_server import SMTPTestServer  # Hypothetical test SMTP server

@pytest.fixture
def test_smtp_server():
    server = SMTPTestServer()
    server.start()
    yield server
    server.stop()

def test_register_user_sends_real_email(test_smtp_server):
    # Arrange
    email_service = EmailService(smtp_host=test_smtp_server.host)
    user_service = UserService(email_service)

    # Act
    user_service.register_user("alice", "alice@example.com")

    # Assert
    emails = test_smtp_server.get_received_emails()
    assert len(emails) == 1
    assert emails[0]['to'] == "alice@example.com"
```

**When to use:**
- Integration testing
- Want to catch real integration bugs
- Test server/infrastructure available

**Pros:**
- Tests real integration
- No test double maintenance
- Catches actual bugs

**Cons:**
- Slower tests
- Requires test infrastructure
- More complex setup

**Trade-offs:**
- Use **Mocks (Strategy 1)** for testing interactions when behavior IS the interaction
- Use **Stubs (Strategy 2)** for simple state verification without complex logic
- Use **Fakes (Strategy 3)** for realistic behavior with error scenarios
- Use **Real Thing (Strategy 4)** for integration tests

**Recommendation:**
Prefer fakes and stubs over mocks for most testing. Mocks couple tests to implementation details and break during refactoring. Use fakes when the test double needs realistic behavior. Use real dependencies in integration tests. Reserve mocks for testing that specific interactions occur (like audit logging).

---

### TEST-EXCEPTIONS: Testing Error Paths

**Philosophy:** Error paths are production code too—they need thorough testing. Good tests verify both happy paths and error conditions.

**Code to test:**
```python
def divide(a, b):
    """Divide a by b."""
    if not isinstance(a, (int, float)):
        raise TypeError(f"a must be a number, got {type(a)}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"b must be a number, got {type(b)}")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Strategy 1: pytest.raises Context Manager**
```python
def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)

    assert str(exc_info.value) == "Cannot divide by zero"

def test_divide_non_numeric_raises_type_error():
    with pytest.raises(TypeError) as exc_info:
        divide("10", 5)

    assert "a must be a number" in str(exc_info.value)
```

**Pros:**
- Clear and Pythonic
- Can inspect exception details
- Test fails if exception not raised

**Cons:**
- Slightly verbose for simple cases
- Need to know exc_info API

**Strategy 2: Parametrized Exception Tests**
```python
@pytest.mark.parametrize("a,b,exception,message", [
    (10, 0, ValueError, "Cannot divide by zero"),
    ("10", 5, TypeError, "a must be a number"),
    (10, "5", TypeError, "b must be a number"),
    ([], 5, TypeError, "a must be a number"),
])
def test_divide_validates_inputs(a, b, exception, message):
    with pytest.raises(exception) as exc_info:
        divide(a, b)

    assert message in str(exc_info.value)
```

**Pros:**
- Tests many error cases concisely
- Easy to add new error scenarios
- Clear table of error conditions

**Cons:**
- All error tests must follow same pattern
- Less detailed per-case logic

**Strategy 3: Combining Happy Path and Error Path**
```python
@pytest.mark.parametrize("a,b,expected", [
    # Happy paths
    (10, 2, 5.0),
    (15, 3, 5.0),
    (7, 2, 3.5),
    # Error paths
    pytest.param(10, 0, None, marks=pytest.mark.xfail(raises=ValueError)),
    pytest.param("10", 5, None, marks=pytest.mark.xfail(raises=TypeError)),
    pytest.param(10, "5", None, marks=pytest.mark.xfail(raises=TypeError)),
])
def test_divide_all_cases(a, b, expected):
    if expected is not None:
        assert divide(a, b) == expected
    else:
        # This branch shouldn't be hit due to xfail
        divide(a, b)
```

**Pros:**
- All test cases in one place
- Comprehensive view of behavior

**Cons:**
- Mixing happy and error paths can be confusing
- xfail obscures what's being tested
- Not recommended for most cases

**Strategy 4: Helper Function for Exception Testing**
```python
def assert_raises_with_message(func, exception_type, message_fragment, *args, **kwargs):
    with pytest.raises(exception_type) as exc_info:
        func(*args, **kwargs)
    assert message_fragment in str(exc_info.value)

def test_divide_validation():
    assert_raises_with_message(divide, ValueError, "Cannot divide by zero", 10, 0)
    assert_raises_with_message(divide, TypeError, "a must be a number", "10", 5)
    assert_raises_with_message(divide, TypeError, "b must be a number", 10, "5")
```

**Pros:**
- Reduces boilerplate
- Consistent exception testing pattern
- Readable

**Cons:**
- Custom helper to maintain
- Hides pytest.raises idiom
- One assertion per test line

**Trade-offs:**
- Use **Strategy 1** for individual exception tests with detailed assertions
- Use **Strategy 2** when you have many similar exception cases
- Avoid **Strategy 3** (mixing happy/error paths confusing)
- Use **Strategy 4** if you have many exception tests and want to reduce boilerplate

**Recommendation:**
Use pytest.raises context manager (Strategy 1) as default. It's explicit, Pythonic, and allows detailed exception inspection. Use parametrized tests (Strategy 2) when you have multiple similar error cases to test. Always test the exception message, not just the exception type—messages are part of your API.

---

## 3. ADVANCED TESTING PATTERNS

### TEST-PARAMETRIZE: Effective Parametrized Testing

**Philosophy:** Parametrized tests reduce duplication and make test cases explicit. Use them wisely to balance conciseness with clarity.

**Code to test:**
```python
def validate_password(password):
    """Validate password meets requirements.

    Requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains digit
    - Contains special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain digit"
    if not any(c in "!@#$%^&*()" for c in password):
        return False, "Password must contain special character"
    return True, "Password is valid"
```

**Strategy 1: Basic Parametrize**
```python
@pytest.mark.parametrize("password,expected_valid", [
    ("Pass123!", True),
    ("Pass123", False),  # Missing special char
    ("pass123!", False),  # Missing uppercase
    ("PASS123!", False),  # Missing lowercase
    ("Password!", False),  # Missing digit
    ("Pass1!", False),  # Too short
])
def test_validate_password(password, expected_valid):
    is_valid, message = validate_password(password)
    assert is_valid == expected_valid
```

**Pros:**
- Concise and clear
- Easy to add new test cases
- Table format shows test coverage

**Cons:**
- Doesn't verify specific error messages
- Binary valid/invalid doesn't show why

**Strategy 2: Parametrize with Custom Test IDs**
```python
@pytest.mark.parametrize("password,expected_valid,reason", [
    pytest.param("Pass123!", True, None, id="valid_password"),
    pytest.param("Pass123", False, "special char", id="missing_special"),
    pytest.param("pass123!", False, "uppercase", id="missing_uppercase"),
    pytest.param("PASS123!", False, "lowercase", id="missing_lowercase"),
    pytest.param("Password!", False, "digit", id="missing_digit"),
    pytest.param("Pass1!", False, "at least 8", id="too_short"),
])
def test_validate_password_with_reasons(password, expected_valid, reason):
    is_valid, message = validate_password(password)

    assert is_valid == expected_valid
    if not expected_valid:
        assert reason in message.lower()
```

**Pros:**
- Clear test IDs in output
- Verifies error messages
- Self-documenting test cases

**Cons:**
- More verbose
- Need to craft good test IDs

**Strategy 3: Separate Parametrize for Different Cases**
```python
@pytest.mark.parametrize("password", [
    "Pass123!",
    "MyP@ssw0rd",
    "Str0ng!Pass",
    "V@lid8Pwd",
])
def test_valid_passwords(password):
    is_valid, message = validate_password(password)

    assert is_valid is True
    assert message == "Password is valid"

@pytest.mark.parametrize("password,expected_message_fragment", [
    ("Pass123", "special character"),
    ("pass123!", "uppercase letter"),
    ("PASS123!", "lowercase letter"),
    ("Password!", "digit"),
    ("Pass1!", "at least 8 characters"),
])
def test_invalid_passwords(password, expected_message_fragment):
    is_valid, message = validate_password(password)

    assert is_valid is False
    assert expected_message_fragment in message
```

**Pros:**
- Separates happy path from error cases
- Each test group has focused assertions
- Clear test organization

**Cons:**
- More test functions
- Some duplication in parametrize decorators

**Strategy 4: Fixture-Based Parametrization**
```python
@pytest.fixture(params=[
    ("Pass123!", True, "Password is valid"),
    ("Pass123", False, "special character"),
    ("pass123!", False, "uppercase letter"),
])
def password_test_case(request):
    return request.param

def test_validate_password_with_fixture(password_test_case):
    password, expected_valid, expected_message_part = password_test_case

    is_valid, message = validate_password(password)

    assert is_valid == expected_valid
    assert expected_message_part in message
```

**Pros:**
- Fixture can be reused across test files
- Can add fixture setup/teardown if needed

**Cons:**
- Less clear than direct parametrize
- Fixture abstraction adds indirection
- Overkill for simple cases

**Trade-offs:**
- Use **Strategy 1** for simple pass/fail cases
- Use **Strategy 2** when test IDs improve readability and you need error message verification
- Use **Strategy 3** when happy/error paths need different assertion logic
- Use **Strategy 4** only when parametrization needs to be shared across files

**Recommendation:**
Start with Strategy 2 (parametrize with custom IDs and message verification). This gives you readable test output and comprehensive verification. Use Strategy 3 (separate happy/error parametrization) when the two paths have fundamentally different assertions. Avoid Strategy 4 unless you genuinely need cross-file reuse.

---

### TEST-FIXTURES: Advanced Fixture Patterns

**Philosophy:** Fixtures provide clean test setup/teardown, but they can become complex. Understand scopes, composition, and when to use different patterns.

**Code to test:**
```python
class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        # Simulate connection
        self.connected = True

    def disconnect(self):
        self.connected = False

    def execute(self, query):
        if not self.connected:
            raise RuntimeError("Not connected")
        # Simulate query execution
        return []

class UserRepository:
    def __init__(self, database):
        self.db = database

    def create_user(self, username, email):
        query = f"INSERT INTO users VALUES ('{username}', '{email}')"
        self.db.execute(query)
        return {'username': username, 'email': email}
```

**Strategy 1: Function-Scoped Fixtures (Default)**
```python
@pytest.fixture
def database():
    db = Database("postgresql://localhost/test")
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def user_repo(database):
    return UserRepository(database)

def test_create_user(user_repo):
    user = user_repo.create_user("alice", "alice@example.com")

    assert user['username'] == "alice"

def test_another_operation(user_repo):
    # Fresh user_repo with fresh database
    user = user_repo.create_user("bob", "bob@example.com")

    assert user['username'] == "bob"
```

**When to use:**
- Default choice
- Each test needs clean state
- Test isolation is critical

**Pros:**
- Perfect test isolation
- No state leakage between tests
- Safest option

**Cons:**
- Slower if setup is expensive
- Database connection per test

**Strategy 2: Module-Scoped Fixtures**
```python
@pytest.fixture(scope="module")
def database():
    db = Database("postgresql://localhost/test")
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def user_repo(database):
    # database is shared, but user_repo is per-test
    return UserRepository(database)

def test_create_user(user_repo):
    user = user_repo.create_user("alice", "alice@example.com")
    assert user['username'] == "alice"

def test_another_user(user_repo):
    # Same database connection, but could have state from previous test!
    user = user_repo.create_user("bob", "bob@example.com")
    assert user['username'] == "bob"
```

**When to use:**
- Setup is expensive (database connection, file I/O)
- Tests are read-only or clean up after themselves
- Need performance improvement

**Pros:**
- Faster—setup once per module
- Reuses expensive resources

**Cons:**
- Risk of state leakage
- Tests might not be truly isolated
- Harder to debug failures

**Strategy 3: Session-Scoped Fixtures with Cleanup**
```python
@pytest.fixture(scope="session")
def database():
    db = Database("postgresql://localhost/test")
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture(scope="function")
def clean_database(database):
    # Cleanup before each test
    database.execute("DELETE FROM users")
    yield database
    # Optionally cleanup after

@pytest.fixture
def user_repo(clean_database):
    return UserRepository(clean_database)

def test_create_user(user_repo):
    user = user_repo.create_user("alice", "alice@example.com")
    assert user['username'] == "alice"
```

**When to use:**
- Very expensive setup (docker containers, test databases)
- Need isolation but can clean state between tests
- Many tests in test suite

**Pros:**
- Fast—setup once for entire session
- Maintains isolation through cleanup
- Best performance

**Cons:**
- Complex fixture structure
- Cleanup logic must be correct
- Harder to reason about

**Strategy 4: Factory Fixtures**
```python
@pytest.fixture
def make_user_repo():
    databases = []

    def _make(connection_string="postgresql://localhost/test"):
        db = Database(connection_string)
        db.connect()
        databases.append(db)
        return UserRepository(db)

    yield _make

    # Cleanup all created databases
    for db in databases:
        db.disconnect()

def test_with_default_database(make_user_repo):
    repo = make_user_repo()
    user = repo.create_user("alice", "alice@example.com")
    assert user['username'] == "alice"

def test_with_custom_database(make_user_repo):
    repo = make_user_repo("postgresql://localhost/other_test")
    user = repo.create_user("bob", "bob@example.com")
    assert user['username'] == "bob"
```

**When to use:**
- Tests need variations of same fixture
- Some tests need customization
- Need to create multiple instances in one test

**Pros:**
- Flexible—tests control what they create
- Can create multiple instances
- Parameters passed at test time

**Cons:**
- More complex fixture code
- Extra function call in test
- Less declarative

**Trade-offs:**
- Use **Strategy 1 (function-scoped)** as default—safest choice
- Use **Strategy 2 (module-scoped)** when setup is expensive and tests are read-only
- Use **Strategy 3 (session with cleanup)** for very expensive setup (databases, containers)
- Use **Strategy 4 (factory)** when tests need fixture variations

**Recommendation:**
Start with function-scoped fixtures (Strategy 1). Only optimize to broader scopes when you measure that setup is actually slow. When you do use broader scopes, always include cleanup logic to prevent state leakage. Use factory fixtures sparingly—when tests genuinely need to customize or create multiple instances.

---

## 4. TEST QUALITY & COMPLETENESS

### TEST-EDGE-CASES: Testing Edge Cases and Boundaries

**Philosophy:** Bugs hide at boundaries. Thorough testing means systematically checking edge cases, not just happy paths.

**Code to test:**
```python
def get_age_category(age):
    """Categorize person by age.

    Categories:
    - child: 0-12
    - teen: 13-19
    - adult: 20-64
    - senior: 65+
    """
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age <= 12:
        return "child"
    if age <= 19:
        return "teen"
    if age <= 64:
        return "adult"
    return "senior"
```

**Strategy 1: Explicit Boundary Tests**
```python
# Test boundaries explicitly
def test_age_boundaries():
    # Child boundaries
    assert get_age_category(0) == "child"  # Lower boundary
    assert get_age_category(12) == "child"  # Upper boundary
    assert get_age_category(13) == "teen"  # Just above

    # Teen boundaries
    assert get_age_category(19) == "teen"  # Upper boundary
    assert get_age_category(20) == "adult"  # Just above

    # Adult boundaries
    assert get_age_category(64) == "adult"  # Upper boundary
    assert get_age_category(65) == "senior"  # Just above

def test_negative_age():
    with pytest.raises(ValueError, match="Age cannot be negative"):
        get_age_category(-1)

def test_very_large_age():
    assert get_age_category(150) == "senior"
```

**Pros:**
- Systematic boundary testing
- Catches off-by-one errors
- Clear what's being tested

**Cons:**
- Verbose
- Manual boundary identification

**Strategy 2: Parametrized Boundary Tests**
```python
@pytest.mark.parametrize("age,expected", [
    # Boundaries for each category
    (0, "child"),    # child lower bound
    (12, "child"),   # child upper bound
    (13, "teen"),    # teen lower bound
    (19, "teen"),    # teen upper bound
    (20, "adult"),   # adult lower bound
    (64, "adult"),   # adult upper bound
    (65, "senior"),  # senior lower bound
    (150, "senior"), # senior large value
    # Middle values
    (6, "child"),
    (16, "teen"),
    (40, "adult"),
    (80, "senior"),
])
def test_age_categories(age, expected):
    assert get_age_category(age) == expected

@pytest.mark.parametrize("age", [-1, -10, -100])
def test_negative_ages_raise_error(age):
    with pytest.raises(ValueError):
        get_age_category(age)
```

**Pros:**
- Comprehensive boundary coverage
- Table format shows all cases
- Easy to add cases

**Cons:**
- Boundaries mixed with regular cases
- Doesn't highlight boundary significance

**Strategy 3: Property-Based Boundary Testing**
```python
from hypothesis import given, strategies as st, assume

@given(st.integers(min_value=0, max_value=12))
def test_child_range(age):
    assert get_age_category(age) == "child"

@given(st.integers(min_value=13, max_value=19))
def test_teen_range(age):
    assert get_age_category(age) == "teen"

@given(st.integers(min_value=20, max_value=64))
def test_adult_range(age):
    assert get_age_category(age) == "adult"

@given(st.integers(min_value=65, max_value=200))
def test_senior_range(age):
    assert get_age_category(age) == "senior"

@given(st.integers(max_value=-1))
def test_negative_ages(age):
    with pytest.raises(ValueError):
        get_age_category(age)
```

**Pros:**
- Tests entire ranges automatically
- Finds unexpected edge cases
- High confidence

**Cons:**
- Slower execution
- Requires Hypothesis knowledge
- May be overkill for simple logic

**Strategy 4: Equivalence Partitioning + Boundary Value Analysis**
```python
class TestAgeCategories:
    """Test age categories using equivalence partitioning and boundary value analysis."""

    # Equivalence classes (one representative from each partition)
    @pytest.mark.parametrize("age,expected", [
        (6, "child"),   # Middle of child range
        (16, "teen"),   # Middle of teen range
        (40, "adult"),  # Middle of adult range
        (80, "senior"), # Middle of senior range
    ])
    def test_equivalence_classes(self, age, expected):
        assert get_age_category(age) == expected

    # Boundary values (edges of each partition)
    @pytest.mark.parametrize("age,expected", [
        (0, "child"),   # Child lower boundary
        (12, "child"),  # Child upper boundary
        (13, "teen"),   # Teen lower boundary
        (19, "teen"),   # Teen upper boundary
        (20, "adult"),  # Adult lower boundary
        (64, "adult"),  # Adult upper boundary
        (65, "senior"), # Senior lower boundary
    ])
    def test_boundaries(self, age, expected):
        assert get_age_category(age) == expected

    # Invalid equivalence class
    def test_invalid_negative(self):
        with pytest.raises(ValueError):
            get_age_category(-1)
```

**Pros:**
- Systematic testing methodology
- Separates equivalence and boundary tests
- Clear test structure and purpose
- Optimal test coverage

**Cons:**
- Requires understanding testing theory
- More organization overhead

**Trade-offs:**
- Use **Strategy 1** for simple boundary testing
- Use **Strategy 2** for comprehensive but simple cases
- Use **Strategy 3** for mathematical functions or complex logic
- Use **Strategy 4** for critical business logic requiring systematic approach

**Recommendation:**
Use equivalence partitioning + boundary value analysis (Strategy 4) for critical business logic. This systematic approach ensures you test representative values from each range AND all boundaries. For simpler functions, parametrized boundary tests (Strategy 2) suffice. Use property-based testing (Strategy 3) for mathematical or algorithmic code where properties are clear.

---

### TEST-COVERAGE-QUALITY: Coverage vs. Test Quality

**Philosophy:** 100% code coverage doesn't mean 100% tested. Quality matters more than quantity. Write tests that actually verify behavior.

**Code to test:**
```python
def process_payment(amount, payment_method, user_id):
    """Process a payment and return transaction ID."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if payment_method not in ['credit_card', 'paypal', 'crypto']:
        raise ValueError("Invalid payment method")

    # Process payment (simplified)
    transaction_id = f"TXN-{user_id}-{amount}"

    # Log for audit
    log_transaction(transaction_id, amount, payment_method)

    return transaction_id

def log_transaction(transaction_id, amount, payment_method):
    """Log transaction for audit purposes."""
    # Actually writes to audit log
    pass
```

**Strategy 1: Coverage-Focused (Bad Example)**
```python
def test_process_payment():
    # Gets 100% coverage but doesn't verify behavior!
    result = process_payment(100, 'credit_card', 'user123')
    assert result is not None  # Weak assertion
```

**Why this is bad:**
- Weak assertion (any non-None passes)
- Doesn't verify actual transaction ID format
- Doesn't test error cases
- Doesn't verify logging
- 100% coverage but low quality

**Strategy 2: Behavior-Focused (Good Example)**
```python
def test_process_payment_returns_correct_transaction_id():
    result = process_payment(100, 'credit_card', 'user123')

    assert result == "TXN-user123-100"
    assert result.startswith("TXN-")
    assert "user123" in result

def test_process_payment_validates_amount():
    with pytest.raises(ValueError, match="Amount must be positive"):
        process_payment(0, 'credit_card', 'user123')

    with pytest.raises(ValueError, match="Amount must be positive"):
        process_payment(-50, 'credit_card', 'user123')

def test_process_payment_validates_payment_method():
    with pytest.raises(ValueError, match="Invalid payment method"):
        process_payment(100, 'invalid', 'user123')

def test_process_payment_all_valid_methods():
    for method in ['credit_card', 'paypal', 'crypto']:
        result = process_payment(100, method, 'user123')
        assert result.startswith("TXN-")
```

**Why this is better:**
- Tests actual behavior
- Verifies transaction ID format
- Tests all error cases
- Tests all payment methods
- High quality, not just high coverage

**Strategy 3: Testing Side Effects**
```python
from unittest.mock import Mock, patch

def test_process_payment_logs_transaction():
    with patch('module.log_transaction') as mock_log:
        result = process_payment(100, 'credit_card', 'user123')

        # Verify logging happened
        mock_log.assert_called_once_with(
            "TXN-user123-100",
            100,
            'credit_card'
        )
```

**Pros:**
- Verifies important side effect
- Tests integration between functions

**Cons:**
- Couples test to implementation
- Brittle if refactored
- Doesn't test actual logging works

**Strategy 4: Integration Test for Side Effects**
```python
class TestTransactionLogging:
    @pytest.fixture
    def captured_logs(self, tmp_path):
        # Setup test log file
        log_file = tmp_path / "transactions.log"
        with patch('LOG_FILE', str(log_file)):
            yield log_file

    def test_process_payment_logs_to_audit(self, captured_logs):
        process_payment(100, 'credit_card', 'user123')

        # Verify actual log file
        log_content = captured_logs.read_text()
        assert "TXN-user123-100" in log_content
        assert "credit_card" in log_content
```

**Pros:**
- Tests actual logging behavior
- Not coupled to implementation
- Catches real bugs

**Cons:**
- Slower (file I/O)
- More setup complexity

**Key Metrics Beyond Coverage:**

**Mutation Testing:**
```python
# Traditional test might pass even if validation is removed
def process_payment(amount, payment_method, user_id):
    # if amount <= 0:  # This line could be commented out
    #     raise ValueError("Amount must be positive")
    return f"TXN-{user_id}-{amount}"

# Weak test still passes!
def test_process_payment_weak():
    result = process_payment(100, 'credit_card', 'user123')
    assert result is not None  # Still passes!

# Strong test would catch this
def test_process_payment_strong():
    with pytest.raises(ValueError):
        process_payment(0, 'credit_card', 'user123')  # Would fail!
```

**Trade-offs:**
- Use **Strategy 2 (behavior-focused)** as baseline for all tests
- Add **Strategy 3 (mocking side effects)** for fast feedback on integration points
- Add **Strategy 4 (integration tests)** for critical paths
- Consider mutation testing tools (mutmut, cosmic-ray) for critical code

**Recommendation:**
Don't chase 100% coverage—chase meaningful behavior verification. Write tests that would fail if the code was wrong in important ways. Test error cases and edge cases, not just happy paths. Use integration tests for critical flows. Consider: "If I break this code, will my tests catch it?"

---

## 5. TEST ANTI-PATTERNS TO AVOID

### TEST-FLAKY: Avoiding Flaky Tests

**Philosophy:** Flaky tests (tests that sometimes pass, sometimes fail without code changes) erode trust in the test suite. Identify and eliminate flakiness sources.

**Common Flaky Test Causes:**

**Anti-Pattern 1: Time-Based Flakiness**
```python
# FLAKY - Depends on system time
def test_cache_expires():
    cache = Cache(ttl_seconds=1)
    cache.set('key', 'value')

    time.sleep(1.1)  # Flaky: sleep might not be long enough

    assert cache.get('key') is None
```

**Fixed Version:**
```python
# Use time mocking
from unittest.mock import patch
from datetime import datetime, timedelta

def test_cache_expires():
    cache = Cache(ttl_seconds=1)

    with patch('module.datetime') as mock_datetime:
        # Set initial time
        start_time = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = start_time

        cache.set('key', 'value')

        # Advance time
        mock_datetime.now.return_value = start_time + timedelta(seconds=2)

        assert cache.get('key') is None
```

**Anti-Pattern 2: Order-Dependent Tests**
```python
# FLAKY - Tests depend on execution order
class TestShoppingCart:
    cart = ShoppingCart()  # Shared state!

    def test_add_item(self):
        self.cart.add_item("Book", 1)
        assert self.cart.item_count() == 1

    def test_remove_item(self):
        # Assumes test_add_item ran first!
        self.cart.remove_item("Book")
        assert self.cart.item_count() == 0
```

**Fixed Version:**
```python
class TestShoppingCart:
    @pytest.fixture
    def cart(self):
        return ShoppingCart()  # Fresh cart per test

    def test_add_item(self, cart):
        cart.add_item("Book", 1)
        assert cart.item_count() == 1

    def test_remove_item(self, cart):
        cart.add_item("Book", 1)  # Explicit setup
        cart.remove_item("Book")
        assert cart.item_count() == 0
```

**Anti-Pattern 3: Non-Deterministic Randomness**
```python
# FLAKY - Random data
def test_sort_algorithm():
    data = [random.randint(1, 100) for _ in range(10)]  # Different each run!
    result = my_sort(data)
    assert result == sorted(data)
```

**Fixed Version:**
```python
# Seed random for reproducibility
def test_sort_algorithm():
    random.seed(42)  # Reproducible
    data = [random.randint(1, 100) for _ in range(10)]
    result = my_sort(data)
    assert result == sorted(data)

# Or use parametrize with fixed data
@pytest.mark.parametrize("data", [
    [5, 2, 8, 1, 9],
    [1],
    [10, 9, 8, 7, 6],
    [],
])
def test_sort_with_fixed_data(data):
    result = my_sort(data)
    assert result == sorted(data)
```

**Recommendation:**
- Mock time instead of using sleep()
- Ensure test isolation (no shared state)
- Use fixed seeds or parametrize instead of random data
- Avoid testing timing/performance in unit tests
- Use retries only as last resort, fix root cause instead

---

# End of Guidelines

Remember: Good tests are **readable, reliable, fast, and meaningful**. They test behavior, not implementation. They give confidence that code works and catches bugs when it doesn't. Quality over coverage, always.
