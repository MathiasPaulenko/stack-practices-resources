#!/usr/bin/env bash
# Zero-downtime secret rotation: create new -> roll deploy -> verify -> revoke old
set -euo pipefail
SECRET_NAME="${1:?usage: rotate_secret.sh <secret-name> <new-value>}"
NEW_VALUE="${2:?usage: rotate_secret.sh <secret-name> <new-value>}"

echo "1. Storing new version of $SECRET_NAME (old stays active)..."
aws secretsmanager put-secret-value --secret-id "$SECRET_NAME" --secret-string "$NEW_VALUE" --version-stages AWSPENDING

echo "2. Rolling deploy — instances pick up AWSPENDING/CURRENT as configured..."
# kubectl rollout restart deployment/myapp   # uncomment for K8s
# aws ecs update-service --service myapp --force-new-deployment

echo "3. Verify consumers migrated, then promote:"
echo "   aws secretsmanager update-secret-version-stage --secret-id $SECRET_NAME --version-stage AWSCURRENT --move-to-version-id <new-version>"
echo "4. Previous version auto-deprecates. Audit with: aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=$SECRET_NAME"
