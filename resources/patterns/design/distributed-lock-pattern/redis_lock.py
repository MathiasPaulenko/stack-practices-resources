"""Distributed lock using Redis SET NX with TTL and fencing token."""

import time
import uuid
from typing import Optional


class RedisDistributedLock:
    """Distributed lock using Redis with automatic TTL and a fencing token."""

    def __init__(self, redis_client, lock_key: str,
                 ttl_seconds: int = 30, retry_delay: float = 0.1):
        self.redis = redis_client
        self.lock_key = f"distlock:{lock_key}"
        self.ttl = ttl_seconds
        self.retry_delay = retry_delay
        self.token = None
        self._acquired = False

    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        """Acquire the lock with an optional blocking timeout."""
        self.token = str(uuid.uuid4())
        start_time = time.time()

        while True:
            acquired = self.redis.set(
                self.lock_key, self.token, nx=True, ex=self.ttl
            )
            if acquired:
                self._acquired = True
                return True

            if not blocking:
                return False

            if timeout and (time.time() - start_time) >= timeout:
                return False

            time.sleep(self.retry_delay)

    def release(self) -> bool:
        """Release the lock only if we still own it (compare token)."""
        if not self._acquired:
            return False

        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        result = self.redis.eval(lua_script, 1, self.lock_key, self.token)
        self._acquired = False
        return result == 1

    def extend(self, additional_ttl: int) -> bool:
        """Extend the lock TTL if we still own it."""
        if not self._acquired:
            return False

        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("expire", KEYS[1], ARGV[2])
        else
            return 0
        end
        """
        result = self.redis.eval(
            lua_script, 1, self.lock_key, self.token, additional_ttl
        )
        return result == 1

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
