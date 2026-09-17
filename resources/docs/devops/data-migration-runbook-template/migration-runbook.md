# Data Migration Runbook: `<Migration Name>`

Companion to [Data Migration Runbook Template](https://stackpractices.com/docs/data-migration-runbook-template/) on StackPractices.com. Copy this file, fill in every `______` blank, and rehearse before the production run.

## 1. Pre-Migration Checklist

### Source System

```bash
pg_dump -h source.db.internal -U admin mydb | gzip > /backups/pre-migration.sql.gz
gunzip -t /backups/pre-migration.sql.gz

## Record baseline metrics
psql -h source.db.internal -c "SELECT pg_size_pretty(pg_database_size('mydb'));"
psql -h source.db.internal -c "SELECT COUNT(*) FROM orders;"
psql -h source.db.internal -c "SELECT MAX(updated_at) FROM orders;"
```

| Metric | Value | Notes |
|--------|-------|-------|
| Database size | ______ | |
| Table row counts | ______ | |
| Latest update timestamp | ______ | |
| Active connections | ______ | |
| Replication lag | ______ | |

### Target System

- [ ] Target schema created and matches source structure
- [ ] Target indexes built and validated
- [ ] Target storage capacity > 2x expected data size
- [ ] Network connectivity verified between source and target
- [ ] Target performance baseline established

### Application

- [ ] Feature flags configured for dual-write or read-after-write
- [ ] Application code deployed that supports both old and new systems
- [ ] Monitoring dashboards updated with target system metrics

## 2. Migration Strategy Selection

| Strategy | Downtime | Complexity | Use Case |
|----------|----------|------------|----------|
| Big Bang | Minutes to hours | Low | Small datasets (< 100GB), simple schema |
| Incremental / Batch | Near-zero | Medium | Large datasets, can tolerate eventual consistency |
| Dual Write | Zero | High | Live systems requiring 100% availability |
| CDC (Change Data Capture) | Near-zero | High | Continuous replication, minimal downtime |

### Decision Record

**Selected strategy:** ______

**Justification:** ______

## 3. Dry Run Execution

```bash
## Run migration on a copy of production data
## Do NOT connect to production systems

cp /backups/pre-migration.sql.gz /tmp/dry-run.sql.gz
gunzip /tmp/dry-run.sql.gz

## Execute migration script
psql -h target-staging.db.internal -f /tmp/dry-run.sql

## Validate dry run
./validate-migration.sh \
  --source source-staging.db.internal \
  --target target-staging.db.internal
```

| Dry Run Result | Status |
|----------------|--------|
| Duration | ______ |
| Rows migrated | ______ |
| Errors encountered | ______ |
| Validation passed | [ ] |

**Decision Gate:** Only proceed to production if dry run completed without errors and validation passed.

## 4. Production Migration Execution

### Step 4a: Final Backup

```bash
## Create point-in-time backup immediately before migration
aws rds create-db-snapshot \
  --db-instance-identifier source-db \
  --db-snapshot-identifier pre-migration-$(date +%Y%m%d-%H%M%S)
```

### Step 4b: Stop Writes (if using Big Bang)

```bash
## Set application to read-only
curl -X POST http://app.internal/admin/maintenance-mode

## Verify no active writes
psql -h source.db.internal -c "SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active';"
```

### Step 4c: Execute Migration

```bash
## Log migration start time
MIGRATION_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "Migration started: $MIGRATION_START"

## Execute migration
psql -h target.db.internal -f migration-script.sql 2>&1 | tee migration.log

## Log migration end time
MIGRATION_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "Migration ended: $MIGRATION_END"
```

### Step 4d: Resume Writes (if applicable)

```bash
## Verify target is healthy before switching writes
curl -X POST http://app.internal/admin/target-health-check

## Switch application to target
curl -X POST http://app.internal/admin/switch-datastore \
  -H "Content-Type: application/json" \
  -d '{"target": "new-database"}'

## Resume normal operations
curl -X POST http://app.internal/admin/normal-mode
```

## 5. Post-Migration Validation

### Row Count Verification

```sql
-- Compare row counts for all major tables
SELECT 'source_orders' as table_name, COUNT(*) as row_count FROM source.orders
UNION ALL
SELECT 'target_orders', COUNT(*) FROM target.orders
UNION ALL
SELECT 'source_users', COUNT(*) FROM source.users
UNION ALL
SELECT 'target_users', COUNT(*) FROM target.users;
```

### Data Integrity Checks

```sql
-- Checksum comparison for critical tables
SELECT 'source', SUM(CHECKSUM(id, amount, created_at)) FROM source.payments
UNION ALL
SELECT 'target', SUM(CHECKSUM(id, amount, created_at)) FROM target.payments;

-- Verify no NULL values in required columns
SELECT COUNT(*) FROM target.orders WHERE customer_id IS NULL;
SELECT COUNT(*) FROM target.orders WHERE created_at IS NULL;
```

### Application Smoke Tests

```bash
## Critical user flows
./scripts/smoke-test.sh --environment=production

## Performance baseline comparison
./scripts/performance-test.sh --target=new-db --baseline=old-db
```

| Validation Check | Source | Target | Match | Time |
|------------------|--------|--------|-------|------|
| Total row count | ______ | ______ | [ ] | ______ |
| Table-level counts | ______ | ______ | [ ] | ______ |
| Checksum for payments | ______ | ______ | [ ] | ______ |
| NULL constraint checks | N/A | ______ | [ ] | ______ |
| Smoke tests pass | N/A | ______ | [ ] | ______ |
| Performance within 10% | ______ | ______ | [ ] | ______ |

## 6. Rollback Procedure

### Trigger Conditions

Rollback if ANY of the following occur:

- Error rate > 1% after migration
- Data integrity check fails
- Performance degradation > 50%
- Customer-facing feature broken

### Rollback Steps

```bash
## 1. Stop writes to target immediately
curl -X POST http://app.internal/admin/maintenance-mode

## 2. Switch application back to source
curl -X POST http://app.internal/admin/switch-datastore \
  -d '{"target": "source-database"}'

## 3. Resume operations on source
curl -X POST http://app.internal/admin/normal-mode

## 4. DO NOT DELETE target data until root cause is resolved
## 5. Document all findings for postmortem
```

| Rollback Step | Status | Time |
|---------------|--------|------|
| Maintenance mode activated | [ ] | ______ |
| Source restored as primary | [ ] | ______ |
| Application switched | [ ] | ______ |
| Smoke tests passed on source | [ ] | ______ |
| Target data preserved | [ ] | ______ |

## 7. Post-Migration Actions

- [ ] Monitor target system for 24 hours minimum
- [ ] Compare error rates between pre and post migration
- [ ] Validate backup of target system
- [ ] Update runbook with actual duration and issues encountered
- [ ] Schedule cleanup of source data (after 30-day retention)
- [ ] Document lessons learned
- [ ] Close incident channel when stable
