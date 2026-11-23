import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import psycopg2

@dataclass
class DomainEvent:
    event_type: str
    aggregate_type: str
    aggregate_id: str
    payload: dict

class OutboxPublisher:
    def __init__(self, db_connection):
        self.conn = db_connection

    def publish(self, event: DomainEvent):
        """Write event to outbox table within caller's transaction."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
                VALUES (%s, %s, %s, %s)
                """,
                (event.aggregate_type, event.aggregate_id,
                 event.event_type, json.dumps(event.payload))
            )

class OrderService:
    def __init__(self, db_connection, outbox: OutboxPublisher):
        self.conn = db_connection
        self.outbox = outbox

    def place_order(self, user_id: str, product_id: str, amount: float):
        with self.conn:
            with self.conn.cursor() as cur:
                # Business operation
                cur.execute(
                    "INSERT INTO orders (user_id, product_id, amount) VALUES (%s, %s, %s) RETURNING id",
                    (user_id, product_id, amount)
                )
                order_id = cur.fetchone()[0]

                # Event written in same transaction
                self.outbox.publish(DomainEvent(
                    event_type="OrderPlaced",
                    aggregate_type="Order",
                    aggregate_id=str(order_id),
                    payload={"user_id": user_id, "product_id": product_id, "amount": amount}
                ))

class OutboxRelay:
    def __init__(self, db_connection, message_broker):
        self.conn = db_connection
        self.broker = message_broker

    def run(self):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, aggregate_type, aggregate_id, event_type, payload
                    FROM outbox
                    WHERE published_at IS NULL
                    ORDER BY id
                    LIMIT 100
                    FOR UPDATE SKIP LOCKED
                    """
                )
                rows = cur.fetchall()

                for row in rows:
                    event_id, agg_type, agg_id, event_type, payload = row
                    try:
                        self.broker.publish(event_type, {
                            "aggregate_type": agg_type,
                            "aggregate_id": agg_id,
                            "payload": payload
                        })
                        cur.execute(
                            "UPDATE outbox SET published_at = NOW() WHERE id = %s",
                            (event_id,)
                        )
                    except Exception:
                        cur.execute(
                            "UPDATE outbox SET retry_count = retry_count + 1 WHERE id = %s",
                            (event_id,)
                        )
