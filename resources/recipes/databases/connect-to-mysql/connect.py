# Connect to MySQL with mysql-connector-python: pool, context manager, retry.
# pip install mysql-connector-python tenacity
import os
from contextlib import contextmanager

import mysql.connector
from mysql.connector import pooling
from tenacity import retry, stop_after_attempt, wait_exponential

mysql_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "mydb"),
    user=os.getenv("DB_USER", "user"),
    password=os.getenv("DB_PASSWORD", "pass"),
    # Local dev needs no SSL; in production set ssl_ca + ssl_verify_cert=True.
    connection_timeout=5,
    charset="utf8mb4",
)


@contextmanager
def get_db_cursor():
    conn = mysql_pool.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        yield cursor
        conn.commit()
        cursor.close()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()  # returns the connection to the pool


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def get_user(user_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()


if __name__ == "__main__":
    print(get_user(1))

    with get_db_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM users WHERE active = %s", (True,))
        print(cur.fetchone())
