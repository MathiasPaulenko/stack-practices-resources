"""Cursor pagination with ExclusiveStartKey / LastEvaluatedKey."""

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('AppTable')


def get_user_orders_page(user_id: str, page_size: int = 20, last_key: dict = None):
    kwargs = {
        'KeyConditionExpression': 'PK = :pk AND begins_with(SK, :sk)',
        'ExpressionAttributeValues': {
            ':pk': f'USER#{user_id}',
            ':sk': 'ORDER#',
        },
        'Limit': page_size,
    }
    if last_key:
        kwargs['ExclusiveStartKey'] = last_key

    response = table.query(**kwargs)
    return {
        'items': response.get('Items', []),
        'next_key': response.get('LastEvaluatedKey'),  # None when done
    }
