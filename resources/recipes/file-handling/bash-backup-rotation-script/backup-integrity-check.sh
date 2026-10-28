#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${1:-/var/backups/app}"

echo "[$(date -Iseconds)] Starting backup verification..."

FAILURES=0
for archive in "$BACKUP_DIR"/daily/*.tar.gz; do
    [[ -f "$archive" ]] || continue
    filename=$(basename "$archive")

    # Listing reads the compressed stream and tar headers; it isn't a restore test.
    if ! tar -tzf "$archive" > /dev/null 2>&1; then
        echo "FAIL: $filename — tar archive is corrupt"
        FAILURES=$((FAILURES + 1))
        continue
    fi

    # Check file count in archive
    FILE_COUNT=$(tar -tzf "$archive" | wc -l)
    ARCHIVE_SIZE=$(du -h "$archive" | cut -f1)
    echo "OK: $filename — $FILE_COUNT files, $ARCHIVE_SIZE"
done

if (( FAILURES > 0 )); then
    echo "[$(date -Iseconds)] Verification FAILED: $FAILURES corrupt archives"
    exit 1
fi
echo "[$(date -Iseconds)] All archive streams passed the listing check"
