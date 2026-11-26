"""Lambda warmer — invoke functions periodically to keep containers warm."""
import boto3
import json
import logging

lambda_client = boto3.client('lambda')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

WARM_FUNCTIONS = [
    {"name": "order-service-prod-processOrder", "concurrency": 5},
    {"name": "order-service-prod-sendEmail", "concurrency": 3},
]


def handler(event, context):
    for func in WARM_FUNCTIONS:
        for _ in range(func["concurrency"]):
            try:
                lambda_client.invoke(
                    FunctionName=func["name"],
                    InvocationType='Event',
                    Payload=json.dumps({"warmer": True, "source": "warmer"}),
                )
            except Exception as e:
                logger.error(f"Failed to warm {func['name']}: {e}")

    logger.info(f"Warmed {len(WARM_FUNCTIONS)} functions")
