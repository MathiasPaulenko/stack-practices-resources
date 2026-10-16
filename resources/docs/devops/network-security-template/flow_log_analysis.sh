#!/bin/bash
# Analyze VPC flow logs for rejected traffic and scanning attempts.
# Source article: https://stackpractices.com/docs/network-security-template/
# Requires: aws CLI + CloudWatch Logs access to the flow log group.
set -euo pipefail

LOG_GROUP="${1:-/aws/vpc/flow-logs}"
START_TIME=$(date -d '24 hours ago' +%s)000
END_TIME=$(date +%s)000

echo "Querying $LOG_GROUP for REJECT events in the last 24h..."

aws logs filter-log-events \
  --log-group-name "$LOG_GROUP" \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --filter-pattern "REJECT" \
  --query 'events[*].message' \
  --output text | while read -r line; do
    # Flow log fields (space separated):
    # version account-id srcaddr dstaddr srcport dstport
    # protocol packets bytes start end action log-status
    SRC=$(echo "$line" | awk '{print $4}')
    DST=$(echo "$line" | awk '{print $5}')
    DSTPORT=$(echo "$line" | awk '{print $7}')
    ACTION=$(echo "$line" | awk '{print $13}')

    echo "REJECTED: $SRC -> $DST:$DSTPORT ($ACTION)"
  done

echo ""
echo "=== Top Source IPs by Rejected Connections ==="
aws logs filter-log-events \
  --log-group-name "$LOG_GROUP" \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --filter-pattern "REJECT" \
  --query 'events[*].message' \
  --output text | \
  awk '{print $4}' | \
  sort | uniq -c | sort -rn | head -20
