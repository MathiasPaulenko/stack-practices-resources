#!/usr/bin/env bash
# Ordered Kubernetes network debugging workflow.
# Work the layers top-down: endpoints -> DNS -> connectivity -> policy
# -> CNI -> Ingress -> packets -> conntrack.
# Usage: NAMESPACE=production POD=<pod> SVC=api-service ./debug-commands.sh
set -euo pipefail

NAMESPACE="${NAMESPACE:-production}"
POD="${POD:?Set POD to a running pod name}"
SVC="${SVC:?Set SVC to the service name}"

echo "== 1. Endpoints (empty = selector/readiness problem) =="
kubectl get endpoints "$SVC" -n "$NAMESPACE"
kubectl describe svc "$SVC" -n "$NAMESPACE"

echo "== 2. DNS from inside the pod =="
kubectl exec -it "$POD" -n "$NAMESPACE" -- nslookup "$SVC.$NAMESPACE" || true
kubectl get svc -n kube-system kube-dns

echo "== 3. Direct connectivity =="
kubectl exec -it "$POD" -n "$NAMESPACE" -- curl -sv "http://$SVC.$NAMESPACE:80" || true

echo "== 4. NetworkPolicies in scope =="
kubectl get networkpolicy -n "$NAMESPACE"

echo "== 5. CNI health =="
kubectl get pods -n kube-system | grep -E "calico|cilium|flannel" || true

echo "== 6. Ingress programming =="
kubectl get ingress -n "$NAMESPACE"

echo "Done. For packet-level checks use nicolaka/netshoot via 'kubectl debug'."
