"""Transactional writes: create an order atomically and update status
on both copies (header + user index entry)."""

import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('AppTable')


def create_order_with_items(user_id: str, order_id: str, items: list, total: float):
    transact_items = [
        # Order header under the order partition
        {
            'Put': {
                'TableName': 'AppTable',
                'Item': {
                    'PK': f'ORDER#{order_id}',
                    'SK': 'DETAILS',
                    'entityType': 'Order',
                    'orderId': order_id,
                    'userId': user_id,
                    'status': 'PENDING',
                    'total': total,
                    'createdAt': datetime.now(timezone.utc).isoformat(),
                },
            }
        },
        # Index copy under the user partition
        {
            'Put': {
                'TableName': 'AppTable',
                'Item': {
                    'PK': f'USER#{user_id}',
                    'SK': f'ORDER#{order_id}',
                    'GSI1PK': 'ORDERSTATUS#PENDING',
                    'GSI1SK': f'ORDER#{order_id}',
                    'entityType': 'OrderIndex',
                    'orderId': order_id,
                    'status': 'PENDING',
                    'total': total,
                },
            }
        },
    ]

    for item in items:
        transact_items.append({
            'Put': {
                'TableName': 'AppTable',
                'Item': {
                    'PK': f'ORDER#{order_id}',
                    'SK': f'ITEM#{item["id"]}',
                    'entityType': 'OrderItem',
                    'itemId': item['id'],
                    'orderId': order_id,
                    'productId': item['product_id'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                },
            }
        })

    dynamodb.meta.client.transact_write_items(TransactItems=transact_items)


def update_order_status(order_id: str, user_id: str, new_status: str):
    # Status lives on two copies: the header (ORDER# partition) and the
    # index entry (USER# partition, which also feeds GSI1). Update both.
    dynamodb.meta.client.transact_write_items(TransactItems=[
        {
            'Update': {
                'TableName': 'AppTable',
                'Key': {'PK': f'ORDER#{order_id}', 'SK': 'DETAILS'},
                'UpdateExpression': 'SET #status = :status',
                'ConditionExpression': 'attribute_exists(PK)',
                'ExpressionAttributeNames': {'#status': 'status'},
                'ExpressionAttributeValues': {':status': new_status},
            }
        },
        {
            'Update': {
                'TableName': 'AppTable',
                'Key': {'PK': f'USER#{user_id}', 'SK': f'ORDER#{order_id}'},
                'UpdateExpression': 'SET #status = :status, GSI1PK = :gsi_pk',
                'ConditionExpression': 'attribute_exists(PK) AND attribute_exists(SK)',
                'ExpressionAttributeNames': {'#status': 'status'},
                'ExpressionAttributeValues': {
                    ':status': new_status,
                    ':gsi_pk': f'ORDERSTATUS#{new_status}',
                },
            }
        },
    ])
