# Disaster Recovery — Companion Resources

Runnable building blocks from the [Disaster Recovery guide](https://stackpractices.com/guides/disaster-recovery-guide/).

| File | What it is |
|---|---|
| `dr-tiers.yaml` | Service-tier RTO/RPO/strategy mapping. Fill in your own services per tier. |
| `postgres-backup.sh` | PostgreSQL backup: enables WAL archiving, takes a daily `pg_basebackup`, ships it to S3 in a second region, prunes locals after 7 days. |
| `test-backup-restore.py` | Restore-integrity check: restores the newest backup into a scratch DB and verifies a critical table has rows. Run it on a schedule — a backup you never restore is not a backup. |
| `failover-runbook.md` | Copy-ready database failover runbook: trigger, timed steps, rollback notes. |

## Quick start

```bash
# 1. Edit dr-tiers.yaml with your services.

# 2. Review postgres-backup.sh: set BACKUP_DIR and S3_BUCKET.

# 3. Verify a backup actually restores (needs pg_restore/psql + scratch DB):
export PGHOST=localhost PGUSER=postgres BACKUP_DIR=/backups CRITICAL_TABLE=orders
python test-backup-restore.py

# 4. Adapt failover-runbook.md to your DNS, alert names, and comms channels.
```

Requirements: PostgreSQL client tools (`pg_basebackup`, `pg_restore`, `psql`, `createdb`, `dropdb`), AWS CLI for the S3 copy, Python 3.10+ for the restore check.
