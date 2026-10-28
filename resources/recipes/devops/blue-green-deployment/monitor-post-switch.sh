#!/bin/bash
# monitor-post-switch.sh — watch health and error rate for 5 minutes after a switch.

DURATION=300
INTERVAL=10
END=$((SECONDS + DURATION))

while [ $SECONDS -lt $END ]; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
  LATENCY=$(curl -s -o /dev/null -w "%{time_total}" https://api.example.com/health)
  ERROR_RATE=$(curl -s https://api.example.com/metrics | grep error_rate | awk '{print $2}')

  echo "$(date -Iseconds) status=$STATUS latency=${LATENCY}s error_rate=$ERROR_RATE"

  if [ "$STATUS" != "200" ] || (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
    echo "ALERT: Rolling back"
    kubectl patch svc app-active -p '{"spec":{"selector":{"version":"blue"}}}'
    exit 1
  fi

  sleep $INTERVAL
done

echo "Monitoring complete. Green is stable."
