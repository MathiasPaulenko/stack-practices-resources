"""producer.py — publishes OrderCreated events to the `orders` topic.

Keys are userIds: same key always lands on the same partition, so each
user's events stay ordered. `enable.idempotence` deduplicates retries.
"""
import json
import time
from confluent_kafka import Producer


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered {msg.key().decode()} -> {msg.topic()}[{msg.partition()}] @ offset {msg.offset()}")


def main():
    producer = Producer({
        'bootstrap.servers': 'localhost:9092',
        'acks': 'all',
        'enable.idempotence': True,
    })

    user_ids = ['user-1', 'user-2', 'user-3']
    for i in range(30):
        user_id = user_ids[i % len(user_ids)]
        order = {
            'id': f'order-{int(time.time())}-{i}',
            'userId': user_id,
            'totalCents': 1000 + i * 250,
        }
        producer.produce(
            topic='orders',
            key=user_id.encode('utf-8'),
            value=json.dumps(order).encode('utf-8'),
            callback=delivery_report,
        )
        producer.poll(0)

    producer.flush()
    print("Done — 30 orders sent to 'orders'.")


if __name__ == '__main__':
    main()
