#!/usr/bin/env bash
# validate-migration.sh — compare row counts between source and target databases.
# Companion to https://stackpractices.com/docs/data-migration-runbook-template/
#
# Usage:
#   ./validate-migration.sh --source source.db.internal --target target.db.internal
#
# Environment variables:
#   DB_NAME   Database name on both hosts        (default: mydb)
#   DB_USER   Read-only user for both hosts      (default: readonly)
#   TABLES    Space-separated tables to compare  (default: orders users payments)
#
# Requires: psql on PATH. Source/target credentials via PGPASSWORD or .pgpass.

set -euo pipefail

DB_NAME="${DB_NAME:-mydb}"
DB_USER="${DB_USER:-readonly}"
TABLES="${TABLES:-orders users payments}"
SOURCE=""
TARGET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) SOURCE="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$SOURCE" || -z "$TARGET" ]]; then
  echo "Usage: $0 --source <host> --target <host>" >&2
  exit 2
fi

count_rows() {
  local host="$1" table="$2"
  psql -h "$host" -U "$DB_USER" -d "$DB_NAME" -tA \
    -c "SELECT COUNT(*) FROM ${table};"
}

failures=0
printf '%-20s %15s %15s %s\n' "table" "source" "target" "match"
printf '%-20s %15s %15s %s\n' "----" "------" "------" "-----"

for table in $TABLES; do
  src_count="$(count_rows "$SOURCE" "$table")"
  tgt_count="$(count_rows "$TARGET" "$table")"

  if [[ "$src_count" == "$tgt_count" ]]; then
    match="yes"
  else
    match="NO"
    failures=$((failures + 1))
  fi

  printf '%-20s %15s %15s %s\n' "$table" "$src_count" "$tgt_count" "$match"
done

if [[ "$failures" -gt 0 ]]; then
  echo "VALIDATION FAILED: $failures table(s) mismatched" >&2
  exit 1
fi

echo "VALIDATION PASSED: all row counts match"
