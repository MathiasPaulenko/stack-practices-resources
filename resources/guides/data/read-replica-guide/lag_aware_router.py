"""Lag-aware routing: measure replica lag before deciding where a read goes,
plus a read-after-write wrapper with primary fallback."""


class LagAwareRouter:
    def __init__(self, primary, replica, max_lag_seconds=5):
        self.primary = primary
        self.replica = replica
        self.max_lag = max_lag_seconds

    def get_replica_lag(self):
        """Current replication lag in seconds (PostgreSQL)."""
        cursor = self.replica.cursor()
        cursor.execute(
            """
            SELECT
                EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))
            AS lag_seconds
            """
        )
        return cursor.fetchone()[0] or 0

    def route_query(self, query, requires_freshness=False):
        """Route to replica if lag is acceptable and freshness isn't required."""
        if requires_freshness:
            return self.primary

        lag = self.get_replica_lag()
        if lag > self.max_lag:
            return self.primary

        return self.replica


def read_after_write(conn_master, conn_replica, query, params, max_wait=2.0):
    """Read from the replica, falling back to the primary when lag is high."""
    with conn_master.cursor() as cur:
        cur.execute(
            """
            SELECT EXTRACT(EPOCH FROM (now() - replay_lag))::float
            FROM pg_stat_replication LIMIT 1
            """
        )
        lag = cur.fetchone()[0] or 0

    if lag > max_wait:
        with conn_master.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    try:
        with conn_replica.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    except Exception:
        with conn_master.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
