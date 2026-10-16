"""FastAPI demo for the Health Check Pattern.

Exposes three probe endpoints matching the Kubernetes lifecycle:
- /health/live     — process is alive (liveness)
- /health/ready    — dependencies are reachable (readiness)
- /health/startup  — initialization finished (startup)

Run locally:  uvicorn app:app --port 8080
Or with deps: docker compose up --build
"""
import asyncio
import os
import time
from contextlib import asynccontextmanager

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.responses import JSONResponse

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/demo")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

ready_since: float | None = None
shutting_down = False


async def check_database(timeout: float = 2.0) -> bool:
    try:
        conn = await asyncio.wait_for(asyncpg.connect(DATABASE_URL), timeout=timeout)
        await conn.execute("SELECT 1")
        await conn.close()
        return True
    except Exception:
        return False


async def check_redis(timeout: float = 1.0) -> bool:
    try:
        client = aioredis.from_url(REDIS_URL)
        pong = await asyncio.wait_for(client.ping(), timeout=timeout)
        await client.aclose()
        return pong
    except Exception:
        return False


async def run_dependency_checks() -> dict:
    database, redis_ok = await asyncio.gather(check_database(), check_redis())
    return {"database": database, "redis": redis_ok}


async def is_initialization_complete() -> bool:
    """Placeholder for real boot work: model load, cache warmup, migrations."""
    await asyncio.sleep(0)
    return True


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ready_since, shutting_down
    ready_since = time.time()
    yield
    # SIGTERM lands here. Flag unready first so readiness returns 503,
    # then give endpoints propagation a moment before draining.
    shutting_down = True
    await asyncio.sleep(5)


app = FastAPI(lifespan=lifespan)


@app.get("/health/live")
async def liveness():
    """Liveness probe — process is running. Never checks dependencies."""
    return {"status": "alive"}


@app.get("/health/ready")
async def readiness():
    """Readiness probe — 503 during shutdown or when a dependency is down."""
    if shutting_down:
        return JSONResponse(status_code=503, content={"status": "shutting down"})
    if ready_since is None:
        return JSONResponse(status_code=503, content={"status": "initializing"})
    checks = await run_dependency_checks()
    if not all(checks.values()):
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "checks": checks},
        )
    return {"status": "ready", "checks": checks}


@app.get("/health/startup")
async def startup():
    """Startup probe — gates liveness/readiness until boot completes."""
    if ready_since is None:
        if await is_initialization_complete():
            return {"status": "started"}
        return JSONResponse(status_code=503, content={"status": "starting"})
    return {"status": "started", "ready_since": ready_since}
