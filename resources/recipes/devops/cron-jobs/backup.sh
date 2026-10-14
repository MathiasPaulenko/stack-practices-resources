#!/usr/bin/env bash
# Example backup script safe to run under cron.
# - set -euo pipefail: fail fast, report through MAILTO/logging
# - absolute paths only (cron's PATH is minimal)
# - timestamps in logs so journal/syslog review is possible
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/backup}"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG_PREFIX="[backup ${STAMP}]"

echo "${LOG_PREFIX} starting"

# Example: dump a Postgres database. Adapt the command to your stack.
# pg_dump "$DATABASE_URL" > "${BACKUP_DIR}/db-${STAMP}.sql"

# Retention: delete backups older than 30 days.
/usr/bin/find "${BACKUP_DIR}" -name '*.sql' -mtime +30 -delete 2>/dev/null || true

echo "${LOG_PREFIX} done"
