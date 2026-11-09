# Disaster Recovery Test Plan Template

> Fill in every `______` and `<placeholder>` before the test window. Keep the sign-off table — auditors ask for it.

# Disaster Recovery Test Plan: `<Service Name>`

## 1. Test Objectives

| Objective | Target | Measurement |
|-----------|--------|-------------|
| Recovery Time Objective (RTO) | < 4 hours | Time from disaster declaration to service availability |
| Recovery Point Objective (RPO) | < 15 minutes | Maximum acceptable data loss in recovery |
| Data Integrity | 100% | All transactions verified against source |
| Communication | < 30 minutes | All stakeholders notified of test start |

## 2. Scope & Assumptions

### In Scope
- Database failover and restoration from backup
- Application redeployment to DR region
- DNS cutover and traffic routing
- Smoke test validation of core user flows

### Out of Scope
- Third-party service dependencies (assumed available)
- Physical data center failures (cloud-based test)
- Complete network isolation scenarios

### Assumptions
- Latest backup snapshot is valid and complete
- DR region has sufficient capacity
- Network connectivity between regions is functional
- Team members are available during the test window

## 3. Test Scenarios

### Scenario A: Primary Region Complete Failure

**Trigger:** Simulated complete unavailability of the primary AWS region.

**Steps:**
1. **Declare disaster** (0:00) — Lead engineer announces DR test in incident channel
2. **Restore database** (0:30) — Restore from latest snapshot in DR region
3. **Deploy applications** (1:00) — Deploy application stack to DR Kubernetes cluster
4. **Update DNS** (1:30) — Cutover traffic to DR load balancer
5. **Validate** (2:00) — Run smoke tests and verify data integrity
6. **Measure RTO** — Record time from declaration to passing validation

### Scenario B: Database Corruption

**Trigger:** Primary database has corrupt data requiring point-in-time recovery.

**Steps:**
1. Identify corruption point from monitoring alerts
2. Restore database to 5 minutes before corruption timestamp
3. Verify transactional integrity with checksum queries
4. Promote restored instance to primary
5. Redirect application traffic

## 4. Test Execution

### Pre-Test Checklist

| Item | Status | Owner |
|------|--------|-------|
| Backup snapshot created | [ ] | DBA |
| DR environment provisioned | [ ] | Platform |
| Runbooks printed / accessible offline | [ ] | SRE |
| Stakeholders notified | [ ] | Incident Lead |
| Rollback plan confirmed | [ ] | SRE |
| Monitoring dashboards ready | [ ] | Observability |

### Execution Timeline

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
1. Pause test immediately
2. Revert DNS to primary region
3. Do NOT delete DR resources until post-test review
4. Escalate to engineering manager
5. Schedule follow-up test after fixes

## 5. Data Integrity Verification
