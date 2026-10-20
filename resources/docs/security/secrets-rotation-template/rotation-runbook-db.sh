#!/bin/bash
# Rotate a database password with zero downtime using the dual-read
# pattern: the old and new credentials stay valid during the transition.
# Usage: ./rotation-runbook-db.sh
# Requires: psql, aws cli, kubectl configured for the target environment.

set -euo pipefail

DB_HOST="db.internal"
DB_NAME="appdb"
OLD_USER="app_user_old"
NEW_USER="app_user_new"
NEW_PASSWORD=$(openssl rand -base64 32)

# 1. Create the new user with identical permissions
psql -h "$DB_HOST" -U admin -d "$DB_NAME" -c "
  CREATE USER $NEW_USER WITH PASSWORD '$NEW_PASSWORD';
  GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO $NEW_USER;
  GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO $NEW_USER;
"

# 2. Push the new credentials to the secret manager
aws secretsmanager update-secret \
  --secret-id prod/db/app-user \
  --secret-string "{\"username\":\"$NEW_USER\",\"password\":\"$NEW_PASSWORD\"}"

# 3. Rolling restart so pods pick up the new secret
kubectl rollout restart deployment/app -n production
kubectl rollout status deployment/app -n production --timeout=300s

# 4. Verify connections now use the new user
psql -h "$DB_HOST" -U admin -d "$DB_NAME" -c "
  SELECT usename, count(*) FROM pg_stat_activity
  WHERE datname='appdb' GROUP BY usename;
"

# 5. After the validation window (24-48h), drop the old user.
#    Run this step manually once you confirm zero connections on OLD_USER:
# psql -h "$DB_HOST" -U admin -d "$DB_NAME" -c "DROP USER $OLD_USER;"

echo "Rotation staged. Verify connections, then drop $OLD_USER manually."
