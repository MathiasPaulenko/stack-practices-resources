#!/bin/bash
# Verify that every namespace has a default-deny NetworkPolicy.
# Source article: https://stackpractices.com/docs/network-security-template/
# Requires: kubectl + jq.
set -euo pipefail

NAMESPACES=$(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}')
MISSING=0

for ns in $NAMESPACES; do
  POLICIES=$(kubectl get networkpolicy -n "$ns" -o json | \
    jq -r '.items[] | select(.metadata.name | test("default-deny")) | .metadata.name')

  if [ -z "$POLICIES" ]; then
    echo "WARNING: Namespace '$ns' has no default-deny network policy"
    MISSING=$((MISSING + 1))
  else
    echo "OK: Namespace '$ns' has policy: $POLICIES"
  fi
done

if [ "$MISSING" -gt 0 ]; then
  echo "$MISSING namespace(s) missing default-deny" >&2
  exit 1
fi
