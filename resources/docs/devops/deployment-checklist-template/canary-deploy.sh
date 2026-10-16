#!/bin/bash
# Canary deployment with health checks (Kubernetes + Istio VirtualService)
set -euo pipefail

SERVICE="api"
NAMESPACE="production"
CANARY_PERCENT=10
BUILD_TAG="${BUILD_TAG:?required — set to the image tag you are releasing}"

echo "=== Canary Deployment: $SERVICE ==="

# Step 1: Deploy canary
echo "[1/5] Deploying canary pod..."
kubectl set image "deployment/$SERVICE-canary" "$SERVICE=registry.example.com/$SERVICE:$BUILD_TAG" -n "$NAMESPACE"
kubectl rollout status "deployment/$SERVICE-canary" -n "$NAMESPACE" --timeout=120s

# Step 2: Route 10% traffic to canary
echo "[2/5] Routing $CANARY_PERCENT% traffic to canary..."
kubectl patch virtualservice "$SERVICE" -n "$NAMESPACE" --type merge -p '{"spec":{"http":[{"route":[{"destination":{"host":"'"$SERVICE"'","subset":"stable"},"weight":90},{"destination":{"host":"'"$SERVICE"'","subset":"canary"},"weight":'"$CANARY_PERCENT"'}]}]}}'

# Step 3: Monitor for 10 minutes
echo "[3/5] Monitoring canary for 10 minutes..."
sleep 600

# Empty result is treated as a failure: unknown health is not healthy
ERROR_RATE=$(kubectl exec -n "$NAMESPACE" "deployment/$SERVICE-canary" -- curl -s http://localhost:8080/metrics | grep error_rate | awk '{print $2}' || true)
ERROR_RATE="${ERROR_RATE:-1}"
echo "  Error rate: $ERROR_RATE"

if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
  echo "  ERROR: Error rate too high, rolling back canary"
  kubectl patch virtualservice "$SERVICE" -n "$NAMESPACE" --type merge -p '{"spec":{"http":[{"route":[{"destination":{"host":"'"$SERVICE"'","subset":"stable"},"weight":100}]}]}}'
  kubectl delete "deployment/$SERVICE-canary" -n "$NAMESPACE"
  exit 1
fi

# Step 4: Promote to full rollout
echo "[4/5] Promoting canary to full rollout..."
kubectl set image "deployment/$SERVICE" "$SERVICE=registry.example.com/$SERVICE:$BUILD_TAG" -n "$NAMESPACE"
kubectl rollout status "deployment/$SERVICE" -n "$NAMESPACE" --timeout=300s

# Step 5: Clean up canary
echo "[5/5] Cleaning up canary resources..."
kubectl patch virtualservice "$SERVICE" -n "$NAMESPACE" --type merge -p '{"spec":{"http":[{"route":[{"destination":{"host":"'"$SERVICE"'","subset":"stable"},"weight":100}]}]}}'
kubectl delete "deployment/$SERVICE-canary" -n "$NAMESPACE"

echo "=== Canary Deployment Complete ==="
