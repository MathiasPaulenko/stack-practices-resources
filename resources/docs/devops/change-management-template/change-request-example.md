# Change Request: Add composite index on orders table

## 1. Change Summary

| Field | Value |
|-------|-------|
| Change ID | `CHG-2026-0142` |
| Title | Add composite index `orders(user_id, created_at)` |
| Requester | `@maria.chen` |
| Team | `platform` |
| Environment | `production` |
| Scheduled Date / Time | `2026-10-22 09:00 UTC` |
| Duration (expected) | `20 minutes` |
| Risk Level | `High` |

## 2. Change Description

**What is changing?**
Adding a composite index on `orders(user_id, created_at)` to fix the 1.8s p95
on the order-history endpoint. The migration runs `CREATE INDEX CONCURRENTLY`
so the table stays writable during the build.

**Why is it needed?**
INC-3391 — order-history queries time out for accounts with > 2M orders.

**What are the expected results?**
p95 latency for `/orders/history` drops from 1.8s to under 300ms. Verified in
staging on a production-size dataset.

## 3. Impact Analysis

| System / Service | Impact | Validation Method |
|------------------|--------|-------------------|
| orders Postgres (primary) | Index build on an 8GB table, ~15 min | `pg_stat_progress_create_index` |
| order-history API | Read-only; no code change | Smoke test + Grafana latency panel |
| Reporting replica | Replication lag possible during build | `pg_stat_replication` lag metric |

### Dependencies
- [x] No dependent services affected
- [x] Dependent services notified: `#team-data` (read-replica consumers)
- [x] External partners / customers notified: n/a — no downtime expected

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Index build locks writes | Low | High | `CONCURRENTLY` avoids the lock; tested on staging |
| Replication lag breaks dashboards | Medium | Medium | Run in the 09:00 UTC low-traffic window; watch lag |
| Disk space exhausted | Low | Medium | 40GB free; index needs ~6GB |

## 4. Rollback Plan

| Condition | Rollback Action | Time to Complete | Owner |
|-----------|----------------|-------------------|-------|
| Lock contention blocks writes > 60s | `pg_cancel_backend` on the index build, retry off-peak | 2 min | `@maria.chen` |
| Replication lag > 5 min | Pause build; resume when lag clears | 10 min | `@maria.chen` |
| Query plan regresses other queries | `DROP INDEX CONCURRENTLY orders_user_created_idx` | 5 min | `@dba-on-call` |

- [x] Rollback tested in staging (index dropped cleanly)
- [x] Rollback command documented in `runbooks/postgres-index-ops.md`
- [x] Schema snapshot taken 2026-10-21
- [x] Feature flag kill switch: n/a — no flag involved

## 5. Approval

| Role | Name | Approved | Date |
|------|------|----------|------|
| Requester | maria.chen | yes | 2026-10-20 |
| Technical Reviewer | j.okafor | yes | 2026-10-20 |
| CAB / Manager (High+ risk) | s.ramirez | yes | 2026-10-21 |

## 6. Execution Log

| Time (UTC) | Step | Result | Notes |
|------------|------|--------|-------|
| 09:02 | Migration started | OK | `CREATE INDEX CONCURRENTLY` running |
| 09:17 | Index build complete | OK | 15 min; replication lag peaked at 90s |
| 09:20 | Smoke tests | OK | p95 now 240ms |

## 7. Post-Change Review

- [x] Change completed as planned
- [x] Monitoring clean for 1 hour post-change
- [x] Follow-up logged: index builds on 8GB tables take ~15 min, not 10
