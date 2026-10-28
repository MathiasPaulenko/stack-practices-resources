#!/usr/bin/env bash
set -euo pipefail

DB_NAME="myapp"
DB_USER="postgres"          # expects ~/.pgpass or PGUSER auth — no password prompt in cron
BACKUP_DIR="/backups/db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DUMP_FILE="${BACKUP_DIR}/db_${TIMESTAMP}.sql.gz"

mkdir -p "${BACKUP_DIR}"

# pipefail makes the pipeline fail if pg_dump fails, not just gzip
pg_dump -U "${DB_USER}" -w "${DB_NAME}" | gzip > "${DUMP_FILE}"
gzip -t "${DUMP_FILE}"

# Keep last 14 days — only runs when the dump above succeeded
find "${BACKUP_DIR}" -name "db_*.sql.gz" -type f -mtime +14 -delete

echo "Database backup created: db_${TIMESTAMP}.sql.gz"
