"""Safe raw SQL with sqlite3 (stdlib). Same patterns apply to psycopg2 with %s."""

import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute(
    "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, role TEXT, active INTEGER)"
)

# Parameterized insert — never interpolate values
cur.execute(
    "INSERT INTO users (email, role, active) VALUES (?, ?, ?)",
    ("alice@example.com", "admin", 1),
)

# Bulk insert with executemany
cur.executemany(
    "INSERT INTO users (email, role, active) VALUES (?, ?, ?)",
    [("bob@example.com", "user", 1), ("carol@example.com", "user", 0)],
)
conn.commit()

# Parameterized SELECT
cur.execute("SELECT id, email FROM users WHERE email = ? AND active = ?", ("alice@example.com", 1))
print("found:", cur.fetchone())

# Dynamic IN clause — expand placeholders to match the list
emails = ["alice@example.com", "bob@example.com"]
placeholders = ",".join("?" * len(emails))
cur.execute(f"SELECT email FROM users WHERE email IN ({placeholders})", emails)
print("in-clause:", [r[0] for r in cur.fetchall()])

# Dynamic identifier — whitelist, then interpolate the validated name
ALLOWED_COLUMNS = {"id", "email", "role", "active"}
column = "role"
if column not in ALLOWED_COLUMNS:
    raise ValueError(f"Invalid column: {column}")
cur.execute(f"SELECT {column}, COUNT(*) FROM users GROUP BY {column}")
print("whitelist:", cur.fetchall())

conn.close()
