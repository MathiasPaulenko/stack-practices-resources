#!/usr/bin/env bash
# Configure the HashiCorp Vault database secrets engine for dynamic
# credentials. Requires VAULT_ADDR and a Vault token with mount/write
# permissions on database/*.
set -euo pipefail

DB_HOST="${DB_HOST:-db-prod:5432}"
DB_NAME="${DB_NAME:-payment}"
# Never hardcode the admin password — read it from the environment
: "${VAULT_DB_ADMIN_PASSWORD:?Set VAULT_DB_ADMIN_PASSWORD before running}"

# Enable the database secrets engine
vault secrets enable database

# Configure the PostgreSQL connection
vault write database/config/payment-postgres \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@${DB_HOST}/${DB_NAME}?sslmode=require" \
    allowed_roles="payment-service" \
    username="vault-admin" \
    password="${VAULT_DB_ADMIN_PASSWORD}"

# Rotate the root credentials immediately so only Vault knows them
vault write -force database/rotate-root/payment-postgres

# Create a role that issues short-lived credentials
vault write database/roles/payment-service \
    db_name=payment-postgres \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

echo "Setup complete. Test with: vault read database/creds/payment-service"
