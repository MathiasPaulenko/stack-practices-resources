"""Publish order events to an SNS topic for fanout to subscribers.

Each subscriber (SQS queue, Lambda, HTTP endpoint) gets its own copy of the
message. The producer stays decoupled: it never knows how many consumers
exist or what they do with the event.
"""

import json
import os
import time

import boto3

sns = boto3.client("sns")
TOPIC_ARN = os.environ.get("TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:order-events")


def publish_order_event(order_id: str, customer_id: str, total: float) -> str:
    """Publish an OrderPlaced event and return the SNS MessageId."""
    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="OrderPlaced",
        Message=json.dumps(
            {
                "eventType": "OrderPlaced",
                "orderId": order_id,
                "customerId": customer_id,
                "total": total,
                "timestamp": time.time(),
            }
        ),
        # Attributes let subscribers filter without parsing the body.
        MessageAttributes={
            "eventType": {"DataType": "String", "StringValue": "OrderPlaced"}
        },
    )
    return response["MessageId"]


if __name__ == "__main__":
    msg_id = publish_order_event("order-123", "customer-42", 149.99)
    print(f"Published to {TOPIC_ARN}: {msg_id}")
