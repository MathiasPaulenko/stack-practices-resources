"""Context Object Pattern — runnable demo.

Builds an immutable RequestContext at the boundary (RequestHandler) and passes
it through the service layer without threading request metadata through every
signature.
"""

from dataclasses import dataclass, field, replace
from typing import Any
from datetime import datetime
import logging
import uuid

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


@dataclass(frozen=True)
class RequestContext:
    """Request-scoped state, immutable after construction."""

    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: str | None = None
    correlation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def with_user(self, user_id: str) -> "RequestContext":
        return replace(self, user_id=user_id, metadata=dict(self.metadata))


class OrderService:
    def process_order(self, ctx: RequestContext, order_data: dict) -> dict:
        logging.info("[%s] Processing order for %s", ctx.request_id, ctx.user_id)
        validated = self._validate(order_data)
        return self._persist(ctx, validated)

    def _validate(self, data: dict) -> dict:
        return {**data, "validated": True}

    def _persist(self, ctx: RequestContext, data: dict) -> dict:
        logging.info("[%s] Persisting order", ctx.request_id)
        return {**data, "order_id": "ORD-123"}


class RequestHandler:
    """Boundary layer: builds the context once."""

    def __init__(self, service: OrderService):
        self.service = service

    def handle_request(self, raw_request: dict) -> dict:
        ctx = RequestContext(
            user_id=raw_request.get("user_id"),
            correlation_id=raw_request.get("correlation_id"),
        )
        return self.service.process_order(ctx, raw_request.get("order_data", {}))


if __name__ == "__main__":
    handler = RequestHandler(OrderService())
    result = handler.handle_request({
        "user_id": "user-42",
        "correlation_id": "corr-abc",
        "order_data": {"items": ["book", "pen"]},
    })
    assert result["order_id"] == "ORD-123"

    # Immutability check: with_user returns a new object
    ctx = RequestContext(user_id="u1")
    ctx2 = ctx.with_user("u2")
    assert ctx.user_id == "u1" and ctx2.user_id == "u2"
    print("context-object-pattern OK")
