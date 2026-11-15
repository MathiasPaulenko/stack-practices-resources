#!/usr/bin/env bash
# Quick quota audit for a namespace.
# Usage: ./check_quota.sh <namespace>
set -euo pipefail

NS="${1:-team-payments}"

echo "== ResourceQuotas in ${NS} =="
kubectl get resourcequota -n "${NS}" -o wide

echo
echo "== Used vs hard =="
kubectl describe resourcequota -n "${NS}"

echo
echo "== LimitRanges =="
kubectl get limitrange -n "${NS}"

echo
echo "== Top pods by CPU (requires metrics-server) =="
kubectl top pods -n "${NS}" --sort-by=cpu || echo "metrics-server not available"
