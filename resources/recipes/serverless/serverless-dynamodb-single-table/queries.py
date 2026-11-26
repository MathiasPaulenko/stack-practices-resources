"""Query implementations for the eight access patterns."""

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('AppTable')


# AP1: Get user by ID
def get_user(user_id: str) -> dict:
    response = table.get_item(
        Key={'PK': f'USER#{user_id}', 'SK': 'PROFILE'}
    )
    return response.get('Item')


# AP2: Get all orders for a user
def get_user_orders(user_id: str) -> list:
    response = table.query(
        KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
        ExpressionAttributeValues={
            ':pk': f'USER#{user_id}',
            ':sk': 'ORDER#',
        },
    )
    return response.get('Items', [])


# AP3/AP4: Get order header + items in one query
def get_order_with_items(order_id: str) -> dict:
    response = table.query(
        KeyConditionExpression='PK = :pk',
        ExpressionAttributeValues={':pk': f'ORDER#{order_id}'},
    )
    items = response.get('Items', [])
    order = next((i for i in items if i.get('entityType') == 'Order'), None)
    order_items = [i for i in items if i.get('entityType') == 'OrderItem']
    return {'order': order, 'items': order_items}


# AP3 (fast path): Get just the order header
def get_order(order_id: str) -> dict:
    response = table.get_item(
        Key={'PK': f'ORDER#{order_id}', 'SK': 'DETAILS'}
    )
    return response.get('Item')


# AP5: Get orders by status (using GSI1)
def get_orders_by_status(status: str) -> list:
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :pk',
        ExpressionAttributeValues={':pk': f'ORDERSTATUS#{status}'},
    )
    return response.get('Items', [])


# AP6: Get orders in a date range (using GSI1)
def get_orders_by_date_range(start: str, end: str) -> list:
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :pk AND GSI1SK BETWEEN :start AND :end',
        ExpressionAttributeValues={
            ':pk': 'ORDERBYDATE',
            ':start': f'DATE#{start}',
            ':end': f'DATE#{end}',
        },
    )
    return response.get('Items', [])


# AP7: Get product by ID
def get_product(product_id: str) -> dict:
    response = table.get_item(
        Key={'PK': f'PRODUCT#{product_id}', 'SK': 'DETAILS'}
    )
    return response.get('Item')


# AP8: Get products by category (using GSI1)
def get_products_by_category(category: str) -> list:
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression='GSI1PK = :pk',
        ExpressionAttributeValues={':pk': f'CATEGORY#{category}'},
    )
    return response.get('Items', [])
