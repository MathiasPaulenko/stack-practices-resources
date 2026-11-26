#!/usr/bin/env bash
# Cold start rate over the last hour for a given log group.
# Usage: ./cold-start-rate.sh /aws/lambda/my-function
set -euo pipefail
LOG_GROUP="${1:?usage: $0 <log-group-name>}"
START=$(($(date -d '1 hour ago' +%s)000))
END=$(($(date +%s)000))

total=$(aws logs filter-log-events \
  --log-group-name "$LOG_GROUP" \
  --filter-pattern '"INVOCATION"' \
  --start-time "$START" --end-time "$END" \
  --limit 10000 | jq '.events | length')

cold=$(aws logs filter-log-events \
  --log-group-name "$LOG_GROUP" \
  --filter-pattern '"COLD_START"' \
  --start-time "$START" --end-time "$END" \
  --limit 10000 | jq '.events | length')

echo "Cold start rate: $(echo "scale=2; $cold * 100 / $total" | bc)%"
