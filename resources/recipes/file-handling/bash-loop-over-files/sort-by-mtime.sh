#!/bin/bash
# Iterate files newest-first using find -printf + sort -z.
set -euo pipefail

mapfile -d '' -t files < <(find . -type f -name '*.log' -printf '%T@ %p\0' | sort -rz -n | cut -z -d' ' -f2-)

for file in "${files[@]}"; do
    echo "$(date -r "$file" '+%Y-%m-%d %H:%M') $file"
done
