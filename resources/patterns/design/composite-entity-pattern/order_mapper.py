"""Composite Entity Pattern — runnable example with sqlite3.

The OrderMapper treats Order + LineItem + ShippingAddress as one
persistence unit: one save() writes all three tables in a single
transaction, and find_by_id() rehydrates the whole aggregate.

Run: python order_mapper.py  -> prints "Order total: $109.97"
"""
from dataclasses import dataclass, field
from typing import List, Optional
import sqlite3


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


class OrderMapper:
    """Composite entity mapper loading from multiple tables."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def find_by_id(self, order_id: str) -> Optional[Order]:
        row = self._conn.execute(
            "SELECT order_id, customer_id FROM orders WHERE order_id = ?",
            (order_id,),
        ).fetchone()
        if not row:
            return None

        order = Order(order_id=row["order_id"], customer_id=row["customer_id"])

        for item_row in self._conn.execute(
            "SELECT product_id, quantity, unit_price FROM line_items WHERE order_id = ?",
            (order_id,),
        ):
            order.line_items.append(
                LineItem(
                    product_id=item_row["product_id"],
                    quantity=item_row["quantity"],
                    unit_price=item_row["unit_price"],
                )
            )

        addr_row = self._conn.execute(
            "SELECT street, city, country, postal_code FROM shipping_addresses WHERE order_id = ?",
            (order_id,),
        ).fetchone()
        if addr_row:
            order.shipping_address = ShippingAddress(
                street=addr_row["street"],
                city=addr_row["city"],
                country=addr_row["country"],
                postal_code=addr_row["postal_code"],
            )

        return order

    def save(self, order: Order) -> None:
        # One transaction keeps the three tables consistent.
        with self._conn:
            self._conn.execute(
                "INSERT OR REPLACE INTO orders (order_id, customer_id) VALUES (?, ?)",
                (order.order_id, order.customer_id),
            )
            # Delete-then-insert: simplest correct way to handle orphans.
            self._conn.execute(
                "DELETE FROM line_items WHERE order_id = ?", (order.order_id,)
            )
            for item in order.line_items:
                self._conn.execute(
                    "INSERT INTO line_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order.order_id, item.product_id, item.quantity, item.unit_price),
                )
            if order.shipping_address:
                self._conn.execute(
                    """INSERT OR REPLACE INTO shipping_addresses
                       (order_id, street, city, country, postal_code)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        order.order_id,
                        order.shipping_address.street,
                        order.shipping_address.city,
                        order.shipping_address.country,
                        order.shipping_address.postal_code,
                    ),
                )


def main() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT)"
    )
    conn.execute(
        """CREATE TABLE line_items (
            order_id TEXT, product_id TEXT, quantity INTEGER, unit_price REAL
        )"""
    )
    conn.execute(
        """CREATE TABLE shipping_addresses (
            order_id TEXT PRIMARY KEY, street TEXT, city TEXT,
            country TEXT, postal_code TEXT
        )"""
    )

    mapper = OrderMapper(conn)
    order = Order(
        order_id="ORD-001",
        customer_id="CUST-001",
        line_items=[
            LineItem("PROD-1", 2, 29.99),
            LineItem("PROD-2", 1, 49.99),
        ],
        shipping_address=ShippingAddress(
            "123 Main St", "Springfield", "USA", "62701"
        ),
    )

    mapper.save(order)
    loaded = mapper.find_by_id("ORD-001")
    print(f"Order total: ${loaded.total:.2f}")


if __name__ == "__main__":
    main()
