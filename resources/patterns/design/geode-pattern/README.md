# Geode Pattern

Companion resources for the [Geode Pattern](https://stackpractices.com/patterns/geode-pattern/) on StackPractices.

Three runnable implementations of a partitioned cluster: each node owns a hash range, stores its own data, and fails in isolation. The demos insert users, print shard stats, then kill a node to show that only its shard is affected.

## Files

| File | Description |
|------|-------------|
| `geode_cluster.py` | Python (dataclasses + hashlib); run with `python geode_cluster.py` |
| `geode_cluster.js` | Node.js (crypto + Map); run with `node geode_cluster.js` |
| `GeodeCluster.java` | Java 16+ (MessageDigest + HashMap); run with `javac GeodeCluster.java && java GeodeCluster` |

## What to try

- Add a `restore_node`/`restoreNode` method and bring `node-2` back mid-run.
- Change `num_nodes` and watch how fixed ranges redistribute every key — then look up consistent hashing to see why production systems avoid fixed ranges.
- Log which node each user lands on and check the distribution is roughly even.

## Notes

- `owns_key`/`ownsKey` is the single source of routing truth — `find_node`/`findNode` delegates to it so the ownership check never drifts.
- No replication or rebalancing here by design; the pattern page covers consistent hashing and virtual nodes for that.
