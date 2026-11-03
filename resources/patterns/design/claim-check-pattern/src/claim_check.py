"""Claim Check Pattern demo — stdlib only.

Simulates: large payload -> object storage -> claim token -> broker -> consumer.
Run: python claim_check.py
"""

import json
import uuid
from datetime import datetime
from typing import Optional


class BlobStorage:
    """In-memory blob store standing in for S3 / Azure Blob / GCS."""

    def __init__(self):
        self._store = {}

    def upload(self, data: bytes, content_type: str = "application/json") -> str:
        token = str(uuid.uuid4())
        self._store[token] = {
            "data": data,
            "content_type": content_type,
            "created_at": datetime.now(),
        }
        return token

    def download(self, token: str) -> Optional[bytes]:
        entry = self._store.get(token)
        return entry["data"] if entry else None

    def delete(self, token: str):
        self._store.pop(token, None)


class MessageBroker:
    """In-memory broker standing in for SQS / Kafka / RabbitMQ."""

    def __init__(self):
        self._queues = {}

    def publish(self, queue: str, message: dict):
        self._queues.setdefault(queue, []).append(message)

    def consume(self, queue: str) -> Optional[dict]:
        messages = self._queues.get(queue, [])
        return messages.pop(0) if messages else None


class ClaimCheckProducer:
    """Publishes messages with claim check tokens instead of large payloads."""

    def __init__(self, broker: MessageBroker, storage: BlobStorage):
        self.broker = broker
        self.storage = storage

    def publish_large_message(
        self, queue: str, payload: dict, metadata: Optional[dict] = None
    ):
        payload_bytes = json.dumps(payload).encode("utf-8")
        token = self.storage.upload(payload_bytes, "application/json")

        message = {
            "claim_check": token,
            "metadata": metadata or {},
            "payload_size": len(payload_bytes),
            "timestamp": datetime.now().isoformat(),
        }
        self.broker.publish(queue, message)
        print(f"Published claim check: {token}")
        print(f"  payload size in storage: {len(payload_bytes):,} bytes")
        print(f"  message size on broker:  ~{len(json.dumps(message))} bytes")
        return token


class ClaimCheckConsumer:
    """Consumes messages and retrieves full payloads via claim check."""

    def __init__(self, broker: MessageBroker, storage: BlobStorage):
        self.broker = broker
        self.storage = storage

    def process_next(self, queue: str):
        message = self.broker.consume(queue)
        if not message:
            return None

        token = message["claim_check"]
        payload_bytes = self.storage.download(token)

        if payload_bytes is None:
            print(f"ERROR: claim check {token} not found in storage")
            return None

        payload = json.loads(payload_bytes.decode("utf-8"))
        print(f"Retrieved payload ({message['payload_size']:,} bytes): {payload['report_id']}")

        self.storage.delete(token)
        print(f"Deleted claim check: {token}")
        return payload


if __name__ == "__main__":
    storage = BlobStorage()
    broker = MessageBroker()
    producer = ClaimCheckProducer(broker, storage)
    consumer = ClaimCheckConsumer(broker, storage)

    large_report = {
        "report_id": "RPT-2024-Q1",
        "generated_at": datetime.now().isoformat(),
        "records": [{"id": i, "data": "x" * 1000} for i in range(1000)],
        "summary": {"total": 1000, "revenue": 500000.00},
    }

    producer.publish_large_message("reports.queue", large_report, {"priority": "high"})
    consumer.process_next("reports.queue")
