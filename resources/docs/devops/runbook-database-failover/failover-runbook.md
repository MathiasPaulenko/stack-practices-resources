# Database Failover Runbook: `<Service Name>`

## 1. Verify the Failure (2 minutes)

### Check Primary Health

```bash
psql -h primary.db.internal -U monitor -c "SELECT pg_is_in_recovery();"

## MySQL
mysql -h primary.db.internal -u monitor -e "SHOW STATUS LIKE 'Threads_connected';"
```

| Check | Expected | Action if Failed |
|-------|----------|------------------|
| Ping primary | < 10ms response | Proceed to failover |
| Connection count | < max_connections | Check for connection storm |
| Replication lag | N/A (primary) | Confirm primary is source |
| Disk space | > 10% free | If full, failover is only option |

### Confirm Replica is Ready

```bash
## PostgreSQL
psql -h replica.db.internal -U monitor -c "SELECT pg_last_xact_replay_timestamp();"

## MySQL 8.0.22+ (use SHOW SLAVE STATUS / Seconds_Behind_Master on older versions)
mysql -h replica.db.internal -u monitor -e "SHOW REPLICA STATUS\G" | grep Seconds_Behind_Source
```

**Decision Gate:** Only proceed if replica lag < 5 seconds and replica disk is healthy.

## 2. Stop Writes to Primary (1 minute)

```bash
## Set application to read-only mode (if available)
curl -X POST http://app.internal/admin/read-only

## Or block at load balancer
## Block port 5432/3306 at primary security group
```

## 3. Promote Replica to Primary (3 minutes)

### PostgreSQL

```bash
## On the replica
sudo -u postgres pg_ctl promote -D /var/lib/postgresql/data

## Verify promotion
psql -h replica.db.internal -U monitor -c "SELECT pg_is_in_recovery();"  # Should return false
```

### MySQL

```bash
## On the replica (MySQL 8.0.22+; use STOP SLAVE / RESET SLAVE ALL on older versions)
mysql -u root -e "STOP REPLICA; RESET REPLICA ALL;"

## Verify
mysql -u root -e "SHOW REPLICA STATUS\G"    # Should return Empty set
mysql -u root -e "SHOW BINARY LOG STATUS;"  # Should show binary log position (SHOW MASTER STATUS on MySQL < 8.4)
```

### AWS RDS

```bash
aws rds promote-read-replica \
  --db-instance-identifier replica-01 \
  --region us-east-1
```

## 4. Update Application Configuration (2 minutes)

```bash
## Update environment variable or config map
export DB_HOST=replica.db.internal

## Reload application (zero-downtime if using connection pool)
sudo systemctl reload app

## Or for Kubernetes
kubectl set env deployment/app DB_HOST=replica.db.internal
kubectl rollout status deployment/app
```

## 5. DNS / Load Balancer Cutover (2 minutes)

| Method | Command | RTO |
|--------|---------|-----|
| DNS A record | Update to replica IP | 5-60 seconds (TTL dependent) |
| Load balancer | Swap target group | 10-30 seconds |
| Service mesh (Consul) | `consul catalog services` update | 5-10 seconds |
| Kubernetes Service | Update endpoint or service selector | Immediate |

```bash
## Example: AWS Route53
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456789 \
  --change-batch file://failover-dns.json
```

## 6. Verify Application Functionality (3 minutes)

```bash
## Health check
curl -f http://app.internal/health

## Write test
curl -X POST http://app.internal/api/test \
  -H "Content-Type: application/json" \
  -d '{"test": "failover-write-2026-06-26"}'

## Read verification — replace <id> with the ID returned by the write test
curl http://app.internal/api/test/<id>
```

| Verification | Status | Time |
|--------------|--------|------|
| Health checks passing | [ ] | ___ |
| Write successful | [ ] | ___ |
| Read-back correct | [ ] | ___ |
| Replication lag (new replica) | < 1s | ___ |
| Error rate < 0.1% | [ ] | ___ |

## 7. Establish New Replication (5 minutes)

### Option A: Repair Old Primary (if recoverable)

```bash
## Reconfigure old primary as replica
## PostgreSQL — the target data directory must be empty (move or wipe the old one first)
pg_basebackup -h new-primary.db.internal -D /var/lib/postgresql/data -Fp -Xs -P
## Edit recovery.conf or postgresql.auto.conf with primary_conninfo
sudo -u postgres pg_ctl start
```

### Option B: Spin Up New Replica

```bash
## From snapshot or base backup
aws rds create-db-instance-read-replica \
  --db-instance-identifier new-replica-01 \
  --source-db-instance-identifier new-primary-01
```

## 8. Post-Incident Actions

- [ ] Update incident timeline with exact times for each step
- [ ] Capture logs from old primary for root cause analysis
- [ ] Document data loss (if any) with exact transaction IDs
- [ ] Schedule postmortem within 24 hours
- [ ] Update this runbook with lessons learned
