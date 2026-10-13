"""fastapi-cache-headers.py — FastAPI app with HTTP Cache-Control patterns.

Companion to https://stackpractices.com/recipes/http-cache-control-headers/

Run:  pip install fastapi uvicorn && uvicorn fastapi-cache-headers:app
Try:  curl -I http://localhost:8000/api/products

Note: `StaticFiles` does NOT accept a `max_age` argument — add the header
with a middleware, as shown below.
"""

import hashlib
import json

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="public"), name="static")


@app.middleware("http")
async def cache_headers(request: Request, call_next):
    response = await call_next(request)
    # Static assets with content hashes — one year, never revalidated.
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    return response


@app.get("/api/products")
async def get_products(request: Request):
    products = [
        {"id": 1, "name": "Keyboard", "price": 89},
        {"id": 2, "name": "Mouse", "price": 45},
    ]
    body = json.dumps(products)
    etag = f'"{hashlib.sha256(body.encode()).hexdigest()[:16]}"'

    # Conditional request: If-None-Match matches -> 304, empty body.
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    return Response(
        content=body,
        media_type="application/json",
        headers={
            "Cache-Control": "public, max-age=60, stale-while-revalidate=300",
            "ETag": etag,
        },
    )


@app.get("/api/users/me")
async def get_current_user():
    # Authenticated data — browser only, always revalidated.
    return Response(
        content=json.dumps({"id": 1, "name": "Ada"}),
        media_type="application/json",
        headers={"Cache-Control": "private, no-cache"},
    )


@app.get("/api/user/billing")
async def get_billing():
    # Sensitive data — nothing stored anywhere.
    return Response(
        content=json.dumps({"balance": 120}),
        media_type="application/json",
        headers={"Cache-Control": "no-store"},
    )
