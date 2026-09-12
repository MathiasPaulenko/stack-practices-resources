from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, make_asgi_app
import time

app = FastAPI()

REQUEST_COUNT = Counter(
    "fastapi_requests_total",
    "Total FastAPI requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "fastapi_request_duration_seconds",
    "FastAPI request latency",
    ["endpoint"]
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=str(response.status_code)
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)

    return response


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/users")
async def get_users():
    return {"users": []}


app.mount("/metrics", make_asgi_app())
