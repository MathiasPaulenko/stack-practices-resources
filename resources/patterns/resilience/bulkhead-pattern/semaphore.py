# semaphore.py — Semaphore-based concurrency limiting.
import threading
import time
from contextlib import contextmanager
from functools import wraps

from exceptions import BulkheadFullError


class SemaphoreBulkhead:
    """Limits concurrent calls using a semaphore.
    Lighter than a thread pool — works with any execution model."""

    def __init__(self, max_concurrent, timeout=30):
        self._semaphore = threading.Semaphore(max_concurrent)
        self._max = max_concurrent
        self._timeout = timeout
        self._active = 0
        self._lock = threading.Lock()

    @contextmanager
    def acquire(self):
        """Context manager that acquires a permit."""
        acquired = self._semaphore.acquire(timeout=self._timeout)
        if not acquired:
            raise BulkheadFullError(
                f"Could not acquire permit within {self._timeout}s"
            )
        with self._lock:
            self._active += 1
        try:
            yield
        finally:
            with self._lock:
                self._active -= 1
            self._semaphore.release()

    def __call__(self, fn):
        """Decorator that wraps a function with bulkhead protection."""
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with self.acquire():
                return fn(*args, **kwargs)
        return wrapper

    @property
    def active(self):
        return self._active

    @property
    def available(self):
        return self._max - self._active


if __name__ == "__main__":
    db_bulkhead = SemaphoreBulkhead(max_concurrent=20)

    @db_bulkhead
    def query_database(sql):
        time.sleep(0.1)
        return {"rows": 42}

    api_bulkhead = SemaphoreBulkhead(max_concurrent=5, timeout=10)

    def call_external_api(endpoint):
        with api_bulkhead.acquire():
            time.sleep(0.5)
            return {"data": "response"}

    print(query_database("SELECT 1"))
    print(call_external_api("/status"))
