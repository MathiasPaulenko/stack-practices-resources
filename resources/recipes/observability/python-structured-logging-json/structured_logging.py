"""Structured JSON logging with structlog — runnable examples.

Covers the processor chain, context binding, contextvars, a sensitive-data
redaction processor, a timing processor, and a FastAPI-style middleware.
Run directly for a smoke test that prints JSON lines to stdout.
"""

import logging
import sys
import time
import uuid

import structlog


def redact_sensitive_data(logger, method_name, event_dict):
    """Replace values of sensitive keys with [REDACTED]."""
    sensitive_keys = {"password", "api_key", "token", "credit_card"}
    for key in list(event_dict.keys()):
        if key.lower() in sensitive_keys:
            event_dict[key] = "[REDACTED]"
    return event_dict


def add_timing(logger, method_name, event_dict):
    """Convert a start_time kwarg into duration_ms."""
    if "start_time" in event_dict:
        event_dict["duration_ms"] = round(
            (time.time() - event_dict.pop("start_time")) * 1000, 2
        )
    return event_dict


def configure(level=logging.INFO):
    """Configure structlog with a production-style JSON processor chain."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            redact_sensitive_data,
            add_timing,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=level)


async def logging_middleware(request, call_next):
    """FastAPI-style middleware: bind request context, clear on exit."""
    structlog.contextvars.bind_contextvars(
        request_id=request.headers.get("X-Request-ID", str(uuid.uuid4())),
        method=request.method,
        path=request.url.path,
    )
    try:
        response = await call_next(request)
        structlog.get_logger().info(
            "request_completed", status_code=response.status_code
        )
        return response
    finally:
        structlog.contextvars.clear_contextvars()


if __name__ == "__main__":
    configure()
    logger = structlog.get_logger()

    request_logger = logger.bind(request_id="req-abc-123", user_id=42)
    request_logger.info("processing_order", order_id="ord_456")
    request_logger.info("user_login", email="alice@example.com",
                        password="secret123")

    start = time.time()
    time.sleep(0.01)
    logger.info("database_query", start_time=start,
                query="SELECT * FROM users")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("division_failed", operation="calculate_ratio")
