from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import hashlib

@dataclass
class GeodeNode:
    node_id: str
    shard_range: tuple
    data: Dict[str, Any] = field(default_factory=dict)
    healthy: bool = True

    def owns_key(self, key: str) -> bool:
        h = int(hashlib.md5(key.encode()).hexdigest(), 16) % 10000
        return self.shard_range[0] <= h <= self.shard_range[1]

    def get(self, key: str) -> Optional[Any]:
        if not self.healthy:
            raise RuntimeError(f"Node {self.node_id} is down")
        return self.data.get(key)

    def put(self, key: str, value: Any) -> None:
        if not self.healthy:
            raise RuntimeError(f"Node {self.node_id} is down")
        self.data[key] = value

class GeodeCluster:
    def __init__(self, num_nodes: int = 4):
        shard_size = 10000 // num_nodes
        self.nodes: List[GeodeNode] = [
            GeodeNode(
                node_id=f"node-{i}",
                shard_range=(
                    i * shard_size,
                    i * shard_size + shard_size - 1
                    if i < num_nodes - 1 else 9999,
                ),
            )
            for i in range(num_nodes)
        ]

    def find_node(self, key: str) -> Optional[GeodeNode]:
        return next((n for n in self.nodes if n.owns_key(key)), None)

    def get(self, key: str) -> Optional[Any]:
        node = self.find_node(key)
        if node is None:
            raise KeyError(f"No node owns key: {key}")
        return node.get(key)

    def put(self, key: str, value: Any) -> None:
        node = self.find_node(key)
        if node is None:
            raise KeyError(f"No node owns key: {key}")
        node.put(key, value)

    def fail_node(self, node_id: str) -> None:
        for n in self.nodes:
            if n.node_id == node_id:
                n.healthy = False

    def stats(self) -> List[dict]:
        return [{"node_id": n.node_id, "keys": len(n.data),
                 "healthy": n.healthy, "range": n.shard_range}
                for n in self.nodes]

# Usage
cluster = GeodeCluster(num_nodes=4)
users = ["alice", "bob", "carol", "dave", "eve", "frank", "grace", "heidi"]
for u in users:
    cluster.put(u, {"email": f"{u}@example.com", "score": len(u) * 10})

for s in cluster.stats():
    print(f"  {s}")

print("\n=== Simulate node-2 failure ===")
cluster.fail_node("node-2")
for u in users:
    node = cluster.find_node(u)
    try:
        cluster.get(u)
        print(f"  {u} -> {node.node_id}: OK")
    except RuntimeError as e:
        print(f"  {u} -> {node.node_id}: FAILED ({e})")
