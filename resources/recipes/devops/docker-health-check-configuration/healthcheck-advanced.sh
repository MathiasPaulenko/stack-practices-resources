#!/bin/bash
# healthcheck-advanced.sh — Multi-step health verification.
# Fails if the HTTP endpoint is down, disk is over 90%, the app
# process is missing, or memory usage exceeds 95%.
set -e

FAIL=0

# Step 1: Check HTTP endpoint
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ]; then
    echo "FAIL: HTTP endpoint returned $HTTP_CODE"
    FAIL=1
fi

# Step 2: Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print int($5)}')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "FAIL: Disk usage at ${DISK_USAGE}%"
    FAIL=1
fi

# Step 3: Check if critical process is running
if ! pgrep -x "gunicorn" > /dev/null; then
    echo "FAIL: gunicorn process not found"
    FAIL=1
fi

# Step 4: Check memory usage
MEM_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 95 ]; then
    echo "FAIL: Memory usage at ${MEM_USAGE}%"
    FAIL=1
fi

if [ "$FAIL" -eq 0 ]; then
    exit 0
else
    exit 1
fi
