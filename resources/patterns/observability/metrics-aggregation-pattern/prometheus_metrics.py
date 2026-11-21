"""Prometheus metrics demo — all four metric types.

Run:
    pip install prometheus-client
    python prometheus_metrics.py

Then scrape http://localhost:9090/metrics or run the PromQL queries
from dashboard_queries.promql against a Prometheus server configured
with prometheus.yml.
"""
import random
import time

from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server

# Counter — monotonically increasing (request count, error count)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

# Gauge — can go up or down (active connections, queue depth)
ACTIVE_CONNECTIONS = Gauge(
    "active_connections",
    "Currently active connections",
)

QUEUE_DEPTH = Gauge(
    "message_queue_depth",
    "Messages waiting in queue",
    ["queue_name"],
)

# Histogram — distribution of values (request latency)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Summary — quantiles of values
RESPONSE_SIZE = Summary(
    "http_response_size_bytes",
    "HTTP response size in bytes",
    ["endpoint"],
)

ENDPOINTS = ["/api/orders", "/api/users", "/api/products"]
METHODS = ["GET", "GET", "GET", "POST"]


def handle_request(method: str, endpoint: str) -> int:
    """Simulate one request and record the metrics it produces."""
    start_time = time.time()

    time.sleep(random.uniform(0.01, 0.2))
    status = random.choice([200, 200, 200, 200, 404, 500])

    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(
        time.time() - start_time
    )
    RESPONSE_SIZE.labels(endpoint=endpoint).observe(random.randint(100, 5000))

    return status


def main() -> None:
    start_http_server(9090)
    print("Metrics available at http://localhost:9090/metrics — Ctrl+C to stop")

    ACTIVE_CONNECTIONS.set(42)
    QUEUE_DEPTH.labels(queue_name="orders").set(150)

    try:
        while True:
            handle_request(random.choice(METHODS), random.choice(ENDPOINTS))
            ACTIVE_CONNECTIONS.set(random.randint(20, 80))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
