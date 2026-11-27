import json


def validate_order_handler(event, context):
    order = event.get('order', {})
    items = order.get('items', [])
    customer = order.get('customer', {})

    if not items:
        raise Exception("OrderValidationError: No items in order")
    if not customer.get('email'):
        raise Exception("OrderValidationError: Customer email required")

    return {
        'orderId': order.get('id'),
        'valid': True,
        'itemCount': len(items),
        'total': sum(item['price'] * item['quantity'] for item in items),
    }


def check_inventory_handler(event, context):
    items = event.get('order', {}).get('items', [])
    all_in_stock = all(check_stock(item) for item in items)
    return {
        'orderId': event['orderId'],
        'inStock': all_in_stock,
        'items': items,
    }


def process_payment_handler(event, context):
    total = event.get('total', 0)
    payment_method = event.get('paymentMethod', {})

    result = charge_payment(payment_method, total)
    if not result['success']:
        raise Exception("PaymentDeclinedError: " + result['message'])

    return {
        'orderId': event['orderId'],
        'paymentId': result['paymentId'],
        'charged': total,
    }
