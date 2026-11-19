#!/usr/bin/env bash
# PostgreSQL backup strategy: WAL archiving for point-in-time recovery
# plus a daily compressed base backup. Copy backups to a second region.
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/backups}"
S3_BUCKET="${S3_BUCKET:-s3://my-backups}"
DATE="$(date +%Y%m%d)"
mkdir -p "${BACKUP_DIR}"

# Configure WAL archiving once in postgresql.conf; archive_mode and wal_level
# require a restart. Set archive_command to the WAL destination for this cluster.
# archive_mode = on
# wal_level = replica
# archive_command = 'aws s3 cp %p s3://my-backups/wal/%f'

# 2. Daily base backup, compressed tar format.
pg_basebackup -D "${BACKUP_DIR}/${DATE}" -Ft -z -P

# Create logical archives for isolated restore checks.
DATABASES="${DATABASES:-postgres}"
IFS=',' read -r -a DATABASE_LIST <<< "${DATABASES}"
for DATABASE in "${DATABASE_LIST[@]}"; do
  DUMP_FILE="${BACKUP_DIR}/${DATE}-${DATABASE}.dump"
  pg_dump --format=custom --file="${DUMP_FILE}" "${DATABASE}"
  aws s3 cp "${DUMP_FILE}" "${S3_BUCKET}/logical/${DATE}-${DATABASE}.dump"
done

# 3. Ship the base backup to the DR region.
aws s3 cp --recursive "${BACKUP_DIR}/${DATE}" "${S3_BUCKET}/base/${DATE}/"

# 4. Prune local backups older than 7 days (keep 30d in S3/cold storage).
find "${BACKUP_DIR}" -maxdepth 1 -type d -mtime +7 -exec rm -rf -- {} +
find "${BACKUP_DIR}" -maxdepth 1 -type f -name '*.dump' -mtime +7 -delete

echo "Physical backup and logical dumps for ${DATABASES:-postgres} shipped to ${S3_BUCKET}"
