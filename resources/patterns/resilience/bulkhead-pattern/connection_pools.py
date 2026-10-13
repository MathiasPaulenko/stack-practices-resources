# connection_pools.py — Separate database connection pools per service.
# Requires: pip install psycopg2-binary
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager


class IsolatedConnectionPools:
    """Maintains separate database connection pools per service.
    Critical services can't be starved by non-critical ones."""

    def __init__(self):
        self._pools = {}

    def configure(self, service_name, db_url, min_conn, max_conn):
        self._pools[service_name] = pool.ThreadedConnectionPool(
            minconn=min_conn,
            maxconn=max_conn,
            dsn=db_url
        )

    @contextmanager
    def get_connection(self, service_name):
        if service_name not in self._pools:
            raise ValueError(f"No pool for {service_name}")

        conn = self._pools[service_name].getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pools[service_name].putconn(conn)

    def close_all(self):
        for p in self._pools.values():
            p.closeall()


if __name__ == "__main__":
    pools = IsolatedConnectionPools()

    # Payment: critical, gets more connections
    pools.configure("payment", "postgresql://db:5432/shop", min_conn=5, max_conn=20)

    # Analytics: non-critical, fewer connections
    pools.configure("analytics", "postgresql://db:5432/shop", min_conn=2, max_conn=5)

    def process_payment(order_id):
        with pools.get_connection("payment") as conn:
            cur = conn.cursor()
            cur.execute("UPDATE orders SET status='paid' WHERE id=%s", (order_id,))
            return cur.rowcount

    def log_analytics(event):
        with pools.get_connection("analytics") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO analytics_events (event) VALUES (%s)", (event,))
