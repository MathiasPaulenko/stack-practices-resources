"""FastAPI middleware that records metrics for every request.

Run:
    pip install fastapi uvicorn prometheus-client
    uvicorn fastapi_middleware:app --port 8000

Metrics are exposed on http://localhost:9090/metrics.
"""
import time

from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, start_http_server

app = FastAPI()

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    duration = time.time() - start_time
    endpoint = request.url.path
    method = request.method
    status = str(response.status_code)

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    return response


@app.get("/api/orders")
async def list_orders():
    return {"orders": []}


# Start metrics server on port 9090 alongside uvicorn on 8000
start_http_server(9090)
