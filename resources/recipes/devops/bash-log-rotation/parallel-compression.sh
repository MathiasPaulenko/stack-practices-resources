#!/bin/bash
set -euo pipefail

LOG_DIR="/var/log/myapp"
LOG_FILE="${LOG_DIR}/app.log"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

[ -f "$LOG_FILE" ] || exit 0

ROTATED="${LOG_DIR}/app_${TIMESTAMP}.log"
mv "$LOG_FILE" "$ROTATED"
touch "$LOG_FILE"

# pigz uses all cores — ~2x faster than gzip on multi-core
if command -v pigz >/dev/null; then
    pigz "$ROTATED"
else
    gzip "$ROTATED"
fi

find "$LOG_DIR" -name "app_*.log.gz" -type f -mtime +14 -delete
