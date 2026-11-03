"""Smoke tests for the Lambda production building blocks."""
import json
from unittest.mock import MagicMock

import fakeredis
import pytest

from idempotent_handler import idempotency_key_for, lambda_handler as idem
from sqs_batch_handler import lambda_handler as sqs_handler
from structured_logger import log_event


def test_idempotency_key_stable():
    e1 = {"b": 2, "a": 1}
    e2 = {"a": 1, "b": 2}
    assert idempotency_key_for(e1) == idempotency_key_for(e2)


def test_idempotent_second_call_returns_cached(monkeypatch):
    r = fakeredis.FakeStrictRedis(decode_responses=True)
    monkeypatch.setattr(
        "idempotent_handler.process_event", lambda e: {"ok": True})
    ctx = MagicMock(aws_request_id="r1")
    first = idem({"x": 1}, ctx, redis_client=r)
    second = idem({"x": 1}, ctx, redis_client=r)
    assert first["status"] == "processed"
    assert second["status"] == "already_processed"


def test_sqs_partial_failures(monkeypatch):
    def flaky(msg):
        if msg["bad"]:
            raise ValueError("boom")
    monkeypatch.setattr("sqs_batch_handler.process_message", flaky)
    event = {"Records": [
        {"messageId": "m1", "body": json.dumps({"bad": False})},
        {"messageId": "m2", "body": json.dumps({"bad": True})},
    ]}
    out = sqs_handler(event, MagicMock())
    assert out["batchItemFailures"] == [{"itemIdentifier": "m2"}]


def test_log_event_emits_json(caplog):
    with caplog.at_level("INFO"):
        log_event("INFO", "req-1", event_type="test", n=42)
    entry = json.loads(caplog.records[0].message)
    assert entry["request_id"] == "req-1" and entry["n"] == 42
