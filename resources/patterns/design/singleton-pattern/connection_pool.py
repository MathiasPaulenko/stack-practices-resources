"""Module-level Singleton — the idiomatic Python approach.

Python modules are imported once and cached in sys.modules, so a module-level
instance is a thread-safe singleton for free. Every importer gets this same
`pool` object.

Usage:
    from connection_pool import pool
    conn = pool.getconn()
    pool.putconn(conn)
"""

# In production, initialize the real pool, e.g.:
#
# import psycopg2.pool
# pool = psycopg2.pool.ThreadedConnectionPool(
#     minconn=2, maxconn=10,
#     dsn="postgresql://user:pass@localhost/db",
# )


class _Pool:
    """Stand-in pool so this file runs without psycopg2 installed."""

    def __init__(self):
        self._free = [f"conn-{i}" for i in range(10)]
        self._used = set()

    def getconn(self):
        conn = self._free.pop()
        self._used.add(conn)
        return conn

    def putconn(self, conn):
        self._used.discard(conn)
        self._free.append(conn)


pool = _Pool()

if __name__ == "__main__":
    # Two separate importers receive the same object:
    import importlib
    first = importlib.import_module("connection_pool").pool
    importlib.invalidate_caches()
    second = importlib.import_module("connection_pool").pool
    assert first is second
    c = pool.getconn()
    assert c in pool._used
    pool.putconn(c)
    print("module singleton ok — same object for every import")
