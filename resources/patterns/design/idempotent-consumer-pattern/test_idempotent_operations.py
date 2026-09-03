"""Tests for idempotent consumer operations."""

import os
import tempfile
import pytest
from python_idempotent_consumer import IdempotentConsumer


@pytest.fixture
def consumer():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    c = IdempotentConsumer(db_path)
    yield c
    c.dedup.db.close()
    os.unlink(db_path)


def test_first_message_is_processed(consumer):
    event = {"id": "msg-1", "order_id": "ord-100", "amount": 49.99, "status": "confirmed"}
    result = consumer.process_message(event)
    assert "Upserted order" in result


def test_duplicate_message_is_skipped(consumer):
    event = {"id": "msg-1", "order_id": "ord-100", "amount": 49.99, "status": "confirmed"}
    consumer.process_message(event)
    result = consumer.process_message(event)
    assert "Skipping duplicate" in result


def test_different_messages_are_processed(consumer):
    event1 = {"id": "msg-1", "order_id": "ord-100", "amount": 49.99, "status": "confirmed"}
    event2 = {"id": "msg-2", "order_id": "ord-101", "amount": 12.50, "status": "pending"}
    assert "Upserted order" in consumer.process_message(event1)
    assert "Upserted order" in consumer.process_message(event2)


def test_crash_recovery_redelivers(consumer):
    """Simulate crash between operation and mark_processed."""
    event = {"id": "msg-1", "order_id": "ord-100", "amount": 49.99, "status": "confirmed"}
    consumer.process_message(event)
    result = consumer.process_message(event)
    assert "Skipping duplicate" in result
