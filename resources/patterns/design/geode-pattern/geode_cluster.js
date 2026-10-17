const crypto = require('crypto');

class GeodeNode {
  constructor(nodeId, shardStart, shardEnd) {
    this.nodeId = nodeId;
    this.shardRange = [shardStart, shardEnd];
    this.data = new Map();
    this.healthy = true;
  }

  ownsKey(key) {
    const h = parseInt(
      crypto.createHash('md5').update(key).digest('hex'), 16
    ) % 10000;
    return h >= this.shardRange[0] && h <= this.shardRange[1];
  }

  get(key) {
    if (!this.healthy) throw new Error(`Node ${this.nodeId} is down`);
    return this.data.get(key);
  }

  put(key, value) {
    if (!this.healthy) throw new Error(`Node ${this.nodeId} is down`);
    this.data.set(key, value);
  }
}

class GeodeCluster {
  constructor(numNodes = 4) {
    this.nodes = [];
    const shardSize = Math.floor(10000 / numNodes);
    for (let i = 0; i < numNodes; i++) {
      const start = i * shardSize;
      const end = i < numNodes - 1 ? start + shardSize - 1 : 9999;
      this.nodes.push(new GeodeNode(`node-${i}`, start, end));
    }
  }

  findNode(key) {
    return this.nodes.find(n => n.ownsKey(key)) || null;
  }

  get(key) {
    const node = this.findNode(key);
    if (!node) throw new Error(`No node owns key: ${key}`);
    return node.get(key);
  }

  put(key, value) {
    const node = this.findNode(key);
    if (!node) throw new Error(`No node owns key: ${key}`);
    node.put(key, value);
  }

  failNode(nodeId) {
    const node = this.nodes.find(n => n.nodeId === nodeId);
    if (node) node.healthy = false;
  }

  stats() {
    return this.nodes.map(n => ({
      nodeId: n.nodeId, keys: n.data.size,
      healthy: n.healthy, range: n.shardRange,
    }));
  }
}

// Usage
const cluster = new GeodeCluster(4);
const users = [
  "alice", "bob", "carol", "dave", "eve", "frank", "grace", "heidi",
];
users.forEach(u =>
  cluster.put(u, { email: `${u}@example.com`, score: u.length * 10 }));

cluster.stats().forEach(s => console.log("  ", s));

console.log("\n=== Simulate node-2 failure ===");
cluster.failNode("node-2");
users.forEach(u => {
  const node = cluster.findNode(u);
  try {
    cluster.get(u);
    console.log(`  ${u} -> ${node.nodeId}: OK`);
  } catch (e) {
    console.log(`  ${u} -> ${node.nodeId}: FAILED (${e.message})`);
  }
});
