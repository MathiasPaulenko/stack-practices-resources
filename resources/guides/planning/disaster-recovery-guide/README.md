# Disaster Recovery - Companion Resources

Runnable building blocks from the [Disaster Recovery guide](https://stackpractices.com/guides/disaster-recovery-guide/).

| File | What it is |
|---|---|
| `dr-tiers.yaml` | Service-tier RTO/RPO/strategy mapping. Fill in your own services per tier. |
| `postgres-backup.sh` | Writes a daily physical `pg_basebackup` archive plus custom-format logical dumps for selected databases, then ships both to S3. |
| `test-backup-restore.py` | Restores the newest logical `.dump` archive to a disposable database and checks a configured table. It does not restore the physical base-backup tar archive. |
| `failover-runbook.md` | Copy-ready database failover runbook: trigger, timed steps, rollback notes. |

## Quick start

```bash
# 1. Edit dr-tiers.yaml with your services.

# 2. Set BACKUP_DIR, S3_BUCKET, and DATABASES in postgres-backup.sh.
# DATABASES is a comma-separated list, such as app,reporting.

# 3. Run the backup script with PostgreSQL and AWS credentials configured.
./postgres-backup.sh

# 4. Restore the logical dump into a disposable database and check a real table.
export PGHOST=localhost PGUSER=postgres BACKUP_DIR=/backups CRITICAL_TABLE=public.orders
python test-backup-restore.py

# 5. Adapt failover-runbook.md to your DNS, alert names, and communication channels.
```

The physical base backup and logical dumps are distinct recovery artifacts. The restore check uses a `.dump` created by `pg_dump --format=custom`; it does not prove physical recovery or WAL replay. Run a separate physical recovery drill.

Requirements: PostgreSQL client tools (`pg_basebackup`, `pg_dump`, `pg_restore`, `psql`, `createdb`, `dropdb`), AWS CLI, Bash, and Python 3.10+. The target database must be disposable because the script drops it before restoring.
