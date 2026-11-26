# Lambda + PgBouncer: one warm connection per container, multiplexed server-side.
import os
import psycopg2
from contextlib import contextmanager

DB_HOST = os.environ.get("DB_HOST", "pgbouncer.internal")
DB_PORT = int(os.environ.get("DB_PORT", 6432))
DB_NAME = os.environ.get("DB_NAME", "mydb")
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]

_connection = None


def get_connection():
    global _connection
    if _connection is None or _connection.closed:
        _connection = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASSWORD, connect_timeout=5,
        )
        _connection.autocommit = False
        print("[POOL] New connection via PgBouncer")
    return _connection


@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def handler(event, context):
    user_id = event["pathParameters"]["id"]
    with transaction() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, email FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
    return {"statusCode": 200, "body": {"user": row}}
