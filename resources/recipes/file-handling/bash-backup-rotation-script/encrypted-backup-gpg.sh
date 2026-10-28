#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-/var/app/data}"
BACKUP_DIR="${2:-/var/backups/app}"
GPG_RECIPIENT="${3:-admin@example.com}"
RETENTION_DAYS=30

# Replace the placeholder with the fingerprint of the intended public key.
mkdir -p "$BACKUP_DIR/encrypted"
TODAY=$(date +%Y-%m-%d)
ARCHIVE="$BACKUP_DIR/encrypted/app-$TODAY.tar.gz.gpg"
TEMP_ARCHIVE=$(mktemp "$BACKUP_DIR/encrypted/.app-$TODAY.XXXXXX")
trap 'rm -f -- "$TEMP_ARCHIVE"' EXIT

# Create and encrypt backup in one pipeline (no unencrypted file on disk)
tar -czf - -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")" | \
    gpg --encrypt --recipient "$GPG_RECIPIENT" --output "$TEMP_ARCHIVE"

# GPG can parse the packet headers here; this isn't a restore test.
if ! gpg --list-packets "$TEMP_ARCHIVE" > /dev/null 2>&1; then
    echo "ERROR: Encrypted backup verification failed" >&2
    exit 1
fi
mv -f -- "$TEMP_ARCHIVE" "$ARCHIVE"
trap - EXIT

echo "[$(date -Iseconds)] Encrypted backup created: $ARCHIVE"

# Prune old encrypted files only after the new archive passed the packet check.
find "$BACKUP_DIR/encrypted" -name '*.gpg' -type f -mtime "+$RETENTION_DAYS" -delete

# Decrypt for restore:
# gpg --decrypt app-2026-01-15.tar.gz.gpg | tar -xzf - -C /restore/path
