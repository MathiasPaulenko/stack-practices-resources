"""Smoke tests for the invalidation building blocks."""
import json
import time
from unittest.mock import MagicMock

import fakeredis
import pytest

from event_driven import invalidate_cache, write_then_delete
from race_safe import get_safe, update_safe
from tag_based import cache_product_with_tags, invalidate_tag
from ttl_cache import get_with_ttl, set_with_jitter
from versioned_keys import get_user, update_user


@pytest.fixture
def r():
    return fakeredis.FakeStrictRedis(decode_responses=False)


def test_jitter_spreads_ttl(r):
    set_with_jitter(r, "k", "v", base_ttl=100, jitter_pct=50)
    assert 100 <= r.ttl("k") <= 150


def test_ttl_zero_bypasses_cache(r):
    calls = []
    def loader():
        calls.append(1)
        return {"x": 1}
    get_with_ttl(r, "k", loader, "real_time_stats")
    get_with_ttl(r, "k", loader, "real_time_stats")
    assert len(calls) == 2  # never cached


def test_versioned_key_uses_decoded_version(r):
    r.set("user_version:1", b"2")
    r.set("user:1:v2", json.dumps({"name": "ok"}))
    assert get_user(r, MagicMock(), 1) == {"name": "ok"}
    # Bug would produce key "user:1:vb'2'" and miss the cache


def test_invalidate_tag_removes_entries(r):
    cache_product_with_tags(r, {"id": 7, "category_id": 3, "n": "p"})
    assert r.exists("product:7")
    invalidate_tag(r, "product:7")
    assert not r.exists("product:7")


def test_double_delete_clears_repopulated(r):
    users = MagicMock()
    users.update.return_value = {"id": 1}
    update_safe(r, users, 1, {"x": 1}, delay=0.01)
    time.sleep(0.05)
    assert not r.exists("user:1")


def test_locked_read_returns_fresh(r):
    users = MagicMock()
    users.find_by_id.return_value = {"id": 1}
    assert get_safe(r, users, 1) == {"id": 1}
    assert not r.exists("lock:user:1")
