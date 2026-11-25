#!/usr/bin/env bash
# Online schema change on MySQL with GitHub's gh-ost.
# Syncs via binlog (no triggers) - preferred on high-write tables.
set -euo pipefail

gh-ost \
  --host="${MYSQL_HOST:-localhost}" \
  --user="${MYSQL_USER:-gh-ost-user}" \
  --password="${MYSQL_PASSWORD:?set MYSQL_PASSWORD}" \
  --database="${MYSQL_DB:-mydb}" \
  --table=orders \
  --alter="ADD COLUMN priority INT DEFAULT 0" \
  --max-load=Threads_running=25 \
  --critical-load=Threads_running=50 \
  --chunk-size=1000 \
  --execute
