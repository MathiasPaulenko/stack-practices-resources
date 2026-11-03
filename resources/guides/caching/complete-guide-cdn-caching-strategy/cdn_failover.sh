#!/usr/bin/env bash
# Multi-CDN DNS failover via Route53 health check.
# Source: https://stackpractices.com/guides/complete-guide-cdn-caching-strategy/
set -euo pipefail

if ! curl -s --max-time 5 https://cdn-a.example.com/health; then
  aws route53 change-resource-record-sets \
    --hosted-zone-id Z123 \
    --change-batch '{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"cdn.example.com","Type":"CNAME","TTL":60,"ResourceRecords":[{"Value":"cdn-b.example.com"}]}}]}'
  echo "Failover: routed traffic to cdn-b"
else
  echo "cdn-a healthy, no failover"
fi
