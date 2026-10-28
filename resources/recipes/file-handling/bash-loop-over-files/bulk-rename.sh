#!/bin/bash
# Bulk rename .jpeg -> .jpg in the current directory.
set -euo pipefail
shopt -s nullglob

for file in *.jpeg; do
    # -- prevents filenames starting with '-' from being parsed as options
    mv -- "$file" "${file%.jpeg}.jpg"
    echo "Renamed: $file -> ${file%.jpeg}.jpg"
done
