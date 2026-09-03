"""Tests for RabbitMQ exchange types.

Requires a running RabbitMQ instance (use docker-compose up).
Run: pytest test_exchanges.py -v
"""
import json
import pytest
import pika


@pytest.fixture
def channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = connection.channel()
    yield ch
    connection.close()


def test_direct_exchange_routes_by_exact_key(channel):
    channel.exchange_declare(exchange="test_direct", exchange_type="direct")
    channel.queue_declare(queue="test_direct_created", auto_delete=True)
    channel.queue_bind(exchange="test_direct", queue="test_direct_created", routing_key="created")

    channel.basic_publish(exchange="test_direct", routing_key="created", body="test message")
    channel.basic_publish(exchange="test_direct", routing_key="cancelled", body="wrong queue")

    method, _, body = channel.basic_get(queue="test_direct_created", auto_ack=True)
    assert body == b"test message"
    assert method.routing_key == "created"


def test_topic_exchange_matches_patterns(channel):
    channel.exchange_declare(exchange="test_topic", exchange_type="topic")
    channel.queue_declare(queue="test_topic_errors", auto_delete=True)
    channel.queue_bind(exchange="test_topic", queue="test_topic_errors", routing_key="*.error")

    channel.basic_publish(exchange="test_topic", routing_key="app.error", body="error")
    channel.basic_publish(exchange="test_topic", routing_key="app.warning", body="warning")

    method, _, body = channel.basic_get(queue="test_topic_errors", auto_ack=True)
    assert body == b"error"

    method, _, body = channel.basic_get(queue="test_topic_errors", auto_ack=True)
    assert method is None  # warning should not match


def test_fanout_exchange_broadcasts_to_all(channel):
    channel.exchange_declare(exchange="test_fanout", exchange_type="fanout")
    channel.queue_declare(queue="test_fanout_q1", auto_delete=True)
    channel.queue_declare(queue="test_fanout_q2", auto_delete=True)
    channel.queue_bind(exchange="test_fanout", queue="test_fanout_q1")
    channel.queue_bind(exchange="test_fanout", queue="test_fanout_q2")

    channel.basic_publish(exchange="test_fanout", routing_key="", body="broadcast")

    _, _, body1 = channel.basic_get(queue="test_fanout_q1", auto_ack=True)
    _, _, body2 = channel.basic_get(queue="test_fanout_q2", auto_ack=True)
    assert body1 == b"broadcast"
    assert body2 == b"broadcast"


def test_dlx_routes_rejected_messages(channel):
    channel.exchange_declare(exchange="test_dlx", exchange_type="direct")
    channel.queue_declare(queue="test_dlx_dead", auto_delete=True)
    channel.queue_bind(exchange="test_dlx", queue="test_dlx_dead", routing_key="dead")

    channel.queue_declare(
        queue="test_dlx_main",
        auto_delete=True,
        arguments={
            "x-dead-letter-exchange": "test_dlx",
            "x-dead-letter-routing-key": "dead",
        },
    )

    channel.basic_publish(exchange="", routing_key="test_dlx_main", body="poison")
    method, _, _ = channel.basic_get(queue="test_dlx_main", auto_ack=False)
    channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    # Message should appear in dead letter queue
    _, _, body = channel.basic_get(queue="test_dlx_dead", auto_ack=True)
    assert body == b"poison"
