"""Structured logging setup with structlog (JSON output).

Companion to stackpractices.com/guides/logging-monitoring-observability-guide/
Requires: pip install structlog
"""

import structlog
import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structlog to emit one JSON object per line."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


def bind_trace_context(logger: structlog.BoundLogger, trace_id: str, span_id: str):
    """Return a logger with the current trace context bound.

    Call this at the start of each request/job so every log line carries the
    trace_id that links it to the distributed trace.
    """
    return logger.bind(trace_id=trace_id, span_id=span_id)


if __name__ == "__main__":
    configure_logging()
    logger = structlog.get_logger()
    logger.info("payment_processed", user_id="123", amount=49.99)
