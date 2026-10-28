#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${1:-/var/backups/app}"
S3_BUCKET="${2:-my-app-backups}"
S3_PREFIX="${3:-daily}"

TODAY=$(date +%Y-%m-%d)
ARCHIVE="$BACKUP_DIR/daily/app-$TODAY.tar.gz"

# The AWS CLI sends a SHA-256 checksum; S3 rejects mismatches.
# User metadata is a separate field, not the checksum.
aws s3 cp "$ARCHIVE" "s3://$S3_BUCKET/$S3_PREFIX/app-$TODAY.tar.gz" \
    --checksum-algorithm SHA256 \
    --metadata "created=$(date -I),host=$(hostname)" \
    --no-progress

# List recent backups in S3
echo "=== Recent S3 Backups ==="
aws s3 ls "s3://$S3_BUCKET/$S3_PREFIX/" --recursive | tail -10
