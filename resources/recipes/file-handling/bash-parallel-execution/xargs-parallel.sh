#!/usr/bin/env bash
# Fan-out with xargs -P: N concurrent workers over an input list.
# Usage: ./xargs-parallel.sh [input_dir]
set -euo pipefail

INPUT_DIR="${1:-./input}"
OUT_DIR="./output"
mkdir -p "$OUT_DIR" logs

# One command per file, 4 at a time. Each worker writes its own log so
# failures don't get interleaved. xargs exits 123 if any child fails.
find "$INPUT_DIR" -type f -print0 | \
    xargs -0 -P 4 -I {} sh -c '
        f="$1"
        name=$(basename "$f")
        cp "$f" "./output/${name}.done" \
            && echo "OK  $name" > "logs/${name}.log" \
            || echo "FAIL $name" > "logs/${name}.log"
    ' _ {}

status=$?
echo "xargs exit: $status (123 means at least one child failed)"
grep -l FAIL logs/*.log 2>/dev/null || echo "all jobs OK"
exit "$status"
