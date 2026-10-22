"""Cache warming: pre-populate Redis before traffic arrives.

Run as a post-deploy step in CI/CD. Find hot keys with `redis-cli --hotkeys`
or from analytics, then warm the top 100-500 of them.
"""
import asyncio
import json

import redis

r = redis.Redis(decode_responses=True)


async def warm_single(key, builder):
    value = await builder(key)
    r.setex(key, 3600, json.dumps(value))


async def warm_cache(keys, builder):
    tasks = [warm_single(key, builder) for key in keys]
    await asyncio.gather(*tasks)


async def fake_builder(key):
    # Replace with the real lookup (DB query, API call, etc.)
    await asyncio.sleep(0.01)
    return {"key": key, "payload": "warmed"}


if __name__ == "__main__":
    hot_keys = [f"product:{i}" for i in range(100)]
    asyncio.run(warm_cache(hot_keys, fake_builder))
    print(f"Warmed {len(hot_keys)} keys")
