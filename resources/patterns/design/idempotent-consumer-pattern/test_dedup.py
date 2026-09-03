"""Tests for deduplication logic."""

import os
import tempfile
import pytest
from python_idempotent_consumer import DedupStore, IdempotentConsumer


@pytest.fixture
def store():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    s = DedupStore(db_path)
    yield s
    s.db.close()
    os.unlink(db_path)


def test_new_id_is_accepted(store):
    assert store.is_new("msg-1") is True


def test_duplicate_id_is_rejected(store):
    store.mark_processed("msg-1")
    assert store.is_new("msg-1") is False


def test_different_ids_are_independent(store):
    store.mark_processed("msg-1")
    assert store.is_new("msg-1") is False
    assert store.is_new("msg-2") is True


def test_mark_processed_is_idempotent(store):
    store.mark_processed("msg-1")
    store.mark_processed("msg-1")
    assert store.is_new("msg-1") is False


def test_cleanup_removes_old_entries(store):
    # Insert with an old timestamp manually
    store.db.execute(
        "INSERT INTO processed (message_id, processed_at) VALUES (?, ?)",
        ("msg-old", "2020-01-01 00:00:00")
    )
    store.db.commit()
    removed = store.cleanup_old(days=1)
    assert removed >= 1
    assert store.is_new("msg-old") is True
