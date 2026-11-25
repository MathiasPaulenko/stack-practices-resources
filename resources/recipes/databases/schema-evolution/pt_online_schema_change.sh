#!/usr/bin/env bash
# Add an index to a large MySQL table without locking it.
# Reads credentials from the environment; never put passwords on the CLI.
set -euo pipefail

pt-online-schema-change \
  --alter "ADD INDEX idx_created_at (created_at)" \
  --execute \
  --max-load Threads_running=25 \
  --critical-load Threads_running=50 \
  D="${MYSQL_DB:-mydb}",t=orders
