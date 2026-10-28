#!/bin/bash
set -euo pipefail

LOG_DIR="/var/log/myapp"
LOG_FILE="${LOG_DIR}/app.log"
RETENTION=14

# df column 5 is Use% (how FULL the disk is). -P keeps it on one line
USED_PERCENT=$(df -P "$LOG_DIR" | awk 'NR==2 {gsub(/%/,"",$5); print $5}')

if [ "$USED_PERCENT" -gt 90 ]; then
    echo "CRITICAL: disk at ${USED_PERCENT}% — pruning harder"
    RETENTION=3
fi

[ -f "$LOG_FILE" ] || exit 0

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ROTATED="${LOG_DIR}/app_${TIMESTAMP}.log"
mv "$LOG_FILE" "$ROTATED"
touch "$LOG_FILE"
gzip "$ROTATED"

find "$LOG_DIR" -name "app_*.log.gz" -type f -mtime +$RETENTION -delete

# Alert if the disk is still nearly full after rotation
USED_PERCENT=$(df -P "$LOG_DIR" | awk 'NR==2 {gsub(/%/,"",$5); print $5}')
if [ "$USED_PERCENT" -gt 90 ]; then
    echo "WARNING: disk still at ${USED_PERCENT}% after rotation"
fi
