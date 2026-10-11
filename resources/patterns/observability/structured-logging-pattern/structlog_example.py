"""Structured logging with structlog: JSON output, bound context, redaction."""

import logging
import re
import sys

import structlog

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SENSITIVE_KEYS = {"password", "token", "api_key", "credit_card", "ssn"}
CARD_PATTERN = re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b")


def redact_sensitive(processor, logger, event_dict):
    """Mask values of sensitive keys and card numbers in any string field."""
    for key in list(event_dict.keys()):
        if key.lower() in SENSITIVE_KEYS:
            event_dict[key] = "[REDACTED]"
        elif isinstance(event_dict[key], str):
            event_dict[key] = CARD_PATTERN.sub("[REDACTED]", event_dict[key])
    return event_dict


def configure() -> structlog.stdlib.BoundLogger:
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            redact_sensitive,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()


if __name__ == "__main__":
    # structlog's LoggerFactory routes through stdlib logging, which needs
    # a handler on the root logger to emit anything
    logging.basicConfig(level=logging.INFO)
    log = configure()

    request_logger = log.bind(
        correlation_id="abc-123", user_id=42, endpoint="/api/orders"
    )
    request_logger.info("request_started")
    request_logger.info("request_completed", status_code=200, duration_ms=150)

    # Sensitive values get masked by the processor chain
    log.info(
        "checkout_attempt",
        card="4111 1111 1111 1111",
        api_key="sk-live-abc123",
    )
