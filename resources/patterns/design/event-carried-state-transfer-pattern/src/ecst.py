"""Event-Carried State Transfer — runnable simulation.

A source service publishes events that carry the full updated entity state;
a consumer service applies them to a local SQLite replica and serves reads
locally. Stdlib only — run with: python src/ecst.py
"""

from dataclasses import dataclass
from typing import Dict, Optional, List
import sqlite3
from datetime import datetime


@dataclass
class CustomerStateTransferEvent:
    event_id: str
    event_type: str  # "CUSTOMER_CREATED" or "CUSTOMER_UPDATED"
    customer_id: str
    payload: dict    # Full customer state
    timestamp: str
    version: int     # Sequence number for ordering


class CustomerService:
    """Owns customer data and publishes state transfer events."""

    def __init__(self, event_publisher):
        self.customers: Dict[str, dict] = {}
        self.event_publisher = event_publisher
        self.version_counter = 0

    def create_customer(self, customer_id: str, name: str, email: str,
                        tier: str = "basic") -> dict:
        customer = {
            "customer_id": customer_id,
            "name": name,
            "email": email,
            "tier": tier,
            "loyalty_points": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        self.customers[customer_id] = customer
        self._publish("CUSTOMER_CREATED", customer)
        return customer

    def update_customer_tier(self, customer_id: str, new_tier: str) -> Optional[dict]:
        customer = self.customers.get(customer_id)
        if not customer:
            return None

        customer["tier"] = new_tier
        customer["updated_at"] = datetime.now().isoformat()
        self._publish("CUSTOMER_UPDATED", customer)
        return customer

    def _publish(self, event_type: str, customer: dict) -> None:
        event = CustomerStateTransferEvent(
            event_id=f"evt-{self.version_counter}",
            event_type=event_type,
            customer_id=customer["customer_id"],
            payload=customer.copy(),
            timestamp=datetime.now().isoformat(),
            version=self.version_counter,
        )
        self.version_counter += 1
        self.event_publisher.publish(event)


class EventBus:
    """In-memory stand-in for Kafka/RabbitMQ topic subscriptions."""

    def __init__(self):
        self.topics: Dict[str, List[callable]] = {}

    def subscribe(self, topic: str, handler: callable):
        self.topics.setdefault(topic, []).append(handler)

    def publish(self, event: CustomerStateTransferEvent):
        topic = f"customer.{event.event_type.lower()}"
        for handler in self.topics.get(topic, []):
            handler(event)


class OrderServiceConsumer:
    """Maintains a local read-only copy of customer data for order processing."""

    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS customer_replicas (
                customer_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                tier TEXT NOT NULL,
                loyalty_points INTEGER DEFAULT 0,
                version INTEGER NOT NULL,
                updated_at TIMESTAMP
            )
        """)
        self.conn.commit()

    def on_customer_event(self, event: CustomerStateTransferEvent):
        """Apply a state transfer event to the local replica."""
        payload = event.payload
        self.conn.execute("""
            INSERT OR REPLACE INTO customer_replicas
            (customer_id, name, email, tier, loyalty_points, version, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            payload["customer_id"], payload["name"], payload["email"],
            payload["tier"], payload.get("loyalty_points", 0),
            event.version, payload["updated_at"]
        ))
        self.conn.commit()
        print(f"[OrderService] Replicated customer {payload['customer_id']} (v{event.version})")

    def get_customer_for_order(self, customer_id: str) -> Optional[dict]:
        """Read from the local replica — no cross-service call needed."""
        cursor = self.conn.execute(
            "SELECT * FROM customer_replicas WHERE customer_id = ?", (customer_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "customer_id": row[0], "name": row[1], "email": row[2],
                "tier": row[3], "loyalty_points": row[4], "version": row[5],
            }
        return None


if __name__ == "__main__":
    bus = EventBus()
    customer_service = CustomerService(bus)
    order_service = OrderServiceConsumer()

    bus.subscribe("customer.customer_created", order_service.on_customer_event)
    bus.subscribe("customer.customer_updated", order_service.on_customer_event)

    customer_service.create_customer("C-001", "Alice Johnson", "alice@example.com", "premium")
    print("Order service sees:", order_service.get_customer_for_order("C-001"))

    customer_service.update_customer_tier("C-001", "gold")
    print("After update:", order_service.get_customer_for_order("C-001"))
