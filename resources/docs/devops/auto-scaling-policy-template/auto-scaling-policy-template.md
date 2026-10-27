# Auto-Scaling Policy: `<Service Name>`

## 1. Service Metadata

| Field | Value |
|-------|-------|
| Service | `name` |
| Platform | `AWS / GCP / Azure / Kubernetes` |
| Owner Team | `@team-name` |
| Last Reviewed | `YYYY-MM-DD` |

## 2. Scale-Up Policy

### 2.1. Triggers

| Metric | Threshold | Duration | Scale Action | Cooldown |
|--------|-----------|----------|--------------|----------|
| CPU utilization | > 60% | 2 minutes | Add 1 instance | 3 minutes |
| Memory utilization | > 70% | 2 minutes | Add 1 instance | 3 minutes |
| Request count | > 5,000 RPS | 1 minute | Add 2 instances | 5 minutes |
| Queue depth | > 100 messages | 3 minutes | Add 1 instance | 3 minutes |
| Latency p95 | > 500ms | 2 minutes | Add 2 instances | 5 minutes |

### 2.2. Limits

| Limit | Value | Rationale |
|-------|-------|-----------|
| Max instances | 20 | Cost ceiling, database connection limit |
| Max scale-up per event | 50% of current | Prevent thundering herd on cold start |
| Scale-up cooldown | 3 minutes | Allow metric stabilization |

## 3. Scale-Down Policy

### 3.1. Triggers

| Metric | Threshold | Duration | Scale Action | Cooldown |
|--------|-----------|----------|--------------|----------|
| CPU utilization | < 30% | 10 minutes | Remove 1 instance | 5 minutes |
| Memory utilization | < 30% | 10 minutes | Remove 1 instance | 5 minutes |
| Request count | < 1,000 RPS | 10 minutes | Remove 1 instance | 5 minutes |

### 3.2. Limits

| Limit | Value | Rationale |
|-------|-------|-----------|
| Min instances | 3 | Redundancy, rolling deployment buffer |
| Max scale-down per event | 25% of current | Avoid over-correction |
| Scale-down cooldown | 5 minutes | Allow metric stabilization |

## 4. Instance Requirements

### 4.1. Health Checks

- [ ] Load balancer health check passes before instance receives traffic
- [ ] Instance must serve traffic for minimum 5 minutes before scale-down eligibility
- [ ] Connection draining allows in-flight requests to complete (30 seconds)

### 4.2. Warm-Up

- [ ] New instances complete initialization (app start, cache warm-up) before joining pool
- [ ] Warm-up time documented: `60 seconds`
- [ ] Startup probe / readiness probe configured in orchestrator

## 5. Cost Controls

| Control | Value | Notes |
|---------|-------|-------|
| Max hourly spend | $500 | Alert if exceeded |
| Instance type | `c5.large` | CPU-optimized for API workload |
| Spot / Preemptible | 50% of instances | Use for non-critical batch processing only |
| Reserved capacity | Baseline of 3 instances | Commitment discount for minimum |

## 6. Incident Response

| Scenario | Action | Owner |
|----------|--------|-------|
| Scale-up fails (quota exceeded) | Page on-call, escalate to cloud admin | SRE |
| Scale-down causes errors | Pause auto-scaling, investigate | Platform |
| Costs spike > 2x baseline | Review policy, check for runaway jobs | Finance + SRE |
| Latency rises despite scaling | Alert: likely database bottleneck, not compute | DBA + App Team |
