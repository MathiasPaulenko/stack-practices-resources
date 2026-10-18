"""SQS-triggered Lambda: extracts image metadata into DynamoDB.

Pipeline step 3 of the guide's worked example:
  SQS batch -> metadata Lambda -> DynamoDB ImageMetadata table

Returns batchItemFailures so only failed messages are retried —
a generic error would make SQS redeliver the whole batch.

Environment variables:
    TABLE_NAME: DynamoDB table name (PK imageId, SK version)
"""

import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    failures = []
    for record in event["Records"]:
        try:
            body = json.loads(record["body"])
            for version in ("thumbnail", "medium", "large"):
                table.put_item(
                    Item={
                        "imageId": body["imageId"],
                        "version": version,
                        "originalKey": body["originalKey"],
                        "resizedKey": body[f"{version}Key"],
                    }
                )
        except Exception:
            # Report only this message as failed; the rest are deleted from the queue
            failures.append({"itemIdentifier": record["messageId"]})

    return {"batchItemFailures": failures}
