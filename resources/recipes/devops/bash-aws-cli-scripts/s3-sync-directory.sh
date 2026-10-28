#!/bin/bash

set -euo pipefail

LOCAL_DIR="/var/backups/app"
S3_BUCKET="my-app-backups"
S3_PREFIX="daily"

# Sync with delete and exclude temp files
aws s3 sync "$LOCAL_DIR" "s3://${S3_BUCKET}/${S3_PREFIX}/" \
    --delete \
    --exclude "*.tmp" \
    --exclude "*.lock" \
    --storage-class STANDARD_IA

echo "Synced $LOCAL_DIR to s3://${S3_BUCKET}/${S3_PREFIX}/"
