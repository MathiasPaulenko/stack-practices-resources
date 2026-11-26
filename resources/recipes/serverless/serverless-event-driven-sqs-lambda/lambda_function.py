"""Lambda handler consuming SQS batches with partial batch responses.

Requires FunctionResponseTypes: ReportBatchItemFailures on the SQS event
source so only failed messages are returned to the queue.
"""

import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')


def lambda_handler(event, context):
    records = event.get('Records', [])
    logger.info(f"Processing {len(records)} messages")

    batch_item_failures = []

    for record in records:
        message_id = record['messageId']
        receipt_handle = record['receiptHandle']

        try:
            body = json.loads(record['body'])
            process_message(body)
            logger.info(f"Successfully processed message {message_id}")

        except Exception as e:
            logger.error(f"Failed to process message {message_id}: {e}")
            batch_item_failures.append({
                'itemIdentifier': message_id,
            })

    # Partial batch response — only failed messages go back to SQS
    return {
        'batchItemFailures': batch_item_failures,
    }


def process_message(body: dict):
    order_id = body.get('orderId')
    if not order_id:
        raise ValueError("Missing orderId")

    # Business logic here
    logger.info(f"Processing order {order_id}")
    # e.g., save to DynamoDB, call external API, generate report
