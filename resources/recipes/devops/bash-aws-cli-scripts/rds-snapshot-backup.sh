#!/bin/bash

set -euo pipefail

DB_INSTANCE="my-database"
SNAPSHOT_ID="${DB_INSTANCE}-snapshot-$(date +%Y%m%d-%H%M%S)"

aws rds create-db-snapshot \
    --db-instance-identifier "$DB_INSTANCE" \
    --db-snapshot-identifier "$SNAPSHOT_ID"

echo "Creating snapshot: $SNAPSHOT_ID"

# Wait for snapshot to complete
aws rds wait db-snapshot-available \
    --db-snapshot-identifier "$SNAPSHOT_ID"

echo "Snapshot created: $SNAPSHOT_ID"

# Clean up manual snapshots older than 30 days
# --snapshot-type manual skips automated backups, which delete-db-snapshot can't remove
OLD_SNAPSHOTS=$(aws rds describe-db-snapshots \
    --db-instance-identifier "$DB_INSTANCE" \
    --snapshot-type manual \
    --query "DBSnapshots[?SnapshotCreateTime<\`$(date -d '30 days ago' -I)\`].DBSnapshotIdentifier" \
    --output text)

for snapshot in $OLD_SNAPSHOTS; do
    echo "Deleting old snapshot: $snapshot"
    aws rds delete-db-snapshot --db-snapshot-identifier "$snapshot"
done
