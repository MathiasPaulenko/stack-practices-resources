#!/usr/bin/env bash
# PostgreSQL backup strategy: WAL archiving for point-in-time recovery
# plus a daily compressed base backup. Copy backups to a second region.
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/backups}"
S3_BUCKET="${S3_BUCKET:-s3://my-backups}"
DATE="$(date +%Y%m%d)"

# 1. Enable continuous WAL archiving (run once, requires restart).
cat <<'EOF' >> postgresql.conf
archive_mode = on
archive_command = 'aws s3 cp %p s3://my-backups/wal/%f'
wal_level = replica
EOF

# 2. Daily base backup, compressed tar format.
pg_basebackup -D "${BACKUP_DIR}/${DATE}" -Ft -z -P

# 3. Ship the base backup to the DR region.
aws s3 cp --recursive "${BACKUP_DIR}/${DATE}" "${S3_BUCKET}/base/${DATE}/"

# 4. Prune local backups older than 7 days (keep 30d in S3/cold storage).
find "${BACKUP_DIR}" -maxdepth 1 -type d -mtime +7 -exec rm -rf {} +

echo "Backup ${DATE} complete and shipped to ${S3_BUCKET}"
