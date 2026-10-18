"""Connect to PostgreSQL with psycopg2: pool, context manager, and retry."""
import os
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from tenacity import retry, stop_after_attempt, wait_exponential

DB_CONFIG = dict(
    host=os.environ.get("PGHOST", "localhost"),
    database=os.environ.get("PGDATABASE", "mydb"),
    user=os.environ.get("PGUSER", "user"),
    password=os.environ.get("PGPASSWORD", "pass"),
    # use "verify-full" with sslrootcert in production
    sslmode=os.environ.get("PGSSLMODE", "prefer"),
)

pg_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, **DB_CONFIG)


@contextmanager
def get_db_cursor():
    conn = pg_pool.getconn()
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        yield cursor
        conn.commit()
        cursor.close()
    except Exception:
        conn.rollback()
        raise
    finally:
        pg_pool.putconn(conn)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def query_with_retry(sql, params):
    with get_db_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def bulk_insert_copy(rows):
    """COPY is 10-100x faster than individual INSERTs for large datasets."""
    import io

    buf = io.StringIO()
    for row_id, email in rows:
        buf.write(f"{row_id}\t{email}\n")
    buf.seek(0)

    with get_db_cursor() as cur:
        cur.copy_from(buf, "users", columns=("id", "email"))


if __name__ == "__main__":
    rows = query_with_retry("SELECT * FROM users WHERE active = %s", (True,))
    for row in rows:
        print(row)
    pg_pool.closeall()
