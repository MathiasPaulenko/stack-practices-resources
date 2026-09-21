"""List-view projection — why you should NOT load the whole aggregate.

Loading every LineItem and ShippingAddress just to render a table of
orders is the classic composite-entity waste. Project only the columns
the list view needs.

Run: python order_projection.py
"""
import sqlite3

ORDER_LIST_SQL = """
SELECT o.order_id, o.customer_id, o.created_at,
       COUNT(li.product_id) AS item_count,
       COALESCE(SUM(li.quantity * li.unit_price), 0) AS total
FROM orders o
LEFT JOIN line_items li ON li.order_id = o.order_id
GROUP BY o.order_id
ORDER BY o.created_at DESC
"""


def order_list(conn: sqlite3.Connection):
    """One query, no dependents — enough for a list/table view."""
    return [dict(row) for row in conn.execute(ORDER_LIST_SQL)]


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE orders (order_id TEXT PRIMARY KEY, customer_id TEXT,
                             created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE line_items (order_id TEXT, product_id TEXT,
                                 quantity INTEGER, unit_price REAL);
        INSERT INTO orders VALUES ('ORD-1','C-1','2026-09-01'), ('ORD-2','C-2','2026-09-02');
        INSERT INTO line_items VALUES ('ORD-1','P1',2,29.99), ('ORD-1','P2',1,49.99);
        """
    )
    for row in order_list(conn):
        print(row)
