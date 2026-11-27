#!/bin/bash
# deploy.sh — serverless deployment pipeline
# Stages: tests -> package -> deploy -> smoke tests -> verify
# Usage: ./deploy.sh [stage]   (defaults to staging)

set -euo pipefail

STAGE="${1:-staging}"
SERVICE="order-service"

echo "=== Deploying $SERVICE to $STAGE ==="

# 1. Run tests
echo "Running tests..."
npm run test:unit
npm run test:integration -- --stage=$STAGE

# 2. Package
echo "Packaging..."
npx serverless package --stage $STAGE

# 3. Deploy
echo "Deploying..."
npx serverless deploy --stage $STAGE --verbose

# 4. Run smoke tests
echo "Running smoke tests..."
npm run test:smoke -- --stage=$STAGE --url=$(npx serverless info --stage $STAGE --verbose | grep "endpoint:" | awk '{print $2}')

# 5. Verify deployment
echo "Verifying deployment..."
npx serverless info --stage $STAGE

echo "=== Deployment complete ==="
