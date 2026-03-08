## Review: order_processor.py

### ✅ Strengths
- **NAMED-TUPLE**: Good use of dictionary structures for order data and shipping labels
- **PRECISE-NOUN**: Most variable names like `order_data`, `total`, `order_id` are descriptive

### ⚠️ Suggestions

#### HOIST-IO: I/O operations mixed throughout business logic

**Current code:**
```python
def process(self, order_data):
    """Process an order from raw data."""
    with open("config/pricing.json") as f:  # File I/O mixed with logic
        config = json.load(f)
    
    # Business logic mixed with database queries
    cursor = _db.execute(
        "SELECT price FROM products WHERE id = ?", (item["product_id"],)
    )
    row = cursor.fetchone()
    if row:
        price = row[0] * item["quantity"]
    
    # More I/O mixed in
    _db.execute(
        "INSERT INTO orders VALUES (?, ?)",
        (order_id, json.dumps(order_data)),
    )
    _db.commit()
```

**Suggested refactoring:**
```python
def process_order(order_data, config, product_prices):
    """Pure business logic - no I/O"""
    if not order_data.get("items"):
        return {"error": "No items"}
    
    total = calculate_order_total(order_data, product_prices, config)
    order_id = generate_order_id()
    
    return {
        "order_id": order_id,
        "total": total,
        "order_data": order_data
    }

# Caller handles all I/O at top level
def process_order_with_io(order_data):
    with open("config/pricing.json") as f:
        config = json.load(f)
    
    product_prices = load_product_prices_from_db()
    result = process_order(order_data, config, product_prices)
    
    if "error" not in result:
        save_order_to_db(result)
        send_notification(order_data.get("email"), result["order_id"])
    
    return result
```

**Why this matters:**
Separating I/O from business logic makes `process_order()` testable with simple data structures. You can test pricing calculations, validation, and business rules without mocking databases or files.

**Rhodes' principle:**
"Move all I/O operations to the program's top level, allowing core logic to remain pure and testable."

---

#### NO-IMPORT-FX: Import-time side effects create deployment fragility

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

def setup_logging():
    """Initialize logging - call from main()"""
    logging.basicConfig(level=logging.DEBUG, filename="/var/log/orders.log")

def get_database():
    """Get database connection - call when needed"""
    db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
    db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")
    return db

# In main() or application startup
if __name__ == "__main__":
    setup_logging()
    db = get_database()
```

**Why this matters:**
Import-time side effects break testing and deployment. If the log directory doesn't exist or database is unavailable, the entire module fails to import, making error handling impossible.

**Rhodes' principle:**
"Keep __init__.py files code-free and avoid all import-time side effects. Modules executing database queries or loading config at import time break testability."

---

#### NO-GLOBAL-MUT: Mutable globals create testing nightmares

**Current code:**
```python
REGISTERED_HANDLERS = []
ORDER_CACHE = {}

def register_handler(handler):
    REGISTERED_HANDLERS.append(handler)
```

**Suggested refactoring:**
```python
class HandlerRegistry:
    """Encapsulate handler state in a class"""
    def __init__(self):
        self.handlers = []
    
    def register(self, handler):
        self.handlers.append(handler)
    
    def get_handlers(self):
        return list(self.handlers)  # Return copy

# Pass registry instance around
def create_order_system():
    registry = HandlerRegistry()
    cache = {}  # Local to this instance
    return OrderProcessor(registry, cache)
```

**Why this matters:**
Global mutable state makes tests interdependent. One test's handler registration affects other tests. With instance-based design, each test gets a clean registry.

**Rhodes' principle:**
"Global mutable state creates problems: data enters functions from multiple directions, testing requires mutating globals, threading causes race conditions."

---

#### NO-MULTI-INHERIT: Multiple inheritance creates complexity

**Current code:**
```python
class OrderProcessor(BaseProcessor, PricingMixin, DiscountMixin):
    """Main order processing class using multiple inheritance."""
    
    def process(self, order_data):
        # Scattered logic across inherited methods
        price = self.apply_discount(price, order_data["discount_code"])
        total = self.apply_tax(total, config.get("tax_rate", 0.08))
```

**Suggested refactoring:**
```python
class PricingService:
    def apply_tax(self, amount, rate=0.08):
        return amount * (1 + rate)

class DiscountService:
    def apply_discount(self, amount, code):
        discounts = {"SAVE10": 0.10, "SAVE20": 0.20, "VIP": 0.30}
        rate = discounts.get(code, 0)
        return amount * (1 - rate)

class OrderProcessor:
    def __init__(self, pricing_service, discount_service, logger):
        self.pricing = pricing_service
        self.discounts = discount_service
        self.logger = logger
    
    def process(self, order_data):
        price = self.discounts.apply_discount(price, code)
        total = self.pricing.apply_tax(total, rate)
```

**Why this matters:**
Composition allows testing each service independently and swapping implementations at runtime. Multiple inheritance creates method resolution order complexity and testing combinatorial explosion.

**Rhodes' principle:**
"Multiple inheritance creates complexity and testing nightmares. Use composition—inject dependencies through constructor parameters."

---

#### NO-EVAL: eval() creates security vulnerabilities

**Current code:**
```python
def apply_dynamic_rule(order, rule_string):
    """Apply a dynamic pricing rule.

    rule_string is something like "total * 0.9 if total > 100 else total"
    """
    total = order["total"]
    return eval(rule_string)  # DANGEROUS!
```

**Suggested refactoring:**
```python
class RuleEngine:
    """Safe rule evaluation using predefined operations"""
    
    def __init__(self):
        self.operations = {
            'discount_percent': self._discount_percent,
            'threshold_discount': self._threshold_discount,
        }
    
    def apply_rule(self, order, rule_config):
        """Apply rule using safe configuration"""
        operation = rule_config['operation']
        params = rule_config['params']
        
        if operation not in self.operations:
            raise ValueError(f"Unknown operation: {operation}")
        
        return self.operations[operation](order['total'], **params)
    
    def _discount_percent(self, total, percent):
        return total * (1 - percent/100)
    
    def _threshold_discount(self, total, threshold, discount_percent):
        if total > threshold:
            return total * (1 - discount_percent/100)
        return total

# Usage with safe configuration
rule_config = {
    'operation': 'threshold_discount',
    'params': {'threshold': 100, 'discount_percent': 10}
}
```

**Why this matters:**
`eval()` allows arbitrary code execution, creating severe security vulnerabilities. Rule engines should use safe, predefined operations rather than evaluating arbitrary strings.

**Rhodes' principle:**
"eval() has limited legitimate use in application code but extensive utility in developer tools. Beginners often misuse it."

---

#### INDENT-LIMIT: Deeply nested conditionals indicate design problems

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
        if order.get("status") != "pending":
            continue
        
        if not order.get("items"):
            continue
            
        for item in order["items"]:
            result = validate_order_item(order, item, config)
            if result:
                results.append(result)
    
    return results

def validate_order_item(order, item, config):
    """Validate a single order item"""
    if item.get("quantity", 0) <= 0:
        return None
    
    if not item.get("product_id"):
        return None
    
    product_id = item["product_id"]
    
    if product_id not in config["valid_products"]:
        return create_validation_result(order, item, False, "invalid product")
    
    if item["quantity"] > config["max_quantity"]:
        return create_validation_result(order, item, False, "exceeds max quantity")
    
    return create_validation_result(order, item, True)

def create_validation_result(order, item, valid, reason=None):
    """Create validation result object"""
    result = {
        "order_id": order["id"],
        "item_id": item["product_id"],
        "valid": valid,
    }
    if reason:
        result["reason"] = reason
    return result
```

**Why this matters:**
Deep nesting creates cognitive overhead and maintenance problems. Using early returns (`continue`) and extracting functions creates flatter, more readable code.

**Rhodes' principle:**
"If you need more than 3 levels of indentation, you're screwed anyway. Use continue statements, method extraction, function factoring."

---

#### PRECISE-NOUN: Variable names should reveal intent

**Current code:**
```python
def calc(d, r, t):
    p = d * (1 - r)
    f = p * (1 + t)
    return round(f, 2)
```

**Suggested refactoring:**
```python
def calculate_final_price(discount_amount, discount_rate, tax_rate):
    """Calculate final price after discount and tax"""
    price_after_discount = discount_amount * (1 - discount_rate)
    final_price = price_after_discount * (1 + tax_rate)
    return round(final_price, 2)
```

**Why this matters:**
Single-letter variables create "type desert" where you can't understand what the function does without reading implementation. Descriptive names make code self-documenting.

**Rhodes' principle:**
"Nouns should precisely describe objects. When discovering imprecise variable name, refactor throughout."

---

#### USE-VERBS: Functions should use action verbs

**Current code:**
```python
class ReportService:
    def run(self, data):  # Vague verb
        result = []
        for item in data:
            result.append(self._do(item))  # Very vague verb
        return result
```

**Suggested refactoring:**
```python
class ReportService:
    def generate_report(self, order_data):  # Clear action
        report_items = []
        for order in order_data:
            report_item = self.calculate_order_summary(order)
            report_items.append(report_item)
        return report_items
    
    def calculate_order_summary(self, order):
        return {
            "name": order["name"],
            "total": sum(line["price"] * line["qty"] for line in order["lines"]),
        }
```

**Why this matters:**
Function names should clearly indicate what action they perform. `run()` and `_do()` tell you nothing about the actual operation being performed.

**Rhodes' principle:**
"Functions should use verbs: create_database() rather than database()."

---

### 💡 Rhodes Wisdom
> "If you consider patch() an anti-pattern in production code—why are you doing it in your tests? Mocking signals architectural problems."
> — Hoisting Your I/O (2015)

> "Using mock.patch() indicates code has coupled I/O that should be separated. Tests should act as a 'second caller' from day one to reveal coupling issues."
> — The Clean Architecture in Python (2014)
