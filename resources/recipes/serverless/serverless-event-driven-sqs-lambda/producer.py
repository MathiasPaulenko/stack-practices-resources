"""SQS producer: single sends, batch sends and FIFO ordered sends."""

import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
FIFO_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue.fifo'


def send_order_message(order: dict):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(order),
        MessageAttributes={
            'OrderType': {
                'DataType': 'String',
                'StringValue': order.get('type', 'standard'),
            },
        },
    )
    return response['MessageId']


def send_batch_orders(orders: list):
    entries = [
        {
            'Id': str(i),
            'MessageBody': json.dumps(order),
            'MessageAttributes': {
                'OrderType': {
                    'DataType': 'String',
                    'StringValue': order.get('type', 'standard'),
                },
            },
        }
        for i, order in enumerate(orders)
    ]

    # Send in batches of 10 (SQS limit)
    for i in range(0, len(entries), 10):
        batch = entries[i:i+10]
        response = sqs.send_message_batch(QueueUrl=QUEUE_URL, Entries=batch)
        if response.get('Failed'):
            for failure in response['Failed']:
                logger.error(f"Failed to send message {failure['Id']}: {failure['Message']}")


def send_ordered_message(order: dict, group_id: str):
    # FIFO: messages in the same group are processed in order
    response = sqs.send_message(
        QueueUrl=FIFO_QUEUE_URL,
        MessageBody=json.dumps(order),
        MessageGroupId=group_id,
        MessageDeduplicationId=f"order-{order['id']}",  # Idempotency
    )
    return response['MessageId']
