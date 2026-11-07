#!/usr/bin/env bash
# Pre-compress static assets with Gzip and Brotli for Nginx static serving.
# Usage: ./precompress.sh /path/to/static
set -euo pipefail

dir="${1:?usage: precompress.sh <dir>}"
count=0

for file in "$dir"/*.{js,css,html,json,svg,xml,txt}; do
  [[ -f "$file" ]] || continue
  [[ "$file" == *.gz || "$file" == *.br ]] && continue

  if [[ ! -f "${file}.gz" || "$file" -nt "${file}.gz" ]]; then
    gzip -9 -k -f "$file"
    ((count++))
  fi

  if command -v brotli &>/dev/null; then
    if [[ ! -f "${file}.br" || "$file" -nt "${file}.br" ]]; then
      brotli -q 11 -k -f "$file"
      ((count++))
    fi
  fi
done

echo "Pre-compressed $count files in $dir"
