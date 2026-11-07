"""RabbitMQ correlation ID propagation: publisher + consumer.

The ID travels in BOTH the message headers and the body metadata — some
brokers/middleware strip headers, the body always survives.

Requires: pip install pika ; a local RabbitMQ on localhost.
"""
import json
import uuid

import pika

CORRELATION_ID_HEADER = "X-Correlation-ID"


def publish_order_created(channel, order_data: dict, correlation_id: str | None = None):
    correlation_id = correlation_id or str(uuid.uuid4())
    message = {
        "event": "order.created",
        "data": order_data,
        "metadata": {
            "correlation_id": correlation_id,
            "source": "order-service",
        },
    }
    channel.basic_publish(
        exchange="orders",
        routing_key="order.created",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            headers={CORRELATION_ID_HEADER: correlation_id},
            correlation_id=correlation_id,
        ),
    )
    return correlation_id


def extract_correlation_id(properties, body: dict) -> str:
    """Header first, body metadata as fallback."""
    headers = getattr(properties, "headers", None) or {}
    return (
        headers.get(CORRELATION_ID_HEADER)
        or getattr(properties, "correlation_id", None)
        or body.get("metadata", {}).get("correlation_id")
        or "unknown"
    )


def on_message(channel, method, properties, body_bytes):
    body = json.loads(body_bytes)
    correlation_id = extract_correlation_id(properties, body)
    print(
        json.dumps(
            {
                "level": "info",
                "correlationId": correlation_id,
                "message": f"Processing event: {body.get('event')}",
            }
        )
    )
    channel.basic_ack(method.delivery_tag)


if __name__ == "__main__":
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = conn.channel()
    ch.exchange_declare(exchange="orders", exchange_type="topic")
    cid = publish_order_created(ch, {"order_id": 42})
    print("published with correlation_id:", cid)
    conn.close()
