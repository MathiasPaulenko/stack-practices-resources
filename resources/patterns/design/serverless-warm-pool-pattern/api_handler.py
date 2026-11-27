"""API Lambda handler with warmup detection (Python).

Checks for the `isWarmup` flag first and returns immediately so ping
invocations keep the environment alive without triggering business logic
or side effects.
"""
import json


def handler(event, context):
    # Detect warmup ping and return immediately
    if isinstance(event, dict) and event.get("isWarmup"):
        return {"status": "warm", "instanceId": event.get("instanceId")}

    # Real request processing
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    # Heavy initialization happens here (loaded once, reused for warm invocations)
    # Dependencies, DB connections, etc.

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Request processed", "path": path}),
    }
