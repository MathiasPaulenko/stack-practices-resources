"""problem_details.py — RFC 9457 error handler for Flask.

Register once:

    from problem_details import ApiError, register_problem_details
    register_problem_details(app)

Raise from handlers:

    raise ApiError(
        422, "https://api.example.com/errors/unprocessable",
        "Unprocessable Content", "Cannot schedule delivery for a past date."
    )

With field-level validation errors:

    raise ApiError(
        400, "https://api.example.com/errors/validation-failed",
        "Validation Failed", "3 fields failed validation.",
        errors=[{"field": "email", "message": "must be a valid email address",
                 "code": "invalid_format"}],
    )
"""

import os
import uuid
from datetime import datetime, timezone

from flask import g, jsonify, request

BASE_URI = os.environ.get("API_ERRORS_BASE_URI", "https://api.example.com/errors")


class ApiError(Exception):
    def __init__(self, status, type_, title, detail=None, errors=None):
        super().__init__(detail or title)
        self.status = status
        self.type = type_
        self.title = title
        self.detail = detail
        self.errors = errors


def register_problem_details(app):
    """Attach a request id and register the catch-all problem+json handler."""

    @app.before_request
    def _assign_request_id():
        g.request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:12]}"

    @app.errorhandler(Exception)
    def problem_details(err):  # noqa: ANN001
        status = getattr(err, "status", 500)
        if status >= 500:
            app.logger.error(
                "unhandled exception",
                extra={"request_id": g.request_id},
                exc_info=err,
            )
            detail = (
                "An unexpected error occurred. "
                f"Reference request ID {g.request_id} when contacting support."
            )
        else:
            detail = getattr(err, "detail", None) or str(err)

        body = {
            "type": getattr(err, "type", f"{BASE_URI}/internal"),
            "title": getattr(err, "title", "Internal Server Error" if status >= 500 else "Error"),
            "status": status,
            "detail": detail,
            "instance": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": g.request_id,
        }
        errors = getattr(err, "errors", None)
        if errors:
            body["errors"] = errors

        return jsonify(body), status, {"Content-Type": "application/problem+json"}
