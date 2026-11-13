"""FastAPI health check endpoints: liveness, readiness and startup.

Run:  DATABASE_URL=postgres://user:pass@localhost/db REDIS_URL=redis://localhost:6379/0 \
      uvicorn health_check:app --port 8080
"""

import os
from contextlib import asynccontextmanager

import psycopg2
import redis
from fastapi import FastAPI, HTTPException

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

app_ready = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    global app_ready
    app_ready = check_database()
    yield


app = FastAPI(lifespan=lifespan)


def check_database() -> bool:
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False


def check_cache() -> bool:
    try:
        r = redis.Redis.from_url(REDIS_URL)
        r.ping()
        return True
    except Exception:
        return False


@app.get("/health/live")
def liveness():
    return {"status": "alive"}


@app.get("/health/startup")
def startup():
    if app_ready:
        return {"status": "started"}
    raise HTTPException(status_code=503, detail="Starting")


@app.get("/health/ready")
def readiness():
    db_ok = check_database()
    cache_ok = check_cache()
    if db_ok and cache_ok:
        return {"status": "ready", "checks": {"db": True, "cache": True}}
    raise HTTPException(status_code=503, detail="Not ready")
