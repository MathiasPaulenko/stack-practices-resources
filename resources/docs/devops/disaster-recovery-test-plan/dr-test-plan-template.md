# Disaster Recovery Test Plan Template

Fill in each placeholder before the test window. Adapt all targets and timings to the service; they are not defaults.

# Disaster Recovery Test Plan: `<Service Name>`

## 1. Test Objectives

| Objective | Target | Measurement |
|-----------|--------|-------------|
| Recovery Time Objective (RTO) | `<approved target>` | Start event: `<event>`; stop when: `<critical user transaction succeeds>` |
| Recovery Point Objective (RPO) | `<approved target>` | Compare the latest recovered transaction watermark with the failure boundary |
| Data integrity | `<defined threshold>` | Check required rows and business invariants; record exclusions |
| Communication | `<approved window>` | Notify named stakeholders before the test starts |

## 2. Scope & Assumptions

### In Scope
- Database failover and restoration from backup
- Application redeployment to DR region
- DNS cutover and traffic routing
- Smoke-test validation of core user flows in the isolated recovery environment

### Out of Scope
- Third-party service dependencies not explicitly tested (list each exclusion and its owner)
- Physical data center failures (cloud-based test)
- Complete network isolation scenarios

### Assumptions
- A restore point is available in the destination region and its status has been verified
- The recovery environment has the required capacity, network paths, and access
- Test data and test routes are isolated from customer writes
- Named responders and the rollback controller are available during the window

## 3. Test Scenarios

### Scenario A: Primary Region Complete Failure

**Trigger:** Simulated unavailability of the primary region using the approved mechanism for this environment.

**Steps:**
1. **Declare disaster** (0:00) — Lead engineer announces DR test in incident channel
2. **Restore database** (0:30) — Restore from a verified snapshot already available in the DR region
3. **Deploy applications** (1:00) — Deploy application stack to DR Kubernetes cluster
4. **Update DNS** (1:30) — Cutover traffic to DR load balancer
5. **Validate** (2:00) — Run smoke tests and verify data integrity
6. **Measure RTO** — Record time from declaration to passing validation

### Scenario B: Database Corruption

**Trigger:** The primary database contains a known test record or an isolated copy with corruption that requires point-in-time recovery. Never inject corruption into production data for this exercise.

**Steps:**
1. Identify corruption point from monitoring alerts
2. Select a recovery point before the test corruption marker and record its transaction ID or log sequence number
3. Restore to that point and compare key rows and transaction watermarks
4. Promote restored instance to primary
5. Redirect application traffic

## 4. Test Execution

### Pre-Test Checklist

| Item | Status | Owner |
|------|--------|-------|
| Restore point exists in destination region and is available | [ ] | DBA |
| DR environment and test application route are isolated | [ ] | Platform |
| RTO/RPO clock definitions and pass criteria are approved | [ ] | Service Owner |
| Stop conditions and rollback controller are confirmed | [ ] | Test Lead |
| Runbooks printed / accessible offline | [ ] | SRE |
| Stakeholders notified | [ ] | Incident Lead |
| Rollback plan confirmed | [ ] | SRE |
| Monitoring dashboards ready | [ ] | Observability |

### Execution Timeline

The timings below are an example schedule. Replace them with estimates from a rehearsal and the service's approved objectives; they are not recovery guarantees.

| Time | Activity | Expected Result |
|------|----------|-----------------|
| T+0:00 | Declare test start | Incident channel notified |
| T+0:05 | Initiate database restore | RDS restore job started |
| T+1:00 | Database available | Connection test passes |
| T+1:30 | Deploy application | All pods healthy |
| T+2:00 | DNS cutover | Traffic hitting DR region |
| T+2:30 | Smoke tests | 100% pass rate |
| T+3:00 | Data integrity check | Transaction count matches source |
| T+4:00 | RTO measurement | Record actual vs target |

### Rollback Procedure

If any critical step fails:
1. Stop new test actions and record the current traffic and write paths
2. Ask the controller and database owner to confirm which environment is authoritative
3. Reconcile any writes before sending traffic back to the primary region
4. Preserve the DR resources and evidence until the post-test review
5. Escalate any customer or data impact as an incident, then schedule a retest after fixes

## 5. Data Integrity Verification

```sql
-- Transaction count comparison
SELECT 'primary' as source, COUNT(*) as tx_count FROM orders
UNION ALL
SELECT 'dr', COUNT(*) FROM dr_orders;

-- Compare the same key and business columns in both directions.
-- EXCEPT is supported by PostgreSQL and SQL Server; adapt columns and types.
SELECT COUNT(*) AS rows_missing_in_dr
FROM (
  SELECT payment_id, status, amount_cents, created_at FROM payments
  EXCEPT
  SELECT payment_id, status, amount_cents, created_at FROM dr_payments
) AS missing_in_dr;

SELECT COUNT(*) AS rows_extra_in_dr
FROM (
  SELECT payment_id, status, amount_cents, created_at FROM dr_payments
  EXCEPT
  SELECT payment_id, status, amount_cents, created_at FROM payments
) AS extra_in_dr;

-- A timestamp is only a proxy for RPO; prefer a durable engine-specific watermark.
SELECT MAX(created_at) FROM orders;
```

| Check | Primary | DR | Match |
|-------|---------|-----|-------|
| Transaction count | ______ | ______ | [ ] |
| Rows different in either direction | ______ | ______ | [ ] |
| Latest timestamp | ______ | ______ | [ ] |

## 6. Post-Test Report

### Results Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| RTO | `<approved target>` | ______ | Pass / Fail / Not tested |
| RPO | `<approved target>` | ______ | Pass / Fail / Not tested |
| Data integrity | `<defined threshold>` | ______ | Pass / Fail / Not tested |
| Smoke tests | `<critical flows>` | ______ | Pass / Fail / Not tested |

### Issues Found

| Issue | Severity | Owner | Fix Deadline |
|-------|----------|-------|--------------|
| ______ | Critical / High / Medium / Low | ______ | ______ |

For each finding, attach the expected and observed result, evidence ID, impact, owner, due date, and retest scenario. Mark checks that were excluded or blocked instead of treating them as passes.

### Lessons Learned

- What worked well:
- What took longer than expected:
- What failed unexpectedly:
- What should be automated:

### Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Test Lead | ______ | ______ | ______ |
| Engineering Manager | ______ | ______ | ______ |
| Compliance (if required) | ______ | ______ | ______ |
