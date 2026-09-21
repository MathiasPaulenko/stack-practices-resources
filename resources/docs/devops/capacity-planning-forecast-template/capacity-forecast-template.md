# Capacity Planning Forecast: `<System / Service>`

> Author: ______ | Date: ______ | Review date: ______
> Service owner: ______ | Team: ______ | Forecast horizon: ______

## 1. Current State

| Metric | Current | Peak (last 30d) | Limit | Headroom |
|--------|---------|-----------------|-------|----------|
| Requests / sec | ______ | ______ | ______ | ______ |
| CPU utilization (%) | ______ | ______ | ______ | ______ |
| Memory utilization (%) | ______ | ______ | ______ | ______ |
| Disk I/O (MB/s or IOPS) | ______ | ______ | ______ | ______ |
| Network throughput (Gbps) | ______ | ______ | ______ | ______ |
| Database connections | ______ | ______ | ______ | ______ |
| Storage used (GB) | ______ | ______ | ______ | ______ |
| Queue depth / backlog | ______ | ______ | ______ | ______ |

**Current infrastructure:**
- ______ instances at ______ size
- ______ databases at ______ tier
- ______ cache nodes
- ______ load balancers
- Estimated monthly cost: ______

## 2. Growth Assumptions

| Driver | Expected Change | Timeframe | Confidence |
|--------|-----------------|-----------|------------|
| ______ | ______ | ______ | High / Medium / Low |
| ______ | ______ | ______ | High / Medium / Low |
| ______ | ______ | ______ | High / Medium / Low |

**Key assumptions:**
- [ ] ______
- [ ] ______

## 3. Traffic Projections

| Period | Projected RPS | Projected MAU | Growth Rate |
|--------|---------------|---------------|-------------|
| Current | ______ | ______ | — |
| +3 months | ______ | ______ | ______ |
| +6 months | ______ | ______ | ______ |
| +12 months | ______ | ______ | ______ |

## 4. Resource Forecast

| Resource | Current | +3m | +6m | +12m | First to Hit Limit? |
|----------|---------|-----|-----|------|---------------------|
| CPU | ______ | ______ | ______ | ______ | Yes / No |
| Memory | ______ | ______ | ______ | ______ | Yes / No |
| Disk I/O | ______ | ______ | ______ | ______ | Yes / No |
| Network | ______ | ______ | ______ | ______ | Yes / No |
| DB connections | ______ | ______ | ______ | ______ | Yes / No |
| Storage | ______ | ______ | ______ | ______ | Yes / No |

## 5. Scaling Plan

### Short Term (0-3 months)
- [ ] ______
- [ ] ______

### Medium Term (3-6 months)
- [ ] ______
- [ ] ______

### Long Term (6-12 months)
- [ ] ______
- [ ] ______

## 6. Cost Projection

| Scenario | Monthly Cost | Annual Cost | Notes |
|----------|-------------|-------------|-------|
| Do nothing | ______ | ______ | Risk of outage |
| Minimum viable | ______ | ______ | Just ahead of demand |
| Comfortable headroom | ______ | ______ | 30-40% buffer |

## 7. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Growth exceeds forecast | ______ | ______ | ______ |
| Cloud provider limits | ______ | ______ | ______ |
| Scaling takes longer than expected | ______ | ______ | ______ |
| Budget not approved | ______ | ______ | ______ |

## 8. Action Items

| Task | Owner | Due Date | Status |
|------|-------|----------|--------|
| ______ | ______ | ______ | ______ |

## 9. Appendix

- Links to dashboards: ______
- Historical incident data: ______
- Related ADRs or design docs: ______
