#!/usr/bin/env bash
# Watch a directory with inotifywait (Linux only).
# Requires: apt install inotify-tools
# Usage:    ./watch.sh [directory]
#
# Note: the debounce below is a simplified single-machine approach
# using a shared cache file. For concurrent workloads use a proper
# watcher (watchdog, chokidar) or real file locking.
set -euo pipefail

WATCH_DIR="${1:-./watched}"
DEBOUNCE_SECONDS=0.3

echo "Watching: $WATCH_DIR"

inotifywait -m -r --format '%w%f|%e' \
    -e create,modify,delete,move \
    --exclude '\.(swp|tmp|log)' \
    "$WATCH_DIR" | while IFS='|' read -r file event; do
        # Debounce: skip if same file+event seen recently
        CACHE_KEY="${event}:${file}"
        if [[ -f /tmp/.watch_cache ]] && grep -q "^${CACHE_KEY}$" /tmp/.watch_cache 2>/dev/null; then
            continue
        fi
        echo "${CACHE_KEY}" >> /tmp/.watch_cache
        sleep "$DEBOUNCE_SECONDS"
        sed -i "/^${CACHE_KEY//\//\\/}$/d" /tmp/.watch_cache 2>/dev/null || true

        echo "[$(date +%H:%M:%S)] $event: $file"

        # Trigger action based on extension
        case "$file" in
            *.py) echo "  -> Python file changed, running lint..." ;;
            *.js) echo "  -> JS file changed, rebuilding bundle..." ;;
            *.csv) echo "  -> CSV file added, processing..." ;;
        esac
    done
