import boto3
import json
import os

sqs = boto3.client('sqs')
QUEUE_URL = os.environ["QUEUE_URL"]


def handler(event, context):
    failed_records = []

    for record in event["Records"]:
        try:
            message = json.loads(record["body"])
            process_with_rate_limit(message)
        except Exception:
            failed_records.append({"itemIdentifier": record["messageId"]})

    return {"batchItemFailures": failed_records}


def process_with_rate_limit(message: dict):
    if not check_downstream_capacity():
        raise Exception("Downstream capacity exceeded")
    api_client.post("/process", json=message, timeout=10)


def check_downstream_capacity() -> bool:
    response = api_client.get("/health")
    return response.status_code == 200 and response.json()["capacity"] > 0
