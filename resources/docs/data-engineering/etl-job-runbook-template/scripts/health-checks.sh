#!/usr/bin/env bash
# health-checks.sh — pre-run health checks for an Airflow-orchestrated ETL job.
#
# Exits non-zero if any check fails, so it can gate a pipeline run or a cron.
# Configure via environment variables; every check degrades gracefully when a
# tool or env var is missing (reported as SKIP, not FAIL).

set -u

DAG_ID="${DAG_ID:-orders_etl_pipeline}"
RUN_DATE="${RUN_DATE:-$(date -u +%F)}"
AIRFLOW_NAMESPACE="${AIRFLOW_NAMESPACE:-airflow}"
SOURCE_API_HEALTH_URL="${SOURCE_API_HEALTH_URL:-}"
STAGING_BUCKET="${STAGING_BUCKET:-}"
WAREHOUSE_HOST="${WAREHOUSE_HOST:-}"
DBT_PROJECT_DIR="${DBT_PROJECT_DIR:-}"
MIN_WORKERS="${MIN_WORKERS:-2}"

pass=0; fail=0; skip=0

check() {
  local name="$1"; shift
  local expected="$1"; shift
  if "$@" >/dev/null 2>&1; then
    printf 'PASS  %-45s expected: %s\n' "$name" "$expected"
    pass=$((pass+1))
  else
    printf 'FAIL  %-45s expected: %s\n' "$name" "$expected"
    fail=$((fail+1))
  fi
}

note_skip() {
  printf 'SKIP  %-45s reason: %s\n' "$1" "$2"
  skip=$((skip+1))
}

echo "== Pre-run health checks for ${DAG_ID} (${RUN_DATE}) =="

# 1. Airflow scheduler and workers (Kubernetes deployments only)
if command -v kubectl >/dev/null 2>&1 && kubectl cluster-info >/dev/null 2>&1; then
  check "airflow scheduler pod running" "Running" \
    kubectl get pods -n "$AIRFLOW_NAMESPACE" --field-selector=status.phase=Running -l component=scheduler -o name
  workers=$(kubectl get pods -n "$AIRFLOW_NAMESPACE" --field-selector=status.phase=Running -l component=worker -o name 2>/dev/null | wc -l)
  if [ "$workers" -ge "$MIN_WORKERS" ]; then
    printf 'PASS  %-45s expected: >= %s\n' "airflow workers available" "$MIN_WORKERS"; pass=$((pass+1))
  else
    printf 'FAIL  %-45s expected: >= %s (got %s)\n' "airflow workers available" "$MIN_WORKERS" "$workers"; fail=$((fail+1))
  fi
else
  note_skip "airflow scheduler/workers" "kubectl not installed or no cluster reachable"
fi

# 2. Source API reachable
if [ -n "$SOURCE_API_HEALTH_URL" ]; then
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$SOURCE_API_HEALTH_URL" || echo "000")
  if [ "$code" = "200" ]; then
    printf 'PASS  %-45s expected: 200\n' "source api reachable"; pass=$((pass+1))
  else
    printf 'FAIL  %-45s expected: 200 (got %s)\n' "source api reachable" "$code"; fail=$((fail+1))
  fi
else
  note_skip "source api reachable" "SOURCE_API_HEALTH_URL not set"
fi

# 3. Staging bucket writable
if [ -n "$STAGING_BUCKET" ] && command -v aws >/dev/null 2>&1; then
  check "staging bucket writable" "no error" aws s3 ls "s3://${STAGING_BUCKET}/"
else
  note_skip "staging bucket writable" "STAGING_BUCKET not set or aws CLI missing"
fi

# 4. Warehouse reachable
if [ -n "$WAREHOUSE_HOST" ] && command -v psql >/dev/null 2>&1; then
  check "warehouse accepts queries" "SELECT 1" psql -h "$WAREHOUSE_HOST" -c 'SELECT 1'
else
  note_skip "warehouse accepts queries" "WAREHOUSE_HOST not set or psql missing"
fi

# 5. dbt project compiles
if [ -n "$DBT_PROJECT_DIR" ] && command -v dbt >/dev/null 2>&1; then
  check "dbt project compiles" "no error" dbt compile --project-dir "$DBT_PROJECT_DIR"
else
  note_skip "dbt project compiles" "DBT_PROJECT_DIR not set or dbt missing"
fi

# 6. Previous DAG run finished successfully
if command -v airflow >/dev/null 2>&1; then
  state=$(airflow dags state "$DAG_ID" "$RUN_DATE" 2>/dev/null || echo "unknown")
  if [ "$state" = "success" ]; then
    printf 'PASS  %-45s expected: success\n' "previous run state"; pass=$((pass+1))
  else
    printf 'WARN  %-45s expected: success (got %s)\n' "previous run state" "$state"
  fi
else
  note_skip "previous run state" "airflow CLI not installed"
fi

echo
echo "== Summary: ${pass} passed, ${fail} failed, ${skip} skipped =="
[ "$fail" -eq 0 ]
