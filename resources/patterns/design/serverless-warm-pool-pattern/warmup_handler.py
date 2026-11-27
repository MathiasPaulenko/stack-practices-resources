"""Warmup Lambda handler (Python).

Sends WARM_COUNT concurrent async invocations to TARGET_FUNCTION so Lambda
keeps that many execution environments warm. Each ping carries an
`isWarmup` flag so the target short-circuits before doing real work.
"""
import concurrent.futures
import json
import os

import boto3

lambda_client = boto3.client('lambda')
TARGET_FUNCTION = os.environ['TARGET_FUNCTION']
WARM_COUNT = int(os.environ.get('WARM_COUNT', '5'))


def handler(event, context):
    def send_ping(instance_id: int) -> dict:
        response = lambda_client.invoke(
            FunctionName=TARGET_FUNCTION,
            InvocationType='Event',  # Async invocation
            Payload=json.dumps({
                "source": "warmup.ping",
                "instanceId": instance_id,
                "isWarmup": True,
            }),
        )
        return {"instanceId": instance_id, "status": response['StatusCode']}

    with concurrent.futures.ThreadPoolExecutor(max_workers=WARM_COUNT) as executor:
        results = list(executor.map(send_ping, range(WARM_COUNT)))

    return {
        "warmedInstances": len(results),
        "targetFunction": TARGET_FUNCTION,
    }
