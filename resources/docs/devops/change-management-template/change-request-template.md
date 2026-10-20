# Change Request: `<Title>`

## 1. Change Summary

| Field | Value |
|-------|-------|
| Change ID | `CHG-YYYY-NNNN` |
| Title | `description` |
| Requester | `@name` |
| Team | `team` |
| Environment | `staging / production` |
| Scheduled Date / Time | `YYYY-MM-DD HH:MM UTC` |
| Duration (expected) | `X minutes / hours` |
| Risk Level | `Low / Medium / High / Critical` |

## 2. Change Description

**What is changing?**
[Describe the technical change in one paragraph.]

**Why is it needed?**
[Link to ticket, incident, or business justification.]

**What are the expected results?**
[Measurable outcome: latency reduced by X%, feature enabled for Y% of users.]

## 3. Impact Analysis

| System / Service | Impact | Validation Method |
|------------------|--------|-------------------|
| | | |

### Dependencies
- [ ] No dependent services affected
- [ ] Dependent services notified: `list`
- [ ] External partners / customers notified: `list`

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

## 4. Rollback Plan

| Condition | Rollback Action | Time to Complete | Owner |
|-----------|----------------|-------------------|-------|
| Change fails during deployment | `git revert` / config rollback | 10 min | `@name` |
| Performance degradation > 20% | Rollback to previous image / revert migration | 15 min | `@name` |
| Data inconsistency detected | Restore from pre-change snapshot | 30 min | `@name` |
| Unknown failure mode | Page on-call; execute emergency rollback runbook | 5 min | `@on-call` |

- [ ] Rollback has been tested in staging
- [ ] Rollback command is documented in runbook
- [ ] Database snapshot / backup taken before change
- [ ] Feature flag kill switch is ready (if applicable)

## 5. Approval

| Role | Name | Approved | Date |
|------|------|----------|------|
| Requester | | | |
| Technical Reviewer | | | |
| Product Owner (if user-facing) | | | |
| Security (if data / access change) | | | |
| CAB / Manager (High+ risk) | | | |

## 6. Execution Log

| Time (UTC) | Step | Result | Notes |
|------------|------|--------|-------|
| | | | |

## 7. Post-Change Review

- [ ] Change completed as planned
- [ ] Monitoring shows no anomalies for 1 hour post-change
- [ ] Rollback plan archived / updated based on lessons
- [ ] Ticket closed with outcome summary
