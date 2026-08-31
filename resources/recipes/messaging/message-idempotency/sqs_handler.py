import json
import os
import boto3
from botocore.exceptions import ClientError

sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
table = dynamodb.Table(os.getenv('DEDUP_TABLE_NAME', 'processed-messages'))

queue_url = os.getenv('SQS_QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/123456789012/orders.fifo')


def handle_message(message):
    body = json.loads(message['Body'])
    message_id = message['MessageId']
    idempotency_key = body.get('idempotencyKey', body['orderId'])

    try:
        table.put_item(
            Item={
                'message_id': idempotency_key,
                'sqs_message_id': message_id,
                'result': json.dumps({'status': 'charged', 'order_id': body['orderId']})
            },
            ConditionExpression='attribute_not_exists(message_id)'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(f'Duplicate message skipped: {idempotency_key}')
            return
        raise

    # Replace with your real side effect.
    print(f'Processed order: {body["orderId"]}')


if __name__ == '__main__':
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    for message in response.get('Messages', []):
        handle_message(message)
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
