#!/bin/sh
# wait-for-vault.sh — retry until Vault answers, then exec the real command.
# Usage: ./wait-for-vault.sh node server.js

set -e

VAULT_ADDR="${VAULT_ADDR:-http://vault:8200}"
TRIES=30

echo "Waiting for Vault at $VAULT_ADDR ..."
until wget -q -O- "$VAULT_ADDR/v1/sys/health" >/dev/null 2>&1; do
    TRIES=$((TRIES - 1))
    if [ "$TRIES" -le 0 ]; then
        echo "Vault did not become ready in time" >&2
        exit 1
    fi
    sleep 1
done

echo "Vault is up — starting $*"
exec "$@"
