"""Asynchronous message producer for RabbitMQ (pika).

Companion to https://stackpractices.com/recipes/microservices-communication/
Requires: pika (see requirements.txt) and RabbitMQ at amqp://rabbitmq:5672
(or a broker reachable at the host in RABBITMQ_HOST, default "rabbitmq").
"""

import json
import os

import pika


def publish_order_created(order: dict, host: str = "rabbitmq"):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host))
    ch = conn.channel()
    ch.queue_declare(queue="orders.created", durable=True)
    ch.basic_publish(
        exchange="",
        routing_key="orders.created",
        body=json.dumps(order).encode(),
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    conn.close()


if __name__ == "__main__":
    publish_order_created(
        {"id": "ord_123", "items": [{"sku": "book", "qty": 1}]},
        host=os.environ.get("RABBITMQ_HOST", "rabbitmq"),
    )
    print("Published orders.created")
