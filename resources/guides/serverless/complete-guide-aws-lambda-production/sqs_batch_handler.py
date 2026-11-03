"""SQS batch handler with partial-failure reporting (batchItemFailures).

Source: https://stackpractices.com/guides/complete-guide-aws-lambda-production/
"""
import json


def lambda_handler(event, context):
    batch_failures = []
    for record in event["Records"]:
        try:
            process_message(json.loads(record["body"]))
        except Exception:
            batch_failures.append(
                {"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": batch_failures}
