"""Identity Map pattern — runnable Python example.

Source: https://stackpractices.com/patterns/identity-map-pattern/

Run: python identity_map.py
Expected output: True (both lookups return the same object instance)
"""

import sqlite3
from typing import Any, Dict, Optional, Type


class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}')"


class IdentityMap:
    def __init__(self):
        self._map: Dict[Type, Dict[Any, Any]] = {}

    def add(self, entity):
        entity_type = type(entity)
        if entity_type not in self._map:
            self._map[entity_type] = {}
        key = self._extract_key(entity)
        self._map[entity_type][key] = entity

    def get(self, entity_type: Type, key: Any) -> Optional[Any]:
        return self._map.get(entity_type, {}).get(key)

    def has(self, entity_type: Type, key: Any) -> bool:
        return key in self._map.get(entity_type, {})

    def remove(self, entity_type: Type, key: Any):
        type_map = self._map.get(entity_type)
        if type_map:
            type_map.pop(key, None)

    def _extract_key(self, entity) -> Any:
        return getattr(entity, "id", None)


class UserMapper:
    def __init__(self, connection: sqlite3.Connection, identity_map: IdentityMap):
        self._conn = connection
        self._identity_map = identity_map

    def find_by_id(self, user_id: int) -> Optional[User]:
        # Check the identity map first
        cached = self._identity_map.get(User, user_id)
        if cached:
            return cached

        row = self._conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if row:
            user = User(user_id=row["id"], name=row["name"], email=row["email"])
            self._identity_map.add(user)
            return user
        return None

    def find_all(self):
        rows = self._conn.execute("SELECT id, name, email FROM users").fetchall()
        users = []
        for row in rows:
            user = self._identity_map.get(User, row["id"])
            if not user:
                user = User(user_id=row["id"], name=row["name"], email=row["email"])
                self._identity_map.add(user)
            users.append(user)
        return users


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    # Rows come back dict-like so row["id"] works — without this line
    # sqlite3 returns plain tuples and the mapper crashes.
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")

    identity_map = IdentityMap()
    mapper = UserMapper(conn, identity_map)

    user1 = mapper.find_by_id(1)
    user2 = mapper.find_by_id(1)

    print(user1 is user2)  # True — same object instance

    all_users = mapper.find_all()
    print(all_users[0] is user1)  # True — collection queries reuse the map too
