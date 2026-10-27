"""FastAPI rate limiting with fastapi-limiter (Redis-backed)."""
import redis.asyncio as redis
from fastapi import Depends, FastAPI, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.state.redis = await redis.from_url("redis://localhost")
    await FastAPILimiter.init(app.state.redis)


@app.get("/api/data", dependencies=[Depends(RateLimiter(times=100, minutes=1))])
async def get_data(request: Request):
    # fastapi-limiter checks the request before the handler runs;
    # the key defaults to the client IP — pass an identifier
    # callback to rate-limit by API key instead
    return {"data": "..."}
