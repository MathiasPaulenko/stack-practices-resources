#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-/var/app/data}"
BACKUP_DIR="${2:-/var/backups/app}"
DAILY_RETENTION=7
WEEKLY_RETENTION=4
MONTHLY_RETENTION=3

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "ERROR: Source directory doesn't exist: $SOURCE_DIR" >&2
    exit 1
fi

mkdir -p "$BACKUP_DIR/daily" "$BACKUP_DIR/weekly" "$BACKUP_DIR/monthly"

TODAY=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%u)
DAY_OF_MONTH=$(date +%d)

ARCHIVE="$BACKUP_DIR/daily/app-$TODAY.tar.gz"
TEMP_ARCHIVE=$(mktemp "$BACKUP_DIR/daily/.app-$TODAY.XXXXXX")
trap 'rm -f -- "$TEMP_ARCHIVE"' EXIT

# Build and read-test a temporary archive before replacing today's copy
tar -czf "$TEMP_ARCHIVE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"
tar -tzf "$TEMP_ARCHIVE" > /dev/null
mv -f -- "$TEMP_ARCHIVE" "$ARCHIVE"
trap - EXIT

# Promote to weekly on Sundays
if [[ "$DAY_OF_WEEK" == "7" ]]; then
    cp "$ARCHIVE" "$BACKUP_DIR/weekly/app-week-$TODAY.tar.gz"
fi

# Promote to monthly on the first day of the month
if [[ "$DAY_OF_MONTH" == "01" ]]; then
    cp "$ARCHIVE" "$BACKUP_DIR/monthly/app-month-$TODAY.tar.gz"
fi

# Remove old backups
find "$BACKUP_DIR/daily" -maxdepth 1 -type f -mtime "+$DAILY_RETENTION" -delete
find "$BACKUP_DIR/weekly" -maxdepth 1 -type f -mtime "+$((WEEKLY_RETENTION * 7))" -delete
find "$BACKUP_DIR/monthly" -maxdepth 1 -type f -mtime "+$((MONTHLY_RETENTION * 30))" -delete

echo "Backup completed: $ARCHIVE"
