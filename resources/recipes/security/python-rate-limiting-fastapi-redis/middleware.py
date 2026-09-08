"""FastAPI middleware for rate limiting with per-endpoint decorator support."""
from typing import Callable
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from sliding_window import SlidingWindowRateLimiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        rate_limiter: SlidingWindowRateLimiter,
        max_requests: int = 100,
        window_seconds: int = 60,
    ):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{client_ip}"

        allowed, info = self.rate_limiter.is_allowed(
            key, self.max_requests, self.window_seconds
        )

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "limit": info["limit"],
                    "remaining": info["remaining"],
                    "reset_at": info["reset_at"],
                },
                headers={
                    "Retry-After": str(self.window_seconds),
                    "X-RateLimit-Limit": str(info["limit"]),
                    "X-RateLimit-Remaining": str(info["remaining"]),
                    "X-RateLimit-Reset": str(info["reset_at"]),
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(info["reset_at"])
        return response


def rate_limit(max_requests: int, window_seconds: int, key_func=None):
    """Decorator for per-endpoint rate limiting.

    Args:
        max_requests: Maximum requests in the window.
        window_seconds: Window size in seconds.
        key_func: Function to extract the rate limit key from the request.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if key_func:
                key = key_func(request)
            else:
                key = f"rate_limit:{request.url.path}:{request.client.host}"

            allowed, info = rate_limiter.is_allowed(
                key, max_requests, window_seconds
            )

            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "limit": info["limit"],
                        "remaining": info["remaining"],
                        "reset_at": info["reset_at"],
                    },
                    headers={
                        "Retry-After": str(window_seconds),
                        "X-RateLimit-Limit": str(info["limit"]),
                        "X-RateLimit-Remaining": str(info["remaining"]),
                    },
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator


from functools import wraps

if __name__ == "__main__":
    import redis as redis_lib

    redis_client = redis_lib.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    rate_limiter = SlidingWindowRateLimiter(redis_client)

    app = FastAPI()
    app.add_middleware(
        RateLimitMiddleware,
        rate_limiter=rate_limiter,
        max_requests=100,
        window_seconds=60,
    )

    @app.post("/auth/login")
    @rate_limit(max_requests=5, window_seconds=60)
    async def login(request: Request):
        return {"message": "Login endpoint with strict rate limit"}

    @app.get("/search")
    @rate_limit(max_requests=100, window_seconds=60)
    async def search(request: Request):
        return {"message": "Search endpoint with standard rate limit"}

    print("FastAPI app configured with rate limiting middleware.")
    print("Run with: uvicorn middleware:app --reload")
