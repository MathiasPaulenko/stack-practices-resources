#!/bin/bash
set -euo pipefail

LOG_DIR="${1:-/var/log/myapp}"
S3_BUCKET="${2:-my-app-logs}"
S3_PREFIX="logs/$(hostname)"
RETENTION_DAYS="${4:-90}"

# Upload archives older than a day (already rotated and compressed)
find "$LOG_DIR/archive" -name '*.gz' -type f -mtime +1 | while read -r archive; do
    rel_path="${archive#$LOG_DIR/archive/}"
    if aws s3 cp "$archive" "s3://$S3_BUCKET/$S3_PREFIX/$rel_path" \
        --storage-class STANDARD_IA --no-progress; then
        echo "[$(date -Iseconds)] Uploaded $rel_path"
        rm "$archive"
    else
        echo "[$(date -Iseconds)] FAILED $rel_path"
    fi
done

# Local copies past retention get deleted; a bucket lifecycle
# rule moves them to cheaper storage on S3
find "$LOG_DIR/archive" -name '*.gz' -type f -mtime "+$RETENTION_DAYS" -delete
