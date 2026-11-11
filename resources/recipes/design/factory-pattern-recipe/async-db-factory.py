"""Async factory with lazy connection pooling (asyncpg / Python 3.10+).

Requires a running PostgreSQL and `pip install asyncpg`. The double-checked
locking inside `create()` makes the pool initialization coroutine-safe.
"""
import asyncio
from typing import Optional

import asyncpg


class DatabaseConnectionFactory:
    _pool: Optional[asyncpg.Pool] = None
    _lock = asyncio.Lock()

    @classmethod
    async def create(cls, config: dict) -> "DatabaseConnection":
        if cls._pool is None:
            async with cls._lock:
                if cls._pool is None:
                    cls._pool = await asyncpg.create_pool(
                        dsn=config["url"],
                        min_size=config.get("min_pool", 5),
                        max_size=config.get("max_pool", 20),
                        command_timeout=config.get("timeout", 30),
                    )
        return DatabaseConnection(await cls._pool.acquire())

    @classmethod
    async def close(cls) -> None:
        if cls._pool:
            await cls._pool.close()
            cls._pool = None


class DatabaseConnection:
    def __init__(self, conn):
        self._conn = conn

    async def query(self, sql: str, *args) -> list:
        return await self._conn.fetch(sql, *args)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._conn.close()


async def main():
    config = {"url": "postgresql://localhost/mydb", "max_pool": 10}
    async with await DatabaseConnectionFactory.create(config) as db:
        users = await db.query("SELECT * FROM users WHERE active = $1", True)
        print(users)
    await DatabaseConnectionFactory.close()


if __name__ == "__main__":
    asyncio.run(main())
