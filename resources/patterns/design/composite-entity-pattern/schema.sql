-- Schema for the Composite Entity Pattern example.
-- Ownership is encoded in the schema: child tables key on order_id,
-- cascade on delete, and give dependents a local identity (line_no).

CREATE TABLE orders (
    order_id    TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE line_items (
    order_id    TEXT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    line_no     INTEGER NOT NULL,
    product_id  TEXT NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  REAL NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, line_no)
);

CREATE TABLE shipping_addresses (
    order_id    TEXT PRIMARY KEY REFERENCES orders(order_id) ON DELETE CASCADE,
    street      TEXT NOT NULL,
    city        TEXT NOT NULL,
    country     TEXT NOT NULL,
    postal_code TEXT NOT NULL
);

-- Useful index if you ever query "orders containing product X":
CREATE INDEX idx_line_items_product ON line_items(product_id);
