"""Tests for RabbitMQ consumer patterns.

Requires a running RabbitMQ instance (use docker-compose up).
Run: pytest test_consumer_patterns.py -v
"""
import json
import time
import pytest
import pika


@pytest.fixture
def channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = connection.channel()
    yield ch
    connection.close()


def test_work_queue_distributes_messages(channel):
    channel.queue_declare(queue="test_work", auto_delete=True)
    channel.queue_purge(queue="test_work")

    for i in range(5):
        channel.basic_publish(exchange="", routing_key="test_work", body=json.dumps({"task": i}))

    received = []
    for _ in range(5):
        method, _, body = channel.basic_get(queue="test_work", auto_ack=True)
        if method:
            received.append(json.loads(body)["task"])

    assert sorted(received) == [0, 1, 2, 3, 4]


def test_publisher_confirms(channel):
    channel.confirm_delivery()
    try:
        channel.basic_publish(
            exchange="",
            routing_key="test_confirm_queue",
            body="confirmed message",
            mandatory=False,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        confirmed = True
    except pika.exceptions.UnroutableError:
        confirmed = False
    assert confirmed


def test_priority_queue_orders_by_priority(channel):
    channel.queue_delete(queue="test_priority")
    channel.queue_declare(queue="test_priority", arguments={"x-max-priority": 10})

    channel.basic_publish(
        exchange="",
        routing_key="test_priority",
        body="low",
        properties=pika.BasicProperties(priority=1),
    )
    channel.basic_publish(
        exchange="",
        routing_key="test_priority",
        body="high",
        properties=pika.BasicProperties(priority=9),
    )
    channel.basic_publish(
        exchange="",
        routing_key="test_priority",
        body="medium",
        properties=pika.BasicProperties(priority=5),
    )

    method, _, body = channel.basic_get(queue="test_priority", auto_ack=True)
    assert body == b"high"

    method, _, body = channel.basic_get(queue="test_priority", auto_ack=True)
    assert body == b"medium"

    method, _, body = channel.basic_get(queue="test_priority", auto_ack=True)
    assert body == b"low"

    channel.queue_delete(queue="test_priority")


def test_ttl_expired_messages_go_to_dlx(channel):
    channel.exchange_declare(exchange="test_ttl_dlx", exchange_type="direct")
    channel.queue_declare(queue="test_ttl_dead", auto_delete=True)
    channel.queue_bind(exchange="test_ttl_dlx", queue="test_ttl_dead", routing_key="expired")

    channel.queue_declare(
        queue="test_ttl_main",
        auto_delete=True,
        arguments={
            "x-dead-letter-exchange": "test_ttl_dlx",
            "x-dead-letter-routing-key": "expired",
            "x-message-ttl": 100,  # 100ms TTL
        },
    )

    channel.basic_publish(exchange="", routing_key="test_ttl_main", body="will expire")
    time.sleep(0.3)  # wait for TTL to expire

    method, _, body = channel.basic_get(queue="test_ttl_main", auto_ack=True)
    assert method is None  # message should have expired

    _, _, body = channel.basic_get(queue="test_ttl_dead", auto_ack=True)
    assert body == b"will expire"
