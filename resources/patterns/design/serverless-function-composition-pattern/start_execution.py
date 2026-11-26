"""Start an order workflow execution and poll its status.

Execution names must be unique per state machine for 90 days — include the
order ID plus a timestamp or UUID.
"""

import json
import os
import time

import boto3

sfn = boto3.client("stepfunctions")
STATE_MACHINE_ARN = os.environ.get(
    "ORDER_STATE_MACHINE_ARN",
    "arn:aws:states:us-east-1:123456789012:stateMachine:OrderProcessingStateMachine",
)


def start_order_workflow(order: dict) -> str:
    """Start an execution and return its ARN."""
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps(order),
        name=f"order-{order['orderId']}-{int(time.time())}",
    )
    return response["executionArn"]


def get_workflow_status(execution_arn: str) -> dict:
    """Return status, parsed output (if finished), and error (if failed)."""
    response = sfn.describe_execution(executionArn=execution_arn)
    return {
        "status": response["status"],
        "output": json.loads(response["output"]) if response.get("output") else None,
        "error": response.get("error"),
        "cause": response.get("cause"),
    }


if __name__ == "__main__":
    arn = start_order_workflow(
        {
            "orderId": "order-123",
            "customerId": "customer-42",
            "items": [{"productId": "A1", "quantity": 2, "price": 74.99}],
            "total": 149.98,
        }
    )
    print(f"Started {arn}")
    print(get_workflow_status(arn))
