"""Runnable DAO demo: creates a users table, exercises the DAO, prints results.

The DAO receives an open sqlite3.Connection in its constructor — callers own
the connection lifecycle. Swap `sqlite3.connect(":memory:")` for a file path
(or a pooled connection in a real app) without touching the DAO.

Run: python dao-python.py
"""

from dataclasses import dataclass
from typing import Optional, List
import sqlite3


@dataclass
class User:
    id: int
    name: str
    email: str


class UserDao:
    """Data Access Object for the users table (constructor-injected conn)."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def find_by_id(self, user_id: int) -> Optional[User]:
        row = self.conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return User(*row) if row else None

    def find_all(self) -> List[User]:
        rows = self.conn.execute(
            "SELECT id, name, email FROM users"
        ).fetchall()
        return [User(*row) for row in rows]

    def find_paginated(self, page: int, page_size: int = 50) -> List[User]:
        offset = (page - 1) * page_size
        rows = self.conn.execute(
            "SELECT id, name, email FROM users LIMIT ? OFFSET ?",
            (page_size, offset)
        ).fetchall()
        return [User(*row) for row in rows]

    def save(self, user: User) -> User:
        cursor = self.conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email)
        )
        user.id = cursor.lastrowid
        self.conn.commit()
        return user

    def delete(self, user_id: int) -> None:
        self.conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()


class FakeUserDao:
    """In-memory stand-in with the same interface — drop it into tests."""

    def __init__(self):
        self.users = {}

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def find_all(self) -> List[User]:
        return list(self.users.values())

    def find_paginated(self, page: int, page_size: int = 50) -> List[User]:
        all_users = list(self.users.values())
        offset = (page - 1) * page_size
        return all_users[offset:offset + page_size]

    def save(self, user: User) -> User:
        user.id = len(self.users) + 1
        self.users[user.id] = user
        return user

    def delete(self, user_id: int) -> None:
        self.users.pop(user_id, None)


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )

    dao = UserDao(conn)
    alice = dao.save(User(id=0, name="Alice", email="alice@example.com"))
    bob = dao.save(User(id=0, name="Bob", email="bob@example.com"))

    print("find_by_id:", dao.find_by_id(alice.id))
    print("find_all:", dao.find_all())
    print("paginated page 2:", dao.find_paginated(page=2, page_size=1))

    dao.delete(bob.id)
    print("after delete:", dao.find_all())

    fake = FakeUserDao()
    fake.save(User(id=0, name="Test", email="test@example.com"))
    print("fake DAO:", fake.find_all())
