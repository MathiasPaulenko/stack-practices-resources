#!/usr/bin/env bash
# Safe file read/write utilities for Bash.
# Run: bash safe-file-ops.sh
set -euo pipefail

# Safe write: write to temp file, then atomically rename
safe_write() {
    local file="$1"
    local content="$2"
    local tmp="${file}.tmp.$$"
    local dir
    dir="$(dirname "$file")"
    mkdir -p "$dir"
    printf '%s' "$content" > "$tmp"
    mv "$tmp" "$file"
}

# Safe read: check existence first, provide default
safe_read() {
    local file="$1"
    local default="${2:-}"
    if [[ -f "$file" && -r "$file" ]]; then
        cat "$file"
    else
        printf '%s' "$default"
    fi
}

# Append with timestamp (for logging)
log_append() {
    local file="$1"
    local message="$2"
    local timestamp
    timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf '[%s] %s\n' "$timestamp" "$message" >> "$file"
}

# Read file line by line with error handling
read_lines() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "Error: $file not found" >&2
        return 1
    fi
    while IFS= read -r line || [[ -n "$line" ]]; do
        echo "$line"
    done < "$file"
}

# Create file with restrictive permissions (for secrets)
create_secret_file() {
    local file="$1"
    local content="$2"
    # Create with 600 permissions directly
    (umask 077; printf '%s' "$content" > "$file")
    echo "Created $file with 600 permissions"
}

# Demo
safe_write demo-config.txt "key=value"
content=$(safe_read demo-config.txt "key=default")
printf 'read: %s\n' "$content"
log_append demo-app.log "Application started"
read_lines demo-config.txt
