"""Batch optimistic locking example with PostgreSQL.

Run: pip install psycopg2-binary
"""
import os

import psycopg2


def get_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL", "postgresql://localhost/test"))


def batch_update_with_versions(conn, updates):
    """Update multiple rows with optimistic locking in a single transaction."""
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
        results = batch_update_with_versions(
            conn,
            [
                {"id": 1, "new_price": 19.99, "expected_version": 5},
                {"id": 2, "new_price": 29.99, "expected_version": 3},
                {"id": 3, "new_price": 39.99, "expected_version": 7},
            ],
        )
        print(f"Updated {len(results)} rows")
    except ValueError as e:
        print(f"Batch failed: {e}")
