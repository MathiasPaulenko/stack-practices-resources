#!/bin/bash
set -euo pipefail

LOG_DIR="${1:-/var/log/myapp}"
RETENTION_DAYS="${2:-14}"
MAX_SIZE_MB="${3:-10}"

mkdir -p "$LOG_DIR/archive"

for log in "$LOG_DIR"/*.log; do
    [ -f "$log" ] || continue
    size_mb=$(du -m "$log" | cut -f1)

    if [ "$size_mb" -gt "$MAX_SIZE_MB" ]; then
        base=$(basename "$log" .log)
        timestamp=$(date +%Y%m%d-%H%M%S)
        rotated="$LOG_DIR/archive/${base}-${timestamp}.log"

        mv "$log" "$rotated"
        gzip "$rotated"
        # Recreate the log so the app can keep writing — and if it
        # supports it, signal it to reopen the fd (nginx, most daemons)
        touch "$log"
        # kill -HUP "$(cat /var/run/myapp.pid)" 2>/dev/null || true
    fi
done

find "$LOG_DIR/archive" -name '*.gz' -type f -mtime "+$RETENTION_DAYS" -delete

echo "[$(date -Iseconds)] Rotation done in $LOG_DIR"
