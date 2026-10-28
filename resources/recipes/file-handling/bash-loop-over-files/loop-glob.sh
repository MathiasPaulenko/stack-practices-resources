#!/bin/bash
# Basic safe loop over *.txt files with glob + no-match handling.
set -euo pipefail

txt_count=0
for file in *.txt; do
    # Handle the no-match case (glob leaves literal '*.txt')
    [ -e "$file" ] || continue
    echo "Processing: $file"
    ((txt_count++))
done
echo "Total .txt files: $txt_count"
