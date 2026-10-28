#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
RETENTION_DAYS="${1:-30}"

# Create snapshots of all EBS volumes with the Backup tag
VOLUME_IDS=$(aws ec2 describe-volumes \
    --filters "Name=tag:Backup,Values=true" \
    --query 'Volumes[*].VolumeId' \
    --output text \
    --region "$REGION")

for vol_id in $VOLUME_IDS; do
    SNAP_ID=$(aws ec2 create-snapshot \
        --volume-id "$vol_id" \
        --description "Automated backup $(date -I)" \
        --tag-specifications "ResourceType=snapshot,Tags=[{Key=CreatedBy,Value=bash-script},{Key=Date,Value=$(date -I)}]" \
        --query 'SnapshotId' \
        --output text \
        --region "$REGION")
    echo "Created snapshot $SNAP_ID for volume $vol_id"
done

# Delete snapshots older than retention period
CUTOFF=$(date -d "$RETENTION_DAYS days ago" -I)
OLD_SNAPS=$(aws ec2 describe-snapshots \
    --owner-ids self \
    --filters "Name=tag:CreatedBy,Values=bash-script" \
    --query "Snapshots[?StartTime<='$CUTOFF'].SnapshotId" \
    --output text \
    --region "$REGION")

for snap_id in $OLD_SNAPS; do
    aws ec2 delete-snapshot --snapshot-id "$snap_id" --region "$REGION"
    echo "Deleted old snapshot $snap_id"
done
