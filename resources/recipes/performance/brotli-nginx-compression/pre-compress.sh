#!/usr/bin/env bash
# Pre-compress static assets with Brotli at build time
# Usage: ./pre-compress.sh dist/

set -euo pipefail

DIST_DIR="${1:-dist}"

if [ ! -d "$DIST_DIR" ]; then
  echo "Error: directory '$DIST_DIR' does not exist"
  exit 1
fi

count=0
while IFS= read -r -d '' file; do
  brotli --quality=11 --force --output="${file}.br" "$file"
  count=$((count + 1))
done < <(find "$DIST_DIR" -type f \( -name '*.js' -o -name '*.css' -o -name '*.html' -o -name '*.svg' -o -name '*.json' \) -print0)

echo "Pre-compressed $count files with Brotli level 11"
