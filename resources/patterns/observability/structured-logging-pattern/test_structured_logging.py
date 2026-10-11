"""Tests for the structured logging companion examples."""

import io
import json
import logging

import structlog

from async_logging import build_async_logger
from json_formatter import JsonFormatter
from structlog_example import configure, redact_sensitive


def _capture_stdlib(name, extra):
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger(name)
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    logger.info("test_event", extra=extra)
    return json.loads(stream.getvalue().strip())


def test_json_formatter_includes_extra_fields():
    entry = _capture_stdlib("t1", {"order_id": 123, "total": 99.99})
    assert entry["message"] == "test_event"
    assert entry["order_id"] == 123
    assert entry["level"] == "info"
    assert entry["timestamp"].endswith("+00:00")


def test_json_formatter_filters_internal_attrs():
    entry = _capture_stdlib("t2", {"component": "checkout"})
    for internal in ("pathname", "args", "lineno", "levelno", "created"):
        assert internal not in entry
    assert entry["component"] == "checkout"


def _capture_structlog_stream():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)
    configure()
    return stream


def test_redact_sensitive_masks_keys():
    result = redact_sensitive(None, None, {"password": "hunter2", "ok": "fine"})
    assert result["password"] == "[REDACTED]"
    assert result["ok"] == "fine"


def test_redact_sensitive_masks_card_numbers_in_strings():
    result = redact_sensitive(
        None, None, {"note": "card 4111-1111-1111-1111 declined"}
    )
    assert "4111" not in result["note"]
    assert "[REDACTED]" in result["note"]


def test_structlog_emits_valid_json_line():
    stream = _capture_structlog_stream()
    structlog.get_logger().info("user_login", user_id=42)
    line = stream.getvalue().strip().splitlines()[-1]
    entry = json.loads(line)
    assert entry["event"] == "user_login"
    assert entry["user_id"] == 42
    assert entry["level"] == "info"
    assert "timestamp" in entry


def test_bound_context_appears_in_every_entry():
    stream = _capture_structlog_stream()
    bound = structlog.get_logger().bind(
        correlation_id="abc-123", endpoint="/api/orders"
    )
    bound.info("request_started")
    bound.info("request_completed", status_code=200)
    lines = stream.getvalue().strip().splitlines()
    for line in lines:
        entry = json.loads(line)
        assert entry["correlation_id"] == "abc-123"
        assert entry["endpoint"] == "/api/orders"


def test_async_logger_delivers_entries():
    stream = io.StringIO()
    logger, listener = build_async_logger("async-test", stream=stream)
    logger.info("queued_event", extra={"index": 7})
    listener.stop()
    entry = json.loads(stream.getvalue().strip())
    assert entry["message"] == "queued_event"
    assert entry["index"] == 7
