"""Cache stampede prevention — runnable simulation (stdlib only).

Companion to https://stackpractices.com/patterns/cache-stampede-prevention-pattern/

Simulates a hot key expiring under concurrent load and counts how many times
each strategy hits the "database". MiniRedis reproduces the Redis semantics
used in the pattern (GET, SETEX, SET NX EX, check-and-delete release) with a
thread-safe dict and real TTLs, so the coordination code is the same shape as
production.

Run: python src/stampede_demo.py
"""

import json
import threading
import time
import uuid
from typing import Any, Callable, Optional


class MiniRedis:
    """Thread-safe in-memory stand-in for the Redis commands the pattern uses."""

    def __init__(self) -> None:
        self._data: dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            item = self._data.get(key)
            if item is None:
                return None
            value, expires_at = item
            if expires_at and time.time() > expires_at:
                del self._data[key]
                return None
            return value

    def setex(self, key: str, ttl: int, value: str) -> None:
        with self._lock:
            self._data[key] = (value, time.time() + ttl)

    def set(self, key: str, value: str, nx: bool = False, ex: Optional[int] = None) -> bool:
        with self._lock:
            if nx and key in self._data:
                existing, exp = self._data[key]
                if not exp or time.time() <= exp:
                    return False
            self._data[key] = (value, time.time() + ex if ex else 0.0)
            return True

    def delete_if_owner(self, key: str, expected: str) -> int:
        """Atomic check-and-delete — the Lua release script as a method."""
        with self._lock:
            item = self._data.get(key)
            if item and item[0] == expected:
                del self._data[key]
                return 1
            return 0

    def flush(self) -> None:
        with self._lock:
            self._data.clear()


class FakeDB:
    """Counts queries and simulates a slow read so the stampede is visible."""

    def __init__(self, latency: float = 0.3) -> None:
        self.latency = latency
        self.queries = 0
        self._lock = threading.Lock()

    def query(self, key: str) -> dict[str, Any]:
        with self._lock:
            self.queries += 1
        time.sleep(self.latency)
        return {"key": key, "payload": f"row-for-{key}"}


class NaiveCache:
    """Cache-aside with no stampede protection — every miss reloads."""

    def __init__(self, store: MiniRedis, db: FakeDB, ttl: int = 60) -> None:
        self.store, self.db, self.ttl = store, db, ttl

    def get_or_load(self, key: str) -> Any:
        cached = self.store.get(key)
        if cached is not None:
            return json.loads(cached)
        value = self.db.query(key)
        self.store.setex(key, self.ttl, json.dumps(value))
        return value


class SingleFlightCache:
    """In-memory single-flight: one thread loads, the rest wait on an Event."""

    def __init__(self, store: MiniRedis, db: FakeDB, ttl: int = 60) -> None:
        self.store, self.db, self.ttl = store, db, ttl
        self._inflight: dict[str, threading.Event] = {}
        self._guard = threading.Lock()

    def get_or_load(self, key: str) -> Any:
        cached = self.store.get(key)
        if cached is not None:
            return json.loads(cached)

        with self._guard:
            if key in self._inflight:
                event: Optional[threading.Event] = self._inflight[key]
            else:
                self._inflight[key] = threading.Event()
                event = None  # this thread loads

        if event is not None:
            event.wait(timeout=30)
            cached = self.store.get(key)
            if cached is not None:
                return json.loads(cached)
            return self._load(key)

        try:
            return self._load(key)
        finally:
            with self._guard:
                evt = self._inflight.pop(key, None)
            if evt:
                evt.set()

    def _load(self, key: str) -> Any:
        value = self.db.query(key)
        self.store.setex(key, self.ttl, json.dumps(value))
        return value


class StampedeSafeCache:
    """Distributed lock: SET NX EX wins the right to reload; losers poll."""

    def __init__(self, store: MiniRedis, db: FakeDB, ttl: int = 60, lock_timeout: int = 30) -> None:
        self.store, self.db, self.ttl, self.lock_timeout = store, db, ttl, lock_timeout

    def get_or_load(self, key: str) -> Any:
        cached = self.store.get(key)
        if cached is not None:
            return json.loads(cached)

        lock_key = f"lock:{key}"
        lock_value = str(uuid.uuid4())
        if not self.store.set(lock_key, lock_value, nx=True, ex=self.lock_timeout):
            for _ in range(20):
                time.sleep(0.05)
                cached = self.store.get(key)
                if cached is not None:
                    return json.loads(cached)
            return self._load(key)

        try:
            cached = self.store.get(key)  # double-check after winning the lock
            if cached is not None:
                return json.loads(cached)
            return self._load(key)
        finally:
            self.store.delete_if_owner(lock_key, lock_value)

    def _load(self, key: str) -> Any:
        value = self.db.query(key)
        self.store.setex(key, self.ttl, json.dumps(value))
        return value


def get_swr(
    store: MiniRedis,
    db: FakeDB,
    key: str,
    ttl: float = 0.5,
    stale_window: float = 5.0,
) -> Any:
    """Stale-while-revalidate: serve the stale entry; one caller refreshes."""
    packed = store.get(key)
    if packed is not None:
        entry = json.loads(packed)
        age = time.time() - entry["stored_at"]
        if age < ttl:
            return entry["value"]
        if age < ttl + stale_window:
            if store.set(f"refreshing:{key}", "1", nx=True, ex=int(stale_window)):
                threading.Thread(
                    target=_swr_refresh,
                    args=(store, db, key, ttl, stale_window),
                    daemon=True,
                ).start()
            return entry["value"]
    return _swr_refresh(store, db, key, ttl, stale_window)


def _swr_refresh(store: MiniRedis, db: FakeDB, key: str, ttl: float, stale_window: float) -> Any:
    value = db.query(key)
    entry = {"value": value, "stored_at": time.time()}
    store.setex(key, int(ttl + stale_window) + 1, json.dumps(entry))
    return value


def run_stampede(name: str, worker: Callable[[str], Any], threads: int = 20) -> int:
    """Fire `threads` concurrent callers at a cold key; count DB queries."""
    errors: list[Exception] = []
    barrier = threading.Barrier(threads)

    def hit() -> None:
        try:
            barrier.wait()
            worker("hot-key")
        except Exception as exc:  # noqa: BLE001 — demo collects, not handles
            errors.append(exc)

    pool = [threading.Thread(target=hit) for _ in range(threads)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()
    if errors:
        raise errors[0]
    print(f"{name:<28} threads={threads}  db_queries={demo_db.queries}")
    return demo_db.queries


if __name__ == "__main__":
    demo_db = FakeDB(latency=0.3)

    store = MiniRedis()
    naive = NaiveCache(store, demo_db)
    run_stampede("naive cache-aside", naive.get_or_load)

    demo_db.queries = 0
    store.flush()
    sf = SingleFlightCache(store, demo_db)
    run_stampede("single-flight (in-memory)", sf.get_or_load)

    demo_db.queries = 0
    store.flush()
    safe = StampedeSafeCache(store, demo_db)
    run_stampede("distributed lock (SET NX EX)", safe.get_or_load)

    # SWR needs a warm entry past its logical TTL but inside the stale window.
    store.flush()
    seed = {"value": demo_db.query("hot-key"), "stored_at": time.time() - 0.6}
    store.setex("hot-key", 60, json.dumps(seed))
    demo_db.queries = 0  # count only the stampede, not the seed write
    run_stampede(
        "stale-while-revalidate",
        lambda k: get_swr(store, demo_db, k, ttl=0.5, stale_window=5.0),
    )
    time.sleep(0.5)  # let the background refresh land
    print(f"\nSWR background refresh done — final db_queries={demo_db.queries}")
    print("Expected: naive ~20 queries; protected strategies ~1.")
