"""End-to-end demo: extract -> validate -> transform -> upsert, twice.

Second run should move zero rows (watermark) and leave the warehouse table
unchanged (idempotent load).
"""

import sqlite3

from etl_pipeline import (
    IncrementalExtractor,
    DataTransformer,
    UpsertLoader,
    validate_no_null_ids,
    normalize_emails,
    add_order_total,
)


def main():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """CREATE TABLE orders_src (
            id INTEGER PRIMARY KEY,
            email TEXT,
            quantity INTEGER,
            unit_price REAL,
            discount REAL,
            updated_at TEXT
        )"""
    )
    conn.execute(
        """CREATE TABLE fact_orders (
            id INTEGER PRIMARY KEY,
            email TEXT,
            quantity INTEGER,
            unit_price REAL,
            discount REAL,
            order_total REAL,
            updated_at TEXT
        )"""
    )
    conn.executemany(
        "INSERT INTO orders_src VALUES (?, ?, ?, ?, ?, ?)",
        [
            (1, "  ALICE@Shop.COM ", 2, 10.0, 0.1, "2026-11-01"),
            (2, "bob@shop.com", 1, 25.0, 0.0, "2026-11-02"),
            (3, "carol@shop.com", 4, 5.0, 0.0, "2026-11-03"),
        ],
    )
    conn.commit()

    extractor = IncrementalExtractor(conn)
    transformer = DataTransformer()
    transformer.add_validator(validate_no_null_ids)
    transformer.add_transform(normalize_emails)
    transformer.add_transform(add_order_total)
    loader = UpsertLoader(conn)

    for run in (1, 2):
        rows = extractor.extract_incremental("orders_src")
        clean = transformer.transform(rows)
        loaded = loader.upsert(clean, "fact_orders")
        print(f"run {run}: extracted={len(rows)} loaded={loaded}")

    total = conn.execute("SELECT COUNT(*), SUM(order_total) FROM fact_orders").fetchone()
    print(f"warehouse: {total[0]} rows, total={total[1]}")

    # Simulate an update upstream -> third run picks up only that row
    conn.execute("UPDATE orders_src SET quantity = 9, updated_at = '2026-11-10' WHERE id = 1")
    conn.commit()
    rows = extractor.extract_incremental("orders_src")
    clean = transformer.transform(rows)
    loader.upsert(clean, "fact_orders")
    print(f"run 3 (after update): extracted={len(rows)}")
    r = conn.execute("SELECT quantity, order_total FROM fact_orders WHERE id = 1").fetchone()
    print(f"order 1 now: qty={r[0]} total={r[1]}")


if __name__ == "__main__":
    main()
