"""OpenTelemetry metrics API with the Prometheus exporter.

Run:
    pip install opentelemetry-sdk opentelemetry-exporter-prometheus
    python otel_metrics.py

The Prometheus reader exposes metrics on http://localhost:9464/metrics.
"""
import time

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource

resource = Resource.create({"service.name": "order-service"})
reader = PrometheusMetricReader()
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("order-service")

request_counter = meter.create_counter(
    "http_requests_total",
    description="Total HTTP requests",
    unit="1",
)

request_duration = meter.create_histogram(
    "http_request_duration_seconds",
    description="HTTP request duration",
    unit="s",
)

active_connections = meter.create_up_down_counter(
    "active_connections",
    description="Active connections",
    unit="1",
)


def handle_order(order_id: int) -> None:
    attrs = {"endpoint": "/api/orders", "method": "POST"}
    request_counter.add(1, attrs)
    active_connections.add(1, attrs)

    start = time.time()
    time.sleep(0.05)  # process the order
    request_duration.record(time.time() - start, attrs)

    active_connections.add(-1, attrs)


if __name__ == "__main__":
    print("OTel metrics at http://localhost:9464/metrics")
    for i in range(10):
        handle_order(i)
    print("Recorded 10 orders — metrics remain available while running")
    input("Press Enter to exit")
