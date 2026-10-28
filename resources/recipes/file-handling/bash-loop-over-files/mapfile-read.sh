#!/bin/bash
# Read a large file list into an array, then iterate.
set -euo pipefail

mapfile -d '' -t pyfiles < <(find src/ -type f -name '*.py' -print0 2>/dev/null || true)

echo "Found ${#pyfiles[@]} Python files"
for file in "${pyfiles[@]}"; do
    echo "  $file"
done
