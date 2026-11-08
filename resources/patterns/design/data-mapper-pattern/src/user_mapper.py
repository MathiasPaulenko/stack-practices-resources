"""Data Mapper pattern: domain object + mapper over sqlite3.

Run:  python src/user_mapper.py
"""
import sqlite3
from dataclasses import dataclass
from typing import Optional, List


# Domain Model — knows nothing about the database
@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    email: str = ""

    def update_email(self, new_email: str):
        if "@" not in new_email:
            raise ValueError("Invalid email")
        self.email = new_email


# Data Mapper — handles all persistence logic
class UserMapper:
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection

    def find_by_id(self, user_id: int) -> Optional[User]:
        row = self._conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if row:
            return User(id=row["id"], name=row["name"], email=row["email"])
        return None

    def find_all(self) -> List[User]:
        rows = self._conn.execute("SELECT id, name, email FROM users").fetchall()
        return [User(id=r["id"], name=r["name"], email=r["email"]) for r in rows]

    def insert(self, user: User):
        cursor = self._conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email)
        )
        user.id = cursor.lastrowid

    def update(self, user: User):
        self._conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (user.name, user.email, user.id)
        )

    def delete(self, user_id: int):
        self._conn.execute("DELETE FROM users WHERE id = ?", (user_id,))


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row  # rows support row["column"] access
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )

    mapper = UserMapper(conn)
    user = User(name="Alice", email="alice@example.com")
    mapper.insert(user)
    print(f"Inserted user with ID: {user.id}")

    loaded = mapper.find_by_id(user.id)
    print(loaded.name, loaded.email)
