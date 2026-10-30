#!/usr/bin/env python3
"""Hot-key extraction for cache warmup.

Two strategies:
  * ``--logs``: aggregate ``cache_key`` fields from JSONL access logs.
  * ``--lfu``: rank keys by Redis LFU counter (requires a
    ``maxmemory-policy`` of ``allkeys-lfu`` or ``volatile-lfu``).

Output is a JSON file with keys grouped by priority tier
(``critical`` / ``high`` / ``medium`` / ``low``), ready for warmup.py.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from typing import Iterable

TIER_PATTERNS = {
    "critical": re.compile(r"^(session|auth|token):"),
    "high": re.compile(r"^(user|product|config):"),
    "medium": re.compile(r"^(ratelimit|stats):"),
}


def tier_of(key: str) -> str:
    for tier, pattern in TIER_PATTERNS.items():
        if pattern.match(key):
            return tier
    return "low"


def from_logs(log_path: str, top_n: int = 1000) -> list[str]:
    """Aggregate cache keys from JSONL access logs (last ~24 h)."""
    counter: Counter[str] = Counter()
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = entry.get("cache_key")
            if isinstance(key, str):
                counter[key] += 1
    return [key for key, _ in counter.most_common(top_n)]


def from_lfu(host: str, port: int, top_n: int = 100) -> list[str]:
    """Rank keys by LFU counter. Needs an LFU maxmemory-policy."""
    import redis

    client = redis.Redis(host=host, port=port, db=0)
    ranked: list[tuple[str, int]] = []
    for key in client.scan_iter(count=5000):  # SCAN, never KEYS, in prod
        try:
            freq = client.object("FREQ", key)
        except redis.ResponseError:
            continue  # LFU counter unavailable for this key/policy
        if freq:
            ranked.append((key.decode() if isinstance(key, bytes) else key, freq))
    ranked.sort(key=lambda item: item[1], reverse=True)
    return [key for key, _ in ranked[:top_n]]


def group_by_tier(keys: Iterable[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {t: [] for t in ("critical", "high", "medium", "low")}
    for key in keys:
        groups[tier_of(key)].append(key)
    return {tier: ks for tier, ks in groups.items() if ks}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--logs", metavar="PATH", help="JSONL access log")
    source.add_argument("--lfu", action="store_true", help="rank via OBJECT FREQ")
    parser.add_argument("--redis", default="localhost:6379", help="host:port")
    parser.add_argument("--top", type=int, default=1000)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.logs:
        keys = from_logs(args.logs, args.top)
    else:
        host, _, port = args.redis.partition(":")
        keys = from_lfu(host, int(port or 6379), args.top)

    groups = group_by_tier(keys)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2)
    total = sum(len(v) for v in groups.values())
    print(f"Wrote {total} keys to {args.output}: "
          + ", ".join(f"{t}={len(k)}" for t, k in groups.items()))


if __name__ == "__main__":
    main()
