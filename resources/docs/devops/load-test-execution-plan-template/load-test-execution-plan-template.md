# Load Test Execution Plan — {System Name}

> Companion to https://stackpractices.com/docs/load-test-execution-plan-template/
> Copy this file, fill in every row, and write `N/A` where a field does not apply.

## 1. Test Goals and Scope

| Field | Value |
|-------|-------|
| Test ID | `LT-YYYY-QQ-NNN` |
| System under test | |
| Test date | |
| Test owner | |
| Stakeholders | |
| Goal | |
| Scope | |
| Out of scope | |

## 2. Test Scenarios

| Scenario ID | Description | Endpoint / Flow | Virtual Users | Ramp Up | Duration | Think Time |
|-------------|-------------|-----------------|---------------|---------|----------|------------|
| S01 | | | | | | |
| S02 | | | | | | |
| S03 | | | | | | |
| S04 | | | | | | |
| S05 | | | | | | |

## 3. Success Criteria

| Metric | Baseline | Target | Must Stay Below | Notes |
|--------|----------|--------|-----------------|-------|
| p50 latency | | | | |
| p95 latency | | | | |
| p99 latency | | | | |
| Error rate | | | | |
| Throughput | | | | |
| CPU utilization | | | | |
| Memory utilization | | | | |
| Database connections | | | | |
| Queue depth | | | | |

## 4. Environment Setup

| Resource | dev/test | production | Notes |
|----------|----------|------------|-------|
| Application nodes | | | |
| Load balancer | | | |
| Database | | | |
| Cache | | | |
| Message queue | | | |
| Load generator | | | |
| Network | | | |
| Data volume | | | |

## 5. Execution Plan

| Step | Action | Owner | Time |
|------|--------|-------|------|
| 1 | Verify environment and monitoring | | T-30 min |
| 2 | Reset environment to known state | | T-20 min |
| 3 | Deploy test scripts and data | | T-15 min |
| 4 | Run baseline test at low load | | T-10 min |
| 5 | Execute scenarios | | T0 |
| 6 | Execute peak scenario | | T+15 min |
| 7 | Monitor system and collect metrics | | T+15 to T+30 min |
| 8 | Gradually reduce load and stop test | | T+30 min |
| 9 | Export results and logs | | T+35 min |
| 10 | Restore environment | | T+45 min |

## 6. Results and Analysis

| Scenario | Max VUs | Peak RPS | p95 Latency | p99 Latency | Error Rate | CPU Avg | Memory Avg | Result |
|----------|---------|----------|-------------|-------------|------------|---------|------------|--------|
| S01 | | | | | | | | |
| S02 | | | | | | | | |
| S03 | | | | | | | | |
| S04 | | | | | | | | |
| S05 | | | | | | | | |

## 7. Findings and Remediation

| Finding ID | Description | Severity | Recommendation | Owner | Due Date |
|------------|-------------|----------|----------------|-------|----------|
| LT-001 | | | | | |
| LT-002 | | | | | |
| LT-003 | | | | | |
