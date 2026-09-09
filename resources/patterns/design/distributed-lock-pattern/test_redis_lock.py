"""Tests for RedisDistributedLock using a fake Redis client."""

import time
import pytest
from unittest.mock import MagicMock, patch
from redis_lock import RedisDistributedLock


class FakeRedis:
    """Minimal in-memory Redis fake supporting SET NX EX and EVAL."""

    def __init__(self):
        self.store = {}

    def set(self, key, value, nx=False, ex=None):
        if nx and key in self.store:
            return None
        self.store[key] = value
        return "OK"

    def eval(self, script, numkeys, key, *args):
        if "del" in script:
            if self.store.get(key) == args[0]:
                del self.store[key]
                return 1
            return 0
        if "expire" in script:
            if self.store.get(key) == args[0]:
                return 1
            return 0
        return 0


def test_acquire_blocking_success():
    fake = FakeRedis()
    lock = RedisDistributedLock(fake, "test-lock", ttl_seconds=30)
    assert lock.acquire(blocking=False) is True
    assert lock._acquired is True
    assert lock.token is not None


def test_acquire_non_blocking_when_held():
    fake = FakeRedis()
    fake.store["distlock:test-lock"] = "other-token"
    lock = RedisDistributedLock(fake, "test-lock", ttl_seconds=30)
    assert lock.acquire(blocking=False) is False
    assert lock._acquired is False


def test_release_when_owner():
    fake = FakeRedis()
    lock = RedisDistributedLock(fake, "test-lock", ttl_seconds=30)
    lock.acquire(blocking=False)
    result = lock.release()
    assert result is True
    assert "distlock:test-lock" not in fake.store


def test_release_when_not_owner():
    fake = FakeRedis()
    lock = RedisDistributedLock(fake, "test-lock", ttl_seconds=30)
    lock.acquire(blocking=False)
    fake.store["distlock:test-lock"] = "different-token"
    result = lock.release()
    assert result is False


def test_release_without_acquire():
    fake = FakeRedis()
    lock = RedisDistributedLock(fake, "test-lock", ttl_seconds=30)
    assert lock.release() is False


def test_extend_when_owner():
    fake = FakeRedis()
    lock = RedisDistributedLock(fake, "test-lock", ttl_seconds=30)
    lock.acquire(blocking=False)
    assert lock.extend(60) is True


def test_extend_when_not_owner():
    fake = FakeRedis()
    lock = RedisDistributedLock(fake, "test-lock", ttl_seconds=30)
    lock.acquire(blocking=False)
    fake.store["distlock:test-lock"] = "different-token"
    assert lock.extend(60) is False


def test_context_manager_acquires_and_releases():
    fake = FakeRedis()
    with RedisDistributedLock(fake, "ctx-lock", ttl_seconds=30) as lock:
        assert lock._acquired is True
        assert "distlock:ctx-lock" in fake.store
    assert "distlock:ctx-lock" not in fake.store
