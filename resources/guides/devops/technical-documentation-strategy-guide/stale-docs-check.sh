#!/usr/bin/env bash
# stale-docs-check.sh — list Markdown docs not modified in the last N days.
# Usage: ./stale-docs-check.sh [days] [path]
# Example: ./stale-docs-check.sh 365 ./services
set -euo pipefail

DAYS="${1:-365}"
ROOT="${2:-.}"

echo "Markdown files not modified in the last ${DAYS} days under ${ROOT}:"
echo

find "${ROOT}" -type f -name "*.md" -mtime "+${DAYS}" -printf '%T+ %p\n' \
  | sort \
  | while read -r date file; do
      printf '%s  %s\n' "${date%%T*}" "${file}"
    done
