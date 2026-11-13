"""Idempotent load demo on SQLite — run it twice, the table stays clean.

The pattern: stage the batch, MERGE-equivalent upsert into target,
record the load_id in a history table, skip if it was already loaded.
SQLite has no MERGE, so the demo uses INSERT ... ON CONFLICT upsert.
"""
import hashlib
import sqlite3
from datetime import datetime


def generate_load_id(source_table: str, batch_date: str) -> str:
    raw = f"{source_table}_{batch_date}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def setup(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            email TEXT,
            name TEXT,
            status TEXT
        );
        CREATE TABLE IF NOT EXISTS _load_history (
            load_id TEXT PRIMARY KEY,
            source_table TEXT,
            target_table TEXT,
            row_count INTEGER,
            loaded_at TEXT
        );
    """)


def load(conn: sqlite3.Connection, rows: list[tuple],
         source_table: str, target_table: str, batch_date: str) -> dict:
    """Idempotent load: skip a finished batch, upsert a new one."""
    load_id = generate_load_id(source_table, batch_date)

    done = conn.execute(
        "SELECT 1 FROM _load_history WHERE load_id = ?", (load_id,)
    ).fetchone()
    if done:
        print(f"Load {load_id} already completed. Skipping.")
        return {"load_id": load_id, "status": "skipped", "rows": 0}

    with conn:  # transaction: upsert + history record commit together
        conn.executemany(
            f"""INSERT INTO {target_table} (id, email, name, status)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   email = excluded.email,
                   name = excluded.name,
                   status = excluded.status""",
            rows,
        )
        conn.execute(
            "INSERT INTO _load_history VALUES (?, ?, ?, ?, ?)",
            (load_id, source_table, target_table, len(rows), datetime.now().isoformat()),
        )

    print(f"Load {load_id} completed: {len(rows)} rows")
    return {"load_id": load_id, "status": "loaded", "rows": len(rows)}


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    setup(conn)

    batch = [(1, "ana@x.com", "Ana", "active"), (2, "bob@x.com", "Bob", "active")]

    load(conn, batch, "crm.customers", "customers", "2026-11-13")
    load(conn, batch, "crm.customers", "customers", "2026-11-13")  # retry: skipped

    # Changed batch, same day: upserts, no duplicates
    batch_v2 = [(1, "ana@x.com", "Ana", "churned"), (3, "cat@x.com", "Cat", "new")]
    # Different source name = different load_id, so it loads and merges
    load(conn, batch_v2, "crm.customers_v2", "customers", "2026-11-13")

    print(conn.execute("SELECT * FROM customers ORDER BY id").fetchall())
    # [(1, 'ana@x.com', 'Ana', 'churned'), (2, 'bob@x.com', 'Bob', 'active'),
    #  (3, 'cat@x.com', 'Cat', 'new')] — 3 rows, zero duplicates
