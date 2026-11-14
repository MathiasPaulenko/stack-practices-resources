#!/usr/bin/env bash
# Daily drift check: run `terraform plan -detailed-exitcode` per environment.
# exit 0 = no drift, exit 1 = error, exit 2 = drift detected.
set -u

ENVS="${1:-dev staging production}"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)/environments"
status=0

for env in $ENVS; do
  echo "=== Checking drift for: $env ==="
  (cd "$BASE_DIR/$env" && terraform plan -detailed-exitcode -input=false -no-color)
  code=$?
  case $code in
    0) echo "[$env] no drift" ;;
    2) echo "[$env] DRIFT DETECTED — open a PR to codify, revert, or import"; status=2 ;;
    *) echo "[$env] plan failed (exit $code)"; status=1 ;;
  esac
done

exit $status
