#!/usr/bin/env bash
# Per-job result files with xargs when GNU parallel isn't available.
# Usage: ./xargs-exit-codes.sh [max_jobs] [input_file]
set -euo pipefail

MAX_JOBS="${1:-4}"
INPUT_FILE="${2:-jobs.txt}"
RESULTS_DIR=$(mktemp -d)
trap 'rm -rf "$RESULTS_DIR"' EXIT

process_with_exit() {
    local task="$1"
    local result_file="$2"
    sleep "$((RANDOM % 3 + 1))"
    if (( RANDOM % 10 == 0 )); then
        echo "FAIL" > "$result_file"
        return 1
    fi
    echo "OK" > "$result_file"
    return 0
}
export -f process_with_exit
export RESULTS_DIR

# basename replaces GNU parallel's {//} — xargs -I {} doesn't support it
xargs -P "$MAX_JOBS" -I {} bash -c '
    task="{}"
    process_with_exit "$task" "$RESULTS_DIR/$(basename "$task")_result" || true
' < "$INPUT_FILE"

TOTAL=$(wc -l < "$INPUT_FILE")
SUCCESS=$(grep -l "OK" "$RESULTS_DIR"/*_result 2>/dev/null | wc -l)
echo "Total: $TOTAL, Success: $SUCCESS, Failed: $((TOTAL - SUCCESS))"
