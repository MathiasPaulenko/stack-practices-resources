"""OpenTelemetry tracing setup: provider, exporters, instrumentors, propagation."""
from opentelemetry import trace, propagate
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased, ParentBased
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION


def setup_tracer(
    service_name: str = "demo-service",
    exporter: str = "console",
    sample_ratio: float = 1.0,
) -> trace.Tracer:
    """Configure a TracerProvider with the chosen exporter.

    Args:
        service_name: Value for the service.name resource attribute.
        exporter: "console" (no backend needed), "jaeger", or "otlp".
        sample_ratio: Fraction of traces to keep (1.0 = all, 0.1 = 10%).

    Returns:
        A tracer ready to create spans.
    """
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: "1.0.0",
    })
    provider = TracerProvider(
        resource=resource,
        sampler=ParentBased(TraceIdRatioBased(sample_ratio)),
    )

    if exporter == "jaeger":
        from opentelemetry.exporter.jaeger.thrift import JaegerExporter
        span_exporter = JaegerExporter(agent_host_name="localhost", agent_port=6831)
    elif exporter == "otlp":
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        span_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    else:
        span_exporter = ConsoleSpanExporter()

    provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)


def instrument_requests() -> None:
    """Auto-instrument outgoing HTTP calls made with the requests library."""
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    RequestsInstrumentor().instrument()


def inject_context(headers: dict) -> dict:
    """Inject the current trace context into outgoing headers."""
    propagate.inject(headers)
    return headers


def extract_context(headers: dict):
    """Extract the trace context from incoming headers."""
    return propagate.extract(headers)
