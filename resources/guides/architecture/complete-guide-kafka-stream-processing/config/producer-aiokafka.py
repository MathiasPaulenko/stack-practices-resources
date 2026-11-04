"""aiokafka producer from the guide — acks=all + idempotence."""
from aiokafka import AIOKafkaProducer
import json, asyncio

async def produce_events():
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        acks="all",
        enable_idempotence=True,
    )
    await producer.start()
    try:
        for i in range(100):
            await producer.send_and_wait("orders", key=f"order-{i}",
                value={"order_id": i, "amount": 99.99 * i, "status": "created"})
    finally:
        await producer.stop()

asyncio.run(produce_events())
