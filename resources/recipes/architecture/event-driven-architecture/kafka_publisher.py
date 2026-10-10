"""Publish an OrderPlaced event to Kafka with acks=all."""
import json

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=3,
)


def place_order(order_data):
    """Save the order, then publish the domain event."""
    order = save_order(order_data)

    event = {
        "type": "OrderPlaced",
        "aggregate_id": order.id,
        "payload": {
            "customer_id": order.customer_id,
            "items": [item.to_dict() for item in order.items],
            "total": order.total(),
        },
        "occurred_at": order.created_at.isoformat(),
    }

    producer.send("orders", key=order.id.encode(), value=event)
    producer.flush()
    return order


def save_order(order_data):
    raise NotImplementedError("Provide your own persistence layer")
