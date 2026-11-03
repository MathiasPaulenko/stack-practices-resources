#!/usr/bin/env bash
# Rollback procedures for the CI/CD pipeline design template.
# Usage:
#   ./rollback.sh blue-green      # switch traffic back to blue
#   ./rollback.sh rolling         # undo last rolling deployment
#   ./rollback.sh revision <n>    # rollback to a specific revision
#   ./rollback.sh verify          # run post-rollback checks
set -euo pipefail

NAMESPACE="${NAMESPACE:-production}"
APP="${APP:-app}"

blue_green() {
  kubectl patch service/"$APP" --namespace "$NAMESPACE" \
    -p '{"spec":{"selector":{"version":"blue"}}}'
  echo "Traffic switched back to blue in $NAMESPACE"
}

rolling() {
  kubectl rollout undo "deployment/$APP" --namespace "$NAMESPACE"
  kubectl rollout status "deployment/$APP" --namespace "$NAMESPACE" --timeout=5m
}

revision() {
  local rev="${1:?usage: rollback.sh revision <n>}"
  kubectl rollout undo "deployment/$APP" --namespace "$NAMESPACE" --to-revision="$rev"
  kubectl rollout status "deployment/$APP" --namespace "$NAMESPACE" --timeout=5m
}

verify() {
  echo "== current image =="
  kubectl get deployment "$APP" --namespace "$NAMESPACE" \
    -o jsonpath='{.spec.template.spec.containers[0].image}'
  echo
  echo "== pods =="
  kubectl get pods -l "app=$APP" --namespace "$NAMESPACE" \
    --field-selector=status.phase=Running
  echo "== recent logs =="
  kubectl logs -l "app=$APP" --namespace "$NAMESPACE" --tail=50
}

case "${1:-}" in
  blue-green) blue_green ;;
  rolling)    rolling ;;
  revision)   revision "${2:-}" ;;
  verify)     verify ;;
  *) echo "usage: $0 {blue-green|rolling|revision <n>|verify}" >&2; exit 1 ;;
esac
