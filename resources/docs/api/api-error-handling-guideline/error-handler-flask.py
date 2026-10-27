import uuid
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify, g

logger = logging.getLogger(__name__)

class ApiError(Exception):
    def __init__(self, code, message, status_code, details=None, retryable=False):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        self.retryable = retryable
        super().__init__(message)

@app.errorhandler(ApiError)
def handle_api_error(e):
    error_id = f"err_{uuid.uuid4().hex[:12]}"
    payload = {
        "error": {
            "id": error_id,
            "code": e.code,
            "message": e.message,
            "details": e.details,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "path": request.path,
            "retryable": e.retryable,
            "documentation_url": f"https://docs.example.com/errors/{e.code}",
        }
    }

    if e.status_code >= 500:
        logger.error(
            "API error",
            extra={
                "errorId": error_id,
                "code": e.code,
                "requestId": getattr(g, "request_id", None),
                "userId": getattr(g, "user_id", None),
            },
        )

    return jsonify(payload), e.status_code
