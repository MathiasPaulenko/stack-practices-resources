# pigz compresses across all cores (GNU tar only — bsdtar has no -I)
tar -I pigz -cf "${BACKUP_FILE}" -C "${SOURCE_DIR}" .

# Skip caches, logs, and temp files
tar -czf "${BACKUP_FILE}"     --exclude="*.log"     --exclude="*.tmp"     --exclude="cache/*"     --exclude="node_modules/*"     -C "${SOURCE_DIR}" .

# Don't let backups starve production I/O
ionice -c 3 tar -czf "${BACKUP_FILE}" -C "${SOURCE_DIR}" .
