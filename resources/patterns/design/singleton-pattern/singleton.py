"""Thread-safe Singleton in Python.

The naive `__new__` singleton has two traps:
  1. `__init__` re-runs on every `Singleton()` call and re-initializes state.
  2. The check-then-act inside `__new__` is not atomic — the GIL does not
     make it safe; two threads can race between the None check and assignment.

This version guards creation with a lock and skips re-init.
Prefer the simpler module-level instance (see connection_pool.py) in real code.
"""

import threading


class ConnectionPool:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.connections = []
        self.max_connections = 10
        self._initialized = True

    def acquire(self):
        if len(self.connections) >= self.max_connections:
            raise RuntimeError("pool exhausted")
        conn = f"conn-{len(self.connections)}"
        self.connections.append(conn)
        return conn

    def release(self, conn):
        if conn in self.connections:
            self.connections.remove(conn)


if __name__ == "__main__":
    a = ConnectionPool()
    b = ConnectionPool()
    assert a is b
    conn = a.acquire()
    assert conn in b.connections
    b.acquire()
    assert len(a.connections) == 2
    print("singleton ok:", a is b, "| connections:", len(a.connections))
