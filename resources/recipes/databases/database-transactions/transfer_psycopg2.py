"""ACID transfer between accounts with psycopg2.

Covers: BEGIN/COMMIT/ROLLBACK, savepoints for nested operations,
and SELECT ... FOR UPDATE for pessimistic locking.
Requires: pip install psycopg2-binary and a reachable PostgreSQL.
"""

import os

import psycopg2

CONN_STR = os.environ.get("DATABASE_URL", "dbname=mydb user=postgres")


def transfer(conn, from_id: int, to_id: int, amount: float) -> None:
    """Move `amount` between two accounts atomically.

    The balance check is folded into the UPDATE so the guard itself
    is atomic — no SELECT-then-UPDATE race.
    """
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        try:
            cur.execute(
                "UPDATE accounts SET balance = balance - %s "
                "WHERE id = %s AND balance >= %s",
                (amount, from_id, amount),
            )
            if cur.rowcount == 0:
                raise ValueError("Insufficient funds or account not found")
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE id = %s",
                (amount, to_id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def transfer_with_audit_log(conn, from_id: int, to_id: int, amount: float) -> None:
    """Same transfer, but the audit insert is optional thanks to a savepoint."""
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        try:
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE id = %s",
                (amount, from_id),
            )

            cur.execute("SAVEPOINT before_audit")
            try:
                cur.execute(
                    "INSERT INTO audit_log (action, amount) VALUES ('transfer', %s)",
                    (amount,),
                )
            except Exception:
                # Roll back only the audit insert, keep the main transaction
                cur.execute("ROLLBACK TO SAVEPOINT before_audit")

            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE id = %s",
                (amount, to_id),
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def lock_row_for_update(conn, account_id: int) -> None:
    """Pessimistic locking: pin the row until the transaction ends."""
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        cur.execute(
            "SELECT balance FROM accounts WHERE id = %s FOR UPDATE",
            (account_id,),
        )
        # Application logic here — other writers wait on this row
        cur.execute(
            "UPDATE accounts SET balance = balance - 100 WHERE id = %s",
            (account_id,),
        )
        conn.commit()


if __name__ == "__main__":
    conn = psycopg2.connect(CONN_STR)
    try:
        transfer(conn, from_id=1, to_id=2, amount=100.0)
        print("Transfer committed")
    except Exception as exc:
        print(f"Rolled back: {exc}")
    finally:
        conn.close()
