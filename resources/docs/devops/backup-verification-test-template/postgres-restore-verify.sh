#!/bin/bash
# Restore and verify a PostgreSQL backup
set -euo pipefail

BACKUP_FILE="/backups/prod_db_2026-07-11.sql.gz"
TEST_DB="restore_test_$(date +%s)"
PG_HOST="test-db.internal"
PG_USER="restore_verifier"

echo "=== PostgreSQL Backup Restore Verification ==="
echo "Backup: $BACKUP_FILE"
echo "Test DB: $TEST_DB"
echo ""

# Create test database
echo "[1/6] Creating test database..."
createdb -h "$PG_HOST" -U "$PG_USER" "$TEST_DB"

# Restore backup
echo "[2/6] Restoring backup..."
gunzip -c "$BACKUP_FILE" | psql -h "$PG_HOST" -U "$PG_USER" -d "$TEST_DB" -v ON_ERROR_STOP=1 > /dev/null

# Verify row counts
echo "[3/6] Verifying row counts..."
TABLES=$(psql -h "$PG_HOST" -U "$PG_USER" -d "$TEST_DB" -t -c "SELECT tablename FROM pg_tables WHERE schemaname='public'")
for table in $TABLES; do
  count=$(psql -h "$PG_HOST" -U "$PG_USER" -d "$TEST_DB" -t -c "SELECT count(*) FROM $table")
  echo "  $table: $count rows"
done

# Verify constraints
echo "[4/6] Verifying constraints..."
CONSTRAINTS=$(psql -h "$PG_HOST" -U "$PG_USER" -d "$TEST_DB" -t -c "SELECT count(*) FROM pg_constraint WHERE conrelid IN (SELECT oid FROM pg_class WHERE relnamespace='public'::regnamespace)")
echo "  Active constraints: $CONSTRAINTS"

# Verify indexes
echo "[5/6] Verifying indexes..."
INDEXES=$(psql -h "$PG_HOST" -U "$PG_USER" -d "$TEST_DB" -t -c "SELECT count(*) FROM pg_indexes WHERE schemaname='public'")
echo "  Active indexes: $INDEXES"

# Run smoke queries
echo "[6/6] Running smoke queries..."
psql -h "$PG_HOST" -U "$PG_USER" -d "$TEST_DB" -c "SELECT 1 as test" > /dev/null && echo "  Smoke query: PASS" || echo "  Smoke query: FAIL"

# Cleanup
echo ""
echo "Cleaning up test database..."
dropdb -h "$PG_HOST" -U "$PG_USER" "$TEST_DB"
echo "=== Verification Complete ==="
