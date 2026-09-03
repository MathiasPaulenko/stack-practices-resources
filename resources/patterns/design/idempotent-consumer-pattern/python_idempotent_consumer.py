"""Idempotent Consumer Pattern — Python implementation with SQLite dedup."""

import json
import sqlite3
from datetime import datetime
from typing import Optional


class DedupStore:
    """SQLite-backed deduplication store with TTL support."""

    def __init__(self, db_path: str = "processed.db"):
        self.db = sqlite3.connect(db_path)
        self._init_table()

    def _init_table(self) -> None:
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS processed (
                message_id TEXT PRIMARY KEY,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.db.commit()

    def is_new(self, message_id: str) -> bool:
        cursor = self.db.execute(
            "SELECT 1 FROM processed WHERE message_id = ?",
            (message_id,)
        )
        return cursor.fetchone() is None

    def mark_processed(self, message_id: str) -> None:
        self.db.execute(
            "INSERT OR IGNORE INTO processed (message_id) VALUES (?)",
            (message_id,)
        )
        self.db.commit()

    def cleanup_old(self, days: int = 7) -> int:
        cursor = self.db.execute(
            "DELETE FROM processed WHERE processed_at < datetime('now', ?)",
            (f"-{days} days",)
        )
        self.db.commit()
        return cursor.rowcount


class IdempotentConsumer:
    """Kafka consumer with deduplication for exactly-once processing."""

    def __init__(self, db_path: str = "processed.db"):
        self.dedup = DedupStore(db_path)

    def process_message(self, event: dict) -> Optional[str]:
        message_id = event["id"]

        if not self.dedup.is_new(message_id):
            return f"Skipping duplicate: {message_id}"

        result = self._upsert_order(
            order_id=event["order_id"],
            amount=event["amount"],
            status=event["status"],
        )

        self.dedup.mark_processed(message_id)
        return result

    def _upsert_order(self, order_id: str, amount: float, status: str) -> str:
        return f"Upserted order {order_id}: ${amount} ({status})"


if __name__ == "__main__":
    consumer = IdempotentConsumer()

    events = [
        {"id": "msg-1", "order_id": "ord-100", "amount": 49.99, "status": "confirmed"},
        {"id": "msg-2", "order_id": "ord-101", "amount": 12.50, "status": "pending"},
        {"id": "msg-1", "order_id": "ord-100", "amount": 49.99, "status": "confirmed"},
    ]

    for event in events:
        result = consumer.process_message(event)
        print(result)
