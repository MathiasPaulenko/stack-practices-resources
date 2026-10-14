#!/usr/bin/env bash
set -euo pipefail

ALERT_EMAIL="admin@example.com"

# Format: "mountpoint:threshold"
PARTITIONS=(
    "/:80"
    "/var:90"
    "/home:75"
    "/tmp:85"
)

for entry in "${PARTITIONS[@]}"; do
    mount="${entry%%:*}"
    threshold="${entry##*:}"

    usage_val=$(df -H "$mount" | awk 'NR>1 {print $5}' | tr -d '%')

    if (( usage_val >= threshold )); then
        echo "ALERT: $mount at ${usage_val}% (threshold: ${threshold}%)"
        echo "Partition $mount at ${usage_val}%" | mail -s "Disk alert: $mount" "$ALERT_EMAIL"
    fi
done
