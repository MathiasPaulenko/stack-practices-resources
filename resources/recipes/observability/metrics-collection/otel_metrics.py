"""OpenTelemetry metrics in Python, exported for Prometheus scraping.

Run: pip install opentelemetry-sdk opentelemetry-exporter-prometheus && python otel_metrics.py
The reader exposes metrics on http://localhost:9464/metrics by default.
"""

import time

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider

reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)

counter = meter.create_counter("orders.created", description="Orders created")
histogram = meter.create_histogram("order.value", description="Order value in USD")


class Order:
    def __init__(self, items, total):
        self.items = items
        self.total = total


def create_order(items, total):
    counter.add(1, {"region": "us-east"})
    histogram.record(total, {"region": "us-east"})
    return Order(items=items, total=total)


if __name__ == "__main__":
    create_order(["book"], 42.50)
    print("Serving metrics for Prometheus scraping on :9464 (Ctrl+C to stop)")
    while True:
        time.sleep(60)
