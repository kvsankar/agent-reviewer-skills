## Review: order_processor.py

### ✅ Strengths
- **NAMED-TUPLE**: Good use of dictionary structure for shipping labels with clear field names
- **DICT-COMP**: Clean dictionary comprehension usage in discount lookup

### ⚠️ Suggestions

#### HOIST-IO: I/O operations deeply embedded in business logic

**Current code:**
```python
def process(self, order_data):
    """Process an order from raw data."""
    with open("config/pricing.json") as f:  # File I/O in business logic
        config = json.load(f)
    
    # Business logic mixed with database calls
    cursor = _db.execute(
        "SELECT price FROM products WHERE id = ?", (item["product_id"],)
    )
    row = cursor.fetchone()
    
    _db.execute(
        "INSERT INTO orders VALUES (?, ?)",
        (order_id, json.dumps(order_data)),
    )
    _db.commit()
```

**Suggested refactoring:**
```python
def process_order_data(order_data, config, product_prices):
    """Pure function for order processing logic."""
    if not order_data.get("items"):
        return {"error": "No items"}
    
    total = 0
    for item in order_data["items"]:
        price = product_prices.get(item["product_id"], 0)
        if price:
            item_total = price * item["quantity"]
            if order_data.get("discount_code"):
                item_total = apply_discount(item_total, order_data["discount_code"])
            total += item_total
    
    total = apply_tax(total, config.get("tax_rate", 0.08))
    return {"total": total, "processed_items": order_data["items"]}

# I/O at top level
def process(self, order_data):
    with open("config/pricing.json") as f:
        config = json.load(f)
    
    product_prices = self._load_product_prices(order_data["items"])
    result = process_order_data(order_data, config, product_prices)
    
    if "error" not in result:
        order_id = self._save_order(order_data, result["total"])
        result["order_id"] = order_id
    
    return result
```

**Why this matters:**
`process_order_data()` becomes instantly testable with simple data structures. No file mocking or database setup required. Tests run 100x faster and reveal business logic bugs clearly.

**Rhodes' principle:**
"Move all I/O operations to the program's top level, allowing core logic to remain pure and testable."

---

#### NO-IMPORT-FX: Critical import-time side effects breaking modularity

**Current code:**
```python
import logging
import sqlite3

logging.basicConfig(level=logging.DEBUG, filename="/var/log/orders.log")
_db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
_db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")
```

**Suggested refactoring:**
```python
import logging
import sqlite3

# No side effects at import time
_db = None
_logger = None

def get_database():
    global _db
    if _db is None:
        _db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
        _db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")
    return _db

def get_logger():
    global _logger
    if _logger is None:
        logging.basicConfig(level=logging.DEBUG, filename="/var/log/orders.log")
        _logger = logging.getLogger(__name__)
    return _logger
```

**Why this matters:**
Import-time side effects make modules untestable and fragile. If `/var/log/orders.log` is read-only or the database path is invalid, importing this module crashes before your program even starts. Deferred initialization allows graceful handling.

**Rhodes' principle:**
"Avoid import-time side effects. Errors at import time are far more serious than errors at runtime."

---

#### NO-EVAL: Dangerous eval() usage creating security vulnerability

**Current code:**
```python
def apply_dynamic_rule(order, rule_string):
    """Apply a dynamic pricing rule.
    
    rule_string is something like "total * 0.9 if total > 100 else total"
    """
    total = order["total"]
    return eval(rule_string)  # SECURITY RISK!
```

**Suggested refactoring:**
```python
def apply_dynamic_rule(order, rule_name):
    """Apply a pre-defined pricing rule."""
    total = order["total"]
    
    rules = {
        "bulk_discount": lambda t: t * 0.9 if t > 100 else t,
        "premium_surcharge": lambda t: t * 1.1 if t > 500 else t,
        "loyalty_discount": lambda t: t * 0.95,
    }
    
    rule_func = rules.get(rule_name)
    if rule_func:
        return rule_func(total)
    return total
```

**Why this matters:**
`eval()` allows arbitrary code execution. If `rule_string` comes from user input, attackers can execute `"__import__('os').system('rm -rf /')"`. The dictionary approach provides safe, predefined rules while maintaining flexibility.

**Rhodes' principle:**
"Avoid eval() in application code. It has legitimate uses in developer tools but creates security risks in applications."

---

#### NO-MULTI-INHERIT: Multiple inheritance creating complex dependencies

**Current code:**
```python
class BaseProcessor:
    def log(self, msg):
        print(f"[LOG] {msg}")

class PricingMixin:
    def apply_tax(self, amount, rate=0.08):
        return amount * (1 + rate)

class DiscountMixin:
    def apply_discount(self, amount, code):
        discounts = {"SAVE10": 0.10, "SAVE20": 0.20, "VIP": 0.30}
        return amount * (1 - discounts.get(code, 0))

class OrderProcessor(BaseProcessor, PricingMixin, DiscountMixin):
    """Main order processing class using multiple inheritance."""
```

**Suggested refactoring:**
```python
class PricingService:
    def apply_tax(self, amount, rate=0.08):
        return amount * (1 + rate)
    
    def apply_discount(self, amount, code):
        discounts = {"SAVE10": 0.10, "SAVE20": 0.20, "VIP": 0.30}
        return amount * (1 - discounts.get(code, 0))

class OrderProcessor:
    def __init__(self, logger, pricing_service):
        self.logger = logger
        self.pricing = pricing_service
        self.orders = []
    
    def process(self, order_data):
        # Use injected dependencies
        price = self.pricing.apply_tax(total, config.get("tax_rate"))
        self.logger.log(f"Processed order {order_id}")
```

**Why this matters:**
Multiple inheritance creates testing nightmares. You can't test `PricingMixin` independently from `OrderProcessor`. Composition allows easy mocking: `processor = OrderProcessor(MockLogger(), MockPricing())`.

**Rhodes' principle:**
"Use composition—inject dependencies through constructor parameters. Multiple inheritance creates complexity and testing difficulties."

---

#### LIST-FRONT: O(n) operations on list front destroying performance

**Current code:**
```python
class PriorityQueue:
    def __init__(self):
        self.items = []

    def add_urgent(self, order):
        """Add urgent order to front of queue."""
        self.items.insert(0, order)  # O(n) operation!

    def add_batch(self, orders):
        """Add batch of orders, each to front for LIFO processing."""
        for order in orders:
            self.items.insert(0, order)  # O(n) for each item = O(n²)!
```

**Suggested refactoring:**
```python
from collections import deque

class PriorityQueue:
    def __init__(self):
        self.items = deque()

    def add_urgent(self, order):
        """Add urgent order to front of queue."""
        self.items.appendleft(order)  # O(1) operation

    def add_batch(self, orders):
        """Add batch of orders efficiently."""
        for order in orders:
            self.items.appendleft(order)  # O(1) for each = O(n) total
    
    def get_next(self):
        """Get next order to process."""
        return self.items.popleft() if self.items else None
```

**Why this matters:**
With 1000 orders, `add_batch()` performs ~500,000 operations (O(n²)). Using `deque` reduces this to 1000 operations—a 500x performance improvement. For high-volume e-commerce, this difference is critical.

**Rhodes' principle:**
"Never use pop(0) or insert(0, v) on large lists. Use collections.deque for double-ended operations."

---

#### NO-GLOBAL-MUT: Dangerous global mutable state creating coupling

**Current code:**
```python
REGISTERED_HANDLERS = []
ORDER_CACHE = {}

def register_handler(handler):
    REGISTERED_HANDLERS.append(handler)  # Modifies global state
```

**Suggested refactoring:**
```python
class HandlerRegistry:
    def __init__(self):
        self.handlers = []
        self.cache = {}
    
    def register(self, handler):
        self.handlers.append(handler)
    
    def get_handlers(self):
        return list(self.handlers)

# Create instance, pass as dependency
registry = HandlerRegistry()

class OrderProcessor:
    def __init__(self, handler_registry):
        self.registry = handler_registry
```

**Why this matters:**
Global mutable state makes tests non-isolated. One test registering handlers affects all subsequent tests. Threading creates race conditions. Debugging becomes impossible when data enters from multiple global sources.

**Rhodes' principle:**
"Global mutable state creates dangerous coupling between distant code sections and eliminates testing flexibility."

---

#### PRECISE-NOUN: Cryptic variable names hiding intent

**Current code:**
```python
def calc(d, r, t):
    p = d * (1 - r)
    f = p * (1 + t)
    return round(f, 2)
```

**Suggested refactoring:**
```python
def calculate_final_price(base_price, discount_rate, tax_rate):
    """Calculate final price after discount and tax."""
    discounted_price = base_price * (1 - discount_rate)
    final_price = discounted_price * (1 + tax_rate)
    return round(final_price, 2)
```

**Why this matters:**
`calc(100, 0.1, 0.08)` tells you nothing. `calculate_final_price(100, 0.1, 0.08)` immediately reveals this calculates a price with 10% discount and 8% tax. Self-documenting code eliminates need for comments and reduces bugs.

**Rhodes' principle:**
"Nouns should precisely describe objects. In duck-typed Python, names are critical for communicating intent."

---

#### INDENT-LIMIT: Deep nesting creating unmaintainable complexity

**Current code:**
```python
def validate_order_batch(orders, config):
    """Validate a batch of orders."""
    results = []
    for order in orders:
        if order.get("status") == "pending":
            if order.get("items"):
                for item in order["items"]:
                    if item.get("quantity", 0) > 0:
                        if item.get("product_id"):
                            if item["product_id"] in config["valid_products"]:
                                if item["quantity"] <= config["max_quantity"]:
                                    # 6 levels deep!
```

**Suggested refactoring:**
```python
def validate_order_batch(orders, config):
    """Validate a batch of orders."""
    results = []
    for order in orders:
        results.extend(validate_single_order(order, config))
    return results

def validate_single_order(order, config):
    """Validate one order, returning list of validation results."""
    if order.get("status") != "pending":
        return []
    
    items = order.get("items")
    if not items:
        return []
    
    return [validate_item(order["id"], item, config) for item in items]

def validate_item(order_id, item, config):
    """Validate a single item."""
    if item.get("quantity", 0) <= 0:
        return {"order_id": order_id, "valid": False, "reason": "zero quantity"}
    
    product_id = item.get("product_id")
    if not product_id:
        return {"order_id": order_id, "valid": False, "reason": "missing product"}
    
    if product_id not in config["valid_products"]:
        return {"order_id": order_id, "valid": False, "reason": "invalid product"}
    
    if item["quantity"] > config["max_quantity"]:
        return {"order_id": order_id, "item_id": product_id, 
                "valid": False, "reason": "exceeds max quantity"}
    
    return {"order_id": order_id, "item_id": product_id, "valid": True}
```

**Why this matters:**
Six levels of indentation create cognitive overload. Early returns and function extraction eliminate nesting. Each function now has a single responsibility and is independently testable.

**Rhodes' principle:**
"If you need more than 3 levels of indentation, you're screwed anyway." — Linus Torvalds

### 💡 Rhodes Wisdom
> "If you consider patch() an anti-pattern in production code—why are you doing it in your tests? Mocking signals architectural problems."
> — Hoisting Your I/O (2015)

> "Show me your tables, and I won't usually need your flowchart; it'll be obvious."
> — The Clean Architecture (2014)
