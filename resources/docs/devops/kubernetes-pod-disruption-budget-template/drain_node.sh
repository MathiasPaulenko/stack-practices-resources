#!/usr/bin/env bash
# Drain a node respecting Pod Disruption Budgets.
# Usage: ./drain_node.sh <node-name> [timeout]
set -euo pipefail

NODE="${1:?Usage: $0 <node-name> [timeout]}"
TIMEOUT="${2:-5m}"

echo "==> Cordoning ${NODE}"
kubectl cordon "${NODE}"

echo "==> PDBs that may block the drain"
kubectl get pdb -A -o wide

echo "==> Draining ${NODE} (timeout: ${TIMEOUT})"
kubectl drain "${NODE}" \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --timeout="${TIMEOUT}"

echo "==> Pods left on ${NODE}:"
kubectl get pods -A -o wide --field-selector "spec.nodeName=${NODE}"
