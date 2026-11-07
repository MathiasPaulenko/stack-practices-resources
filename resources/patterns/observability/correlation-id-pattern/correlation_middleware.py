"""FastAPI correlation ID middleware with contextvars + structured logging.

Usage:
    uvicorn correlation_middleware:app --reload
    curl -i http://localhost:8000/orders -H "X-Correlation-ID: demo-123"
"""
import json
import logging
import uuid
from contextvars import ContextVar

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

CORRELATION_ID_HEADER = "X-Correlation-ID"
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="unknown")

app = FastAPI()


class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_var.get()
        return True


logger = logging.getLogger("myapp")
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
        '"correlation_id": "%(correlation_id)s", "message": "%(message)s"}'
    )
)
logger.addHandler(handler)
logger.addFilter(CorrelationIdFilter())
logger.setLevel(logging.INFO)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get(CORRELATION_ID_HEADER) or str(uuid.uuid4())
        token = correlation_id_var.set(correlation_id)
        request.state.correlation_id = correlation_id
        try:
            response = await call_next(request)
            response.headers[CORRELATION_ID_HEADER] = correlation_id
            return response
        finally:
            correlation_id_var.reset(token)


app.add_middleware(CorrelationIdMiddleware)


@app.post("/orders")
async def create_order():
    logger.info("Processing order for customer 12345")
    return {"status": "created"}
