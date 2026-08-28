"""Read-after-write handler with replication lag fallback.

Checks replication lag before reading from a replica. If lag exceeds the
threshold, reads from the primary instead.
"""

import psycopg2


def read_after_write(conn_master, conn_replica, query, params, max_wait=2.0):
    """Read from replica with fallback to master if lag is too high.

    Args:
        conn_master: psycopg2 connection to the primary.
        conn_replica: psycopg2 connection to the replica.
        query: SQL query string.
        params: Query parameters tuple.
        max_wait: Maximum acceptable lag in seconds.

    Returns:
        Query results as a list of tuples.
    """
    with conn_master.cursor() as cur:
        cur.execute("""
            SELECT EXTRACT(EPOCH FROM (now() - replay_lag))::float
            FROM pg_stat_replication LIMIT 1
        """)
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


if __name__ == "__main__":
    master = psycopg2.connect("postgresql://user:pass@localhost:5432/app")
    replica = psycopg2.connect("postgresql://user:pass@localhost:5433/app")

    results = read_after_write(
        master, replica,
        "SELECT * FROM users WHERE id = %s",
        (1,),
        max_wait=1.0,
    )
    print(f"Results: {results}")

    master.close()
    replica.close()
