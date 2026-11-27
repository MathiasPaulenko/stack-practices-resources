#!/bin/bash
set -euo pipefail

DAYS_THRESHOLD=30

echo "Checking TLS certificates across all namespaces..."

kubectl get secrets --all-namespaces -o json | \
  jq -r '.items[] | select(.type=="kubernetes.io/tls") | "\(.metadata.namespace) \(.metadata.name) \(.data."tls.crt")"' | \
  while read -r namespace secret_name cert_b64; do
    cert_pem=$(echo "$cert_b64" | base64 -d)
    expiry_date=$(echo "$cert_pem" | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
    if [ -z "$expiry_date" ]; then
      continue
    fi

    expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null || date -j -f "%b %d %H:%M:%S %Y %Z" "$expiry_date" +%s 2>/dev/null)
    now_epoch=$(date +%s)
    days_left=$(( (expiry_epoch - now_epoch) / 86400 ))

    if [ "$days_left" -lt "$DAYS_THRESHOLD" ]; then
      echo "WARNING: $namespace/$secret_name expires in $days_left days ($expiry_date)"
    fi
  done
