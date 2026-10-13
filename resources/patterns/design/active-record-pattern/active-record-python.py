"""Active Record pattern: a User class where each instance is a table row.

Run: python active-record-python.py
Requires: Python 3.8+, no dependencies (sqlite3 from stdlib).
"""

import sqlite3
from typing import Optional, List


class User:
    _db_path = "app.db"

    def __init__(self, id: int = None, name: str = "", email: str = ""):
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def _connect(cls):
        return sqlite3.connect(cls._db_path)

    @classmethod
    def create_table(cls):
        with cls._connect() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )"""
            )

    def save(self):
        with self._connect() as conn:
            if self.id is None:
                cursor = conn.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (self.name, self.email),
                )
                self.id = cursor.lastrowid
            else:
                conn.execute(
                    "UPDATE users SET name = ?, email = ? WHERE id = ?",
                    (self.name, self.email, self.id),
                )
            conn.commit()
        return self

    def delete(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (self.id,))
            conn.commit()

    @classmethod
    def find_by_id(cls, user_id: int) -> Optional["User"]:
        with cls._connect() as conn:
            row = conn.execute(
                "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            return cls(*row) if row else None

    @classmethod
    def find_all(cls) -> List["User"]:
        with cls._connect() as conn:
            rows = conn.execute("SELECT id, name, email FROM users").fetchall()
            return [cls(*row) for row in rows]

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"


if __name__ == "__main__":
    User.create_table()

    user = User(name="Alice", email="alice@example.com")
    user.save()
    print("saved:", User.find_by_id(user.id))

    user.name = "Alice Cooper"
    user.save()  # UPDATE this time
    print("updated:", User.find_by_id(user.id))

    user.delete()
    print("after delete:", User.find_by_id(user.id))
