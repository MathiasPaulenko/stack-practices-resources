import json
import os
import redis
from kafka import KafkaConsumer

r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

consumer = KafkaConsumer(
    os.getenv('KAFKA_TOPIC', 'orders'),
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(','),
    group_id=os.getenv('KAFKA_GROUP_ID', 'payment-workers'),
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


def charge_customer(payload):
    # Replace with your real payment call.
    return {'status': 'charged', 'order_id': payload['orderId']}


for message in consumer:
    payload = message.value
    key = f"idempotency:{payload.get('idempotencyKey', payload['orderId'])}"

    if r.set(key, 'processing', nx=True, ex=86400):
        try:
            result = charge_customer(payload)
            r.set(key, json.dumps(result), ex=86400)
            consumer.commit_sync()
            print(f"Processed: {result}")
        except Exception:
            r.delete(key)
            raise
    else:
        print(f"Skipping duplicate: {key}")
        consumer.commit_sync()
