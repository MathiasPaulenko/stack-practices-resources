#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-/var/app/data}"
BACKUP_DIR="${2:-/var/backups/rsync}"
SNAPSHOT_COUNT=7

mkdir -p "$BACKUP_DIR"

TODAY=$(date +%Y-%m-%d)
CURRENT_SNAPSHOT="$BACKUP_DIR/snapshot-$TODAY"

# Snapshot names use ISO dates, so lexical order is chronological. The first
# run has no --link-dest; each destination is a dedicated snapshot directory.
LAST_SNAPSHOT=""
for snapshot in "$BACKUP_DIR"/snapshot-*/; do
    [[ -d "$snapshot" ]] || continue
    snapshot="${snapshot%/}"
    if [[ "$snapshot" != "$CURRENT_SNAPSHOT" ]]; then
        if [[ -z "$LAST_SNAPSHOT" || "$snapshot" > "$LAST_SNAPSHOT" ]]; then
            LAST_SNAPSHOT="$snapshot"
        fi
    fi
done

RSYNC_ARGS=(-a --delete)
if [[ -n "$LAST_SNAPSHOT" ]]; then
    RSYNC_ARGS+=(--link-dest="$LAST_SNAPSHOT")
fi
rsync "${RSYNC_ARGS[@]}" "$SOURCE_DIR/" "$CURRENT_SNAPSHOT/"

# Verify snapshot integrity
SNAPSHOT_SIZE=$(du -sh "$CURRENT_SNAPSHOT" | cut -f1)
FILE_COUNT=$(find "$CURRENT_SNAPSHOT" -type f | wc -l)
echo "[$(date -Iseconds)] Snapshot created: $CURRENT_SNAPSHOT ($FILE_COUNT files, $SNAPSHOT_SIZE)"

# Rotate old dated snapshots without word-splitting paths that contain spaces.
snapshots=()
snapshot_count=0
for snapshot in "$BACKUP_DIR"/snapshot-*/; do
    [[ -d "$snapshot" ]] || continue
    snapshots[snapshot_count]="${snapshot%/}"
    snapshot_count=$((snapshot_count + 1))
done

if (( snapshot_count > SNAPSHOT_COUNT )); then
    remove_count=$((snapshot_count - SNAPSHOT_COUNT))
    for ((i = 0; i < remove_count; i++)); do
        snapshot="${snapshots[i]}"
        rm -r -- "$snapshot"
        echo "[$(date -Iseconds)] Removed old snapshot: $snapshot"
    done
fi

# Disk usage report
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "[$(date -Iseconds)] Total backup size: $TOTAL_SIZE"
