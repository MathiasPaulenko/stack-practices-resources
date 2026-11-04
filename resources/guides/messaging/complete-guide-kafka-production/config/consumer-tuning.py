"""Consumer tuning config from the guide — fetch sizing, manual commit."""
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers=["localhost:9092","localhost:9094","localhost:9096"],
    group_id="order-processor",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    fetch_min_bytes=1024,
    fetch_max_wait_ms=500,
    max_poll_records=500,
    max_poll_interval_ms=300000,
    key_deserializer=lambda k: k.decode("utf-8") if k else None,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

for message in consumer:
    try:
        print("processing", message.value)
        consumer.commit()
    except Exception as e:
        print("failed:", e)
