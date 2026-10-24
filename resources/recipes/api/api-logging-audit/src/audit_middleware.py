"""FastAPI audit middleware: correlation ID + structured JSON audit entry per request."""
import json
import logging
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.audit")


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        response = await call_next(request)

        audit = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "correlation_id": correlation_id,
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "user_agent": request.headers.get("user-agent"),
            "client_ip": request.client.host if request.client else None,
        }
        logger.info(json.dumps(audit))
        response.headers["X-Correlation-Id"] = correlation_id
        return response


app = FastAPI()
app.add_middleware(AuditMiddleware)


@app.get("/health")
def health():
    return {"status": "ok"}

# Run: uvicorn audit_middleware:app --reload
# Try: curl -i http://127.0.0.1:8000/health  -> note X-Correlation-Id in response
