#!/usr/bin/env bash
set -euo pipefail

CLEANUP_THRESHOLD="${1:-90}"
LOG_DIR="${2:-/var/log/app}"
ARCHIVE_DIR="${3:-/var/log/archive}"

df -Hl | awk 'NR>1 && /^\/dev/{print $1, $5, $6}' | while read -r fs usage mount; do
    usage_val="${usage%\%}"
    if (( usage_val >= CLEANUP_THRESHOLD )); then
        echo "[$(date -Iseconds)] CRITICAL: $mount at $usage — triggering cleanup"

        # Compress logs older than 7 days
        find "$LOG_DIR" -name "*.log" -mtime +7 -exec gzip -9 {} \;

        # Move compressed logs to archive
        find "$LOG_DIR" -name "*.gz" -mtime +1 -exec mv {} "$ARCHIVE_DIR/" \;

        # Delete archives older than 90 days
        find "$ARCHIVE_DIR" -name "*.gz" -mtime +90 -delete

        # Clean package manager cache
        if command -v apt-get &>/dev/null; then
            apt-get clean
        elif command -v yum &>/dev/null; then
            yum clean all
        fi

        # Clean Docker if present
        if command -v docker &>/dev/null; then
            docker system prune -f --volumes
        fi

        # Report freed space
        new_usage=$(df -Hl "$mount" | awk 'NR>1 {print $5}')
        echo "[$(date -Iseconds)] Cleanup complete. $mount now at $new_usage"
    fi
done
