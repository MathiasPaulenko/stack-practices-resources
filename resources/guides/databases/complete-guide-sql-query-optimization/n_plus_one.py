"""Offline N+1 demo — runs with stdlib sqlite3 only, no server needed.

Seeds a small users/orders database in memory, then runs the same page
of data two ways and counts the queries issued:

  1. N+1:   one query for the users, one per user for their orders.
  2. JOIN:  a single grouped query.

Usage:  python n_plus_one.py [num_users]
"""

import sqlite3
import sys
import time

QUERY_COUNT = 0


def counted_execute(conn, *args):
    global QUERY_COUNT
    QUERY_COUNT += 1
    return conn.execute(*args)


def seed(conn, num_users):
    conn.executescript(
        """
        CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE orders (
          id INTEGER PRIMARY KEY,
          user_id INTEGER NOT NULL REFERENCES users(id),
          total REAL
        );
        """
    )
    conn.executemany(
        "INSERT INTO users VALUES (?, ?)",
        [(i, f"user{i}") for i in range(1, num_users + 1)],
    )
    orders = []
    oid = 1
    for user_id in range(1, num_users + 1):
        for _ in range(user_id % 5):  # 0-4 orders per user
            orders.append((oid, user_id, oid * 1.25))
            oid += 1
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?)", orders)
    conn.commit()


def run_n_plus_one(conn):
    """One query for the list + one query per item."""
    users = counted_execute(conn, "SELECT id, name FROM users").fetchall()
    out = []
    for user_id, name in users:
        rows = counted_execute(
            conn, "SELECT COUNT(*), COALESCE(SUM(total),0) FROM orders WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        out.append((name, rows[0], rows[1]))
    return out


def run_join(conn):
    """The same data in a single grouped query."""
    return counted_execute(
        conn,
        """
        SELECT u.name, COUNT(o.id), COALESCE(SUM(o.total),0)
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        GROUP BY u.id, u.name
        """,
    ).fetchall()


def main():
    num_users = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    conn = sqlite3.connect(":memory:")
    seed(conn, num_users)

    global QUERY_COUNT

    QUERY_COUNT = 0
    t0 = time.perf_counter()
    slow = run_n_plus_one(conn)
    t_slow = time.perf_counter() - t0
    q_slow = QUERY_COUNT

    QUERY_COUNT = 0
    t0 = time.perf_counter()
    fast = run_join(conn)
    t_fast = time.perf_counter() - t0
    q_fast = QUERY_COUNT

    assert sorted(slow) == sorted(fast), "both approaches must return the same data"

    print(f"users:           {num_users}")
    print(f"N+1 approach:    {q_slow} queries, {t_slow * 1000:.2f} ms")
    print(f"JOIN approach:   {q_fast} query,  {t_fast * 1000:.2f} ms")
    print()
    print("sqlite in-memory hides network latency — against a real server")
    print("each of those N extra queries also pays a round trip.")


if __name__ == "__main__":
    main()
