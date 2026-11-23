#!/bin/bash
set -euo pipefail

IMAGE_NAME="myapp"
REGISTRY="registry.example.com"
NEW_BASE="node:20-slim"

docker pull "$NEW_BASE"
docker build \
  --build-arg BASE_IMAGE="$NEW_BASE" \
  -t "$REGISTRY/$IMAGE_NAME:patched-$(date +%Y%m%d)" \
  -t "$REGISTRY/$IMAGE_NAME:latest" \
  .
trivy image --exit-code 1 --severity HIGH,CRITICAL \
  "$REGISTRY/$IMAGE_NAME:patched-$(date +%Y%m%d)"
docker push "$REGISTRY/$IMAGE_NAME:patched-$(date +%Y%m%d)"
docker push "$REGISTRY/$IMAGE_NAME:latest"
kubectl set image deployment/myapp \
  "app=$REGISTRY/$IMAGE_NAME:patched-$(date +%Y%m%d)" \
  -n production
kubectl rollout status deployment/myapp -n production
