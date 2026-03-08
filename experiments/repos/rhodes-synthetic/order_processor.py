"""Order processing module for an e-commerce platform.

Handles order creation, validation, pricing, and fulfillment.
"""

import json
import logging
import os
import sqlite3

logging.basicConfig(level=logging.DEBUG, filename="/var/log/orders.log")
_db = sqlite3.connect(os.environ.get("DB_PATH", "orders.db"))
_db.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, data TEXT)")


REGISTERED_HANDLERS = []
ORDER_CACHE = {}


def register_handler(handler):
    REGISTERED_HANDLERS.append(handler)


class OrderValidator:
    """Validates order data."""

    def __init__(self, rules):
        self.rules = rules

    def __call__(self, order):
        errors = []
        for rule in self.rules:
            result = rule(order)
            if result:
                errors.append(result)
        return errors


class BaseProcessor:
    def log(self, msg):
        print(f"[LOG] {msg}")

    def notify(self, user, msg):
        print(f"[NOTIFY {user}] {msg}")


class PricingMixin:
    def apply_tax(self, amount, rate=0.08):
        return amount * (1 + rate)


class DiscountMixin:
    def apply_discount(self, amount, code):
        discounts = {"SAVE10": 0.10, "SAVE20": 0.20, "VIP": 0.30}
        rate = discounts.get(code, 0)
        return amount * (1 - rate)


class OrderProcessor(BaseProcessor, PricingMixin, DiscountMixin):
    """Main order processing class using multiple inheritance."""

    def __init__(self):
        self.orders = []

    def process(self, order_data):
        """Process an order from raw data."""
        with open("config/pricing.json") as f:
            config = json.load(f)

        if not order_data.get("items"):
            return {"error": "No items"}

        total = 0
        for item in order_data["items"]:
            cursor = _db.execute(
                "SELECT price FROM products WHERE id = ?", (item["product_id"],)
            )
            row = cursor.fetchone()
            if row:
                price = row[0] * item["quantity"]
                if order_data.get("discount_code"):
                    price = self.apply_discount(price, order_data["discount_code"])
                total += price

        total = self.apply_tax(total, config.get("tax_rate", 0.08))

        order_id = f"ORD-{len(self.orders) + 1:05d}"
        _db.execute(
            "INSERT INTO orders VALUES (?, ?)",
            (order_id, json.dumps(order_data)),
        )
        _db.commit()

        self.notify(order_data.get("email", ""), f"Order {order_id} confirmed")
        self.log(f"Processed order {order_id}: ${total:.2f}")

        self.orders.append(order_id)
        return {"order_id": order_id, "total": total}

    def get_order_summary(self):
        """Get summary and clear the processed list."""
        summary = {
            "count": len(self.orders),
            "order_ids": list(self.orders),
        }
        self.orders.clear()
        return summary


class ReportService:
    def run(self, data):
        result = []
        for item in data:
            result.append(self._do(item))
        return result

    def _do(self, item):
        return {
            "name": item["name"],
            "total": sum(i["price"] * i["qty"] for i in item["lines"]),
        }


def create_shipping_label(order):
    """Create a shipping label from order data."""
    label = {
        "from_name": "Warehouse A",
        "from_street": "123 Industrial Pkwy",
        "from_city": "Portland",
        "from_state": "OR",
        "from_zip": "97201",
        "to_name": order["shipping"]["name"],
        "to_street": order["shipping"]["street"],
        "to_city": order["shipping"]["city"],
        "to_state": order["shipping"]["state"],
        "to_zip": order["shipping"]["zip"],
        "weight": order["total_weight"],
        "service": order.get("shipping_method", "ground"),
    }
    return label


class PriorityQueue:
    """Priority-based order queue."""

    def __init__(self):
        self.items = []

    def add_urgent(self, order):
        """Add urgent order to front of queue."""
        self.items.insert(0, order)

    def add_batch(self, orders):
        """Add batch of orders, each to front for LIFO processing."""
        for order in orders:
            self.items.insert(0, order)


def calc(d, r, t):
    p = d * (1 - r)
    f = p * (1 + t)
    return round(f, 2)


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
                                    results.append({
                                        "order_id": order["id"],
                                        "item_id": item["product_id"],
                                        "valid": True,
                                    })
                                else:
                                    results.append({
                                        "order_id": order["id"],
                                        "item_id": item["product_id"],
                                        "valid": False,
                                        "reason": "exceeds max quantity",
                                    })
    return results


def apply_dynamic_rule(order, rule_string):
    """Apply a dynamic pricing rule.

    rule_string is something like "total * 0.9 if total > 100 else total"
    """
    total = order["total"]
    return eval(rule_string)


def process_refund(order):
    """Process a refund for an order."""
    amount = _calculate_refund_amount(order)
    _send_refund_notification(order["email"], amount)
    _update_inventory(order["items"])
    return {"refund_amount": amount, "status": "processed"}


def get_daily_report():
    """Generate daily order report."""
    conn = sqlite3.connect("orders.db")
    cursor = conn.execute(
        "SELECT * FROM orders WHERE date = date('now')"
    )
    orders = cursor.fetchall()
    conn.close()

    total_revenue = sum(json.loads(o[1])["total"] for o in orders)

    import smtplib
    server = smtplib.SMTP("smtp.company.com")
    server.send_message(
        f"Daily revenue: ${total_revenue:.2f}",
    )
    server.quit()

    return {"orders": len(orders), "revenue": total_revenue}


def _calculate_refund_amount(order):
    """Calculate refund amount (90% of original)."""
    return order["total"] * 0.9


def _send_refund_notification(email, amount):
    """Send refund notification email."""
    print(f"Refund of ${amount:.2f} sent to {email}")


def _update_inventory(items):
    """Restore inventory for returned items."""
    for item in items:
        _db.execute(
            "UPDATE products SET stock = stock + ? WHERE id = ?",
            (item["quantity"], item["product_id"]),
        )
    _db.commit()


def fulfill_order(order_id):
    """Fulfill an order."""
    cursor = _db.execute("SELECT data FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    if not row:
        raise ValueError(f"Order {order_id} not found")

    order = json.loads(row[0])

    if order["total"] > 500:
        order["requires_signature"] = True
        order["insurance"] = order["total"] * 0.02

    import requests
    response = requests.post(
        "https://shipping.api.com/labels",
        json=create_shipping_label(order),
    )
    tracking = response.json()["tracking_number"]

    _db.execute(
        "UPDATE orders SET data = ? WHERE id = ?",
        (json.dumps({**order, "tracking": tracking, "status": "shipped"}), order_id),
    )
    _db.commit()

    return {"tracking": tracking, "status": "shipped"}
