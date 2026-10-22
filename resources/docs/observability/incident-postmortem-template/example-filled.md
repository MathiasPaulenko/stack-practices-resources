# Incident Postmortem: INC-2026-07-05-001

> Incident ID: INC-2026-07-05-001 | Date: 2026-07-05 | Severity: P0
> Incident Commander: <Name> | Postmortem Author: <Name>
> Review date: 2026-07-06 | Status: Reviewed

## 1. Incident Summary

| Field | Value |
|-------|-------|
| Incident ID | INC-2026-07-05-001 |
| Title | Payment service outage during checkout peak |
| Severity | P0 |
| Status | Resolved |
| Start Time | 14:32 UTC |
| Detection Time | 14:35 UTC (3 min to detect) |
| Mitigation Time | 14:52 UTC (20 min to mitigate) |
| Resolution Time | 15:48 UTC (76 min total) |
| Affected Services | Payment Service, Checkout Service |
| Affected Users | ~12,000 active users |
| Revenue Impact | ~$45,000 lost orders |

## 2. Impact Summary

### User-Facing Impact

| Impact | Duration | Affected Users |
|--------|----------|----------------|
| Checkout page returned 500 error | 20 minutes (14:32-14:52) | ~12,000 |
| Payment processing failed | 20 minutes | ~3,500 attempted checkouts |
| Order confirmation emails delayed | 76 minutes | ~1,200 orders queued |

### Business Impact

| Metric | Normal | During Incident | Impact |
|--------|--------|-----------------|--------|
| Orders per minute | 180 | 0 (for 20 min) | 3,600 lost orders |
| Revenue per minute | $2,250 | $0 (for 20 min) | $45,000 lost revenue |
| Support tickets | 5/hour | 85/hour | 80 extra tickets |

### SLO Impact

| SLO | Target | Before Incident | After Incident | Budget Consumed |
|-----|--------|-----------------|----------------|-----------------|
| Availability | 99.9% | 99.92% | 99.85% | 70% of monthly budget |

## 3. Timeline

| Time (UTC) | Event | Source |
|------------|-------|--------|
| 14:30 | Deployment v2.5.0 goes live — includes new payment provider integration | CI/CD pipeline |
| 14:32 | Error rate spikes from 0.1% to 45% on `/api/v1/payments` endpoint | Prometheus alert |
| 14:35 | PagerDuty alert fires: `HighErrorRate-PaymentService` | Alertmanager |
| 14:44 | On-call engineer confirms v2.5.0 deployed at 14:30, 2 minutes before errors started | CI/CD logs |
| 14:48 | Decision made to roll back to v2.4.1 | Incident channel |
| 14:50 | Rollback initiated: `kubectl rollout undo deployment/payment` | Terminal |
| 14:52 | Rollback complete — error rate drops to 0.1% | Grafana |
| 15:48 | All pending refunds processed — incident fully resolved | Payment service |
| 16:00 | Incident declared resolved in PagerDuty | PagerDuty |

## 4. Root Cause Analysis

### What Happened

Deployment v2.5.0 introduced a new payment provider integration. The new code expected the provider's API to always return `transaction.id`, but for Amex and Discover cards the ID arrives nested in `transaction.metadata.transaction_id`. Accessing `transaction.id` directly returned `undefined` and threw a `TypeError` that crashed the request handler.

### Five Whys Analysis

1. **Why did the payment service return 500 errors?** The code threw a `TypeError` when accessing `transaction.id` on undefined.
2. **Why was `transaction.id` undefined?** The provider returns transaction IDs nested in `transaction.metadata.transaction_id` for Amex and Discover cards.
3. **Why didn't tests catch this?** Integration tests used mocked responses that always included `transaction.id`.
4. **Why wasn't the real response format verified?** No contract testing existed between the payment service and the provider.
5. **Why did the deployment affect all users immediately?** No canary or gradual rollout was configured — the deploy went to 100% of traffic.

### Contributing Factors

| Factor | Impact | Category |
|--------|--------|----------|
| Deployment during peak hours (14:30 UTC) | Maximized user impact | Process |
| Alert threshold too high (5% error rate) | 3-minute detection delay | Monitoring |
| Single payment provider | No fallback when integration broke | Architecture |

## 5. What Went Well

- [x] Alert fired within 3 minutes of error start
- [x] Root cause identified within 10 minutes
- [x] Rollback completed within 20 minutes
- [x] No data corruption — all orders were preserved

## 6. What Went Wrong

- [x] Deployment went to 100% traffic without canary
- [x] Tests did not cover non-Visa/Mastercard response formats
- [x] No contract testing with payment provider
- [x] No feature flag to disable the new integration

## 7. Where We Got Lucky

- [x] The rollback was fast because the previous version was still available
- [x] The error was consistent and easy to reproduce

## 8. Action Items

| # | Action | Type | Owner | Priority | Due Date | Status |
|---|--------|------|-------|----------|----------|--------|
| 1 | Add contract tests for payment provider API responses | Prevent | Backend team | High | 2026-07-12 | Open |
| 2 | Implement canary deployment for payment service | Prevent | Platform team | High | 2026-07-19 | Open |
| 3 | Lower error rate alert threshold from 5% to 2% | Improve | SRE team | Medium | 2026-07-08 | Open |
| 4 | Add deployment freeze policy for peak hours | Process | Eng Manager | Medium | 2026-07-10 | Open |
| 5 | Evaluate secondary payment provider as fallback | Architect | Backend team | Low | 2026-08-05 | Open |

## 9. Lessons Learned

### Technical Lessons

1. Mock responses must match real API behavior — contract tests against the real API would have caught the schema mismatch.
2. Canary deployments catch integration bugs — a 5% canary would have affected ~600 users instead of 12,000.

### Process Lessons

1. Deployment timing matters — a freeze during peak hours is a simple policy change.
2. Alert thresholds should be tuned — 5% is too high for a critical service.
