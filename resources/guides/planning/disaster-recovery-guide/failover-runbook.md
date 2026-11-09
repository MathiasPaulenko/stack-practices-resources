# Runbook: Database Failover to Secondary Region

## Trigger

- Primary region database health check fails for >2 minutes
- Automatic alert fires: `database-primary-down`

## Steps

1. **Verify outage** (1 min)
   - Check the monitoring dashboard
   - Confirm it is a region-level issue (not an isolated instance)

2. **Initiate failover** (2 min)
   - Run: `kubectl exec failover-script -- promote-replica`
   - Verify: the new primary accepts writes

3. **Update DNS** (2 min)
   - Switch the database CNAME to the secondary region
   - TTL: 60 seconds (pre-configured)

4. **Verify application health** (3 min)
   - Check application error rates
   - Verify critical user flows

5. **Communicate** (5 min)
   - Update the status page
   - Notify stakeholders

## Rollback

- When the primary recovers, plan failback during a maintenance window
- Sync writes that happened on the replica during the outage
- Validate data consistency (row counts, checksums) before failing back
