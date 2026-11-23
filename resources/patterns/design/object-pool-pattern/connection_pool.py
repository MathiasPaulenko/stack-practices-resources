"""Object Pool pattern — Python implementation.

Pre-warmed fixed-size pool of expensive connections with acquire/release.
Wrap checkouts in try/finally (or the `pooled()` context manager below)
so objects always return to the pool.
"""
import queue
import threading
from contextlib import contextmanager


class DatabaseConnection:
    _id_counter = 0
    _lock = threading.Lock()

    def __init__(self):
        with DatabaseConnection._lock:
            DatabaseConnection._id_counter += 1
            self.id = DatabaseConnection._id_counter
        self.active = False
        print(f"Created connection {self.id} (expensive)")

    def open(self):
        self.active = True
        return self

    def close(self):
        self.active = False

    def query(self, sql):
        if not self.active:
            raise RuntimeError("Connection not open")
        return f"Result for: {sql}"


class PoolExhaustedError(Exception):
    """Raised when acquire() times out waiting for a free object."""


class ConnectionPool:
    def __init__(self, max_size=5, acquire_timeout=5):
        self.max_size = max_size
        self.acquire_timeout = acquire_timeout
        self._available = queue.Queue()
        self._in_use = set()
        self._lock = threading.Lock()

        # Pre-warm the pool
        for _ in range(max_size):
            self._available.put(DatabaseConnection())

    def acquire(self):
        try:
            conn = self._available.get(timeout=self.acquire_timeout)
        except queue.Empty:
            raise PoolExhaustedError(
                f"No free objects after {self.acquire_timeout}s — pool size {self.max_size}"
            )
        with self._lock:
            self._in_use.add(conn)
        return conn.open()

    def release(self, conn):
        conn.close()
        with self._lock:
            self._in_use.discard(conn)
        self._available.put(conn)

    @contextmanager
    def pooled(self):
        """Acquire/release via `with pool.pooled() as conn:` — no leaks."""
        conn = self.acquire()
        try:
            yield conn
        finally:
            self.release(conn)

    def size(self):
        return self._available.qsize() + len(self._in_use)


if __name__ == "__main__":
    pool = ConnectionPool(max_size=3)

    with pool.pooled() as conn:
        print(conn.query("SELECT * FROM users"))

    # Second consumer reuses the same object — no new "(expensive)" line
    with pool.pooled() as conn:
        print(conn.query("SELECT * FROM orders"))
