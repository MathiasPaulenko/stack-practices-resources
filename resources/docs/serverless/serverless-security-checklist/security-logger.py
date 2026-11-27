import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_security_event(event_type: str, user_id: str, detail: str):
    logger.info(json.dumps({
        "security_event": True,
        "event_type": event_type,
        "user_id": user_id,
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat(),
    }))

def handler(event, context):
    user = authenticate(event)
    if not user:
        log_security_event("auth_failure", "unknown", "Invalid token")
        return {"statusCode": 401, "body": json.dumps({"error": "Unauthorized"})}

    if not authorize(user, "read:orders"):
        log_security_event("authz_failure", user["id"], "Insufficient permissions")
        return {"statusCode": 403, "body": json.dumps({"error": "Forbidden"})}

    return process_order(event, user)
