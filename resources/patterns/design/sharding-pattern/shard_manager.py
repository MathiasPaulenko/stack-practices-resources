"""Hash-based sharding across multiple Redis instances.

Each key maps to exactly one shard via `hash(key) % num_shards`.
Batch reads (mget) group keys by shard to issue one MGET per node.
"""

import hashlib
import json
import redis
from typing import Any, Dict, List


class ShardManager:
    """Routes keys to Redis shards using hash-based sharding."""

    def __init__(self, shards: List[redis.Redis]):
        self.shards = shards
        self.num_shards = len(shards)

    def _get_shard_index(self, key: str) -> int:
        """Map a key to a shard index via its MD5 hash."""
        hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
        return hash_value % self.num_shards

    def get(self, key: str):
        shard = self.shards[self._get_shard_index(key)]
        return shard.get(key)

    def set(self, key: str, value: str):
        shard = self.shards[self._get_shard_index(key)]
        return shard.set(key, value)

    def delete(self, key: str):
        shard = self.shards[self._get_shard_index(key)]
        return shard.delete(key)

    def mget(self, keys: List[str]) -> Dict[str, Any]:
        """Batch get: group keys by shard, then issue one MGET per shard."""
        shard_keys: Dict[int, List[str]] = {}
        for key in keys:
            idx = self._get_shard_index(key)
            shard_keys.setdefault(idx, []).append(key)

        results = {}
        for idx, shard_keys_batch in shard_keys.items():
            values = self.shards[idx].mget(shard_keys_batch)
            results.update(dict(zip(shard_keys_batch, values)))
        return results


if __name__ == "__main__":
    shards = [
        redis.Redis(host="redis-1", port=6379, db=0),
        redis.Redis(host="redis-2", port=6379, db=0),
        redis.Redis(host="redis-3", port=6379, db=0),
    ]

    manager = ShardManager(shards)

    # Data is distributed across shards by key hash
    manager.set("user:1001", json.dumps({"name": "Alice", "region": "US"}))
    manager.set("user:1002", json.dumps({"name": "Bob", "region": "EU"}))
    manager.set("user:1003", json.dumps({"name": "Carol", "region": "APAC"}))

    # Reads route to the owning shard transparently
    user = manager.get("user:1001")
    print(user)
