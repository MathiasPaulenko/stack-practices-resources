# Failover Drill Checklist

Print or paste into the incident channel before starting a failover drill.

## Before the drill

- [ ] Declare the drill window and notify on-call
- [ ] Confirm backup/recovery path is green (last restore test < 30 days)
- [ ] Verify secondary region health checks pass
- [ ] Snapshot current metrics (error rate, p99, replication lag)
- [ ] Assign roles: incident commander, recovery lead, comms lead, scribe

## During the failover

- [ ] Timestamp: declare scenario start
- [ ] Promote replica / secondary region
- [ ] Update DNS or load balancer
- [ ] Run smoke tests on critical flows (login, payments, checkout)
- [ ] Verify replication caught up (compare record counts)
- [ ] Timestamp: service restored — compare against RTO target

## After the drill

- [ ] Fail back to primary (or document why not)
- [ ] Record actual vs target RTO/RPO for each step
- [ ] Log every gap: stale contact, missing credential, unclear step
- [ ] File one ticket per gap with owner and deadline
- [ ] Update the DR plan; schedule the next drill
