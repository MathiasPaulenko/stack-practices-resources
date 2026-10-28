#!/usr/bin/env bash
set -euo pipefail
# restore-backup.sh — extracts an archive into an empty dir for inspection

BACKUP_FILE="${1:?Usage: $0 <backup_file>}"
RESTORE_DIR="/tmp/restore"

mkdir -p "${RESTORE_DIR}"

if [[ "$BACKUP_FILE" == *.gpg ]]; then
    gpg -d "${BACKUP_FILE}" | tar -xzf - -C "${RESTORE_DIR}"
else
    tar -xzf "${BACKUP_FILE}" -C "${RESTORE_DIR}"
fi

echo "Restored to ${RESTORE_DIR} — verify the tree before copying anything over live data"
