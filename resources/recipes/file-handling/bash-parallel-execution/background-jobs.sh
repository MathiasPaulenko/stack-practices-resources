#!/usr/bin/env bash
# Background-job pool with correct per-PID exit-code collection.
# Key points: save $! at launch, wait -n for slot management,
# wait "$pid" per job — a bare `wait` first would reap everything
# and leave jobs -p empty.
# Usage: ./background-jobs.sh [num_jobs]
set -uo pipefail   # no -e: it can't catch background failures anyway

NUM_JOBS="${1:-6}"
MAX_JOBS=3
pids=()

worker() {
    local id="$1"
    sleep $((RANDOM % 3 + 1))
    # job 3 fails on purpose so you can see the exit-code path
    [ "$id" -eq 3 ] && return 1
    echo "job $id done" > "logs/job-$id.log"
    return 0
}

mkdir -p logs

for ((i = 1; i <= NUM_JOBS; i++)); do
    while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do
        wait -n 2>/dev/null || sleep 0.1
    done
    worker "$i" &
    pids+=($!)
done

failed=0
for pid in "${pids[@]}"; do
    if ! wait "$pid"; then
        echo "job (pid $pid) failed" >&2
        ((failed++))
    fi
done

echo "done: $((NUM_JOBS - failed))/$NUM_JOBS succeeded"
[ "$failed" -eq 0 ] || exit 1
