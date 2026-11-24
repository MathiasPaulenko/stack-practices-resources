"""Demo: create nested spans and print them to the console (no Jaeger needed)."""
from opentelemetry.trace import Status, StatusCode

from tracing_setup import setup_tracer

tracer = setup_tracer(service_name="order-service", exporter="console")


def process_order(order_id: str) -> None:
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.total", 99.99)
        with tracer.start_as_current_span("validate_payment"):
            span.add_event("payment_validated")
        with tracer.start_as_current_span("save_to_database"):
            try:
                raise RuntimeError("simulated failure")
            except RuntimeError as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))


if __name__ == "__main__":
    process_order("ord-123")
