#!/bin/bash
# Rotate a Docker Swarm secret without downtime.
# Swarm secrets are immutable: create a new one, re-point the service, drop the old one.
set -e

SECRET_NAME="db_password"
SERVICE_NAME="api"
NEW_VALUE=$(openssl rand -base64 32)

# Create the new secret
echo "$NEW_VALUE" | docker secret create "${SECRET_NAME}_v2" -

# Re-point the service: drop the old mount, mount the new secret under the same name
docker service update \
    --secret-rm "$SECRET_NAME" \
    --secret-add "source=${SECRET_NAME}_v2,target=${SECRET_NAME}" \
    "$SERVICE_NAME"

# Wait for the rolling update
sleep 30

# Remove the old secret
docker secret rm "$SECRET_NAME"

echo "Rotation complete for $SECRET_NAME"
