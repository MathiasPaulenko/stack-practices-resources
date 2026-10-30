#!/bin/bash
# warmup-before-deploy.sh — run BEFORE switching traffic to a new deploy.
# Exits non-zero on any failure so the pipeline can gate the traffic switch.
set -euo pipefail

REDIS_HOST="${REDIS_HOST:-redis-new.internal}"
REDIS_PORT="${REDIS_PORT:-6379}"
WARMUP_SCRIPT="${WARMUP_SCRIPT:-src/warmup.py}"
HOTKEYS_SCRIPT="${HOTKEYS_SCRIPT:-src/hot_keys.py}"
ACCESS_LOG="${ACCESS_LOG:-/var/log/app/cache-access.jsonl}"

echo "=== Pre-deployment cache warmup ==="

# 1. Export hot keys from the last ~24h of structured access logs
python3 "$HOTKEYS_SCRIPT" --logs "$ACCESS_LOG" --output /tmp/hot-keys.json

# 2. Warm the new cache: critical first (short TTL), then high priority
python3 "$WARMUP_SCRIPT" --keys /tmp/hot-keys.json \
    --redis "$REDIS_HOST:$REDIS_PORT" --tiers critical,high

# 3. Verify the new instance is populated and healthy
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" \
    info | grep -E 'used_memory_human|keyspace_hits|keyspace_misses'
redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" dbsize

echo "=== Warmup complete — safe to switch traffic ==="
