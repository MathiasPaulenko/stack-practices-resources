"""Optimistic locking example with PostgreSQL.

Run: pip install psycopg2-binary
Set: DATABASE_URL environment variable or conn string
"""
import os

import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL", "postgresql://localhost/test"))


def update_product_price(conn, product_id: int, new_price: float, expected_version: int):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            UPDATE products
            SET price = %s, version = version + 1
            WHERE id = %s AND version = %s
            RETURNING id, version;
            """,
            (new_price, product_id, expected_version),
        )
        updated = cur.fetchone()
        if not updated:
            raise ValueError(
                f"Conflict: product {product_id} was modified by another transaction. "
                "Please refresh and retry."
            )
        conn.commit()
        return updated


def batch_update_prices(conn, updates):
    """Update multiple rows with optimistic locking in one transaction."""
    results = []
    with conn.cursor() as cur:
        for item in updates:
            cur.execute(
                """
                UPDATE products
                SET price = %s, version = version + 1
                WHERE id = %s AND version = %s
                RETURNING id, version;
                """,
                (item["new_price"], item["id"], item["expected_version"]),
            )
            updated = cur.fetchone()
            if not updated:
                conn.rollback()
                raise ValueError(
                    f"Conflict on product {item['id']}: "
                    f"expected version {item['expected_version']}"
                )
            results.append(updated)
    conn.commit()
    return results


if __name__ == "__main__":
    conn = get_connection()
    try:
        result = update_product_price(conn, product_id=1, new_price=19.99, expected_version=3)
        print(f"Updated to version {result['version']}")
    except ValueError as e:
        print(e)
