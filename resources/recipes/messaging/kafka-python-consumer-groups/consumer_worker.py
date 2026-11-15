"""consumer_worker.py — one member of the `order-processors` consumer group.

Run several instances in different terminals:

    python consumer_worker.py worker-1
    python consumer_worker.py worker-2
    python consumer_worker.py worker-3

Kafka assigns partitions automatically. Watch the rebalance happen live
when a worker joins (start a new one) or leaves (Ctrl+C an old one).
The `on_revoke` callback commits offsets before partitions move, so the
new owner does not replay completed work.
"""
import json
import sys
from confluent_kafka import Consumer, KafkaError


def make_callbacks(worker_id):
    def on_assign(consumer, partitions):
        print(f"[{worker_id}] assigned: {[f'{p.topic}[{p.partition}]' for p in partitions]}")

    def on_revoke(consumer, partitions):
        print(f"[{worker_id}] revoked: {[f'{p.topic}[{p.partition}]' for p in partitions]} — committing")
        consumer.commit(asynchronous=False)

    def on_lost(consumer, partitions):
        print(f"[{worker_id}] lost: {[f'{p.topic}[{p.partition}]' for p in partitions]}")

    return on_assign, on_revoke, on_lost


def process_event(value):
    return value.get('totalCents', 0)


def start_worker(worker_id: str, group_id: str = 'order-processors', topic: str = 'orders'):
    on_assign, on_revoke, on_lost = make_callbacks(worker_id)

    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'partition.assignment.strategy': 'cooperative-sticky',
        'on_assign': on_assign,
        'on_revoke': on_revoke,
        'on_lost': on_lost,
    })

    consumer.subscribe([topic])
    print(f"[{worker_id}] subscribed to '{topic}' in group '{group_id}'")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f"[{worker_id}] error: {msg.error()}")
                continue

            value = json.loads(msg.value().decode('utf-8'))
            process_event(value)
            print(f"[{worker_id}] P={msg.partition()} O={msg.offset()} — {value['id']} (${value['totalCents'] / 100:.2f})")
            consumer.commit(msg)
    except KeyboardInterrupt:
        print(f"\n[{worker_id}] stopping…")
    finally:
        consumer.close()


if __name__ == '__main__':
    worker = sys.argv[1] if len(sys.argv) > 1 else 'worker-1'
    start_worker(worker)
