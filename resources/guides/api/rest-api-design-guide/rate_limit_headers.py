"""Rate limiting surfaced through response headers.

Honest clients read X-RateLimit-Remaining and slow down before
hitting the limit; abusers get 429 + Retry-After.
"""

import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
LIMIT = 100
WINDOW_SECONDS = 60
_counts: dict[str, tuple[int, float]] = {}


def check_rate(client_id: str) -> tuple[int, int, int]:
    now = time.time()
    count, window_start = _counts.get(client_id, (0, now))
    if now - window_start > WINDOW_SECONDS:
        count, window_start = 0, now
    count += 1
    _counts[client_id] = (count, window_start)
    reset = int(window_start + WINDOW_SECONDS)
    return count, max(LIMIT - count, 0), reset


@app.get("/v1/users")
async def list_users():
    remaining, reset = 87, 1721003460
    return JSONResponse(
        content={"data": [], "cursor": None},
        headers={
            "X-RateLimit-Limit": str(LIMIT),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset),
        },
    )


@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    # In production this lives in the gateway, not the app.
    if request.url.path.startswith("/v1/limited"):
        return JSONResponse(
            status_code=429,
            content={"error": {"code": "RATE_LIMITED", "message": "Too many requests."}},
            headers={"Retry-After": "30"},
        )
    return await call_next(request)
