#!/bin/bash
# healthcheck-logged.sh — Health check that keeps an audit log.
# NOTE: writing to disk on every probe can fill the container layer
# on long-running services — use for debugging, not as a default.
LOG_FILE="/var/log/healthcheck.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    echo "$TIMESTAMP OK HTTP=$HTTP_CODE" >> "$LOG_FILE"
    exit 0
else
    echo "$TIMESTAMP FAIL HTTP=$HTTP_CODE" >> "$LOG_FILE"
    exit 1
fi
