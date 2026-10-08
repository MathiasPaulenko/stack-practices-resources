"""Concurrent URL fetching with asyncio: TaskGroup fan-out plus a semaphore cap.

Requires: pip install aiohttp
Run: python fetch_urls.py https://example.com https://example.org
"""

import asyncio
import sys

import aiohttp


async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return {"url": url, "status": response.status}


async def fetch_all_urls(urls: list[str]) -> list[dict]:
    """Fan-out with structured concurrency: one failure cancels the group."""
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_url(session, url)) for url in urls]
        return [task.result() for task in tasks]


async def fetch_with_limit(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    """Same fan-out, but a semaphore caps how many requests are in flight."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_fetch(session: aiohttp.ClientSession, url: str) -> dict:
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[bounded_fetch(session, url) for url in urls]
        )


if __name__ == "__main__":
    urls = sys.argv[1:] or [
        "https://api.example.com/users/1",
        "https://api.example.com/users/2",
    ]
    for result in asyncio.run(fetch_all_urls(urls)):
        print(result)
