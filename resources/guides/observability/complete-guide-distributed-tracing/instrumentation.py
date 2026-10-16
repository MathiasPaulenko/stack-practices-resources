"""OpenTelemetry auto-instrumentation setup for Python services."""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource


def configure_tracing(
    service_name: str,
    otlp_endpoint: str = "http://otel-collector:4317",
    service_version: str = "1.0.0",
    environment: str = "production",
) -> None:
    """Set up the TracerProvider with batch export to an OTLP collector."""
    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version,
        "deployment.environment": environment,
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def auto_instrument_flask(app, db) -> None:
    """Enable auto-instrumentation for the common library set."""
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor

    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(engine=db.engine)
    RedisInstrumentor().instrument()
