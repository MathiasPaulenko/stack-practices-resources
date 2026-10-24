# NoSQL Database Selection Guide — Companion

Runnable schemas and examples for the [NoSQL Database Selection Guide](https://stackpractices.com/guides/nosql-database-selection-guide/) on StackPractices.com.

## Files

| File | Type | Contents |
|------|------|----------|
| `mongodb_example.js` | mongosh | Embedded product document + nested query |
| `dynamodb_example.py` | Python | Partition/sort-key get and query with boto3 |
| `redis_commands.sh` | Bash | Cache TTL, atomic rate limiting, follower feed sorted set |
| `cassandra.cql` | CQL | Query-first tables: sensor readings and posts_by_user |

## Usage

Each file runs against its own engine — they are per-store reference implementations of the guide's examples, not a single app:

```bash
mongosh nosql_examples mongodb_example.js
python dynamodb_example.py          # needs a Users table (see docstring)
redis-cli < redis_commands.sh
cqlsh -f cassandra.cql
```

## Notes

- The decision matrix in the guide is the actual deliverable — these files exist so the examples can be run, not just read.
- Cassandra's schema is query-first by design: `posts_by_user` exists to serve "recent posts by user", not to model posts in the abstract.
