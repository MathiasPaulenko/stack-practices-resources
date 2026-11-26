"""Scheduled queue draining: an EventBridge rule invokes this handler every
few minutes with the queue URL in the event payload."""

import json
import boto3


def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    queue_url = event['queueUrl']

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5,
        )

        messages = response.get('Messages', [])
        if not messages:
            break

        for msg in messages:
            process_message(json.loads(msg['Body']))
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=msg['ReceiptHandle'],
            )


def process_message(body: dict):
    order_id = body.get('orderId')
    if not order_id:
        raise ValueError("Missing orderId")
    # Business logic here
