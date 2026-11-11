#!/usr/bin/env bash
# Temporary file and directory patterns from the Generate Temporary Files recipe.
#
# Run: bash temp_files.sh

set -euo pipefail

# Create all temp resources up front, honoring $TMPDIR.
TMPFILE=$(mktemp "${TMPDIR:-/tmp}/demo.XXXXXX.json")
TMPDIR_PATH=$(mktemp -d "${TMPDIR:-/tmp}/myapp.XXXXXX")

# One trap covers everything. EXIT also fires after a fatal SIGINT/SIGTERM,
# and because the handler does not call exit, the script keeps its real
# exit status — a failing script never reports success.
cleanup() {
    rm -f "$TMPFILE" 2>/dev/null || true
    rm -rf "$TMPDIR_PATH" 2>/dev/null || true
}
trap cleanup EXIT

echo '{"status": "ok"}' > "$TMPFILE"
echo "temp file: $TMPFILE"
echo "temp dir:  $TMPDIR_PATH"

for i in $(seq 1 3); do
    echo "processing $i..." > "$TMPDIR_PATH/log.txt"
done
cat "$TMPDIR_PATH/log.txt"

echo "done — cleanup runs on exit"
