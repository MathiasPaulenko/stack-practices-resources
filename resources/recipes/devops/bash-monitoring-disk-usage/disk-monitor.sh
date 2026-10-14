#!/usr/bin/env bash
set -euo pipefail

THRESHOLD="${1:-80}"
EMAIL="${2:-admin@example.com}"

# Check all local mount points
df -Hl | awk 'NR>1 && /^\/dev/{print $1, $5, $6}' | while read -r fs usage mount; do
    usage_val="${usage%\%}"
    if (( usage_val >= THRESHOLD )); then
        echo "WARNING: $mount ($fs) is at $usage"
        # Send alert (example with mail)
        echo "Disk usage on $mount is $usage" | mail -s "Disk alert: $mount" "$EMAIL"
    else
        echo "OK: $mount is at $usage"
    fi
done

# Optional: trigger cleanup for specific mounts
# if (( usage_val >= 90 )); then
#     /usr/local/bin/cleanup-logs.sh
# fi
