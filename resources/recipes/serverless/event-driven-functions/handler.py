import json
import os
import uuid

import boto3

_processed_ids_table = os.environ.get("IDEMPOTENCY_TABLE")
_dynamo = boto3.resource("dynamodb") if _processed_ids_table else None


def lambda_handler(event, context):
    """SQS-triggered Lambda with idempotency and partial batch response."""
    failures = []
    for record in event["Records"]:
        try:
            body = json.loads(record["body"])
            order_id = body["orderId"]
            event_id = body.get("eventId", record["messageId"])

            if not _mark_processed(event_id):
                # Already processed — at-least-once delivery replay
                continue

            process_order(order_id)
        except Exception:
            failures.append({"itemIdentifier": record["messageId"]})

    # Report only failed items so SQS retries those, not the whole batch
    return {"batchItemFailures": failures}


def _mark_processed(event_id):
    """Return True the first time we see event_id; False on duplicates."""
    if _dynamo is None:
        return True
    try:
        _dynamo.Table(_processed_ids_table).put_item(
            Item={"eventId": event_id},
            ConditionExpression="attribute_not_exists(eventId)",
        )
        return True
    except _dynamo.meta.client.exceptions.ConditionalCheckFailedException:
        return False


def process_order(order_id):
    # Business logic: validate, charge, notify
    print(f"Processing order {order_id}")
