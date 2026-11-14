#!/bin/bash
# cleanup-old-version.sh — retire v1 after full canary promotion
set -e

# 1. Remove old VirtualService weights (apply the v2-only manifest)
kubectl apply -f virtual-service-v2-only.yaml

# 2. Scale down v1 deployment
kubectl scale deployment api-v1 --replicas=0

# 3. Wait for pods to terminate
kubectl wait --for=delete pods -l app=api,version=v1 --timeout=60s

# 4. Remove v1 deployment
kubectl delete deployment api-v1

# 5. Remove v1 subset from DestinationRule
kubectl apply -f destination-rule-v2-only.yaml

echo "Cleanup complete. Only v2 is running."
