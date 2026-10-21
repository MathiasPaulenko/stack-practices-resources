#!/bin/bash
# Check and report key rotation status across AWS KMS
set -euo pipefail

REGION="us-east-1"
ALERT_DAYS=7

for key_id in $(aws kms list-keys --region $REGION --query 'Keys[*].KeyId' --output text); do
  rotation_status=$(aws kms get-key-rotation-status --key-id $key_id --region $REGION --query 'KeyRotationEnabled' --output text 2>/dev/null || echo "N/A")
  key_desc=$(aws kms describe-key --key-id $key_id --region $REGION --query 'KeyMetadata.Description' --output text 2>/dev/null || echo "N/A")
  creation_date=$(aws kms describe-key --key-id $key_id --region $REGION --query 'KeyMetadata.CreationDate' --output text 2>/dev/null || echo "N/A")

  echo "Key: $key_id | Description: $key_desc | Rotation: $rotation_status | Created: $creation_date"

  if [ "$rotation_status" = "False" ]; then
    echo "WARNING: Key $key_id does not have automatic rotation enabled"
  fi
done
