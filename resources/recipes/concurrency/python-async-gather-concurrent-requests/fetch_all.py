"""Runnable companion for the "Concurrent HTTP Requests with asyncio.gather" recipe.

Usage:
    pip install -r requirements.txt
    python fetch_all.py

Fetches 5 endpoints concurrently with a semaphore, per-request timeout and
per-result error handling. Adjust URLS and MAX_CONCURRENT as needed.
"""

import asyncio
import time

import aiohttp

URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/status/404",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/html",
]
MAX_CONCURRENT = 3
TIMEOUT = aiohttp.ClientTimeout(total=10, connect=5)


async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch one URL; return status plus a content preview."""
    async with session.get(url, timeout=TIMEOUT) as response:
        text = await response.text()
        return {"url": url, "status": response.status, "bytes": len(text)}


async def fetch_all(urls: list[str]) -> list[dict | BaseException]:
    """Fetch all URLs concurrently with a semaphore and error capture."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async def bounded(url: str):
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [bounded(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)


def main() -> None:
    start = time.perf_counter()
    results = asyncio.run(fetch_all(URLS))
    elapsed = time.perf_counter() - start

    for result in results:
        if isinstance(result, BaseException):
            print(f"FAILED: {result}")
        else:
            print(f"{result['status']}  {result['bytes']:>6}B  {result['url']}")
    print(f"\n{len(results)} requests in {elapsed:.2f}s (sequential would take ~4-5s)")


if __name__ == "__main__":
    main()
