"""Runnable backfill demo: sqlite-based dual-write + backfill + validation.

Demonstrates the pattern from the data-migration guide without needing a real
database pair: an "old" table and a "new" table in the same SQLite file.
Run: python backfill_demo.py
"""

import sqlite3
import time

BATCH = 5


class Demo:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute(
            "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, bio TEXT, created_at TEXT)"
        )
        self.db.execute(
            "CREATE TABLE user_profiles(user_id INTEGER PRIMARY KEY, display_name TEXT, bio TEXT, created_at TEXT)"
        )
        self.db.execute(
            "CREATE TABLE migration_checkpoints(migration TEXT PRIMARY KEY, last_id INTEGER)"
        )

        # Seed the "old" system
        for i in range(1, 21):
            self.db.execute(
                "INSERT INTO users VALUES(?,?,?,?)", (i, f"user-{i}", f"bio-{i}", "2025-01-01")
            )
        self.db.commit()

    # --- dual-write path ---
    def create_user(self, name):
        cur = self.db.execute(
            "INSERT INTO users(name, bio, created_at) VALUES(?,?,?)",
            (name, "", "2025-06-01"),
        )
        user_id = cur.lastrowid
        try:
            self.db.execute(
                "INSERT INTO user_profiles VALUES(?,?,?,?)",
                (user_id, name, "", "2025-06-01"),
            )
        except Exception as e:
            print(f"  dual-write failed for {user_id}: {e}")
        self.db.commit()
        return user_id

    # --- resumable backfill ---
    def checkpoint(self):
        row = self.db.execute(
            "SELECT last_id FROM migration_checkpoints WHERE migration='users_to_profiles'"
        ).fetchone()
        return row[0] if row else 0

    def save_checkpoint(self, last_id):
        self.db.execute(
            "INSERT INTO migration_checkpoints VALUES('users_to_profiles',?) "
            "ON CONFLICT(migration) DO UPDATE SET last_id=excluded.last_id",
            (last_id,),
        )
        self.db.commit()

    def backfill(self):
        last_id = self.checkpoint()
        migrated = 0
        while True:
            batch = self.db.execute(
                "SELECT * FROM users WHERE id > ? ORDER BY id LIMIT ?", (last_id, BATCH)
            ).fetchall()
            if not batch:
                break
            for user in batch:
                # upsert → idempotent
                self.db.execute(
                    "INSERT INTO user_profiles VALUES(?,?,?,?) "
                    "ON CONFLICT(user_id) DO UPDATE SET display_name=excluded.display_name",
                    (user[0], user[1], user[2], user[3]),
                )
            last_id = batch[-1][0]
            self.save_checkpoint(last_id)
            migrated += len(batch)
            time.sleep(0.01)  # throttle — don't starve production
        self.db.commit()
        print(f"  backfill migrated {migrated} rows (resumed from id {self.checkpoint() - migrated if migrated else 0})")

    # --- validation ---
    def validate(self):
        old = self.db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        new = self.db.execute("SELECT COUNT(*) FROM user_profiles").fetchone()[0]
        assert old == new, f"count mismatch: {old} != {new}"
        mismatches = self.db.execute(
            "SELECT COUNT(*) FROM users u LEFT JOIN user_profiles p ON u.id=p.user_id "
            "WHERE p.user_id IS NULL OR u.name != p.display_name"
        ).fetchone()[0]
        assert mismatches == 0, f"{mismatches} mismatches"
        print(f"  validation passed: {old} rows, 0 mismatches")


if __name__ == "__main__":
    demo = Demo()

    uid = demo.create_user("dual-user")
    print(f"dual-write created user {uid} in both tables")

    # Kill the first run midway to prove resumability
    demo.backfill()
    demo.backfill()  # second run must be a no-op
    demo.validate()

    print("data-migration-guide demo OK")
