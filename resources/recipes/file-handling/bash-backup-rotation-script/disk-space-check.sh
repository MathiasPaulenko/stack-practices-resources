#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/backups"
SOURCE_DIR="/var/www/myapp"

mkdir -p "${BACKUP_DIR}"   # df fails on a missing dir — create it first

# df -kP is POSIX: kilobytes on GNU and BSD, one line of output
available_kb=$(df -kP "${BACKUP_DIR}" | awk 'NR==2 {print $4}')
required_kb=$(du -sk "${SOURCE_DIR}" | awk '{print $1}')
available_gb=$((available_kb / 1024 / 1024))

if [ "$available_kb" -lt "$required_kb" ]; then
    echo "ERROR: only ${available_gb}GB free in ${BACKUP_DIR}, source needs $((required_kb / 1024 / 1024))GB"
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf "${BACKUP_DIR}/backup_${TIMESTAMP}.tar.gz" -C "${SOURCE_DIR}" .
echo "Backup created with ${available_gb}GB free space"
