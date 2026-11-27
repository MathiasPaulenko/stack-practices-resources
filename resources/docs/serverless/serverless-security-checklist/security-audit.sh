#!/bin/bash
# security-audit.sh — dependency audit for serverless projects
# Runs npm audit, pip safety check and Snyk; exits non-zero on high/critical findings.
# Usage: ./security-audit.sh

set -uo pipefail

FAILED=0

if [ -f package.json ]; then
  echo "=== npm audit ==="
  npm audit --audit-level=high || FAILED=1
fi

if [ -f requirements.txt ]; then
  echo "=== pip safety check ==="
  pip install -q safety && safety check --full-report || FAILED=1
fi

if command -v npx >/dev/null 2>&1; then
  echo "=== Snyk ==="
  npx snyk test --severity-threshold=high || FAILED=1
fi

# Lockfile provenance check (npm only) — catches registry/typosquat swaps
if [ -f package-lock.json ]; then
  echo "=== lockfile lint ==="
  npx lockfile-lint --path package-lock.json --allowed-hosts npm --validate-https || FAILED=1
fi

[ "$FAILED" -eq 0 ] && echo "All dependency checks passed" || { echo "Security audit failed"; exit 1; }
