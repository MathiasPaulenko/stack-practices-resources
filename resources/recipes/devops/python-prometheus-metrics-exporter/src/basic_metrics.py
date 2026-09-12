from prometheus_client import start_http_server, Counter, Gauge, Histogram
import time
import random

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

ACTIVE_CONNECTIONS = Gauge(
    "active_connections",
    "Number of active connections"
)

QUEUE_DEPTH = Gauge(
    "queue_depth",
    "Number of items in the processing queue",
    ["queue_name"]
)


def handle_request(method: str, endpoint: str):
    start = time.time()
    status = 200
    try:
        time.sleep(random.uniform(0.01, 0.3))
        if random.random() < 0.05:
            status = 500
    except Exception:
        status = 500

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - start)


if __name__ == "__main__":
    start_http_server(8000)
    print("Metrics server on http://localhost:8000/metrics")

    while True:
        handle_request("GET", "/api/users")
        handle_request("POST", "/api/orders")
        ACTIVE_CONNECTIONS.set(random.randint(1, 50))
        QUEUE_DEPTH.labels(queue_name="email").set(random.randint(0, 100))
        time.sleep(0.1)
