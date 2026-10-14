# Load Test Report — {Service Name}

**Date:** {YYYY-MM-DD}
**Tester:** {Name}
**Environment:** Staging (replica of production)
**Tool:** {k6 / JMeter / Locust + version}

## Test Configuration

| Parameter       | Value          |
|-----------------|----------------|
| Max users       | {200}          |
| Duration        | {34 min}       |
| Ramp-up         | {5 min to 200} |
| Peak hold       | {15 min at 200}|

## Results Summary

| Metric              | Target  | Actual  | Status |
|---------------------|---------|---------|--------|
| P50 response time   | < 100ms |         |        |
| P95 response time   | < 300ms |         |        |
| P99 response time   | < 500ms |         |        |
| Error rate          | < 0.1%  |         |        |
| Throughput          | > 500   |         |        |
| Peak CPU            | < 70%   |         |        |
| Peak memory         | < 75%   |         |        |

## Bottlenecks Identified

1. {Component} — {symptom at load}
   - Fix: {action}

## Recommendations

1. {Action, owner, tracking ticket}
2. Re-run load test after fixes to verify improvements
