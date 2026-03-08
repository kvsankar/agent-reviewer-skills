# Python Code Review: order_processor.py

## Critical Issues

### SEC-EVAL: Dangerous use of eval() for dynamic rules
**Severity: CRITICAL**

**Problematic Code:**
```python
def apply_dynamic_rule(order, rule_string):
    """Apply a dynamic pricing rule.

    rule_string is something like "total * 0.9 if total > 100 else total"
    """
    total = order["total"]
    return eval(rule_string)
```

**Improved Code:**
```python
from ast import literal_eval
import operator
import re

class SafeRuleEvaluator:
    """Safely evaluate pricing rules with restricted operations."""
    
    ALLOWED_OPS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    
    def apply_rule(self, order: dict, rule_type: str, threshold: float = 0.0, 
                   discount: float = 0.0) -> float:
        """Apply predefined pricing rules safely."""
        total = order["total"]
        
        if rule_type == "threshold_discount" and total > threshold:
            return total * (1 - discount)
        elif rule_type == "bulk_discount" and len(order["items"]) >= threshold:
            return total * (1 - discount)
        
        return total
```

**Why this matters:** `eval()` executes arbitrary code, creating a severe security vulnerability. Attackers could inject malicious code through rule strings. The improved version uses predefined, safe rule types.

### DB-RESOURCE: Global database connection and resource leaks
**Severity: CRITICAL**

**Problematic Code:**
```python
_db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
_db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")

# Later in code:
cursor = _db.execute("SELECT price FROM products WHERE id = ?", (item["product_id"],))
# No connection cleanup
```

**Improved Code:**
```python
from contextlib import contextmanager
from typing import Iterator

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_tables()
    
    def _init_tables(self):
        with self.get_connection() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")
            conn.execute("CREATE TABLE IF NOT EXISTS products (id TEXT, price REAL, stock INTEGER)")
    
    @contextmanager
    def get_connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

# Usage:
db_manager = DatabaseManager(os.environ.get("DB_PATH", "orders.db"))

# In methods:
with db_manager.get_connection() as conn:
    cursor = conn.execute("SELECT price FROM products WHERE id = ?", (product_id,))
    result = cursor.fetchone()
```

**Why this matters:** Global database connections create resource leaks, concurrency issues, and make testing difficult. The improved version properly manages connections with automatic cleanup.

## High Severity Issues

### GLOBAL-STATE: Module-level side effects and global variables
**Severity: HIGH**

**Problematic Code:**
```python
logging.basicConfig(level=logging.DEBUG, filename="/var/log/orders.log")
_db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))

REGISTERED_HANDLERS = []
ORDER_CACHE = {}
```

**Improved Code:**
```python
from typing import List, Dict, Any
import logging

class OrderProcessingService:
    """Encapsulates order processing with proper dependency injection."""
    
    def __init__(self, db_manager: DatabaseManager, 
                 logger: logging.Logger = None):
        self.db_manager = db_manager
        self.logger = logger or self._setup_logger()
        self.registered_handlers: List[callable] = []
        self.order_cache: Dict[str, Any] = {}
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.FileHandler("/var/log/orders.log")
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
```

**Why this matters:** Global state makes code difficult to test, creates hidden dependencies, and causes issues in multi-threaded environments. Dependency injection makes dependencies explicit and testable.

### ERROR-HANDLING: Missing error handling and validation
**Severity: HIGH**

**Problematic Code:**
```python
def process(self, order_data):
    with open("config/pricing.json") as f:  # Could raise FileNotFoundError
        config = json.load(f)  # Could raise JSONDecodeError
    
    total = 0
    for item in order_data["items"]:  # Could raise KeyError
        cursor = _db.execute(
            "SELECT price FROM products WHERE id = ?", (item["product_id"],)
        )
        row = cursor.fetchone()
        if row:  # Silent failure if product not found
            price = row[0] * item["quantity"]  # Could raise KeyError
```

**Improved Code:**
```python
from typing import Dict, Any, Optional
import json
from pathlib import Path

class OrderProcessingError(Exception):
    """Custom exception for order processing errors."""
    pass

def process(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process an order with comprehensive error handling."""
    try:
        config = self._load_config()
        self._validate_order_data(order_data)
        
        total = self._calculate_total(order_data, config)
        order_id = self._generate_order_id()
        
        self._save_order(order_id, order_data)
        self._send_notification(order_data.get("email"), order_id)
        
        return {"order_id": order_id, "total": total}
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise OrderProcessingError(f"Configuration error: {e}")
    except KeyError as e:
        raise OrderProcessingError(f"Missing required field: {e}")
    except Exception as e:
        self.logger.error(f"Unexpected error processing order: {e}")
        raise OrderProcessingError(f"Processing failed: {e}")

def _validate_order_data(self, order_data: Dict[str, Any]) -> None:
    """Validate required order fields."""
    required_fields = ["items", "email"]
    for field in required_fields:
        if field not in order_data:
            raise OrderProcessingError(f"Missing required field: {field}")
    
    if not order_data["items"]:
        raise OrderProcessingError("Order must contain at least one item")
```

**Why this matters:** Missing error handling leads to crashes and poor user experience. Proper validation prevents data corruption and provides clear error messages.

## Medium Severity Issues

### SRP-VIOLATION: Single Responsibility Principle violations
**Severity: MEDIUM**

**Problematic Code:**
```python
class OrderProcessor(BaseProcessor, PricingMixin, DiscountMixin):
    def process(self, order_data):
        # Handles: file I/O, database operations, pricing, tax calculation,
        # notifications, logging, order ID generation
        with open("config/pricing.json") as f:
            config = json.load(f)
        # ... 30 lines doing multiple responsibilities
```

**Improved Code:**
```python
from dataclasses import dataclass
from decimal import Decimal
from typing import List

@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: Decimal

@dataclass
class Order:
    items: List[OrderItem]
    email: str
    discount_code: Optional[str] = None

class PricingService:
    """Handles all pricing calculations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.tax_rate = Decimal(str(config.get("tax_rate", 0.08)))
        self.discounts = {
            "SAVE10": Decimal("0.10"),
            "SAVE20": Decimal("0.20"),
            "VIP": Decimal("0.30")
        }
    
    def calculate_total(self, order: Order) -> Decimal:
        subtotal = sum(item.price * item.quantity for item in order.items)
        discounted = self._apply_discount(subtotal, order.discount_code)
        return self._apply_tax(discounted)

class OrderService:
    """Handles order persistence and ID generation."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self._order_counter = 0
    
    def save_order(self, order: Order) -> str:
        order_id = self._generate_order_id()
        with self.db_manager.get_connection() as conn:
            conn.execute(
                "INSERT INTO orders (id, data) VALUES (?, ?)",
                (order_id, json.dumps(asdict(order)))
            )
        return order_id
```

**Why this matters:** Classes with multiple responsibilities are hard to maintain, test, and extend. Separating concerns makes code more modular and reusable.

### DEEP-NESTING: Complex nested conditional logic
**Severity: MEDIUM**

**Problematic Code:**
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
                                    # Success case deeply nested
                                    results.append({...})
```

**Improved Code:**
```python
from typing import List, Dict, Any

class OrderValidationResult:
    def __init__(self, order_id: str, item_id: str, valid: bool, reason: str = ""):
        self.order_id = order_id
        self.item_id = item_id
        self.valid = valid
        self.reason = reason

class OrderValidator:
    def __init__(self, config: Dict[str, Any]):
        self.valid_products = set(config["valid_products"])
        self.max_quantity = config["max_quantity"]
    
    def validate_batch(self, orders: List[Dict]) -> List[OrderValidationResult]:
        """Validate orders using early returns to reduce nesting."""
        results = []
        
        for order in orders:
            if order.get("status") != "pending":
                continue
                
            items = order.get("items", [])
            if not items:
                continue
                
            for item in items:
                result = self._validate_item(order["id"], item)
                if result:
                    results.append(result)
        
        return results
    
    def _validate_item(self, order_id: str, item: Dict) -> Optional[OrderValidationResult]:
        """Validate a single item with early returns."""
        quantity = item.get("quantity", 0)
        if quantity <= 0:
            return None
            
        product_id = item.get("product_id")
        if not product_id:
            return OrderValidationResult(order_id, "", False, "missing product ID")
            
        if product_id not in self.valid_products:
            return OrderValidationResult(order_id, product_id, False, "invalid product")
            
        if quantity > self.max_quantity:
            return OrderValidationResult(order_id, product_id, False, "exceeds max quantity")
            
        return OrderValidationResult(order_id, product_id, True)
```

**Why this matters:** Deep nesting makes code hard to read and understand. Early returns and guard clauses improve readability and reduce cognitive load.

## Lower Severity Issues

### NAMING-CLARITY: Unclear function and variable names
**Severity: LOW**

**Problematic Code:**
```python
def calc(d, r, t):
    p = d * (1 - r)
    f = p * (1 + t)
    return round(f, 2)

def _do(self, item):
    return {
        "name": item["name"],
        "total": sum(i["price"] * i["qty"] for i in item["lines"]),
    }
```

**Improved Code:**
```python
from decimal import Decimal
from typing import Dict, Any

def calculate_final_price(base_amount: Decimal, discount_rate: Decimal, 
                         tax_rate: Decimal) -> Decimal:
    """Calculate final price after discount and tax."""
    discounted_price = base_amount * (1 - discount_rate)
    final_price = discounted_price * (1 + tax_rate)
    return final_price.quantize(Decimal('0.01'))

def calculate_order_summary(self, order_item: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate summary for a single order item."""
    return {
        "name": order_item["name"],
        "total": sum(
            line["price"] * line["quantity"] 
            for line in order_item["order_lines"]
        ),
    }
```

**Why this matters:** Clear names make code self-documenting and reduce the need for comments. Future maintainers can understand the purpose without deciphering cryptic abbreviations.

### TYPE-SAFETY: Missing type hints
**Severity: LOW**

**Problematic Code:**
```python
def create_shipping_label(order):
    """Create a shipping label from order data."""
    label = {
        "from_name": "Warehouse A",
        # ... rest of label
    }
    return label
```

**Improved Code:**
```python
from typing import Dict, Any, TypedDict

class ShippingAddress(TypedDict):
    name: str
    street: str
    city: str
    state: str
    zip: str

class ShippingLabel(TypedDict):
    from_name: str
    from_street: str
    from_city: str
    from_state: str
    from_zip: str
    to_name: str
    to_street: str
    to_city: str
    to_state: str
    to_zip: str
    weight: float
    service: str

def create_shipping_label(order: Dict[str, Any]) -> ShippingLabel:
    """Create a shipping label from order data."""
    shipping_addr = order["shipping"]
    
    return ShippingLabel(
        from_name="Warehouse A",
        from_street="123 Industrial Pkwy",
        from_city="Portland",
        from_state="OR", 
        from_zip="97201",
        to_name=shipping_addr["name"],
        to_street=shipping_addr["street"],
        to_city=shipping_addr["city"],
        to_state=shipping_addr["state"],
        to_zip=shipping_addr["zip"],
        weight=order["total_weight"],
        service=order.get("shipping_method", "ground"),
    )
```

**Why this matters:** Type hints improve code clarity, enable better IDE support, and catch type-related errors early through static analysis tools like mypy.

## Summary

The code has several critical security and resource management issues that should be addressed immediately. The overall architecture would benefit from better separation of concerns, proper error handling, and dependency injection to improve testability and maintainability.

**Priority fixes:**
1. Remove `eval()` usage (SEC-EVAL)
2. Implement proper database connection management (DB-RESOURCE)
3. Eliminate global state (GLOBAL-STATE)
4. Add comprehensive error handling (ERROR-HANDLING)
