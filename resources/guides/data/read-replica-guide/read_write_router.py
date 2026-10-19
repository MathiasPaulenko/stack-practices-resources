"""Read/write splitting with two psycopg2 connection pools."""
import psycopg2
from contextlib import contextmanager

primary_pool = psycopg2.pool.ThreadedConnectionPool(1, 10, dsn="dbname=app host=primary")
replica_pool = psycopg2.pool.ThreadedConnectionPool(1, 10, dsn="dbname=app host=replica1")


@contextmanager
def get_db_connection(read_only=False):
    """Get a connection: primary for writes, replica for reads."""
    pool = replica_pool if read_only else primary_pool
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)


def get_user(user_id):
    with get_db_connection(read_only=True) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()


def update_user(user_id, data):
    with get_db_connection(read_only=False) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = %s WHERE id = %s", (data["name"], user_id))
        conn.commit()
