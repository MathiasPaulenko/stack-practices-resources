"""FastAPI audit middleware: correlation ID + request log + audit record for non-GET ops."""
import json
import logging
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
request_logger = logging.getLogger("api.requests")
audit_logger = logging.getLogger("api.audit")


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        response = await call_next(request)

        request_logger.info(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "correlation_id": correlation_id,
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "user_agent": request.headers.get("user-agent"),
            "client_ip": request.client.host if request.client else None,
        }))

        # Audit record: only for state-changing or sensitive operations
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            audit_logger.info(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "correlation_id": correlation_id,
                "actor": getattr(request.state, "user_id", "anonymous"),
                "action": request.method,
                "resource": request.url.path,
                "outcome": "success" if response.status_code < 400 else "failure",
                "client_ip": request.client.host if request.client else None,
            }))

        response.headers["X-Correlation-Id"] = correlation_id
        return response


app = FastAPI()
app.add_middleware(AuditMiddleware)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo():
    return {"status": "created"}

# Run: uvicorn audit_middleware:app --reload
# Try: curl -i -X POST http://127.0.0.1:8000/echo -> note X-Correlation-Id and the api_audit entry
