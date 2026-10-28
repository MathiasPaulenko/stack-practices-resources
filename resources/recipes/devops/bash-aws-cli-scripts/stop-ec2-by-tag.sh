#!/bin/bash

set -euo pipefail

# Stop all instances tagged Environment=dev
INSTANCE_IDS=$(aws ec2 describe-instances \
    --filters "Name=tag:Environment,Values=dev" "Name=instance-state-name,Values=running" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text)

if [ -z "$INSTANCE_IDS" ]; then
    echo "No running dev instances found"
    exit 0
fi

echo "Stopping instances: $INSTANCE_IDS"
aws ec2 stop-instances --instance-ids $INSTANCE_IDS

# Wait for stop
aws ec2 wait instance-stopped --instance-ids $INSTANCE_IDS
echo "All dev instances stopped"
