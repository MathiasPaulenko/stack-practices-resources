# http_pool.py — aiohttp connection pool with concurrency cap.
import asyncio

import aiohttp


class HttpClientPool:
    """One session + connector pool + semaphore; close() on shutdown."""

    def __init__(self, pool_size: int = 100, timeout: float = 30.0):
        self.pool_size = pool_size
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: aiohttp.ClientSession | None = None
        self.semaphore = asyncio.Semaphore(pool_size)

    async def start(self) -> None:
        connector = aiohttp.TCPConnector(
            limit=self.pool_size,
            limit_per_host=20,
            ttl_dns_cache=300,
        )
        self.session = aiohttp.ClientSession(
            connector=connector, timeout=self.timeout
        )

    async def fetch(self, url: str):
        async with self.semaphore:
            async with self.session.get(url) as response:
                return await response.json()

    async def close(self) -> None:
        if self.session:
            await self.session.close()
