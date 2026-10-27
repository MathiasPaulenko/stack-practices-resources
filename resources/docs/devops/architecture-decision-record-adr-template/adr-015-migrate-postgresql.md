# ADR-015: Migrate to PostgreSQL as primary data store

## Status
Accepted (2026-07-11)

## Context
The application has used MySQL 5.7 since 2023. With team and data growth, we have hit limitations:
- No JSONB support or native JSON queries
- Limited logical replication compared to PostgreSQL
- No declarative partitioning
- MySQL Enterprise licensing costs

The platform team needs table-level partitioning to handle the events table growth (currently 2TB, growing 50% annually).

## Decision
Migrate to PostgreSQL 16 as the primary database.

## Alternatives Considered

### 1. Stay on MySQL 8.0
- Pros: Simpler migration, team familiarity
- Cons: Weaker JSONB, limited partitioning
- Rejected: Does not solve partitioning requirement

### 2. Migrate to Amazon Aurora PostgreSQL
- Pros: PostgreSQL compatible, managed, global replication
- Cons: Higher cost, vendor lock-in
- Deferred: Evaluate after self-managed PostgreSQL migration

### 3. Migrate to CockroachDB
- Pros: Distributed, PostgreSQL-compatible SQL
- Cons: Cost, complexity, no team experience
- Rejected: Over-engineering for current needs

## Consequences

### Positive
- Native declarative partitioning
- JSONB for semi-structured data
- Solid logical replication

### Negative
- Team learning curve (2-4 weeks)
- Need to migrate MySQL-specific queries

### Mitigations
- Team training on PostgreSQL before migration
- Use pgloader for automatic schema and data migration
- Keep MySQL in parallel for 30 days as fallback

## Implementation Notes
1. Phase 1: Set up PostgreSQL in staging, migrate schema with pgloader
2. Phase 2: Migrate data in staging, run application tests
3. Phase 3: Migrate production with planned downtime
4. Phase 4: Monitor for 30 days, decommission MySQL

## Change Log
| Date | Change | Author |
|------|--------|--------|
| 2026-07-04 | Proposed | alice@example.com |
| 2026-07-11 | Accepted | platform-team |
