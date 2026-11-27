# Sharding Pattern

Companion code for [Sharding Pattern: Split Data Across Database Servers](https://stackpractices.com/patterns/sharding-pattern/) on StackPractices.

Three routing strategies, one per language:

| File | Strategy | Notes |
|------|----------|-------|
| `shard_manager.py` | Hash-based (`hash(key) % N`) | Redis `ShardManager` with single-key ops and grouped `mget` |
| `directory_shard_manager.js` | Directory-based | Lookup table routing plus live `migrateEntity` between shards |
| `RangeShardRouter.java` | Range-based | Spring `JdbcTemplate` router over contiguous ID boundaries |

## Requirements

- `shard_manager.py` — Python 3.8+, `redis` package, reachable Redis instances at `redis-1..3:6379`.
- `directory_shard_manager.js` — Node.js 18+; expects connection pool objects (`usEastPool`, `euWestPool`, `apSouthPool`) exposing `query(sql, params)`.
- `RangeShardRouter.java` — Spring context providing the `DataSource` list and boundary list.

None of these files include the connections themselves — they are the routing layer you'd place in front of real pools.
