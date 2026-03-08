## Code Review Findings (highest severity first)

### 1) `SEC-001` Unsafe dynamic rule execution (`apply_dynamic_rule`)
**Problematic code**
```python
def apply_dynamic_rule(order, rule_string):
    total = order["total"]
    return eval(rule_string)
```

**Improved code**
```python
RULES = {
    "TEN_OFF_OVER_100": lambda total: total * 0.9 if total > 100 else total,
    "VIP_5": lambda total: total * 0.95,
}

def apply_dynamic_rule(order, rule_name):
    total = float(order["total"])
    try:
        return RULES[rule_name](total)
    except KeyError as exc:
        raise ValueError(f"Unknown pricing rule: {rule_name}") from exc
```

**Why this matters**  
`eval` allows arbitrary code execution. Replacing it with named rules eliminates a critical security risk.

---

### 2) `DB-001` Import-time side effects for logging and DB
**Problematic code**
```python
logging.basicConfig(level=logging.DEBUG, filename="/var/log/orders.log")
_db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
_db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")
```

**Improved code**
```python
logger = logging.getLogger(__name__)

def init_db(db_path=None):
    path = db_path or os.environ.get("DB_PATH", "orders.db")
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    return conn
```

**Why this matters**  
Importing the module now triggers I/O and global state changes. That hurts testability, startup reliability, and reuse.

---

### 3) `ID-001` Non-unique order ID generation
**Problematic code**
```python
order_id = f"ORD-{len(self.orders) + 1:05d}"
```

**Improved code**
```python
import uuid
order_id = f"ORD-{uuid.uuid4().hex[:12].upper()}"
```

**Why this matters**  
`len(self.orders)` is process-local and resets on restart; collisions are likely in multi-instance systems.

---

### 4) `DATA-001` Stored order payload missing computed fields
**Problematic code**
```python
_db.execute(
    "INSERT INTO orders VALUES (?, ?)",
    (order_id, json.dumps(order_data)),
)
```

**Improved code**
```python
stored_order = {
    **order_data,
    "order_id": order_id,
    "total": total,
    "status": "created",
}
_db.execute(
    "INSERT INTO orders (id, data, created_at) VALUES (?, ?, datetime('now'))",
    (order_id, json.dumps(stored_order)),
)
```

**Why this matters**  
Later code expects `order["total"]` (e.g., fulfillment). Not storing it causes runtime failures and inconsistent data.

---

### 5) `DB-002` Daily report queries nonexistent schema and wrong DB path
**Problematic code**
```python
conn = sqlite3.connect("orders.db")
cursor = conn.execute("SELECT * FROM orders WHERE date = date('now')")
```

**Improved code**
```python
def get_daily_report(conn):
    cursor = conn.execute(
        "SELECT data FROM orders WHERE date(created_at) = date('now', 'localtime')"
    )
    orders = [json.loads(row[0]) for row in cursor.fetchall()]
```

**Why this matters**  
`date` column does not exist in your table. Also hardcoding `"orders.db"` can ignore `DB_PATH`.

---

### 6) `NET-001` SMTP API misuse in report emailing
**Problematic code**
```python
server = smtplib.SMTP("smtp.company.com")
server.send_message(f"Daily revenue: ${total_revenue:.2f}")
server.quit()
```

**Improved code**
```python
from email.message import EmailMessage
import smtplib

msg = EmailMessage()
msg["Subject"] = "Daily Order Report"
msg["From"] = "noreply@company.com"
msg["To"] = "ops@company.com"
msg.set_content(f"Daily revenue: ${total_revenue:.2f}")

with smtplib.SMTP("smtp.company.com", 587, timeout=10) as server:
    server.starttls()
    server.send_message(msg)
```

**Why this matters**  
`send_message` expects an `EmailMessage`, not a string. The current version likely fails at runtime.

---

### 7) `NET-002` Shipping API call lacks timeout and response validation
**Problematic code**
```python
response = requests.post("https://shipping.api.com/labels", json=create_shipping_label(order))
tracking = response.json()["tracking_number"]
```

**Improved code**
```python
response = requests.post(
    "https://shipping.api.com/labels",
    json=create_shipping_label(order),
    timeout=10,
)
response.raise_for_status()
payload = response.json()
tracking = payload.get("tracking_number")
if not tracking:
    raise RuntimeError("Shipping API response missing tracking_number")
```

**Why this matters**  
Without timeout/error checks, calls can hang or fail silently, causing partial fulfillment updates.

---

### 8) `VAL-001` Deeply nested validation with silent drops (`validate_order_batch`)
**Problematic code**
```python
if order.get("status") == "pending":
    if order.get("items"):
        for item in order["items"]:
            if item.get("quantity", 0) > 0:
                if item.get("product_id"):
                    if item["product_id"] in config["valid_products"]:
                        if item["quantity"] <= config["max_quantity"]:
                            ...
```

**Improved code**
```python
def validate_order_batch(orders, config):
    valid_products = set(config.get("valid_products", []))
    max_quantity = config.get("max_quantity", 0)
    results = []

    for order in orders:
        if order.get("status") != "pending":
            continue

        for item in order.get("items", []):
            pid = item.get("product_id")
            qty = item.get("quantity", 0)

            reason = None
            if not pid:
                reason = "missing product_id"
            elif pid not in valid_products:
                reason = "invalid product"
            elif qty <= 0:
                reason = "quantity must be > 0"
            elif qty > max_quantity:
                reason = "exceeds max quantity"

            results.append({
                "order_id": order.get("id"),
                "item_id": pid,
                "valid": reason is None,
                **({"reason": reason} if reason else {}),
            })
    return results
```

**Why this matters**  
Guard clauses improve readability, reduce bugs, and produce complete diagnostics instead of silently ignoring invalid items.

---

### 9) `OBS-001` `print` used for operational logging/notification
**Problematic code**
```python
class BaseProcessor:
    def log(self, msg):
        print(f"[LOG] {msg}")

    def notify(self, user, msg):
        print(f"[NOTIFY {user}] {msg}")
```

**Improved code**
```python
class BaseProcessor:
    def __init__(self, logger, notifier):
        self.logger = logger
        self.notifier = notifier

    def log(self, msg):
        self.logger.info(msg)

    def notify(self, user, msg):
        self.notifier(user, msg)
```

**Why this matters**  
`print` is not structured, filterable, or test-friendly. Injected logger/notifier improves observability and design.

---

### 10) `PERF-001` Queue front insertion is inefficient and order semantics are unclear
**Problematic code**
```python
self.items = []
...
for order in orders:
    self.items.insert(0, order)
```

**Improved code**
```python
from collections import deque

class PriorityQueue:
    def __init__(self):
        self.items = deque()

    def add_urgent(self, order):
        self.items.appendleft(order)

    def add_batch(self, orders):
        self.items.extendleft(reversed(orders))
```

**Why this matters**  
`list.insert(0, ...)` is O(n). `deque` is the right structure for front insertions and clearer queue intent.

---

### 11) `STYLE-001` Cryptic helper naming (`calc`)
**Problematic code**
```python
def calc(d, r, t):
    p = d * (1 - r)
    f = p * (1 + t)
    return round(f, 2)
```

**Improved code**
```python
def calculate_final_price(amount, discount_rate, tax_rate):
    discounted = amount * (1 - discount_rate)
    final_amount = discounted * (1 + tax_rate)
    return round(final_amount, 2)
```

**Why this matters**  
Descriptive names reduce cognitive load and prevent misuse.

---

### 12) `CFG-001` Per-request config file read in `process`
**Problematic code**
```python
with open("config/pricing.json") as f:
    config = json.load(f)
```

**Improved code**
```python
class OrderProcessor(BaseProcessor, PricingMixin, DiscountMixin):
    def __init__(self, conn, pricing_config):
        self.conn = conn
        self.pricing_config = pricing_config
        self.orders = []
```

**Why this matters**  
Disk I/O on every request hurts performance and reliability. Load once and inject dependencies.

---

### 13) `VAL-002` Unknown product IDs are silently ignored in pricing loop
**Problematic code**
```python
row = cursor.fetchone()
if row:
    price = row[0] * item["quantity"]
    ...
    total += price
```

**Improved code**
```python
row = cursor.fetchone()
if row is None:
    raise ValueError(f"Unknown product_id: {item['product_id']}")

quantity = int(item["quantity"])
if quantity <= 0:
    raise ValueError(f"Invalid quantity for {item['product_id']}: {quantity}")

price = row[0] * quantity
```

**Why this matters**  
Silent skips undercharge orders and mask data issues. Failing fast keeps pricing correct and auditable.