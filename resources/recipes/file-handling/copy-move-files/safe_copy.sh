#!/usr/bin/env bash
set -euo pipefail

safe_copy() {
    local src="$1"
    local dest="$2"
    local overwrite="${3:-false}"

    [[ -f "$src" ]] || { echo "ERROR: Source not found: $src"; return 1; }

    if [[ -f "$dest" && "$overwrite" != "true" ]]; then
        echo "ERROR: Destination exists: $dest"
        return 1
    fi

    mkdir -p "$(dirname "$dest")"
    cp -p "$src" "$dest"

    local src_sum dest_sum
    src_sum=$(sha256sum "$src" | cut -d' ' -f1)
    dest_sum=$(sha256sum "$dest" | cut -d' ' -f1)

    if [[ "$src_sum" != "$dest_sum" ]]; then
        rm -f "$dest"
        echo "ERROR: Checksum mismatch after copy"
        return 1
    fi

    echo "OK: $src -> $dest (verified)"
}

batch_copy() {
    local src_dir="$1"
    local dest_dir="$2"
    local pattern="${3:-*}"

    mkdir -p "$dest_dir"
    local count=0
    for file in "$src_dir"/$pattern; do
        [[ -f "$file" ]] || continue
        safe_copy "$file" "$dest_dir/$(basename "$file")" true && count=$((count + 1))
    done
    echo "Copied $count files"
}
