# Database Indexing Strategies — Companion Resources

Companion repository for the [Database Indexing Strategies Guide](https://stackpractices.com/guides/indexing-strategies-guide/).

## Contents

| File | Description |
|------|-------------|
| `unused-indexes-audit.sql` | Quarterly audit script to find and drop unused indexes (PostgreSQL + MySQL) |
| `create-index-concurrently-examples.sql` | Production-safe `CREATE INDEX CONCURRENTLY` examples (PostgreSQL + MySQL 8+) |
| `index-monitoring-queries.sql` | Queries to track index usage, cache hit ratio, and bloat |

## Usage

1. **Audit unused indexes quarterly:**
   ```bash
   psql -d your_db -f unused-indexes-audit.sql
   ```

2. **Build indexes safely in production:**
   ```bash
   psql -d your_db -f create-index-concurrently-examples.sql
   ```

3. **Monitor index health:**
   ```bash
   psql -d your_db -f index-monitoring-queries.sql
   ```

## Requirements

- PostgreSQL 12+ (for `CONCURRENTLY`, `pgstattuple`)
- MySQL 8+ (for `ALGORITHM=INPLACE`)
- `pgstattuple` extension for bloat analysis: `CREATE EXTENSION pgstattuple;`

## Related Guide

- [Database Indexing Strategies — From B-Trees to BRIN](https://stackpractices.com/guides/indexing-strategies-guide/)
- [Spanish version](https://stackpractices.com/es/guides/indexing-strategies-guide/)
