"""Lambda step handlers for the order-processing state machine.

Each handler receives the previous step's output (unwrapped by
output_path="$.Payload") and returns a dict the orchestrator feeds to the
next state. Keep every step idempotent — the orchestrator may retry it.
"""


def validate(event, context):
    """Reject malformed orders before charging anything."""
    order_id = event.get("orderId")
    customer_id = event.get("customerId")
    items = event.get("items", [])
    total = event.get("total", 0)

    if not order_id or not customer_id or not items:
        return {
            "statusCode": 400,
            "error": "INVALID_ORDER",
            "message": "Missing required fields",
        }

    if total <= 0:
        return {
            "statusCode": 400,
            "error": "INVALID_TOTAL",
            "message": "Total must be positive",
        }

    return {
        "statusCode": 200,
        "orderId": order_id,
        "customerId": customer_id,
        "items": items,
        "total": total,
        "validated": True,
    }


def process_payment(event, context):
    """Charge the customer. Idempotent on orderId."""
    # Replace with your payment provider call, keyed on event["orderId"].
    return {
        "orderId": event["orderId"],
        "paymentStatus": "SUCCESS",
        "transactionId": f"txn-{event['orderId']}",
    }


def reserve_inventory(event, context):
    """Reserve stock for the validated order."""
    return {
        "orderId": event["orderId"],
        "reserved": True,
    }


def send_notification(event, context):
    """Tell the customer the order is confirmed."""
    return {
        "orderId": event["orderId"],
        "notified": True,
    }


def refund_payment(event, context):
    """Compensation step: undo the charge."""
    return {
        "orderId": event["orderId"],
        "refunded": True,
    }
