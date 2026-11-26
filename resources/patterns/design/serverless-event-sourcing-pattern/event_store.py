"""Event store on DynamoDB with optimistic concurrency.

Appends immutable events per aggregate and rebuilds state by replaying the
event log. Optimistic concurrency is enforced by a conditional write on the
full key (aggregateId + version): two writers that read the same
expected_version both compute expected_version + 1, and the second put fails
with ConditionalCheckFailedException.

Requires: boto3, a DynamoDB table keyed on (aggregateId S, version N).
"""

import json
import logging
import time
import uuid

import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb")
event_table = dynamodb.Table("event_store")


class EventStore:
    def __init__(self, table):
        self.table = table

    def append(
        self,
        aggregate_id: str,
        event_type: str,
        data: dict,
        expected_version: int | None = None,
    ) -> dict:
        event = {
            "aggregateId": aggregate_id,
            "eventId": str(uuid.uuid4()),
            "eventType": event_type,
            "data": json.dumps(data),
            "timestamp": int(time.time() * 1000),
            "version": self._get_next_version(aggregate_id),
        }

        if expected_version is not None and event["version"] != expected_version + 1:
            raise ValueError(
                f"Stale write: expected version {expected_version}, "
                f"store is at {event['version'] - 1}"
            )

        self.table.put_item(
            Item=event,
            ConditionExpression="attribute_not_exists(aggregateId) AND attribute_not_exists(#v)",
            ExpressionAttributeNames={"#v": "version"},
        )
        logger.info("appended %s v%s to %s", event_type, event["version"], aggregate_id)
        return event

    def get_events(self, aggregate_id: str, from_version: int = 0) -> list[dict]:
        response = self.table.query(
            KeyConditionExpression=Key("aggregateId").eq(aggregate_id)
            & Key("version").gte(from_version),
            ScanIndexForward=True,
        )
        return response.get("Items", [])

    def _get_next_version(self, aggregate_id: str) -> int:
        response = self.table.query(
            KeyConditionExpression=Key("aggregateId").eq(aggregate_id),
            ScanIndexForward=False,
            Limit=1,
        )
        items = response.get("Items", [])
        return (int(items[0]["version"]) + 1) if items else 1


event_store = EventStore(event_table)


def create_order(order_id: str, customer_id: str, items: list) -> None:
    event_store.append(order_id, "OrderCreated", {
        "customerId": customer_id,
        "items": items,
        "status": "PENDING",
    })


def confirm_order(order_id: str) -> None:
    events = event_store.get_events(order_id)
    current_version = max(int(e["version"]) for e in events)
    event_store.append(order_id, "OrderConfirmed", {
        "status": "CONFIRMED",
    }, expected_version=current_version)


def get_order_state(order_id: str) -> dict:
    state = {}
    for event in event_store.get_events(order_id):
        state.update(json.loads(event["data"]))
        state["version"] = int(event["version"])
    return state
