"""Export pool metrics to Prometheus and alert on exhaustion signals.

Graph three series per service: active connections, pending waiters and
acquire-wait latency. Waiters > 0 while active == max means the pool is
the bottleneck. Pair with pg_stat_activity on the database side.

See https://stackpractices.com/guides/connection-pooling-deep-dive-guide/
"""
import time

from prometheus_client import Counter, Gauge, start_http_server

pool_active = Gauge("db_pool_connections_active", "Connections currently in use")
pool_idle = Gauge("db_pool_connections_idle", "Idle connections in the pool")
pool_waiters = Gauge("db_pool_waiters", "Threads waiting for a connection")
pool_timeouts = Counter("db_pool_timeouts_total", "Connection acquire timeouts")
pool_wait_seconds = Gauge("db_pool_wait_seconds", "Avg acquire wait time")


def monitor_pool(pool):
    """Call on a schedule (e.g. every 15s) with your pool object."""
    pool_active.set(pool.size())
    pool_idle.set(pool.maxsize - pool.size())
    # Alert externally if waiters > 0 or active == max for > 30s.


if __name__ == "__main__":
    start_http_server(9100)
    while True:
        # monitor_pool(my_pool)
        time.sleep(15)
