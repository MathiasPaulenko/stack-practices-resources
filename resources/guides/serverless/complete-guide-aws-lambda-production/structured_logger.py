"""Structured JSON logging for Lambda — every line carries request_id.

Source: https://stackpractices.com/guides/complete-guide-aws-lambda-production/
"""
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def log_event(level, request_id, **fields):
    entry = {"level": level, "request_id": request_id, **fields}
    getattr(logger, level.lower())(json.dumps(entry))


def lambda_handler(event, context):
    request_id = context.aws_request_id
    log_event("INFO", request_id,
              function=context.function_name,
              event_type="request_start",
              user_id=event.get("user_id"),
              path=event.get("path"))
    try:
        result = process_request(event)
        log_event("INFO", request_id,
                  event_type="request_success", duration_ms=150)
        return result
    except Exception as e:
        log_event("ERROR", request_id,
                  event_type="request_error",
                  error=str(e), error_type=type(e).__name__)
        return {"statusCode": 500,
                "body": json.dumps({"error": "Internal error"})}
