#!/usr/bin/env bash
# Usage: ./game-day.sh --scenario <network|disk|cpu|full> [--execute]
# Required: KUBE_CONTEXT. For full: PRIMARY_REGION. Optional: NAMESPACE, SERVICE.
set -euo pipefail

NAMESPACE="${NAMESPACE:-dr-test}"
SERVICE="${SERVICE:-api}"
KUBE_CONTEXT="${KUBE_CONTEXT:-}"
PRIMARY_REGION="${PRIMARY_REGION:-}"
OBSERVATION_SECONDS="${OBSERVATION_SECONDS:-300}"
FILL_SIZE="${FILL_SIZE:-}"
EXECUTE=false
FULL_DRAIN_STARTED=false
NETWORK_INJECTED=false
DISK_FILE_CREATED=false
CPU_INJECTED=false

if [[ "${1:-}" == "--scenario" ]]; then
  SCENARIO="${2:-}"
  if (( $# >= 2 )); then shift 2; else shift || true; fi
else
  SCENARIO="${1:-}"
  shift || true
fi
if [[ "${1:-}" == "--execute" ]]; then
  EXECUTE=true
  shift
fi

usage() {
  echo "Usage: KUBE_CONTEXT=<test-context> [PRIMARY_REGION=<region>] ./game-day.sh --scenario <network|disk|cpu|full> [--execute]"
  exit 2
}

[[ -n "$SCENARIO" && $# -eq 0 ]] || usage
[[ -n "$KUBE_CONTEXT" ]] || { echo "Set KUBE_CONTEXT to the dedicated test cluster." >&2; exit 2; }
if [[ "$SCENARIO" == "full" && -z "$PRIMARY_REGION" ]]; then
  echo "Set PRIMARY_REGION for the full scenario." >&2
  exit 2
fi
if [[ "$EXECUTE" == "true" && "$SCENARIO" == "disk" && -z "$FILL_SIZE" ]]; then
  echo "Set FILL_SIZE after checking the test filesystem capacity." >&2
  exit 2
fi

LOG_FILE="/tmp/game-day-$(date +%s).log"
log() { echo "[$(date -u +%H:%M:%S)] $1" | tee -a "$LOG_FILE"; }
kubectl() { command kubectl --context "$KUBE_CONTEXT" "$@"; }

cleanup() {
  trap - EXIT INT TERM
  if [[ "$NETWORK_INJECTED" == "true" ]]; then
    kubectl exec -n "$NAMESPACE" "deployment/${SERVICE}" -- tc qdisc del dev eth0 root || true
  fi
  if [[ "$DISK_FILE_CREATED" == "true" ]]; then
    kubectl exec -n "$NAMESPACE" "deployment/${SERVICE}" -- rm -f /tmp/fill || true
  fi
  if [[ "$CPU_INJECTED" == "true" ]]; then
    kubectl delete pod -n "$NAMESPACE" -l "app=${SERVICE}" --grace-period=0 --force || true
  fi
  if [[ "$FULL_DRAIN_STARTED" == "true" ]]; then
    log "Restoring schedulability for nodes in ${PRIMARY_REGION}..."
    kubectl uncordon --selector="topology.kubernetes.io/region=${PRIMARY_REGION}" || true
  fi
  return 0
}
trap cleanup EXIT
trap 'exit 130' INT TERM

if [[ "$EXECUTE" != "true" ]]; then
  log "DRY RUN: scenario=${SCENARIO}, context=${KUBE_CONTEXT}, namespace=${NAMESPACE}. No cluster changes were made."
  exit 0
fi

case "$SCENARIO" in
  network|disk|cpu|full) ;;
  *) usage ;;
esac

if [[ "$SCENARIO" == "full" ]]; then
  confirmation="${KUBE_CONTEXT}/${PRIMARY_REGION}"
  read -r -p "Type ${confirmation} to confirm the full node disruption: " answer
  [[ "$answer" == "$confirmation" ]] || { echo "Confirmation did not match; stopping." >&2; exit 1; }
fi

case "$SCENARIO" in
  network)
    log "Injecting network latency into ${SERVICE} in ${NAMESPACE}..."
    kubectl exec -n "$NAMESPACE" "deployment/${SERVICE}" -- \
      tc qdisc add dev eth0 root netem delay 500ms
    NETWORK_INJECTED=true
    log "Observing for ${OBSERVATION_SECONDS} seconds..."
    sleep "$OBSERVATION_SECONDS"
    kubectl exec -n "$NAMESPACE" "deployment/${SERVICE}" -- \
      tc qdisc del dev eth0 root
    NETWORK_INJECTED=false
    log "Network latency removed."
    ;;

  disk)
    log "Writing ${FILL_SIZE} to the test container filesystem..."
    kubectl exec -n "$NAMESPACE" "deployment/${SERVICE}" -- \
      fallocate -l "$FILL_SIZE" /tmp/fill
    DISK_FILE_CREATED=true
    sleep "$OBSERVATION_SECONDS"
    kubectl exec -n "$NAMESPACE" "deployment/${SERVICE}" -- rm -f /tmp/fill
    DISK_FILE_CREATED=false
    log "Temporary file removed."
    ;;

  cpu)
    log "Starting a CPU load in ${SERVICE} in ${NAMESPACE}..."
    kubectl exec -n "$NAMESPACE" "deployment/${SERVICE}" -- \
      sh -c 'yes > /dev/null & yes > /dev/null & yes > /dev/null &'
    CPU_INJECTED=true
    sleep "$OBSERVATION_SECONDS"
    kubectl delete pod -n "$NAMESPACE" -l "app=${SERVICE}" --grace-period=0 --force
    CPU_INJECTED=false
    log "Test pods restarted after the CPU exercise."
    ;;

  full)
    log "Starting the full node disruption in context ${KUBE_CONTEXT}..."
    FULL_DRAIN_STARTED=true
    kubectl cordon --selector="topology.kubernetes.io/region=${PRIMARY_REGION}"
    kubectl drain --selector="topology.kubernetes.io/region=${PRIMARY_REGION}" \
      --ignore-daemonsets --delete-emptydir-data --timeout=300s
    log "Observing recovery for ${OBSERVATION_SECONDS} seconds..."
    sleep "$OBSERVATION_SECONDS"
    kubectl get pods -n "$NAMESPACE"
    kubectl uncordon --selector="topology.kubernetes.io/region=${PRIMARY_REGION}"
    FULL_DRAIN_STARTED=false
    log "Full scenario complete."
    ;;
esac

log "Game-day results saved to ${LOG_FILE}"
