# middleware.py — Correlation ID middleware (Starlette/FastAPI)
import uuid
from typing import Optional

import structlog
from starlette.middleware.base import BaseHTTPMiddleware


def extract_user_id(authorization: Optional[str]) -> Optional[int]:
    """Pull user ID from a Bearer JWT. Returns None for anonymous requests."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        import base64
        import json

        payload = authorization.removeprefix("Bearer ").split(".")[1]
        payload += "=" * (-len(payload) % 4)  # base64 padding
        return json.loads(base64.b64decode(payload)).get("sub")
    except (ValueError, IndexError, KeyError):
        return None


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        structlog.contextvars.clear_contextvars()
        bound = {"request_id": request_id}
        if user_id := extract_user_id(request.headers.get("authorization")):
            bound["user_id"] = user_id
        structlog.contextvars.bind_contextvars(**bound)

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
