"""Tests for the Pipes and Filters Pattern — Python implementation.

Run: python -m pytest test_pipe_python.py -v
or:  python test_pipe_python.py
"""
from pipe_python import (
    pipe, parse_csv, filter_active, normalize_emails, deduplicate, to_json, process_users,
)


def test_parse_csv():
    raw = "name,email\nAlice,a@x.com\nBob,b@x.com"
    result = parse_csv(raw)
    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[1]["email"] == "b@x.com"


def test_filter_active():
    records = [
        {"name": "Alice", "status": "active"},
        {"name": "Bob", "status": "inactive"},
    ]
    result = filter_active(records)
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_normalize_emails():
    records = [{"email": "  ALICE@X.COM  "}]
    result = normalize_emails(records)
    assert result[0]["email"] == "alice@x.com"


def test_deduplicate():
    records = [
        {"email": "a@x.com"},
        {"email": "a@x.com"},
        {"email": "b@x.com"},
    ]
    result = deduplicate(records)
    assert len(result) == 2


def test_full_pipeline():
    raw = "name,email,status\nAlice,A@X.COM,active\nBob,b@x.com,inactive\nAlice,a@x.com,active"
    result = process_users(raw)
    import json
    parsed = json.loads(result)
    assert len(parsed) == 1
    assert parsed[0]["email"] == "a@x.com"


def test_pipe_composability():
    double = lambda x: x * 2
    add_one = lambda x: x + 1
    pipeline = pipe(double, add_one)
    assert pipeline(3) == 7  # (3 * 2) + 1


if __name__ == "__main__":
    test_parse_csv()
    test_filter_active()
    test_normalize_emails()
    test_deduplicate()
    test_full_pipeline()
    test_pipe_composability()
    print("All tests passed!")
