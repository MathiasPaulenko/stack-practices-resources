"""Parameterized-query examples with sqlite3.

Run directly: `python parameterized_queries.py`
Creates an in-memory database, seeds demo rows, and shows how a
concatenated query gets exploited while the parameterized version
returns a safe result.
"""

import sqlite3

ALLOWED_SORT_COLUMNS = {
    "name": "name",
    "email": "email",
    "created_at": "created_at",
}


def seed(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT
        );
        INSERT INTO users (name, email, active, created_at) VALUES
            ('Ada',   'ada@example.com',   1, '2026-01-01'),
            ('Grace', 'grace@example.com', 1, '2026-02-01'),
            ('Linus', 'linus@example.com', 0, '2026-03-01');
        """
    )


def find_user_unsafe(conn: sqlite3.Connection, email: str):
    """VULNERABLE — input is concatenated into the SQL string."""
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return conn.execute(query).fetchall()


def find_user_safe(conn: sqlite3.Connection, email: str):
    """SAFE — the driver binds input as data, never as SQL."""
    return conn.execute(
        "SELECT * FROM users WHERE email = ? AND active = ?",
        (email, 1),
    ).fetchall()


def get_users_safe(
    conn: sqlite3.Connection,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    limit: int = 20,
    offset: int = 0,
):
    """Dynamic ORDER BY via allowlist; LIMIT/OFFSET stay parameterized."""
    column = ALLOWED_SORT_COLUMNS.get(sort_by)
    if column is None:
        raise ValueError(f"Invalid sort column: {sort_by}")
    direction = "ASC" if sort_dir.upper() == "ASC" else "DESC"
    query = (
        f"SELECT id, name, email, created_at FROM users "
        f"WHERE active = 1 ORDER BY {column} {direction} LIMIT ? OFFSET ?"
    )
    return conn.execute(query, (limit, offset)).fetchall()


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    seed(conn)

    attack = "x' OR '1'='1"
    print("unsafe:", find_user_unsafe(conn, attack))
    # -> returns every row: the input changed the SQL the DB parsed
    print("safe:  ", find_user_safe(conn, attack))
    # -> returns []: the same text is just a literal value

    print("sorted:", get_users_safe(conn, sort_by="name", sort_dir="asc"))
    try:
        get_users_safe(conn, sort_by="name; DROP TABLE users--")
    except ValueError as exc:
        print("rejected:", exc)
