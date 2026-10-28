#!/bin/bash
# Batch + parallel processing with xargs: compress .log files 4 at a time.
set -euo pipefail

logdir="${1:-/var/log}"

find "$logdir" -type f -name '*.log' -print0 | xargs -0 -P 4 -I{} gzip "{}"

# Run a linter in batches of 20:
# find src/ -type f -name '*.js' -print0 | xargs -0 -n 20 eslint
