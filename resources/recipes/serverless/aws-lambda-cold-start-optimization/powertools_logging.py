from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event, context):
    logger.info("Processing request", extra={"path": event["path"]})
    return {"statusCode": 200, "body": json.dumps({"ok": True})}
