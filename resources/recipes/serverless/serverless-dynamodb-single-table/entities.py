"""Entity writers: User, Order (two partitions), OrderItem and Product."""

import boto3
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('AppTable')


def put_user(user_id: str, name: str, email: str):
    table.put_item(Item={
        'PK': f'USER#{user_id}',
        'SK': 'PROFILE',
        'entityType': 'User',
        'userId': user_id,
        'name': name,
        'email': email,
        'createdAt': datetime.now(timezone.utc).isoformat(),
    })


def put_order(order_id: str, user_id: str, status: str, total: float):
    # Header under ORDER#<id>: direct get by ID, colocated with items.
    table.put_item(Item={
        'PK': f'ORDER#{order_id}',
        'SK': 'DETAILS',
        'entityType': 'Order',
        'orderId': order_id,
        'userId': user_id,
        'status': status,
        'total': total,
        'createdAt': datetime.now(timezone.utc).isoformat(),
    })
    # Index copy under USER#<id>: "all orders for a user" + GSI1 by status.
    table.put_item(Item={
        'PK': f'USER#{user_id}',
        'SK': f'ORDER#{order_id}',
        'GSI1PK': f'ORDERSTATUS#{status}',
        'GSI1SK': f'ORDER#{order_id}',
        'entityType': 'OrderIndex',
        'orderId': order_id,
        'status': status,
        'total': total,
    })


def put_order_item(order_id: str, item_id: str, product_id: str, quantity: int, price: float):
    table.put_item(Item={
        'PK': f'ORDER#{order_id}',
        'SK': f'ITEM#{item_id}',
        'entityType': 'OrderItem',
        'itemId': item_id,
        'orderId': order_id,
        'productId': product_id,
        'quantity': quantity,
        'price': price,
    })


def put_product(product_id: str, category: str, name: str, price: float):
    table.put_item(Item={
        'PK': f'PRODUCT#{product_id}',
        'SK': 'DETAILS',
        'GSI1PK': f'CATEGORY#{category}',
        'GSI1SK': f'PRODUCT#{product_id}',
        'entityType': 'Product',
        'productId': product_id,
        'category': category,
        'name': name,
        'price': price,
    })
