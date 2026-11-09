#!/bin/bash
# game-day.sh - Chaos engineering DR test
# Usage: ./game-day.sh --scenario <network|disk|cpu|full>

set -euo pipefail

SCENARIO="${1:---scenario}"
shift || true

case "$SCENARIO" in
  --scenario) SCENARIO="$1" ;;
esac

NAMESPACE="production"
SERVICE="api"
LOG_FILE="/tmp/game-day-$(date +%s).log"

log() { echo "[$(date -u +%H:%M:%S)] $1" | tee -a "$LOG_FILE"; }

case "$SCENARIO" in
  network)
    log "Injecting network latency to ${SERVICE} pods..."
    kubectl exec -n "$NAMESPACE" deployment/"$SERVICE" -- \
      tc qdisc add dev eth0 root netem delay 500ms 2>/dev/null || true
    log "Monitoring for 5 minutes..."
    sleep 300
    kubectl exec -n "$NAMESPACE" deployment/"$SERVICE" -- \
      tc qdisc del dev eth0 root 2>/dev/null || true
    log "Network latency removed."
    ;;

  disk)
    log "Filling disk on ${SERVICE} pods to 90%..."
    kubectl exec -n "$NAMESPACE" deployment/"$SERVICE" -- \
      fallocate -l $(df --output=avail -BG / | tail -1 | tr -d 'G ')M /tmp/fill 2>/dev/null || true
    sleep 120
    kubectl exec -n "$NAMESPACE" deployment/"$SERVICE" -- rm -f /tmp/fill 2>/dev/null || true
    log "Disk space restored."
    ;;

  cpu)
    log "Spiking CPU on ${SERVICE} pods..."
    kubectl exec -n "$NAMESPACE" deployment/"$SERVICE" -- \
      sh -c 'yes > /dev/null & yes > /dev/null & yes > /dev/null &' 2>/dev/null || true
    sleep 120
    kubectl delete pod -n "$NAMESPACE" -l app="$SERVICE" --grace-period=0 --force 2>/dev/null || true
    log "CPU spike ended (pods restarted)."
    ;;

  full)
    log "Starting full region failure simulation..."
    log "1. Cordoning all nodes in primary region..."
    kubectl cordon --selector=topology.kubernetes.io/region=us-east-1
    log "2. Draining workloads..."
    kubectl drain --selector=topology.kubernetes.io/region=us-east-1 \
      --ignore-daemonsets --delete-emptydir-data --timeout=300s || true
    log "3. Waiting 5 minutes for failover..."
    sleep 300
    log "4. Checking DR region health..."
    kubectl get pods -n production --context=dr-cluster
    log "5. Uncordoning primary region..."
    kubectl uncordon --selector=topology.kubernetes.io/region=us-east-1
    log "Full region simulation complete."
    ;;

  *)
    echo "Usage: $0 --scenario <network|disk|cpu|full>"
    exit 1
    ;;
esac

log "Game day results saved to $LOG_FILE"
