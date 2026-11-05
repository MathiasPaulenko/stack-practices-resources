"""Connection pooling examples — requires a running PostgreSQL.

  pip install psycopg2-binary asyncpg

Sync:  psycopg2.pool.ThreadedConnectionPool (min 5 / max 20 as a start)
Async: asyncpg.create_pool — the standard choice for asyncio workloads.

Sizing: 5-20 connections per app instance; the fleet total must stay
under max_connections (default 100 in PostgreSQL). Past that, put
PgBouncer in transaction mode in front.
"""

import psycopg2
from psycopg2 import pool

DSN = "dbname=app user=postgres password=password host=localhost"


# ---- Bad: a fresh connection per call (30-60 ms overhead each) ----

def get_user_slow(user_id):
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# ---- Good: a shared pool ----

connection_pool = pool.ThreadedConnectionPool(minconn=5, maxconn=20, dsn=DSN)


def get_user_fast(user_id):
    conn = connection_pool.getconn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()
    finally:
        connection_pool.putconn(conn)  # always return the connection


# ---- Async variant ----

ASYNC_EXAMPLE = '''
import asyncpg
import asyncio

async def main():
    pool = await asyncpg.create_pool(
        host="localhost", database="app",
        user="postgres", password="password",
        min_size=5, max_size=20,
    )
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1", 123
        )
        print(user)
    await pool.close()

asyncio.run(main())
'''

if __name__ == "__main__":
    print("Pool-based get_user_fast ready. Async variant:")
    print(ASYNC_EXAMPLE)
