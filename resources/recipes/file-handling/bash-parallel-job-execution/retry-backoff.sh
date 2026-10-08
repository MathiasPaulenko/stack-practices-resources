#!/usr/bin/env bash
# Retries with exponential backoff, fanned out by GNU parallel.
# Usage: ./retry-backoff.sh [max_jobs] [max_retries] [timeout] [input_file]
set -euo pipefail

MAX_JOBS="${1:-4}"
MAX_RETRIES="${2:-3}"
TIMEOUT="${3:-60}"
INPUT_FILE="${4:-jobs.txt}"

process_task() {
    local task="$1"
    # Replace with real work; must succeed on retry
    sleep "$((RANDOM % 3 + 1))"
    (( RANDOM % 3 != 0 ))  # fails ~1 in 3 for demo purposes
}
export -f process_task

run_with_retry() {
    local task="$1"
    local attempt=1

    while (( attempt <= MAX_RETRIES )); do
        if timeout "$TIMEOUT" bash -c 'process_task "$1"' _ "$task"; then
            echo "SUCCESS: $task (attempt $attempt)"
            return 0
        fi
        echo "RETRY: $task (attempt $attempt failed)" >&2
        ((attempt++))
        sleep "$((2 ** (attempt - 1)))"  # 2s, 4s, 8s...
    done

    echo "FAILED: $task after $MAX_RETRIES attempts"
    return 1
}
export -f run_with_retry
export MAX_RETRIES TIMEOUT

parallel --jobs "$MAX_JOBS" run_with_retry {} < "$INPUT_FILE"
