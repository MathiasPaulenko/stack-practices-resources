"""RabbitMQ producer that publishes persistent JSON messages to a durable queue."""

import json
import uuid
import time

import pika


def get_connection(host: str = "localhost", port: int = 5672) -> pika.BlockingConnection:
    credentials = pika.PlainCredentials("guest", "guest")
    params = pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=7200,
    )
    return pika.BlockingConnection(params)


def publish_message(queue_name: str, message: dict, host: str = "localhost") -> None:
    connection = get_connection(host)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
            message_id=str(uuid.uuid4()),
            content_type="application/json",
            timestamp=int(time.time()),
        ),
    )
    print(f"Published to {queue_name}: {message['id']}")
    connection.close()


if __name__ == "__main__":
    publish_message("task_queue", {
        "id": "task-001",
        "type": "email",
        "payload": {"to": "user@example.com", "subject": "Welcome"},
    })
