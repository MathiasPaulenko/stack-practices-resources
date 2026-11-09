"""FastAPI service showing both halves of trace-context propagation.

- The middleware extracts ``traceparent``/``tracestate`` from incoming
  requests so server spans join the caller's trace.
- The ``/orders`` handler injects the context into an outgoing HTTP call
  so the downstream service can do the same.

Run with ``uvicorn fastapi_traced_app:app`` after ``pip install -r
requirements.txt``. Send a ``traceparent`` header and watch the incoming
parent span ID appear in the exported span.
"""

import requests
from fastapi import FastAPI, Request
from opentelemetry import propagate, trace

from otel_setup import init_tracing

tracer = init_tracing("order-service")
app = FastAPI()


@app.middleware("http")
async def tracing_middleware(request: Request, call_next):
    """Attach each request to the incoming trace context, if any."""
    ctx = propagate.extract(request.headers)
    with tracer.start_as_current_span(
        f"{request.method} {request.url.path}",
        context=ctx,
        kind=trace.SpanKind.SERVER,
    ) as span:
        span.set_attribute("http.request.method", request.method)
        span.set_attribute("url.path", request.url.path)
        span.set_attribute("url.scheme", request.url.scheme)

        response = await call_next(request)
        span.set_attribute("http.response.status_code", response.status_code)
        return response


@app.post("/orders")
async def create_order(order_id: str, amount: float = 99.0):
    """Create an order and call the payment service with propagated context."""
    with tracer.start_as_current_span("call_payment_service") as span:
        span.set_attribute("order.id", order_id)
        headers: dict[str, str] = {}
        propagate.inject(headers)  # writes traceparent into headers
        try:
            resp = requests.post(
                "http://localhost:9000/charge",
                json={"order_id": order_id, "amount": amount},
                headers=headers,
                timeout=5,
            )
            span.set_attribute("http.response.status_code", resp.status_code)
            return {"status": "created", "payment": resp.json()}
        except requests.RequestException as exc:
            span.record_exception(exc)
            span.set_status(trace.StatusCode.ERROR)
            return {"status": "payment_unreachable", "order_id": order_id}
