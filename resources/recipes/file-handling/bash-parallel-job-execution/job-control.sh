#!/usr/bin/env bash
# Complete job-control wrapper: GNU parallel + joblog + summary report.
# Usage: ./job-control.sh [max_jobs] [input_file] [log_dir]
set -euo pipefail

MAX_JOBS="${1:-4}"
INPUT_FILE="${2:-jobs.txt}"
LOG_DIR="${3:-./parallel-logs}"

mkdir -p "$LOG_DIR"

process_task() {
    local task="$1"
    echo "Processing $task"
    sleep "$((RANDOM % 3 + 1))"
    echo "Done $task"
}
export -f process_task

# Run with a joblog: every job's exit code, duration, and command is recorded
parallel --jobs "$MAX_JOBS" \
    --joblog "$LOG_DIR/joblog.txt" \
    --timeout 300 \
    --halt soon,fail=20% \
    process_task {} \
    < "$INPUT_FILE"

# Summarize: joblog columns are Seq Host Starttime Runtime Send Receive Exitval Signal Command
awk 'NR>1 {codes[$7]++} END {for (c in codes) printf "Exit %s: %d jobs\n", c, codes[c]}' \
    "$LOG_DIR/joblog.txt"

# List what failed so you can rerun just those
awk 'NR>1 && $7!=0 {print $NF}' "$LOG_DIR/joblog.txt" > "$LOG_DIR/failed.txt" || true
if [[ -s "$LOG_DIR/failed.txt" ]]; then
    echo "Failed jobs written to $LOG_DIR/failed.txt"
fi
