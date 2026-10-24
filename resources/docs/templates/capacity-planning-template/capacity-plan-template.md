# Capacity Plan: [System Name]

## 1. Current Baseline (as of [date])

### Compute Resources

| Service | Instance type | Count | CPU avg | CPU peak | Memory avg | Memory peak | Notes |
|---------|--------------|-------|---------|----------|------------|-------------|-------|
| API servers | c6i.xlarge | 6 | 35% | 72% | 45% | 68% | Auto-scaling 4-10 |
| Workers | c6i.large | 4 | 20% | 55% | 30% | 50% | Batch processing |
| Dashboard | t3.medium | 2 | 15% | 40% | 25% | 45% | Static + SSR |

### Database Resources

| Cluster | Type | Storage used | Storage capacity | Connections avg | Connections peak | Replication lag |
|---------|------|-------------|-----------------|-----------------|------------------|-----------------|
| Primary | r6i.2xlarge | 340 GB | 500 GB | 80 | 140 | — |
| Replica 1 | r6i.large | 340 GB | 500 GB | 45 | 90 | < 1s |
| Replica 2 | r6i.large | 340 GB | 500 GB | 30 | 60 | < 1s |

### Network

| Metric | Current avg | Current peak | Limit | Headroom |
|--------|-------------|--------------|-------|----------|
| Bandwidth in | 120 Mbps | 280 Mbps | 1 Gbps | 72% |
| Bandwidth out | 200 Mbps | 450 Mbps | 1 Gbps | 55% |
| Requests/sec | 8,000 | 18,000 | 25,000 | 28% |

### Storage Growth

| Dataset | Current size | Growth rate | Projected in 12 months | Retention policy |
|---------|-------------|-------------|------------------------|------------------|
| User data | 12 GB | 0.5 GB/month | 18 GB | Indefinite |
| Orders | 45 GB | 3 GB/month | 81 GB | 7 years (legal) |
| Audit logs | 120 GB | 8 GB/month | 216 GB | 90 days hot, 1 year cold |
| Media uploads | 800 GB | 40 GB/month | 1,280 GB | Indefinite |

## 2. Growth Projections

### Traffic Projections

| Metric | Current (monthly) | Q+1 | Q+2 | Q+3 | Q+4 | Source |
|--------|-------------------|-----|-----|-----|-----|--------|
| Active users | 50,000 | 58,000 | 67,000 | 78,000 | 90,000 | Product roadmap |
| API requests | 24M | 28M | 33M | 38M | 44M | 15% MoM growth |
| Peak RPS | 18,000 | 21,000 | 24,000 | 28,000 | 32,000 | Load tests |
| Storage added | 51 GB | 52 GB | 53 GB | 54 GB | 55 GB | Linear trend |

### Assumptions

- User growth: 15% month-over-month (based on last 6 months)
- API requests per user: stable at ~480/month
- Peak traffic: 2.5x average (based on load test data)
- Marketing campaigns: Q3 product launch may cause 3x burst for 2 weeks
- No major architecture changes are planned — if one lands mid-quarter, the projection resets

### Risk factors

- **Q3 product launch** — marketing expects 3x traffic burst for 2 weeks. Plan for 50k RPS peak.
- **Holiday season** — historical 2x traffic in November-December.
- **New enterprise customer** — sales pipeline includes a 10k-user enterprise contract (Q2). Would add 20% to user base overnight.

## 3. Bottleneck Analysis

| Component | Current limit | Projected breaking point | When | Mitigation |
|-----------|--------------|-------------------------|------|------------|
| API servers (CPU) | 25k RPS | ~28k RPS at current efficiency | Q3 | Add 2 instances + optimize hot paths |
| Database connections | 200 max | ~180 at projected peak | Q2 | Add read replica + connection pooling |
| Primary DB storage | 500 GB | ~480 GB in 12 months | Q4 | Provision 1 TB or partition old data |
| Bandwidth out | 1 Gbps | ~800 Mbps at projected peak | Q3 | Upgrade to 2 Gbps or add CDN |
| Audit log storage | 500 GB allocated | ~480 GB in 12 months | Q4 | Move to cold storage (S3 Glacier) |

## 4. Scaling Plan

### Q1 (current quarter)

| Action | Component | Cost (monthly) | Justification |
|--------|-----------|---------------|---------------|
| Add 2 API instances | API servers | $480 | Headroom for Q2 growth |
| Enable connection pooling | Database | $0 (config change) | Prevent connection exhaustion |
| Set up CDN for media | Network | $200 | Reduce bandwidth pressure |

### Q2

| Action | Component | Cost (monthly) | Justification |
|--------|-----------|---------------|---------------|
| Add read replica 3 | Database | $320 | Enterprise customer read traffic |
| Upgrade bandwidth to 2 Gbps | Network | $150 | Q3 launch burst preparation |
| Implement audit log archival | Storage | $50 (Glacier) | Prevent storage exhaustion |

### Q3

| Action | Component | Cost (monthly) | Justification |
|--------|-----------|---------------|---------------|
| Add 4 API instances (burst pool) | API servers | $960 | Product launch 3x traffic |
| Add 2 worker instances | Workers | $240 | Batch processing for new users |
| Provision 1 TB DB storage | Database | $200 | Storage growth + partitioning |

### Q4

| Action | Component | Cost (monthly) | Justification |
|--------|-----------|---------------|---------------|
| Evaluate DB partitioning | Database | Eng time | Orders table growing fast |
| Add CDN edge in APAC | Network | $300 | User growth in Asia region |

### Total projected cost increase

| Quarter | Additional monthly cost |
|---------|----------------------|
| Q1 | $680 |
| Q2 | $520 |
| Q3 | $1,400 |
| Q4 | $300 |
| **Total annual increase** | **$2,900/month average** |

## 5. Review Schedule

| Review | Date | Owner | Focus |
|--------|------|-------|-------|
| Q1 review | 2026-04-01 | Platform team | Validate Q1 actions, adjust Q2 plan |
| Q2 review | 2026-07-01 | Platform team | Post-launch capacity check |
| Q3 review | 2026-10-01 | Platform team | Holiday prep, Q4 adjustments |
| Q4 review | 2027-01-01 | Platform team | Annual recap, next-year plan |
