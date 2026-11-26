"""Consume fanned-out messages from SQS in a Lambda handler.

With a raw-message SNS -> SQS subscription each record body is the published
JSON directly (no SNS envelope). Idempotency matters: SNS + SQS is
at-least-once delivery, so the same message can arrive twice.

Returns batchItemFailures so only failed records are retried instead of the
whole batch.
"""

import json


def handler(event, context):
    failed = []

    for record in event["Records"]:
        try:
            process_message(json.loads(record["body"]))
        except Exception as exc:  # noqa: BLE001 - report and continue the batch
            print(f"Failed {record['messageId']}: {exc}")
            failed.append({"itemIdentifier": record["messageId"]})

    return {"batchItemFailures": failed}


def process_message(message: dict) -> None:
    """Handle one fanned-out event. Replace with your domain logic."""
    event_type = message.get("eventType")
    order_id = message.get("orderId")

    if event_type == "OrderPlaced":
        # e.g. update inventory, send confirmation email, write analytics row
        print(f"Processing OrderPlaced for {order_id}")
    else:
        print(f"Ignoring event type {event_type}")
