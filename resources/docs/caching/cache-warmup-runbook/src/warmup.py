#!/usr/bin/env python3
"""Cache warmup runner — loads a hot-keys file and preloads tiers in waves.

    python src/warmup.py --keys hot-keys.json --redis localhost:6379 --demo

``--demo`` uses a synthetic loader so you can test the flow without a
database. In production, plug in ``loader(key) -> dict | None`` against
your source of truth (database, service, computed).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

import redis

WORKERS_PER_TIER = {"critical": 20, "high": 15, "medium": 10, "low": 5}
CHUNK_SIZE = 100
CHUNK_PAUSE_S = 0.5

Loader = Callable[[str], "dict | None"]


def demo_loader(key: str) -> "dict | None":
    """Synthetic loader for testing: returns fake payloads per pattern."""
    if key.startswith("session:"):
        return {"key": key, "kind": "session", "user": key.split(":", 1)[1]}
    if key.startswith(("user:", "product:", "config:")):
        return {"key": key, "kind": key.split(":", 1)[0]}
    if key.startswith(("ratelimit:", "stats:")):
        return {"key": key, "value": random.randint(1, 10_000)}
    return {"key": key}


def warmup_key(client: redis.Redis, key: str, loader: Loader, ttl: int) -> bool:
    try:
        if client.exists(key):            # already warm — skip the DB read
            return True
        data = loader(key)
        if data is None:
            return False
        client.setex(key, ttl, json.dumps(data))
        return True
    except (redis.RedisError, OSError) as e:
        print(f"  failed {key}: {e}", file=sys.stderr)
        return False


def warmup_batch(
    client: redis.Redis,
    keys: list[str],
    loader: Loader,
    ttl: int,
    workers: int,
) -> "tuple[int, int]":
    warmed = failed = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(warmup_key, client, k, loader, ttl): k for k in keys}
        for future in as_completed(futures):
            if future.result():
                warmed += 1
            else:
                failed += 1
    return warmed, failed


def health_check(client: redis.Redis) -> bool:
    try:
        client.ping()
        info = client.info()
        print(f"Redis {info['redis_version']}, memory {info['used_memory_human']}")
        return True
    except redis.RedisError as e:
        print(f"Redis not healthy: {e}", file=sys.stderr)
        return False


def progressive_warmup(
    client: redis.Redis,
    key_groups: dict[str, list[str]],
    loader: Loader,
    ttl: int,
    tiers: "tuple[str, ...]" = ("critical", "high", "medium", "low"),
) -> "tuple[int, int]":
    total_ok = total_bad = 0
    for tier in tiers:
        keys = key_groups.get(tier, [])
        if not keys:
            continue
        workers = WORKERS_PER_TIER[tier]
        ok = bad = 0
        for i in range(0, len(keys), CHUNK_SIZE):
            w, f = warmup_batch(client, keys[i:i + CHUNK_SIZE], loader, ttl, workers)
            ok, bad = ok + w, bad + f
            time.sleep(CHUNK_PAUSE_S)      # let the DB breathe between chunks
        print(f"{tier}: {ok} warmed, {bad} failed")
        total_ok, total_bad = total_ok + ok, total_bad + bad
    return total_ok, total_bad


def verify(client: redis.Redis, keys: list[str], sample_size: int = 50) -> float:
    sample = random.sample(keys, min(sample_size, len(keys))) if keys else []
    hits = sum(1 for k in sample if client.exists(k))
    ratio = hits / len(sample) * 100 if sample else 100.0
    print(f"Verification: {hits}/{len(sample)} sampled keys present ({ratio:.1f}%)")
    stats = client.info("stats")
    print(f"Server counters: {stats.get('keyspace_hits', 0)} hits / "
          f"{stats.get('keyspace_misses', 0)} misses")
    return ratio


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keys", required=True, help="hot-keys JSON file")
    parser.add_argument("--redis", default="localhost:6379", help="host:port")
    parser.add_argument("--ttl", type=int, default=3600)
    parser.add_argument("--tiers", default="critical,high",
                        help="comma-separated tiers to warm")
    parser.add_argument("--demo", action="store_true",
                        help="use the synthetic loader instead of a real one")
    args = parser.parse_args()

    if not args.demo:
        parser.error("no production loader configured; "
                     "edit warmup.py and plug in your loader, or run --demo")

    host, _, port = args.redis.partition(":")
    client = redis.Redis(host=host, port=int(port or 6379))
    if not health_check(client):
        sys.exit(1)

    with open(args.keys, encoding="utf-8") as f:
        key_groups = json.load(f)
    tiers = tuple(t.strip() for t in args.tiers.split(",") if t.strip())
    warmed, failed = progressive_warmup(client, key_groups, demo_loader,
                                        args.ttl, tiers)

    wanted = [k for t in tiers for k in key_groups.get(t, [])]
    ratio = verify(client, wanted)
    print(f"Done: {warmed} warmed, {failed} failed")
    sys.exit(0 if ratio >= 80 else 2)


if __name__ == "__main__":
    main()
