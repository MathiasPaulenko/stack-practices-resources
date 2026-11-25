"""Idempotency-Key handling for POST endpoints.

First request with a new key: process and store the result.
Retry with the same key and body: return the stored result.
Same key, different body: 409 Conflict.
"""

import hashlib
import json
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
STORE: dict[str, dict] = {}
KEY_TTL_SECONDS = 24 * 3600


@app.post("/v1/orders")
async def create_order(request: Request):
    key = request.headers.get("idempotency-key")
    body = await request.body()
    body_hash = hashlib.sha256(body).hexdigest()

    if key and key in STORE:
        record = STORE[key]
        if time.time() - record["created_at"] > KEY_TTL_SECONDS:
            del STORE[key]
        elif record["body_hash"] != body_hash:
            return JSONResponse(
                status_code=409,
                content={"error": {"code": "IDEMPOTENCY_MISMATCH", "message": "Same key, different body."}},
            )
        else:
            return JSONResponse(status_code=record["status"], content=record["response"])

    order = {"id": "ord_789", "status": "pending", "created_at": "2026-07-11T14:30:00Z"}
    if key:
        STORE[key] = {"body_hash": body_hash, "status": 201, "response": order, "created_at": time.time()}
    return JSONResponse(status_code=201, content=order, headers={"Location": "/v1/orders/ord_789"})
