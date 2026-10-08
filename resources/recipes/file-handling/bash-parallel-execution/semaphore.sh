#!/usr/bin/env bash
# Rate-limited fan-out with GNU parallel's `sem` counting semaphore.
# Caps concurrent calls at API_LIMIT. Requires GNU parallel installed.
# Usage: ./semaphore.sh [ids_file]
set -euo pipefail

IDS_FILE="${1:-ids.txt}"
API_LIMIT=3
mkdir -p results

if ! command -v sem >/dev/null; then
    echo "error: 'sem' not found — install GNU parallel" >&2
    exit 1
fi

while read -r id; do
    sem --id api_calls -j "$API_LIMIT" \
        sh -c 'sleep 1; echo "item $1" > "results/$1.txt"' _ "$id" &
done < "$IDS_FILE"

wait
sem --id api_calls --wait
echo "done: $(ls results | wc -l) results, max $API_LIMIT concurrent"
