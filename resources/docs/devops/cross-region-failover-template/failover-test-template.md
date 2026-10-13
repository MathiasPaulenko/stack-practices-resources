# Cross-Region Failover Test: `<service-name>`

## 1. Service Metadata

| Field | Value |
|-------|-------|
| Service | `<service-name>` |
| Primary region | `us-east-1` |
| Secondary region | `eu-west-1` |
| RTO target | `15 min` |
| RPO target | `5 min` |
| Data replication | `Aurora Global / async` |
| Last test date | `YYYY-MM-DD` |
| Test owner | `@team-or-person` |

## 2. Roles

| Role | Person | Responsibility |
|------|--------|----------------|
| Test lead | | Owns the clock, calls go/no-go, can abort |
| Executor | | Runs the script, reports each step |
| Data validator | | Checks replication lag and integrity |
| Comms | | Status page, stakeholder channel |
| Observer | | Logs timeline, notes surprises |

## 3. Go/No-Go Criteria

Test proceeds only if ALL are true at T-30 min:

- [ ] Secondary region healthy (compute, database replica, endpoints)
- [ ] Replication lag < 50% of RPO target
- [ ] DNS record TTL <= 60s (checked with `dig`, not assumed)
- [ ] Failback procedure reviewed and executor knows it
- [ ] Stakeholders notified, status page ready
- [ ] Someone has authority to abort and will say so

## 4. Abort Criteria

Abort immediately and fail back (or hold state) if:

- Real production incident starts in either region
- Replication lag exceeds RPO after promotion decision
- Data integrity check fails post-failover
- Any step exceeds its time budget by 2x without a known cause

## 5. Failover Timeline

| T+ | Action | Verify | Budget |
|----|--------|--------|--------|
| 0 | Confirm failure signal / declare drill start | Two independent signals | 2 min |
| 2 | Fence primary: block writes, stop writers | No write connections | 3 min |
| 5 | Promote secondary database | Accepts writes | 5 min |
| 10 | Scale secondary compute to prod size | Desired capacity reached | 5 min |
| 15 | Update DNS / routing to secondary | `dig` from 2+ locations | 2 min |
| 17 | Synthetic transactions against service | 100% success, 5 min | 5 min |
| 22 | Declare failover complete, start soak | — | — |
| 52 | End soak, start failback | See section 6 | — |

## 6. Failback

| Step | Action | Verify |
|------|--------|--------|
| 1 | Re-establish replication secondary -> primary | Lag trending to 0 |
| 2 | Wait until lag = 0, verify checksums | Row counts match |
| 3 | Fence secondary writers | No write connections |
| 4 | Switch DNS back to primary | `dig` confirms |
| 5 | Scale secondary back to standby | Desired capacity |
| 6 | Confirm steady-state replication | Lag < threshold |

## 7. Post-Test Report

| Metric | Target | Actual | Pass |
|--------|--------|--------|------|
| Detection to decision | < 2 min | | |
| Decision to promoted | < 10 min | | |
| Total failover time | < RTO | | |
| Data loss (lag at promotion) | < RPO | | |
| Failback time | < 30 min | | |
| Errors during cutover | < 0.5% | | |

### Surprises and deltas

- What took longer than budgeted and why:
- Which step had no written procedure:
- Which alarm did or didn't fire:
- Action items (owner, due date):
