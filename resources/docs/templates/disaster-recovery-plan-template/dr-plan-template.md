# Disaster Recovery Plan: [Service / System Name]

## Overview

| Field | Value |
|-------|-------|
| **Plan owner** | [team or individual] |
| **Last tested** | [date] |
| **RTO** | [hours — max acceptable downtime] |
| **RPO** | [minutes — max acceptable data loss] |
| **Declaration authority** | [who can declare a disaster] |

## Risk Scenarios

| Scenario | Likelihood | Impact | Mitigation |
|----------|-----------|--------|------------|
| Region outage | Medium | Critical | Multi-region deployment |
| Database corruption | Low | Critical | Point-in-time restore |
| Credential compromise | Medium | High | Token rotation + IAM lockdown |
| Third-party outage | High | Medium | Circuit breakers + fallback |

## Failover Procedures

### Scenario: Primary Region Unavailable

1. **Detect** — monitoring alert confirms regional health check failure
2. **Decide** — incident commander confirms failover (not flapping)
3. **Route** — update DNS / load balancer to secondary region
4. **Verify** — smoke tests pass in secondary region
5. **Communicate** — update status page and internal channels

### Scenario: Database Corruption

1. **Stop writes** — set database to read-only
2. **Identify** — determine corruption scope and time of event
3. **Restore** — restore from latest clean backup to new instance
4. **Replay** — apply WAL / binlog up to just before corruption
5. **Validate** — run data integrity checks
6. **Switch** — promote restored instance to primary

## Recovery Runbook

```bash
# 1. Verify secondary region health
kubectl --context=dr get nodes

# 2. Promote read replicas
gcloud sql instances promote-replica dr-replica

# 3. Update DNS
aws route53 change-resource-record-sets --hosted-zone-id Z123 \
  --change-batch file://failover.json

# 4. Verify
./smoke-tests.sh --env=dr
```

## Dependencies and Their DR Status

| Dependency | Their RTO | Our Fallback |
|------------|-----------|-------------|
| Payment processor | 4 hours | Queue transactions, retry later |
| Identity provider | 1 hour | Cached JWT validation + degraded login |
| CDN | 0 minutes | Multi-CDN switch |

## Roles During a Disaster

| Role | Responsibility |
|------|---------------|
| Incident commander | Declares the disaster, approves failover |
| Recovery lead | Executes the runbook steps |
| Communications lead | Status page, stakeholders, customers |
| Scribe | Timelines every action for the postmortem |

## Testing Schedule

| Test Type | Frequency | Last Completed | Result |
|-----------|-----------|----------------|--------|
| Tabletop exercise | Quarterly | [date] | [pass / gaps found] |
| Failover drill | Bi-annually | [date] | [pass / gaps found] |
| Backup restore test | Monthly | [date] | [pass / gaps found] |
| Chaos engineering | Monthly | [date] | [pass / gaps found] |

## Communication Plan

| Audience | Trigger | Message | Channel |
|----------|---------|---------|---------|
| Engineering | Any DR event | Incident channel | Slack #incidents |
| Leadership | RTO > 50% | Status update | Email + call |
| Customers | RTO > 75% | Status page + tweet | Status page |
