# SQL Table Partitioning Strategies — Companion Scripts

Runnable PostgreSQL scripts that accompany the recipe
[Partition Large SQL Tables by Date, Range, or List](https://stackpractices.com/recipes/sql-partitioning-strategies/).

## Files

| Script | What it does |
|--------|--------------|
| `range-partition-by-month.sql` | Monthly range partitioning (time-series default) |
| `list-partition-by-region.sql` | List partitioning + default partition |
| `hash-partition.sql` | Hash partitioning for even distribution |
| `composite-subpartitioning.sql` | Range + list sub-partitioning |
| `verify-partition-pruning.sql` | Static/dynamic pruning checks with EXPLAIN |
| `detach-and-archive.sql` | Instant archive via DETACH PARTITION |
| `pg-partman-automation.sql` | Automatic partition creation/rotation |
| `partition-indexes.sql` | Parent indexes that propagate to children |
| `monitor-partition-sizes.sql` | Hot-partition and size monitoring |
| `foreign-keys-partitioned.sql` | FKs referencing partitioned tables (PG12+) |

## Usage

Requires PostgreSQL 10+ (declarative partitioning); `pg_partman` and
`DETACH ... CONCURRENTLY` need newer versions/extensions.

```bash
psql -d your_db -f range-partition-by-month.sql
```

Remember: the partition key must be part of the prim
