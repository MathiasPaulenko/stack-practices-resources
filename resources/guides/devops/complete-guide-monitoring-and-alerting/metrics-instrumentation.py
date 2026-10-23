"""FastAPI + prometheus_client instrumentation example.

Exposes RED metrics (rate, errors, duration), gauges for resources,
and a business metric segmented by plan. Requires: fastapi, prometheus-client.
"""

import asyncio
import time

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

app = FastAPI()

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

ACTIVE_CONNECTIONS = Gauge("active_connections", "Active connections")

DB_POOL_SIZE = Gauge("db_pool_size", "Database connection pool size", ["pool_name"])
DB_POOL_USED = Gauge("db_pool_used", "Database connections in use", ["pool_name"])

BUSINESS_METRIC = Counter(
    "api_requests_total",
    "Total API requests by plan",
    ["plan", "endpoint"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    ACTIVE_CONNECTIONS.inc()
    try:
        response = await call_next(request)
        duration = time.time() - start
        REQUEST_COUNT.labels(
            method=request.method, endpoint=request.url.path, status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)
        return response
    finally:
        ACTIVE_CONNECTIONS.dec()


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/api/users")
async def list_users(request: Request):
    plan = request.headers.get("x-plan", "free")
    BUSINESS_METRIC.labels(plan=plan, endpoint="/api/users").inc()
    return {"users": []}


async def update_db_pool_metrics():
    while True:
        for pool_name, pool in db.pools.items():  # noqa: F821 - wire your pool registry here
            DB_POOL_SIZE.labels(pool_name=pool_name).set(pool.size())
            DB_POOL_USED.labels(pool_name=pool_name).set(pool.used())
        await asyncio.sleep(15)


@app.on_event("startup")
async def start_metrics_updater():
    asyncio.create_task(update_db_pool_metrics())
