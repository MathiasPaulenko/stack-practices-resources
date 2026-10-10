#!/bin/bash
# failover.sh - Automated database failover with pre-flight checks
# Usage: ./failover.sh [--force] [--dry-run]

set -euo pipefail

FORCE=false
DRY_RUN=false

for arg in "$@"; do
  case $arg in
    --force) FORCE=true ;;
    --dry-run) DRY_RUN=true ;;
  esac
done

PRIMARY_HOST="primary.db.internal"
REPLICA_HOST="replica.db.internal"
DB_USER="monitor"
MAX_LAG_SECONDS=5

log() { echo "[$(date -u +%H:%M:%S)] $1"; }

# Step 1: Pre-flight checks
log "Running pre-flight checks..."

# Check primary is actually down
if ping -c 1 -W 2 "$PRIMARY_HOST" &>/dev/null && ! $FORCE; then
  log "ERROR: Primary is reachable. Use --force to override."
  exit 1
fi

# Check replica lag
log "Checking replica lag..."
PG_LAG=$(psql -h "$REPLICA_HOST" -U "$DB_USER" -t -c \
  "SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()));" 2>/dev/null | xargs)

if (( $(echo "$PG_LAG > $MAX_LAG_SECONDS" | bc -l) )) && ! $FORCE; then
  log "ERROR: Replica lag is ${PG_LAG}s (max: ${MAX_LAG_SECONDS}s). Use --force to override."
  exit 1
fi

log "Pre-flight checks passed. Replica lag: ${PG_LAG}s"

if $DRY_RUN; then
  log "DRY RUN: Would proceed with failover."
  exit 0
fi

# Step 2: Enable read-only mode
log "Enabling read-only mode..."
curl -sS -X POST http://app.internal/admin/read-only || log "WARN: Could not enable read-only mode"

# Step 3: Promote replica
log "Promoting replica to primary..."
sudo -u postgres pg_ctl promote -D /var/lib/postgresql/data

# Verify promotion
IS_RECOVERY=$(psql -h "$REPLICA_HOST" -U "$DB_USER" -t -c "SELECT pg_is_in_recovery();" | xargs)
if [ "$IS_RECOVERY" != "f" ]; then
  log "ERROR: Promotion failed. pg_is_in_recovery returned: $IS_RECOVERY"
  exit 1
fi
log "Promotion successful."

# Step 4: Update application config
log "Updating application configuration..."
kubectl set env deployment/app DB_HOST="$REPLICA_HOST"
kubectl rollout status deployment/app --timeout=120s

# Step 5: Verify
log "Running post-failover verification..."
sleep 5
HTTP_CODE=$(curl -sS -o /dev/null -w "%{http_code}" http://app.internal/health)
if [ "$HTTP_CODE" != "200" ]; then
  log "ERROR: Health check failed with HTTP $HTTP_CODE"
  exit 1
fi

WRITE_RESULT=$(curl -sS -X POST http://app.internal/api/test \
  -H "Content-Type: application/json" \
  -d "{\"test\": \"failover-$(date +%s)\"}" -w "\n%{http_code}")

WRITE_CODE=$(echo "$WRITE_RESULT" | tail -1)
if [ "$WRITE_CODE" != "200" ] && [ "$WRITE_CODE" != "201" ]; then
  log "ERROR: Write test failed with HTTP $WRITE_CODE"
  exit 1
fi

log "Failover complete. All verifications passed."
log "Next steps:"
log "  1. Establish new replication (Step 7 of runbook)"
log "  2. Update incident timeline"
log "  3. Schedule postmortem"
