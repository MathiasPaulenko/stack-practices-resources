#!/bin/bash
set -euo pipefail

# Kubernetes RBAC audit: cluster-admin bindings, per-namespace role bindings,
# and service accounts still carrying secret references.
# Requires: kubectl context configured, jq

echo "=== ClusterRoleBindings with cluster-admin ==="
kubectl get clusterrolebindings -o json | \
  jq -r '.items[] | select(.roleRef.name=="cluster-admin") | "\(.metadata.name) -> \(.subjects[].name // "unknown")"'

echo ""
echo "=== RoleBindings per namespace ==="
for ns in $(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'); do
  echo "--- Namespace: $ns ---"
  kubectl get rolebindings -n "$ns" -o json | \
    jq -r '.items[] | "\(.metadata.name): role=\(.roleRef.name) subjects=\([.subjects[].name] | join(", "))"'
done

echo ""
echo "=== Service accounts with secrets ==="
kubectl get serviceaccounts --all-namespaces -o json | \
  jq -r '.items[] | select(.secrets != null and (.secrets | length > 0)) | "\(.metadata.namespace)/\(.metadata.name)"'
