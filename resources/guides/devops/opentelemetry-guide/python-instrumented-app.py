"""Minimal runnable OpenTelemetry example.

Install:
    pip install opentelemetry-sdk \
        opentelemetry-exporter-otlp-proto-grpc

Run (with a Collector on localhost:4317):
    python python-instrumented-app.py
"""

import time

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode

resource = Resource.create(
    {
        "service.name": "demo-service",
        "service.version": "0.1.0",
        "deployment.environment": "local",
    }
)

# Traces: provider -> processor -> exporter (exporters MUST be attached
# through a span processor or nothing is exported).
tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)

# Metrics: provider -> reader -> exporter
reader = PeriodicExportingMetricReader(OTLPMetricExporter())
meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)

request_counter = meter.create_counter(
    "demo_requests_total", description="Requests handled"
)


def handle_request(path: str) -> None:
    request_counter.add(1, {"route": path})
    with tracer.start_as_current_span("handle_request") as span:
        span.set_attribute("http.route", path)
        span.set_attribute("http.method", "GET")
        time.sleep(0.05)  # simulate work
        if path == "/fail":
            span.record_exception(RuntimeError("simulated failure"))
            span.set_status(Status(StatusCode.ERROR))
        else:
            span.set_status(Status(StatusCode.OK))


if __name__ == "__main__":
    for route in ["/api/users", "/api/orders", "/fail"]:
        handle_request(route)
    # Always flush before exit or the last batch is lost.
    tracer_provider.force_flush()
    meter_provider.force_flush()
    tracer_provider.shutdown()
    meter_provider.shutdown()
    print("Spans and metrics flushed to OTLP.")
