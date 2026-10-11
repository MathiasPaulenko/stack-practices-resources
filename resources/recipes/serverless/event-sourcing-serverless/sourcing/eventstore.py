"""Append-only event store on DynamoDB (boto3 variant of eventstore.ts).

Key layout: pk = ORDER#<aggregateId>, sk = EVENT#<zero-padded version>.
The per-event ConditionExpression on the transaction keeps optimistic
concurrency — a conflicting append fails instead of silently overwriting.
"""

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeSerializer

serializer = TypeSerializer()


class OrderEventStore:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.client = boto3.client("dynamodb")
        self.table = boto3.resource("dynamodb").Table(table_name)

    def append_events(self, aggregate_id: str, events: list[dict]) -> None:
        current = self.current_version(aggregate_id)
        items = []
        for i, event in enumerate(events):
            version = current + i + 1
            item = {
                "pk": f"ORDER#{aggregate_id}",
                "sk": f"EVENT#{version:010d}",
                "eventId": event["event_id"],
                "eventType": event["event_type"],
                "payload": event["payload"],
                "timestamp": event.get("timestamp"),
                "version": version,
            }
            items.append(
                {
                    "Put": {
                        "TableName": self.table_name,
                        "Item": {k: serializer.serialize(v) for k, v in item.items()},
                        "ConditionExpression": "attribute_not_exists(pk)",
                    }
                }
            )
        self.client.transact_write_items(TransactItems=items)

    def get_events(self, aggregate_id: str) -> list[dict]:
        resp = self.table.query(
            KeyConditionExpression=(
                Key("pk").eq(f"ORDER#{aggregate_id}") & Key("sk").begins_with("EVENT#")
            ),
            ScanIndexForward=True,
        )
        return resp.get("Items", [])

    def current_version(self, aggregate_id: str) -> int:
        events = self.get_events(aggregate_id)
        return events[-1]["version"] if events else 0
