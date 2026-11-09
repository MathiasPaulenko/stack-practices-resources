"""Shared OpenTelemetry setup for the distributed-tracing examples.

Point OTEL_EXPORTER_OTLP_ENDPOINT at your collector (default assumes a
local collector or Jaeger all-in-one on 4317).
"""

import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased


def init_tracing(service_name: str, sample_ratio: float = 1.0) -> trace.Tracer:
    """Configure a tracer provider with OTLP export and head sampling.

    ParentBased keeps the upstream sampling decision when this service is
    called inside an existing trace; TraceIdRatioBased decides for new roots.
    """
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": "1.0.0",
        }
    )
    sampler = ParentBased(root=TraceIdRatioBased(sample_ratio))
    provider = TracerProvider(resource=resource, sampler=sampler)

    endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
    )
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    )
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)
