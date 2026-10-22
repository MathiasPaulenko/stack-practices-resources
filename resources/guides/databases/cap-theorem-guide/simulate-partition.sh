#!/usr/bin/env bash
# Simulates a network partition on the 3-node etcd lab.
#
#   ./simulate-partition.sh cut etcd3   # isolate etcd3 -> minority side
#   ./simulate-partition.sh heal etcd3  # reconnect it
#   ./simulate-partition.sh status      # cluster members + leader
#
# Watching `endpoint status` before and after `cut` shows CP behavior in
# action: the majority side (2 nodes) keeps quorum and serves linearizable
# reads/writes; the isolated node answers serializable reads but rejects
# anything that needs consensus.
set -euo pipefail

ACTION="${1:-status}"
NODE="${2:-etcd3}"
NETWORK="cap-theorem-lab_etcdnet"

etcdctl() {
  docker exec etcd1 etcdctl --endpoints=http://etcd1:2379,http://etcd2:2379,http://etcd3:2379 "$@"
}

case "$ACTION" in
  cut)
    echo "[*] Cutting $NODE from $NETWORK (partition)"
    docker network disconnect "$NETWORK" "$NODE"
    echo "[*] $NODE is now partitioned. Majority side keeps quorum."
    echo "    Try: ./simulate-partition.sh status"
    ;;
  heal)
    echo "[*] Reconnecting $NODE to $NETWORK (heal)"
    docker network connect "$NETWORK" "$NODE"
    echo "[*] $NODE rejoined. Raft catches it up automatically."
    ;;
  status)
    etcdctl endpoint status --write-out=table || true
    echo
    etcdctl endpoint health || true
    ;;
  write)
    # Writes go through consensus: succeeds on the majority side.
    etcdctl put cap-test "$(date +%s)"
    etcdctl get cap-test
    ;;
  *)
    echo "usage: $0 {cut|heal|status|write} [node]" >&2
    exit 1
    ;;
esac
