"""Declare a RabbitMQ queue with its dead-letter exchange (DLX) and DLQ.

Usage:
    python dlq_setup.py
Requires RabbitMQ on localhost:5672 and `pip install pika`.
"""

import pika


def declare_dlx_and_dlq(channel, dlx_name: str, dlq_name: str) -> None:
    channel.exchange_declare(exchange=dlx_name, exchange_type="direct", durable=True)
    channel.queue_declare(queue=dlq_name, durable=True)
    channel.queue_bind(queue=dlq_name, exchange=dlx_name, routing_key=dlq_name)


def setup_dlq(channel, main_queue: str, dlq_queue: str):
    dlx_name = f"{main_queue}.dlx"
    declare_dlx_and_dlq(channel, dlx_name, dlq_queue)

    channel.queue_declare(
        queue=main_queue,
        durable=True,
        arguments={
            "x-dead-letter-exchange": dlx_name,
            "x-dead-letter-routing-key": dlq_queue,
        },
    )
    return main_queue, dlq_queue


def setup_ttl_queue(channel, queue_name: str, dlq_name: str, ttl_ms: int):
    declare_dlx_and_dlq(channel, f"{queue_name}.dlx", dlq_name)
    channel.queue_declare(
        queue=queue_name,
        durable=True,
        arguments={
            "x-dead-letter-exchange": f"{queue_name}.dlx",
            "x-dead-letter-routing-key": dlq_name,
            "x-message-ttl": ttl_ms,
        },
    )


def setup_max_length_queue(channel, queue_name: str, dlq_name: str, max_length: int):
    declare_dlx_and_dlq(channel, f"{queue_name}.dlx", dlq_name)
    channel.queue_declare(
        queue=queue_name,
        durable=True,
        arguments={
            "x-dead-letter-exchange": f"{queue_name}.dlx",
            "x-dead-letter-routing-key": dlq_name,
            "x-max-length": max_length,
            "x-overflow": "reject-publish",
        },
    )


def setup_retry_queues(channel, base_queue: str, intervals_s=(10, 30, 120, 600)):
    """Retry queues that dead-letter back to base_queue when their TTL expires."""
    for i, interval in enumerate(intervals_s):
        channel.queue_declare(
            queue=f"{base_queue}.retry.{i}",
            durable=True,
            arguments={
                "x-dead-letter-exchange": "",
                "x-dead-letter-routing-key": base_queue,
                "x-message-ttl": interval * 1000,
            },
        )
    channel.queue_declare(queue=f"{base_queue}.dlq", durable=True)


if __name__ == "__main__":
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = conn.channel()

    setup_dlq(ch, "orders", "orders.dlq")
    setup_retry_queues(ch, "orders")

    ch.basic_publish(
        exchange="",
        routing_key="orders",
        body=b'{"id": 1, "action": "process"}',
        properties=pika.BasicProperties(delivery_mode=2, content_type="application/json"),
    )
    print("Declared orders + orders.dlq + retry queues, and published a test message.")
    conn.close()
