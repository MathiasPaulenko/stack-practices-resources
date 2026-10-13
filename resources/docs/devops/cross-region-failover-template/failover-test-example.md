# Cross-Region Failover Test: payments-api (filled example)

## 1. Service Metadata

| Field | Value |
|-------|-------|
| Service | `payments-api` |
| Primary region | `us-east-1` |
| Secondary region | `eu-west-1` |
| RTO target | `15 min` |
| RPO target | `5 min` |
| Data replication | `Aurora Global Database, async` |
| Last test date | `2026-09-14` |
| Test owner | `@payments-oncall` |

## 2. Roles

| Role | Person | Responsibility |
|------|--------|----------------|
| Test lead | m.paulenko | Owns the clock, calls go/no-go, can abort |
| Executor | r.sato | Runs the script, reports each step |
| Data validator | a.owens | Checks replication lag and integrity |
| Comms | l.garcia | Status page, stakeholder channel |
| Observer | d.kim | Logs timeline, notes surprises |

## 3. Go/No-Go Criteria

All verified at 14:30 UTC, test window 15:00-16:30 UTC:

- [x] Secondary region healthy (compute, database replica, endpoints)
- [x] Replication lag 212 ms (< 50% of 5 min RPO)
- [x] DNS record TTL 60s (verified with `dig api.payments.internal @1.1.1.1`)
- [x] Failback procedure reviewed, r.sato walked it once on staging
- [x] Stakeholders notified 48h ahead, status page banner ready
- [x] m.paulenko holds abort authority

## 4. Abort Criteria

- Real production incident starts in either region
- Replication lag exceeds 5 min after promotion decision
- Data integrity check fails post-failover
- Any step exceeds its time budget by 2x without a known cause

## 5. Failover Timeline (actual)

| T+ | Action | Planned | Actual |
|----|--------|---------|--------|
| 0 | Drill declared, signals confirmed | 2 min | 1 min |
| 2 | Fence primary writes (DB set read-only) | 3 min | 4 min |
| 6 | `switchover-global-cluster` issued | 5 min | 3 min |
| 9 | Secondary ASG to desired capacity | 5 min | 6 min |
| 15 | Route 53 record updated | 2 min | 1 min |
| 16 | Synthetic transactions green | 5 min | 5 min |
| 21 | Failover declared complete | — | 21 min total |
| 51 | Soak ends, failback starts | — | — |
| 68 | Failback verified complete | 30 min | 17 min |

## 6. Failback notes

- Reverse replication lag hit zero at T+61; checksums matched on `orders` and `transactions`.
- One stale write found on the old primary (a health-check probe wrote a heartbeat row); discarded, documented.

## 7. Post-Test Report

| Metric | Target | Actual | Pass |
|--------|--------|--------|------|
| Detection to decision | < 2 min | 1 min | yes |
| Decision to promoted | < 10 min | 7 min | yes |
| Total failover time | < 15 min | 21 min | **no** |
| Data loss | < 5 min | 0 (switchover) | yes |
| Failback time | < 30 min | 17 min | yes |
| Errors during cutover | < 0.5% | 0.31% | yes |

### Surprises and deltas

- ASG warmup took 6 min vs 5 budgeted because two instances sat in `pending:wait` on a slow AMI pull; pre-bake the image or raise the budget.
- Fencing took 4 min: the read-only flag propagated through a proxy tier we forgot to account for.
- Total failover missed RTO by 6 min; the drill still counted as a successful test because every delay was identified and has an owner.
- Alarm for `AuroraGlobalDBRPOLag > 150s` did not fire during the paused-replication scenario: threshold bug, fixed.

### Action items

- Pre-bake secondary AMI, cut ASG warmup to ~2 min (r.sato, 2026-10-20)
- Add proxy tier to the fencing procedure (a.owens, 2026-10-17)
- Fix lag alarm threshold; retest during next drill (d.kim, 2026-10-15)
- Re-run full drill 2026-12-14 (m.paulenko)
