"""Tests for the runnable ETL pipeline companion."""

import sqlite3

import pytest

from etl_pipeline import (
    IncrementalExtractor,
    DataTransformer,
    UpsertLoader,
    ValidationError,
    validate_no_null_ids,
    normalize_emails,
    add_order_total,
)


@pytest.fixture()
def conn():
    c = sqlite3.connect(":memory:")
    c.execute(
        """CREATE TABLE orders_src (
            id INTEGER PRIMARY KEY, email TEXT, quantity INTEGER,
            unit_price REAL, discount REAL, updated_at TEXT
        )"""
    )
    c.execute(
        """CREATE TABLE fact_orders (
            id INTEGER PRIMARY KEY, email TEXT, quantity INTEGER,
            unit_price REAL, discount REAL, order_total REAL, updated_at TEXT
        )"""
    )
    yield c
    c.close()


def seed(conn):
    conn.executemany(
        "INSERT INTO orders_src VALUES (?, ?, ?, ?, ?, ?)",
        [
            (1, "a@x.com", 1, 10.0, 0.0, "2026-11-01"),
            (2, "b@x.com", 2, 10.0, 0.1, "2026-11-02"),
        ],
    )
    conn.commit()


def test_incremental_extracts_only_new_rows(conn):
    seed(conn)
    ex = IncrementalExtractor(conn)
    assert len(ex.extract_incremental("orders_src")) == 2
    # second run: watermark stored -> nothing new
    assert ex.extract_incremental("orders_src") == []
    conn.execute("INSERT INTO orders_src VALUES (3, 'c@x.com', 1, 5.0, 0.0, '2026-11-05')")
    conn.commit()
    rows = ex.extract_incremental("orders_src")
    assert [r["id"] for r in rows] == [3]


def test_validator_rejects_null_ids(conn):
    t = DataTransformer()
    t.add_validator(validate_no_null_ids)
    with pytest.raises(ValidationError):
        t.transform([{"id": None, "email": "x@y.z"}])


def test_transforms_apply_in_order(conn):
    t = DataTransformer()
    t.add_transform(normalize_emails)
    t.add_transform(add_order_total)
    out = t.transform([{"id": 1, "email": "  A@X.COM ", "quantity": 2, "unit_price": 10.0, "discount": 0.5}])
    assert out[0]["email"] == "a@x.com"
    assert out[0]["order_total"] == 10.0


def test_upsert_is_idempotent(conn):
    seed(conn)
    loader = UpsertLoader(conn)
    rows = [{"id": 1, "email": "a@x.com", "quantity": 1, "unit_price": 10.0,
             "discount": 0.0, "order_total": 10.0, "updated_at": "2026-11-01"}]
    loader.upsert(rows, "fact_orders")
    loader.upsert(rows, "fact_orders")  # re-run
    assert conn.execute("SELECT COUNT(*) FROM fact_orders").fetchone()[0] == 1
    # upsert actually updates
    rows[0]["order_total"] = 99.0
    loader.upsert(rows, "fact_orders")
    assert conn.execute("SELECT order_total FROM fact_orders WHERE id = 1").fetchone()[0] == 99.0
