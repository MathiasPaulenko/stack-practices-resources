#!/bin/bash
set -euo pipefail

LOG_DIR="/var/log/myapp"
LOG_FILE="${LOG_DIR}/app.log"
PID_FILE="/var/run/myapp.pid"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mv "$LOG_FILE" "${LOG_DIR}/app_${TIMESTAMP}.log"
touch "$LOG_FILE"

if [ -f "$PID_FILE" ]; then
    kill -HUP "$(cat "$PID_FILE")"
fi

# Give the app a moment to start writing to the new file
sleep 5
gzip "${LOG_DIR}/app_${TIMESTAMP}.log"

find "$LOG_DIR" -name "app_*.log.gz" -type f -mtime +14 -delete
