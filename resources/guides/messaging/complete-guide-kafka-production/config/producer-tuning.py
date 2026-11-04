"""Producer tuning config from the guide — batching, compression, durability."""
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092","localhost:9094","localhost:9096"],
    batch_size=65536,          # 64KB batches
    linger_ms=10,
    compression_type="lz4",
    buffer_memory=67108864,
    acks="all",
    retries=3,
    max_in_flight_requests_per_connection=5,
    key_serializer=str.encode,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def send_order_event(order_id, event_type, data):
    producer.send("orders", key=str(order_id), value={
        "order_id": order_id, "event_type": event_type, "data": data,
    })
    producer.flush()
