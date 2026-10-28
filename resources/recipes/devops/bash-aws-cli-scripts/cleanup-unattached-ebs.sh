#!/bin/bash

set -euo pipefail

# Find unattached volumes
VOLUMES=$(aws ec2 describe-volumes \
    --filters "Name=status,Values=available" \
    --query 'Volumes[*].[VolumeId,Size,Tags[?Key==`Name`].Value | [0]]' \
    --output text)

if [ -z "$VOLUMES" ]; then
    echo "No unused volumes found"
    exit 0
fi

echo "Unused EBS volumes:"
echo "$VOLUMES"

# Delete each volume
for vol_id in $(echo "$VOLUMES" | awk '{print $1}'); do
    echo "Deleting volume: $vol_id"
    aws ec2 delete-volume --volume-id "$vol_id"
done

echo "Cleanup complete"
