#!/bin/bash
# canary-rollout.sh — progressive traffic shift v1 -> v2 via Istio VirtualService weights
set -e

function set_weight() {
  local v1_weight=$1
  local v2_weight=$((100 - v1_weight))

  cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api
spec:
  hosts:
  - api
  http:
  - route:
    - destination:
        host: api
        subset: v1
      weight: ${v1_weight}
    - destination:
        host: api
        subset: v2
      weight: ${v2_weight}
EOF
}

# Phase 1: 10% traffic to v2
set_weight 90
echo "Deployed v2 at 10%. Monitoring for 5 minutes..."
sleep 300

# Phase 2: 50% traffic to v2
set_weight 50
echo "Deployed v2 at 50%. Monitoring for 5 minutes..."
sleep 300

# Phase 3: 100% traffic to v2
set_weight 0
echo "Deployed v2 at 100%. Canary complete."
