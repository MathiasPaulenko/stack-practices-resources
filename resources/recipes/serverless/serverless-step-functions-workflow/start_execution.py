import boto3
import json
import uuid

stepfunctions = boto3.client('stepfunctions')
STATE_MACHINE_ARN = 'arn:aws:states:us-east-1:123456789012:stateMachine:OrderWorkflow'


def start_order_workflow(order: dict) -> str:
    execution_name = f"order-{order['id']}-{uuid.uuid4().hex[:8]}"
    response = stepfunctions.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=execution_name,
        input=json.dumps({
            'order': order,
            'paymentMethod': order.get('paymentMethod'),
        }),
    )
    return response['executionArn']


def check_execution_status(execution_arn: str) -> dict:
    response = stepfunctions.describe_execution(executionArn=execution_arn)
    return {
        'status': response['status'],
        'output': json.loads(response.get('output', '{}')),
        'startDate': response.get('startDate'),
        'stopDate': response.get('stopDate'),
    }
