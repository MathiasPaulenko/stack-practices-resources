#!/usr/bin/env bash
set -euo pipefail

THRESHOLD=80
STATE_FILE="${STATE_FILE:-/var/run/disk-alert-state}"
touch "$STATE_FILE"

df -Hl | awk 'NR>1 && /^\/dev/{print $1, $5, $6}' | while read -r fs usage mount; do
    usage_val="${usage%\%}"
    if (( usage_val >= THRESHOLD )) && ! grep -qx "$mount" "$STATE_FILE"; then
        echo "$mount" >> "$STATE_FILE"
        echo "Disk alert on $(hostname): $mount at $usage" | mail -s "Disk alert: $mount" admin@example.com
    elif (( usage_val < THRESHOLD )) && grep -qx "$mount" "$STATE_FILE"; then
        sed -i "\|^${mount}$|d" "$STATE_FILE"
        echo "RECOVERED: $mount back to $usage"
    fi
done
