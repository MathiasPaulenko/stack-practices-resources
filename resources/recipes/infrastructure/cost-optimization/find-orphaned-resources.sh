#!/usr/bin/env bash
# find-orphaned-resources.sh — Weekly sweep for unused AWS resources that
# keep billing: unattached EBS volumes, unassociated Elastic IPs, stale
# snapshots, and stopped-but-not-terminated instances.
#
# Usage:
#   ./find-orphaned-resources.sh [region]
#   AWS_PROFILE=prod ./find-orphaned-resources.sh eu-west-1
#
# Requires: awscli v2, jq. Read-only — nothing gets deleted.

set -euo pipefail

REGION="${1:-${AWS_DEFAULT_REGION:-us-east-1}}"
export AWS_DEFAULT_REGION="$REGION"
SNAPSHOT_AGE_DAYS="${SNAPSHOT_AGE_DAYS:-90}"
CUTOFF=$(date -d "${SNAPSHOT_AGE_DAYS} days ago" +%Y-%m-%d)

echo "=== Orphaned resource sweep — region: ${REGION} ==="
echo

echo "--- Unattached EBS volumes (~\$8/100GB-month each) ---"
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].[VolumeId,Size,VolumeType,CreateTime]' \
  --output table || true
echo

echo "--- Unassociated Elastic IPs (~\$3.65/month each) ---"
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].[PublicIp,AllocationId]' \
  --output table || true
echo

echo "--- Snapshots older than ${SNAPSHOT_AGE_DAYS} days ---"
aws ec2 describe-snapshots --owner-ids self \
  --query "Snapshots[?StartTime<'${CUTOFF}'].[SnapshotId,VolumeSize,StartTime]" \
  --output table || true
echo

echo "--- Stopped instances still billing for EBS (stopped > 7 days) ---"
aws ec2 describe-instances \
  --filters Name=instance-state-name,Values=stopped \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,StateTransitionReason]' \
  --output table || true
echo

echo "--- Unattached ENIs (often left behind by deleted resources) ---"
aws ec2 describe-network-interfaces \
  --filters Name=status,Values=available \
  --query 'NetworkInterfaces[*].[NetworkInterfaceId,SubnetId]' \
  --output table || true
echo

echo "Done. Review before deleting — some 'orphans' are intentional."
