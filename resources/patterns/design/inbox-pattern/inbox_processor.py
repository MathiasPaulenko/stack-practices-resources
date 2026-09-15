"""Inbox Pattern implementation with SQLite for idempotent event processing."""

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional


@dataclass
class InboxMessage:
    id: int
    message_id: str
    payload: str
    status: str  # 'pending', 'processing', 'completed', 'failed'
    created_at: datetime
    processed_at: Optional[datetime] = None
    retry_count: int = 0


class InboxProcessor:
    """Inbox pattern implementation with SQLite."""

    MAX_RETRIES = 3

    def __init__(self, db_path: str = "inbox.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS inbox (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE NOT NULL,
                payload TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                retry_count INTEGER DEFAULT 0
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON inbox(status)")
        self.conn.commit()

    def receive(self, raw_payload: dict) -> bool:
        """Store incoming message; returns False if duplicate."""
        message_id = self._generate_message_id(raw_payload)
        payload_json = json.dumps(raw_payload)
        try:
            self.conn.execute(
                "INSERT INTO inbox (message_id, payload) VALUES (?, ?)",
                (message_id, payload_json),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Duplicate

    def _generate_message_id(self, payload: dict) -> str:
        """Generate deterministic message ID from payload."""
        content = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def process_pending(self, processor_func: Callable):
        """Fetch and process pending messages with retries."""
        cursor = self.conn.execute(
            "SELECT id, message_id, payload, retry_count FROM inbox WHERE status = 'pending'"
        )
        for row in cursor.fetchall():
            msg_id, message_id, payload, retries = row
            self.conn.execute(
                "UPDATE inbox SET status = 'processing' WHERE id = ?", (msg_id,)
            )
            self.conn.commit()
            try:
                result = processor_func(json.loads(payload))
                self.conn.execute(
                    "UPDATE inbox SET status = 'completed', processed_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (msg_id,),
                )
                self.conn.commit()
                print(f"Processed {message_id}: {result}")
            except Exception as e:
                new_retries = retries + 1
                status = "failed" if new_retries >= self.MAX_RETRIES else "pending"
                self.conn.execute(
                    "UPDATE inbox SET status = ?, retry_count = ? WHERE id = ?",
                    (status, new_retries, msg_id),
                )
                self.conn.commit()
                print(f"Failed {message_id} (retry {new_retries}): {e}")

    def get_stats(self) -> dict:
        cursor = self.conn.execute(
            "SELECT status, COUNT(*) FROM inbox GROUP BY status"
        )
        return {row[0]: row[1] for row in cursor.fetchall()}


if __name__ == "__main__":
    inbox = InboxProcessor()

    event1 = {"order_id": "ORD-001", "amount": 99.99, "event": "payment.received"}
    event2 = {"order_id": "ORD-001", "amount": 99.99, "event": "payment.received"}

    print(f"Received event1: {inbox.receive(event1)}")  # True
    print(f"Received event2: {inbox.receive(event2)}")  # False (duplicate)

    inbox.process_pending(lambda p: f"Payment of ${p['amount']} processed")
    print(inbox.get_stats())
