"""Idempotent API Endpoints — Python FastAPI implementation.

Demonstrates idempotency key handling with in-memory store, TTL cleanup,
processing state for concurrent request protection, and error recovery.
"""
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uuid
import time
from typing import Optional

app = FastAPI()

idempotency_store: dict[str, dict] = {}
IDEMPOTENCY_TTL = 86400  # 24 hours


class CreateOrderRequest(BaseModel):
    customer_id: str
    amount: float
    currency: str = "USD"


class OrderResponse(BaseModel):
    id: str
    status: str
    cached: bool


@app.post("/orders", response_model=OrderResponse)
def create_order(
    request: CreateOrderRequest,
    idempotency_key: Optional[str] = Header(None),
) -> OrderResponse:
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header required")

    try:
        uuid.UUID(idempotency_key)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Idempotency-Key format")

    now = time.time()

    # TTL cleanup
    expired = [k for k, v in idempotency_store.items() if now - v["timestamp"] > IDEMPOTENCY_TTL]
    for k in expired:
        del idempotency_store[k]

    # Check for existing request
    if idempotency_key in idempotency_store:
        stored = idempotency_store[idempotency_key]
        if stored["status"] == "completed":
            return OrderResponse(id=stored["order_id"], status="completed", cached=True)
        if stored["status"] == "processing":
            raise HTTPException(status_code=409, detail="Request already in progress")

    # Set processing marker
    idempotency_store[idempotency_key] = {
        "status": "processing",
        "timestamp": now,
        "order_id": None,
    }

    try:
        order_id = str(uuid.uuid4())
        # ... save to database ...
        idempotency_store[idempotency_key] = {
            "status": "completed",
            "timestamp": now,
            "order_id": order_id,
        }
        return OrderResponse(id=order_id, status="completed", cached=False)
    except Exception:
        del idempotency_store[idempotency_key]
        raise


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
