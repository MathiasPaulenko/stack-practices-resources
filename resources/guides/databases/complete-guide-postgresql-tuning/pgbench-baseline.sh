#!/usr/bin/env bash
# Capture a pgbench baseline before and after tuning changes.
# Usage: ./pgbench-baseline.sh mydb [label]
set -euo pipefail
DB="${1:?database name}"
LABEL="${2:-baseline}"

pgbench -i -s 50 "$DB"
echo "--- pgbench run ($LABEL) ---"
pgbench -c 20 -j 4 -T 60 "$DB"
