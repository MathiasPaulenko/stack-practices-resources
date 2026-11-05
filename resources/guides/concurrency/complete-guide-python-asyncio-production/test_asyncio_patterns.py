# test_asyncio_patterns.py — pytest-asyncio tests for the patterns.
import asyncio

import pytest

from token_bucket import AsyncTokenBucket


@pytest.mark.asyncio
async def test_gather_results():
    async def fetch(url):
        await asyncio.sleep(0.01)
        return {"url": url, "status": "ok"}

    results = await asyncio.gather(fetch("a"), fetch("b"))
    assert len(results) == 2


@pytest.mark.asyncio
async def test_timeout_fires():
    async def slow():
        await asyncio.sleep(10)

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow(), timeout=0.05)


@pytest.mark.asyncio
async def test_cancellation_cleanup():
    cleaned = []

    async def worker():
        try:
            await asyncio.sleep(10)
        finally:
            cleaned.append(True)

    task = asyncio.create_task(worker())
    await asyncio.sleep(0.01)
    task.cance
