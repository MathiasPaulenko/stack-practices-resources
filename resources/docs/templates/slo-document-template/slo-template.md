# SLO: [Service Name]

## Overview

| Field | Value |
|-------|-------|
| **Service** | [name] |
| **Owner** | [team or individual] |
| **Review date** | [quarterly] |

## SLIs (Service Level Indicators)

| SLI | Description | Measurement |
|-----|-------------|-------------|
| **Availability** | Ratio of successful requests | (total - errors) / total |
| **Latency** | Response time distribution | p95, p99 per endpoint |
| **Throughput** | Requests per second | RPS at peak |

## SLOs (Targets)

| Objective | Target | Measurement Window |
|-----------|--------|-------------------|
| Availability | 99.9% | Rolling 30 days |
| Latency p95 | < 200ms | Rolling 7 days |
| Error rate | < 0.1% | Rolling 24 hours |

## Error Budget

- **Budget:** 100% - SLO target (e.g., 0.1% for 99.9% availability)
- **Period:** 30 days
- **Policy:** When error budget is > 50% consumed in < 50% of period, freeze non-critical deploys

## Alerting Thresholds

| Severity | Threshold | Response |
|----------|-----------|----------|
| Page | Error budget 10% consumed in 1 hour | On-call responds immediately |
| Ticket | Error budget 50% consumed in 7 days | Team reviews in next sprint |

## Dependencies

| Dependency | Their SLO | Impact If They Miss |
|------------|-----------|-------------------|
| Payment API | 99.95% | Our checkout SLO drops |
| Identity Provider | 99.9% | Login failures affect availability |

## Error Budget Policy

```
Budget remaining | Policy
-------------------|--------
> 50%              | Normal operations
25-50%             | Deploy freeze for risky changes
< 25%              | Deploy freeze except critical fixes
< 10%              | All hands on reliability; halt feature work
```

## SLI Selection Guide

| Service Type | Good SLI | Bad SLI | Why |
|--------------|----------|---------|-----|
| HTTP API | Request success rate (2xx+3xx / total) | CPU usage | Users care about responses, not CPU |
| gRPC service | grpc_io_server_completed_rpcs (OK / total) | Memory usage | Users care about RPCs succeeding |
| Batch job | Freshness (time since last successful run) | Disk I/O | Users care about data being current |
| Queue consumer | Lag (messages behind head) | Network throughput | Users care about processing keeping up |
| Database | Query success rate + p99 latency | Connection count | Users care about queries working fast |

### RED vs USE model

- **RED** (for services): Rate, Errors, Duration. Use for HTTP APIs, gRPC services, message consumers.
- **USE** (for infrastructure): Utilization, Saturation, Errors. Use for databases, caches, load balancers.
- Don't mix them: a RED SLI on a database misses saturation; a USE SLI on an API misses user experience.

## Review Notes

- [ ] Are SLOs still aligned with user expectations?
- [ ] Has error budget burn rate changed significantly?
- [ ] Do alerting thresholds need adjustment?
- [ ] Are dependencies still accurate?
- [ ] Any new services that need SLOs?
