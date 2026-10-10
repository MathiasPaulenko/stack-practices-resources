# Database Failover — Companion Resources

Companion files for the [Database Failover Runbook](https://stackpractices.com/docs/runbook-database-failover/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `failover-runbook.md` | Markdown | Ready-to-adapt runbook: verification gates, promotion commands for PostgreSQL/MySQL/RDS, cutover checklist, and post-incident actions |
| `failover.sh` | Bash | Automated failover script with pre-flight checks, `--dry-run` and `--force` safety gates |
| `patroni.yml` | YAML | Patroni configuration for automated PostgreSQL failover with etcd DCS |
| `verify-consistency.py` | Python | Post-failover consistency check: LSN comparison, replication slot health, estimated transaction loss |

## Quick start

### 1. Copy the runbook

```bash
cp failover-runbook.md oncall/failover-runbook.md
```

Fill in your service name, hostnames (`*.db.internal`), credential roles, and lag thresholds before an incident happens.

### 2. Dry-run the automation

```bash
chmod +x failover.sh
./failover.sh --dry-run   # pre-flight checks only, no changes
./failover.sh             # run the real failover when needed
```

Edit `PRIMARY_HOST`, `REPLICA_HOST`, `DB_USER`, and `MAX_LAG_SECONDS` at the top of the script to match your environment.

### 3. Verify after promotion

```bash
pip install psycopg2-binary
python verify-consistency.py
```

Set `new_primary_host` and `old_primary_lsn` in the example call at the bottom of the script.

## Decision gates (defaults from the runbook)

| Gate | Threshold | Action |
|------|-----------|--------|
| Replica lag | < 5 seconds | Proceed only if met; otherwise wait or document data loss |
| Post-promotion lag (new replica) | < 1 second | Confirm before closing the incident |
| Error rate after cutover | < 0.1% | Investigate before declaring success |

## References

- [AWS RDS — Promoting a read replica](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html#USER_ReadRepl.Promote)
- [Patroni documentation](https://patroni.readthedocs.io/en/latest/)
- [PostgreSQL — Log-shipping standby servers](https://www.postgresql.org/docs/current/warm-standby.html)
