"""Load balancing algorithms demo: consistent-hash ring and weighted selection.

Simulates a small backend pool and shows the two selectors that matter in
practice: a consistent-hash ring for cache/session-affine routing, and a
round-robin distribution for comparison. Run: python load_balancer.py
"""

import hashlib
from bisect import bisect
from collections import Counter


class ConsistentHashRing:
    """Hash ring with virtual nodes; removing a node remaps ~1/N of keys."""

    def __init__(self, replicas=150):
        self.replicas = replicas
        self.ring = {}
        self.sorted_keys = []

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key):
        if not self.ring:
            return None
        i = bisect(self.sorted_keys, self._hash(key))
        return self.ring[self.sorted_keys[i % len(self.sorted_keys)]]

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)


def naive_modulo(servers, key):
    """hash(key) % N: correct but remaps almost everything on pool change."""
    return servers[hash(key) % len(servers)]


def smooth_weighted_rr(weights, picks):
    """Nginx-style smooth weighted round-robin: same shares, no bursts."""
    current = {name: 0 for name in weights}
    total = sum(weights.values())
    result = []
    for _ in range(picks):
        best = None
        for name, w in weights.items():
            current[name] += w
            if best is None or current[name] > current[best]:
                best = name
        current[best] -= total
        result.append(best)
    return result


if __name__ == "__main__":
    nodes = ["server-a", "server-b", "server-c"]
    ring = ConsistentHashRing()
    for n in nodes:
        ring.add_node(n)

    keys = [f"user-{i}" for i in range(12)]
    print("== Consistent-hash ring (3 nodes) ==")
    before = {k: ring.get_node(k) for k in keys}
    dist = Counter(before.values())
    print("distribution:", dict(dist))

    ring.remove_node("server-c")
    moved = sum(1 for k in keys if ring.get_node(k) != before[k])
    print(f"after removing server-c: {moved}/{len(keys)} keys remapped (~1/N expected)")

    before_mod = {k: naive_modulo(nodes, k) for k in keys}
    moved_mod = sum(1 for k in keys if naive_modulo(nodes[:-1], k) != before_mod[k])
    print(f"naive hash%N after removal: {moved_mod}/{len(keys)} keys remapped (~all expected)")

    print("\n== Smooth weighted round-robin (5:3:1) ==")
    seq = smooth_weighted_rr({"api1": 5, "api2": 3, "api3": 1}, 9)
    print("sequence:", " ".join(seq))
    print("shares:", dict(Counter(seq)))
