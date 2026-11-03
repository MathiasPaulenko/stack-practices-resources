#!/usr/bin/env bash
# Rollback procedures from the CI/CD Pipeline Guide.
# Usage:
#   ./rollback.sh undo [deployment]    # rollback to previous ReplicaSet
#   ./rollback.sh revision <n> [dep]   # rollback to a specific revision
#   ./rollback.sh verify [deployment]  # post-rollback checks
set -euo pipefail

DEP="${2:-${1:-app}}"
NAMESPACE="${NAMESPACE:-production}"

case "${1:-}" in
  undo)
    kubectl rollout undo "deployment/${DEP}" --namespace "$NAMESPACE"
    kubectl rollout status "deployment/${DEP}" --namespace "$NAMESPACE" --timeout=5m
    ;;
  revision)
    kubectl rollout undo "deployment/${DEP}" --namespace "$NAMESPACE" --to-revision="$2"
    kubectl rollout status "deployment/${DEP}" --namespace "$NAMESPACE" --timeout=5m
    ;;
  verify)
    kubectl get deployment "$DEP" --namespace "$NAMESPACE" -o jsonpath='{.spec.template.spec.containers[0].image}'; echo
    kubectl get pods -l "app=$DEP" --namespace "$NAMESPACE" --field-selector=status.phase=Running
    kubectl logs -l "app=$DEP" --namespace "$NAMESPACE" --tail=30
    ;;
  *) echo "usage: $0 {undo|revision <n>|verify} [deployment]" >&2; exit 1 ;;
esac
