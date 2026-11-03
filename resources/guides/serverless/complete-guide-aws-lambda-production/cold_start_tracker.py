"""Cold/warm start instrumentation: logs init time separately from handler time.

Source: https://stackpractices.com/guides/complete-guide-aws-lambda-production/
"""
import json
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

init_start = time.time()

# Heavy init at module scope: paid once per execution environment
import boto3  # noqa: E402

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("users")

init_ms = round((time.time() - init_start) * 1000)
logger.info(json.dumps({"event": "cold_start_init", "duration_ms": init_ms}))


def lambda_handler(event, context):
    start = time.time()
    user_id = event["pathParameters"]["userId"]
    response = table.get_item(Key={"id": user_id})
    logger.info(json.dumps({
        "event": "invocation_complete",
        "duration_ms": round((time.time() - start) * 1000),
        "request_id": context.aws_request_id,
    }))
    return {"statusCode": 200,
            "body": json.dumps(response.get("Item", {}), default=str)}
