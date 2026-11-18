# Backup Verification Test Record

Fill in every section during or right after the test. Store the completed record next to the DR plan so auditors can find it.

## 1. Test Identification

| Field | Description | Example |
|-------|-------------|---------|
| Test ID | Unique identifier | `BVT-2026-Q3-001` |
| System / Application | What is being tested | `Customer database` |
| Environment | Where the restore is tested | `Isolated DR sandbox` |
| Backup Type | Full, incremental, snapshot, object copy | `Nightly snapshot` |
| Backup Date | Point in time of the backup | `2026-06-25 02:00 UTC` |
| Test Owner | Person responsible for execution | `SRE team` |
| Scheduled Date | When the test is performed | `2026-06-27` |
| Stakeholders | Teams to notify | `DBA, security, application team` |

## 2. Scope and Objectives

| Objective | Target | Measurement |
|-----------|--------|-------------|
| Verify backup integrity | Restore completes without corruption | Hash match or application health check |
| Validate RTO | Restore within agreed time | Compare elapsed time to RTO |
| Validate RPO | Data loss within agreed window | Compare backup age to RPO |
| Confirm dependencies | Required services and credentials available | Checklist passed |
| Test runbook accuracy | Steps produce expected outcome | No deviations logged |

## 3. Restore Procedure

| Step | Action | Expected Result | Actual Result | Pass / Fail |
|------|--------|-----------------|---------------|-------------|
| 1 | Identify backup media and location | Backup found and accessible | | |
| 2 | Provision target restore environment | Environment ready and isolated | | |
| 3 | Copy backup to target | Transfer completes without errors | | |
| 4 | Execute restore command | Restore completes successfully | | |
| 5 | Verify file system or database state | All expected objects present | | |
| 6 | Start application services | Services reach healthy state | | |
| 7 | Run validation checks | Smoke tests pass | | |
| 8 | Capture logs and metrics | Evidence collected | | |
| 9 | Clean up test environment | Resources removed | | |

## 4. Validation Checklist

- [ ] Restored data size matches backup size (within expected tolerance).
- [ ] No corruption errors reported by restore tool or checksum validation.
- [ ] Application can connect to restored database or storage.
- [ ] Critical read queries or file reads return expected results.
- [ ] Write operations can be performed in the test environment without affecting production.
- [ ] RTO is met or a documented exception is recorded.
- [ ] RPO is met or a documented exception is recorded.
- [ ] Credentials, secrets, and network access work after restore.
- [ ] Logs show no unexpected errors during the restore.
- [ ] Runbook steps are accurate and complete.

## 5. Results Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Restore duration | < 60 minutes | 47 minutes | Pass |
| Data freshness | < 4 hours | 3 hours | Pass |
| Application smoke tests | 100% pass | 100% pass | Pass |
| Runbook accuracy | No deviations | 2 minor deviations | Pass with notes |
| Aggregate test result | Pass | | Pass |

## 6. Issue Log and Remediation

| Issue ID | Description | Severity | Owner | Due Date | Status |
|----------|-------------|----------|-------|----------|--------|
| BVT-001 | Restore script uses hard-coded path | Medium | SRE team | 2026-07-04 | Open |
| BVT-002 | Documentation missing step for secret rotation | Low | Platform team | 2026-07-11 | Open |
