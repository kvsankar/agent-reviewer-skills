# Python Code Review: Order Processing Module

## Critical Issues

### GLOBAL-STATE
**Global mutable state and module-level side effects**

**Current code:**
```python
_db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
_db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")
REGISTERED_HANDLERS = []
ORDER_CACHE = {}
```

**Improved version:**
```python
from dataclasses import dataclass
from typing import Protocol

class DatabaseConnection(Protocol):
    def execute(self, query: str, params: tuple = ()) -> Any: ...
    def commit(self) -> None: ...

@dataclass
class OrderConfig:
    db_path: str
    tax_rate: float = 0.08
    log_file: str = "/var/log/orders.log"

class DatabaseFactory:
    @staticmethod
    def create_connection(db_path: str) -> sqlite3.Connection:
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")
        return conn
```

**Explanation:** Global mutable state makes testing impossible and creates hidden dependencies. Use dependency injection and factory patterns instead.

---

### SRP-VIOLATION
**OrderProcessor violates Single Responsibility Principle**

**Current code:**
```python
def process(self, order_data):
    """Process an order from raw data."""
    with open("config/pricing.json") as f:  # File I/O
        config = json.load(f)
    
    if not order_data.get("items"):  # Validation
        return {"error": "No items"}
    
    total = 0
    for item in order_data["items"]:  # Price calculation
        cursor = _db.execute(...)  # Database access
        # ... pricing logic
    
    _db.execute("INSERT INTO orders VALUES (?, ?)", ...)  # Persistence
    self.notify(order_data.get("email", ""), ...)  # Notification
```

**Improved version:**
```python
class OrderService:
    def __init__(
        self, 
        validator: OrderValidator,
        pricing_service: PricingService,
        repository: OrderRepository,
        notification_service: NotificationService
    ):
        self._validator = validator
        self._pricing_service = pricing_service
        self._repository = repository
        self._notification_service = notification_service
    
    def process(self, order_data: dict) -> ProcessingResult:
        # Validate
        errors = self._validator.validate(order_data)
        if errors:
            return ProcessingResult.failure(errors)
        
        # Calculate pricing
        total = self._pricing_service.calculate_total(order_data)
        
        # Create order
        order = Order.from_data(order_data, total)
        order_id = self._repository.save(order)
        
        # Notify
        self._notification_service.send_confirmation(order.email, order_id)
        
        return ProcessingResult.success(order_id, total)
```

**Explanation:** Each class now has a single responsibility, making the code more testable and maintainable.

---

### DEEP-NESTING
**Excessive nesting reduces readability**

**Current code:**
```python
def validate_order_batch(orders, config):
    results = []
    for order in orders:
        if order.get("status") == "pending":
            if order.get("items"):
                for item in order["items"]:
                    if item.get("quantity", 0) > 0:
                        if item.get("product_id"):
                            if item["product_id"] in config["valid_products"]:
                                if item["quantity"] <= config["max_quantity"]:
                                    results.append(...)
```

**Improved version:**
```python
def validate_order_batch(orders: List[dict], config: dict) -> List[ValidationResult]:
    results = []
    
    for order in orders:
        if order.get("status") != "pending":
            continue
            
        items = order.get("items")
        if not items:
            continue
            
        for item in items:
            result = _validate_item(item, order["id"], config)
            if result:
                results.append(result)
    
    return results

def _validate_item(item: dict, order_id: str, config: dict) -> Optional[ValidationResult]:
    if item.get("quantity", 0) <= 0:
        return None
        
    product_id = item.get("product_id")
    if not product_id:
        return None
        
    if product_id not in config["valid_products"]:
        return None
        
    quantity = item["quantity"]
    if quantity > config["max_quantity"]:
        return ValidationResult(
            order_id=order_id,
            item_id=product_id,
            valid=False,
            reason="exceeds max quantity"
        )
    
    return ValidationResult(
        order_id=order_id,
        item_id=product_id,
        valid=True
    )
```

**Explanation:** Use early returns and extract methods to reduce nesting. This follows the "fail fast" principle and improves readability.

---

### SECURITY-RISK
**Using eval() creates security vulnerability**

**Current code:**
```python
def apply_dynamic_rule(order, rule_string):
    """Apply a dynamic pricing rule.
    
    rule_string is something like "total * 0.9 if total > 100 else total"
    """
    total = order["total"]
    return eval(rule_string)
```

**Improved version:**
```python
from typing import Callable

class RuleEngine:
    def __init__(self):
        self._rules: Dict[str, Callable[[float], float]] = {
            "bulk_discount": lambda total: total * 0.9 if total > 100 else total,
            "premium_discount": lambda total: total * 0.85 if total > 500 else total,
        }
    
    def apply_rule(self, rule_name: str, total: float) -> float:
        if rule_name not in self._rules:
            raise ValueError(f"Unknown rule: {rule_name}")
        return self._rules[rule_name](total)
    
    def register_rule(self, name: str, rule_func: Callable[[float], float]):
        self._rules[name] = rule_func
```

**Explanation:** `eval()` can execute arbitrary code. Use a predefined rule system or safe expression evaluators instead.

---

## High Priority Issues

### BAD-NAMES
**Poor naming hurts readability**

**Current code:**
```python
def calc(d, r, t):
    p = d * (1 - r)
    f = p * (1 + t)
    return round(f, 2)

class ReportService:
    def _do(self, item):
        return {
            "name": item["name"],
            "total": sum(i["price"] * i["qty"] for i in item["lines"]),
        }
```

**Improved version:**
```python
def calculate_final_price(discount_amount: float, discount_rate: float, tax_rate: float) -> float:
    """Calculate final price after discount and tax."""
    price_after_discount = discount_amount * (1 - discount_rate)
    final_price = price_after_discount * (1 + tax_rate)
    return round(final_price, 2)

class ReportService:
    def _calculate_order_total(self, order_data: dict) -> dict:
        """Calculate total for a single order."""
        return {
            "name": order_data["name"],
            "total": sum(
                line_item["price"] * line_item["quantity"] 
                for line_item in order_data["line_items"]
            ),
        }
```

**Explanation:** Descriptive names make code self-documenting and reduce cognitive load.

---

### MIXED-CONCERNS
**I/O mixed with business logic**

**Current code:**
```python
def get_daily_report():
    conn = sqlite3.connect("orders.db")  # Database I/O
    cursor = conn.execute("SELECT * FROM orders WHERE date = date('now')")
    orders = cursor.fetchall()
    conn.close()
    
    total_revenue = sum(json.loads(o[1])["total"] for o in orders)  # Business logic
    
    import smtplib  # Email I/O
    server = smtplib.SMTP("smtp.company.com")
    server.send_message(f"Daily revenue: ${total_revenue:.2f}")
    server.quit()
```

**Improved version:**
```python
@dataclass
class DailyReport:
    order_count: int
    total_revenue: float
    date: str

class ReportGenerator:
    def __init__(self, repository: OrderRepository):
        self._repository = repository
    
    def generate_daily_report(self, date: str) -> DailyReport:
        """Generate report data without side effects."""
        orders = self._repository.get_orders_by_date(date)
        return DailyReport(
            order_count=len(orders),
            total_revenue=sum(order.total for order in orders),
            date=date
        )

class ReportDelivery:
    def __init__(self, email_service: EmailService):
        self._email_service = email_service
    
    def send_daily_report(self, report: DailyReport):
        """Send report via email."""
        message = f"Daily revenue for {report.date}: ${report.total_revenue:.2f}"
        self._email_service.send(message)
```

**Explanation:** Separate data retrieval, business logic, and I/O operations for better testability and maintainability.

---

### INHERITANCE-MISUSE
**Multiple inheritance creates complexity**

**Current code:**
```python
class OrderProcessor(BaseProcessor, PricingMixin, DiscountMixin):
    """Main order processing class using multiple inheritance."""
```

**Improved version:**
```python
class OrderProcessor:
    def __init__(
        self,
        pricing_service: PricingService,
        discount_service: DiscountService,
        logger: Logger,
        notification_service: NotificationService
    ):
        self._pricing_service = pricing_service
        self._discount_service = discount_service
        self._logger = logger
        self._notification_service = notification_service

class PricingService:
    def apply_tax(self, amount: float, rate: float = 0.08) -> float:
        return amount * (1 + rate)

class DiscountService:
    def __init__(self):
        self._discount_codes = {"SAVE10": 0.10, "SAVE20": 0.20, "VIP": 0.30}
    
    def apply_discount(self, amount: float, code: str) -> float:
        rate = self._discount_codes.get(code, 0)
        return amount * (1 - rate)
```

**Explanation:** Favor composition over inheritance. It's more flexible and easier to test each component independently.

---

## Medium Priority Issues

### NO-CONTEXT-MGR
**Database connections not properly managed**

**Current code:**
```python
_db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
# Connection never properly closed
```

**Improved version:**
```python
class OrderRepository:
    def __init__(self, db_path: str):
        self._db_path = db_path
    
    def save_order(self, order_id: str, order_data: str) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT INTO orders VALUES (?, ?)",
                (order_id, order_data)
            )
            conn.commit()
```

**Explanation:** Always use context managers for resource management to ensure proper cleanup.

---

### DATA-STRUCTURES
**Using primitive types instead of proper data structures**

**Current code:**
```python
def process(self, order_data):
    # order_data is a raw dict
    if not order_data.get("items"):
        return {"error": "No items"}
```

**Improved version:**
```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: Optional[float] = None

@dataclass
class Order:
    id: str
    items: List[OrderItem]
    email: str
    discount_code: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        items = [OrderItem(**item) for item in data.get("items", [])]
        return cls(
            id=data["id"],
            items=items,
            email=data["email"],
            discount_code=data.get("discount_code")
        )
```

**Explanation:** Use dataclasses or proper domain objects instead of raw dictionaries for better type safety and validation.

---

## Summary

**Most Critical Issues to Address:**
1. **GLOBAL-STATE** - Eliminate global mutable state
2. **SRP-VIOLATION** - Break down large classes into single-responsibility components  
3. **SECURITY-RISK** - Remove `eval()` usage
4. **DEEP-NESTING** - Use early returns and extract methods
5. **MIXED-CONCERNS** - Separate I/O from business logic

These changes will significantly improve the code's testability, maintainability, and security. Focus on dependency injection, proper separation of concerns, and using appropriate data structures.
