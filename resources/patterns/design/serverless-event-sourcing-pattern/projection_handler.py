"""Projection Lambda driven by DynamoDB Streams.

On every INSERT into event_store, rebuilds the aggregate state and upserts it
into the order_projection read model. Idempotent by design: the projection
only writes versions newer than the one already stored.
"""

import json
import logging
import time

import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
event_table = dynamodb.Table("event_store")
projection_table = dynamodb.Table("order_projection")


def get_events(aggregate_id: str, from_version: int = 0) -> list[dict]:
    response = event_table.query(
        KeyConditionExpression=Key("aggregateId").eq(aggregate_id)
        & Key("version").gte(from_version),
        ScanIndexForward=True,
    )
    return response.get("Items", [])


def project_order_state(order_id: str) -> None:
    state = {}
    for event in get_events(order_id):
        state.update(json.loads(event["data"]))
        state["version"] = int(event["version"])

    # Idempotency: never overwrite a newer projection with an older replay.
    projection_table.put_item(
        Item={
            "orderId": order_id,
            "customerId": state.get("customerId"),
            "status": state.get("status"),
            "items": state.get("items", []),
            "version": state.get("version", 0),
            "updatedAt": int(time.time() * 1000),
        },
        ConditionExpression="attribute_not_exists(orderId) OR #v < :incoming",
        ExpressionAttributeNames={"#v": "version"},
        ExpressionAttributeValues={":incoming": state.get("version", 0)},
    )


def lambda_handler(event, context):
    for record in event.get("Records", []):
        if record.get("eventName") != "INSERT":
            continue
        new_image = record["dynamodb"]["NewImage"]
        aggregate_id = new_image["aggregateId"]["S"]
        try:
            project_order_state(aggregate_id)
        except Exception:
            # ConditionalCheckFailedException means a newer projection already
            # exists; anything else should surface in logs and be retried.
            logger.exception("projection failed for %s", aggregate_id)
