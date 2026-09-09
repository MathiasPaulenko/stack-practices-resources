"""PostgreSQL connection pool example using psycopg2."""

import psycopg2
from psycopg2 import pool
from contextlib import contextmanager


# Threaded connection pool: minconn kept warm, maxconn is the ceiling
pg_pool = pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host="localhost",
    database="app",
    user="app",
    password="secret",
)


@contextmanager
def get_conn():
    """Borrow a connection, yield it, always return it to the pool."""
    conn = pg_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pg_pool.putconn(conn)


def get_user(user_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()


def pool_status() -> dict:
    """Return current pool metrics for monitoring."""
    return {
        "minconn": pg_pool.minconn,
        "maxconn": pg_pool.maxconn,
        "closed": pg_pool._closed,
    }


if __name__ == "__main__":
    row = get_user(1)
    print(f"User row: {row}")
    print(f"Pool status: {pool_status()}")