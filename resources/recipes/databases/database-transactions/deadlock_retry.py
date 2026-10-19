"""Deadlock retry wrapper for psycopg2 transactions.

PostgreSQL aborts one of two deadlocked transactions with error 40P01.
Retry with exponential backoff instead of failing the request.
Requires: pip install psycopg2-binary.
"""

import os
import time
from collections.abc import Callable
from typing import TypeVar

import psycopg2
from psycopg2 import errors

T = TypeVar("T")

CONN_STR = os.environ.get("DATABASE_URL", "dbname=mydb user=postgres")


def with_retry(fn: Callable[[], T], max_retries: int = 3, base_delay: float = 0.1) -> T:
    """Run `fn`, retrying on 40P01 deadlock errors with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return fn()
        except errors.DeadlockDetected:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Deadlock detected, retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("unreachable")


def transfer(conn: psycopg2.extensions.connection, from_id: int, to_id: int, amount: float) -> None:
    def _transfer() -> None:
        with conn.cursor() as cur:
            cur.execute("BEGIN")
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE id = %s",
                (amount, from_id),
            )
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE id = %s",
                (amount, to_id),
            )
            conn.commit()

    return with_retry(_transfer)


if __name__ == "__main__":
    conn = psycopg2.connect(CONN_STR)
    try:
        transfer(conn, 1, 2, 100.0)
        print("Transfer committed")
    finally:
        conn.close()
