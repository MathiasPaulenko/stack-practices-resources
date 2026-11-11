# Worked Example — Cutting a SaaS Bill 30%

Scenario: SaaS platform on AWS, $50K/month spend, 15% monthly growth.
Goal: reduce 30% without user impact.

## Phase 1 — Visibility (weeks 1–2)

| Service | Cost/month | % of total |
|---------|-----------|------------|
| EC2 (20 instances) | $18,000 | 36% |
| RDS PostgreSQL | $8,000 | 16% |
| ElastiCache Redis | $5,000 | 10% |
| S3 (50TB) | $4,500 | 9% |
| CloudFront | $3,500 | 7% |
| EKS (3 clusters) | $3,000 | 6% |
| NAT Gateway | $2,000 | 4% |
| Lambda | $1,500 | 3% |
| Other | $4,500 | 9% |
| **Total** | **$50,000** | **100%** |

## Phase 2 — Optimization (weeks 3–6)

### Action 1: Right-size EC2

- Analyze average CPU/memory (CloudWatch, 30 days)
- 12 instances < 20% CPU → reduce type
- 5 instances < 10% CPU → terminate
- **Savings: $6,500/month**

### Action 2: Reserved Instances + Savings Plans

- 8 always-on instances → 1-year RI (40% discount)
- **Savings: $3,200/month**

### Action 3: S3 lifecycle policies

- Objects > 30 days → S3 IA
- Objects > 90 days → Glacier
- **Savings: $2,000/month**

### Action 4: Spot instances for batch jobs

- 5 processing workers → Spot (70% discount)
- **Savings: $1,500/month**

### Action 5: RDS optimization

- Reader replica → remove (use ElastiCache for reads)
- Storage: gp2 → gp3 (20% cheaper)
- **Savings: $1,800/month**

## Phase 3 — Results

| Action | Savings/month |
|--------|---------------|
| Right-size EC2 | $6,500 |
| Reserved Instances | $3,200 |
| S3 lifecycle | $2,000 |
| Spot instances | $1,500 |
| RDS optimization | $1,800 |
| **Total** | **$15,000 (30%)** |

## Phase 4 — Continuous governance

- Mandatory tags: team, env, project, cost-center
- Budget alerts: 80% and 100% of monthly budget
- Weekly cost report per team
- Quarterly cost review with all teams
- FinOps dashboard: AWS Cost Explorer + custom tags

## Lessons

- Visibility first: you cannot optimize what you cannot see
- Right-sizing is the fastest win
- Reserved Instances for always-on workloads
- S3 lifecycle policies are set-and-forget
- Continuous governance prevents cost creep
