"""Sequential Convoy pattern — runnable simulation (no broker required).

Routes events to partitions by entity ID so all events for one entity land
in the same partition in production order. Each partition is drained by a
single consumer that applies events in sequence-number order, buffering
out-of-order arrivals until the gap closes.

Run: python convoy_processor.py
"""

from collections import defaultdict


class PartitionedBroker:
    """Minimal stand-in for Kafka-style partitioning."""

    def __init__(self, num_partitions: int = 4) -> None:
        self.partitions: list[list[dict]] = [[] for _ in range(num_partitions)]

    def publish(self, entity_id: str, event: dict) -> None:
        partition = hash(entity_id) % len(self.partitions)
        self.partitions[partition].append(event)


class ConvoyProducer:
    """Assigns a monotonically increasing sequence number per entity."""

    def __init__(self, broker: PartitionedBroker) -> None:
        self.broker = broker
        self._sequences: dict[str, int] = defaultdict(int)

    def send(self, entity_id: str, event_type: str, payload: dict) -> None:
        self._sequences[entity_id] += 1
        self.broker.publish(entity_id, {
            "entity_id": entity_id,
            "sequence": self._sequences[entity_id],
            "event_type": event_type,
            "payload": payload,
        })


class ConvoyConsumer:
    """Processes one partition at a time, strictly in sequence order."""

    def __init__(self) -> None:
        self._last_processed: dict[str, int] = {}
        self._pending: dict[str, dict[int, dict]] = defaultdict(dict)
        self.processed: list[tuple[str, int]] = []

    def consume(self, event: dict) -> None:
        entity = event["entity_id"]
        seq = event["sequence"]
        expected = self._last_processed.get(entity, 0) + 1

        if seq == expected:
            self._apply(event)
            self._drain_pending(entity)
        elif seq > expected:
            # Out of order — buffer until the missing messages arrive.
            self._pending[entity][seq] = event
        # seq < expected means a duplicate; safe to skip.

    def _apply(self, event: dict) -> None:
        self.processed.append((event["entity_id"], event["sequence"]))
        self._last_processed[event["entity_id"]] = event["sequence"]

    def _drain_pending(self, entity: str) -> None:
        pending = self._pending[entity]
        expected = self._last_processed.get(entity, 0) + 1
        while expected in pending:
            self._apply(pending.pop(expected))
            expected += 1


if __name__ == "__main__":
    broker = PartitionedBroker(num_partitions=4)
    producer = ConvoyProducer(broker)
    consumer = ConvoyConsumer()

    producer.send("user-123", "created", {"name": "Alice"})
    producer.send("user-123", "updated", {"name": "Alice Smith"})
    producer.send("user-456", "created", {"name": "Bob"})
    producer.send("user-123", "deleted", {})

    # Simulate an out-of-order delivery for user-123: skip seq 2, deliver 3 first.
    events = [e for part in broker.partitions for e in part]
    u123 = [e for e in events if e["entity_id"] == "user-123"]
    reordered = [u123[0], u123[2], u123[1]] + [
        e for e in events if e["entity_id"] != "user-123"
    ]

    for event in reordered:
        consumer.consume(event)

    print("Processed order:", consumer.processed)
    assert consumer.processed[:3] == [
        ("user-123", 1), ("user-123", 2), ("user-123", 3)
    ], "convoy ordering broken"
    print("user-123 processed strictly in order despite out-of-order delivery.")
