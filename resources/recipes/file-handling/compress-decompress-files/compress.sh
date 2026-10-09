#!/usr/bin/env bash
set -euo pipefail

# Archive utilities for Bash: tar/gzip with safety checks and pigz.

compress_tarball() {
    local src="$1"
    local dest="$2"
    local level="${3:-6}"
    tar -c -C "$(dirname "$src")" "$(basename "$src")" \
        | gzip -"$level" -c > "$dest"
    echo "Created $dest ($(du -h "$dest" | cut -f1))"
}

extract_tarball_safe() {
    local archive="$1"
    local dest="$2"
    mkdir -p "$dest"
    if tar -tf "$archive" | grep -E '^/|\.\.'; then
        echo "Error: unsafe paths detected in $archive" >&2
        return 1
    fi
    tar -xzf "$archive" -C "$dest"
    echo "Extracted to $dest"
}

compress_parallel() {
    local src="$1"
    local dest="$2"
    if command -v pigz &>/dev/null; then
        tar -c -C "$(dirname "$src")" "$(basename "$src")" | pigz -p 4 > "$dest"
    else
        tar -czf "$dest" -C "$(dirname "$src")" "$(basename "$src")"
    fi
    echo "Created $dest"
}

batch_gzip() {
    local dir="$1"
    local count=0
    for file in "$dir"/*; do
        [[ -f "$file" ]] || continue
        gzip -c "$file" > "${file}.gz"
        ((count++))
    done
    echo "Compressed $count files in $dir"
}
