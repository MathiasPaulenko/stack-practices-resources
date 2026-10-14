#!/usr/bin/env bash
set -euo pipefail

INODE_THRESHOLD="${1:-80}"

df -i | awk 'NR>1 && /^\/dev/{print $1, $5, $6}' | while read -r fs iusage mount; do
    iusage_val="${iusage%\%}"
    if (( iusage_val >= INODE_THRESHOLD )); then
        echo "WARNING: $mount ($fs) inode usage at $iusage"
        # Find directories with the most files
        top_dirs=$(find "$mount" -xdev -type d -exec sh -c 'echo $(find "$0" -maxdepth 1 -type f | wc -l) "$0"' {} \; 2>/dev/null | sort -rn | head -5)
        echo "Top directories by file count:"
        echo "$top_dirs"
    fi
done
