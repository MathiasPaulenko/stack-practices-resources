"""Inspect and replay messages sitting in a dead-letter queue.

Usage:
    python dlq_tools.py inspect orders.dlq
    python dlq_tools.py replay orders.dlq orders
    python dlq_tools.py reason orders.dlq
"""

import json
import sys

import pika


def inspect_dlq(channel, dlq_name: str, limit: int = 10):
    messages = []
    for _ in range(limit):
        method, properties, body = channel.basic_get(queue=dlq_name, auto_ack=False)
        if method is None:
            break
        messages.append(
            {
                "body": json.loads(body),
                "headers": properties.headers or {},
                "message_id": properties.message_id,
            }
        )
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    return messages


def get_dead_letter_reason(properties) -> dict:
    x_death = (properties.headers or {}).get("x-death", [])
    if not x_death:
        return {}
    first = x_death[0]
    return {
        "queue": first.get("queue"),
        "reason": first.get("reason"),  # 'rejected', 'expired', 'maxlen'
        "exchange": first.get("exchange"),
        "count": first.get("count"),
        "time": str(first.get("time")),
    }


def replay_dlq_messages(channel, dlq_name: str, target_queue: str) -> int:
    replayed = 0
    while True:
        method, properties, body = channel.basic_get(queue=dlq_name, auto_ack=False)
        if method is None:
            break
        clean_props = pika.BasicProperties(
            delivery_mode=2,
            content_type=properties.content_type,
            message_id=properties.message_id,
        )
        channel.basic_publish(exchange="", routing_key=target_queue, body=body, properties=clean_props)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        replayed += 1
    return replayed


if __name__ == "__main__":
    action, dlq = sys.argv[1], sys.argv[2]
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    ch = conn.channel()

    if action == "inspect":
        for m in inspect_dlq(ch, dlq):
            print(m)
    elif action == "replay":
        print(f"Replayed {replay_dlq_messages(ch, dlq, sys.argv[3])} messages")
    elif action == "reason":
        method, props, _ = ch.basic_get(queue=dlq, auto_ack=False)
        if method:
            print(get_dead_letter_reason(props))
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    conn.close()
