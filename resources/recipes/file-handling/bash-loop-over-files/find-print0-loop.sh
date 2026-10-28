#!/bin/bash
# Recursive iteration that survives spaces, newlines, and glob chars.
set -euo pipefail

srcdir="${1:-src/}"

while IFS= read -r -d '' file; do
    echo "Found: $file"
done < <(find "$srcdir" -type f -print0)

# One-liner equivalent when a loop isn't needed:
# find "$srcdir" -type f -name '*.py' -print0 | xargs -0 pylint
