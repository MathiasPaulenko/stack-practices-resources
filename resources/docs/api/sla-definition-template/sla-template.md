# Service Level Agreement: `<Service Name>`

**Effective Date:** `2026-07-01`
**Review Cycle:** `Quarterly`
**Owning Team:** `@platform-team`
**Measured By:** `Prometheus + shared Grafana dashboard`

## 1. Service Level Objectives (SLOs)

| Metric | Target | Measurement Window | Data Source |
|--------|--------|--------------------|-------------|
| Availability | 99.9% | Rolling 30 days | LB health checks |
| Latency p95 | < 200ms | Per minute | App metrics (Prometheus) |
| Latency p99 | < 500ms | Per minute | App metrics (Prometheus) |
| Error Rate | < 0.1% | Rolling 7 days | App logs + APM |
| Throughput | > 1,000 req/s | Per minute | LB metrics |

## 2. Service Level Indicators (SLIs)

| SLI | Good Events | Valid Events | Calculation |
|-----|-------------|--------------|-------------|
| Availability | Successful checks | All checks | Good / Valid |
| Latency p95 | Requests < 200ms | All requests | Percentile of valid |
| Error Rate | Responses < 500 | All responses | 1 - (errors / total) |

## 3. Error Budget

| SLO | Error Budget (30 days) | Burn Alert |
|-----|------------------------|------------|
| 99.9% availability | 43.2 min downtime | 2x in 1 day = warn |
| < 0.1% error rate | 0.1% of requests | 10x in 1 day = freeze |

### Burn Rate Alerts

| Burn Rate | Budget Consumed | Action |
|-----------|-----------------|--------|
| 1x | On pace | Monitor |
| 2x | 2x faster | Page on-call (warning) |
| 10x | 10x faster | Page + freeze deploys |

## 4. Response & Resolution Times

| Severity | Definition | Response | Resolution | Escalation |
|----------|------------|----------|------------|------------|
| P1 | Complete outage | 15 min | 2 hours | VP Engineering |
| P2 | Degraded, workaround | 1 hour | 8 hours | Eng. Manager |
| P3 | Partial failure | 4 hours | 3 biz days | Team Lead |
| P4 | Cosmetic | 1 biz day | Next sprint | Ticket queue |

## 5. Exclusions

The following are excluded from SLA calculations:
- **Scheduled maintenance:** <=4 hours/month with 7 days notice
- **Third-party outages:** Dependencies outside our control
- **Force majeure:** Disasters, backbone failures
- **Client-side issues:** Consumer bugs, rate limit abuse

## 6. Penalties & Credits

| Monthly Uptime | Service Credit | Trigger |
|----------------|----------------|---------|
| 99.0% - 99.9% | 10% monthly fee | Automatic |
| 95.0% - 99.0% | 25% monthly fee | Automatic |
| < 95.0% | 50% monthly fee | Auto + postmortem |

## 7. Communication Plan

| Event | Audience | Channel | Timing |
|-------|----------|---------|--------|
| Degradation detected | Internal | PagerDuty + Slack | Immediate |
| P1 outage starts | Customers | Status page + email | <=30 min |
| P1 resolved | Customers | Status page | <=15 min after |
| Monthly SLA report | Customers | Email | <=5 biz days |

## 8. Review & Revision

- **Quarterly review:** Eng + Product + Customer Success
- **Trigger review:** Any P1 or SLA miss triggers ad-hoc review
- **Revision notice:** 14 days before changes take effect
