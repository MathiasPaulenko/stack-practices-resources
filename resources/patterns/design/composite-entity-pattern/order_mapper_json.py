"""JSON-column variant of the composite entity.

Same aggregate, different mapping: line items and the shipping address
live inside the orders row as JSON. One table, one write, zero orphan
cleanup — at the cost of querying inside the dependents.

Run: python order_mapper_json.py  -> prints "Order total: $109.97"
"""
import json
import sqlite3
from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class LineItem:
    product_id: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class ShippingAddress:
    street: str
    city: str
    country: str
    postal_code: str


@dataclass
class Order:
    order_id: Optional[str] = None
    customer_id: str = ""
    line_items: List[LineItem] = field(default_factory=list)
    shipping_address: Optional[ShippingAddress] = None

    @property
    def total(self) -> float:
        return sum(item.total for item in self.line_items)


class OrderJsonMapper:
    """Composite entity stored as one row with JSON dependents."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def find_by_id(self, order_id: str) -> Optional[Order]:
        row = self._conn.execute(
            "SELECT order_id, customer_id, line_items, shipping_address FROM orders WHERE order_id = ?",
            (order_id,),
        ).fetchone()
        if not row:
            return None
        order = Order(order_id=row["order_id"], customer_id=row["customer_id"])
        for item in json.loads(row["line_items"]):
            order.line_items.append(LineItem(**item))
        if row["shipping_address"]:
            order.shipping_address = ShippingAddress(**json.loads(row["shipping_address"]))
        return order

    def save(self, order: Order) -> None:
        # One row, one write — atomic by construction.
        self._conn.execute(
            "INSERT OR REPLACE INTO orders (order_id, customer_id, line_items, shipping_address) VALUES (?, ?, ?, ?)",
            (
                order.order_id,
                order.customer_id,
                json.dumps([asdict(i) for i in order.line_items]),
                json.dumps(asdict(order.shipping_address)) if order.shipping_address else None,
            ),
        )
        self._conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT, line_items TEXT, shipping_address TEXT)"
    )
    mapper = OrderJsonMapper(conn)
    order = Order(
        order_id="ORD-001",
        customer_id="CUST-001",
        line_items=[LineItem("PROD-1", 2, 29.99), LineItem("PROD-2", 1, 49.99)],
        shipping_address=ShippingAddress("123 Main St", "Springfield", "USA", "62701"),
    )
    mapper.save(order)
    loaded = mapper.find_by_id("ORD-001")
    print(f"Order total: ${loaded.total:.2f}")
