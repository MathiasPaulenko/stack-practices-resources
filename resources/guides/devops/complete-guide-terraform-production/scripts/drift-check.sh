#!/bin/bash
# scripts/drift-check.sh — detect real drift: refresh state against actual
# infrastructure WITHOUT evaluating new configuration.
# exit 2 from `plan -refresh-only -detailed-exitcode` = reality changed vs state.
# (Plain `plan -detailed-exitcode` exit 2 also fires on unapplied code changes —
# that is not drift.)
set -euo pipefail

ENV_DIR="${1:-terraform/environments/production}"

cd "$ENV_DIR"
terraform init -input=false

EXIT_CODE=0
terraform plan -refresh-only -detailed-exitcode -out=refresh.tfplan || EXIT_CODE=$?

if [ "$EXIT_CODE" -eq 2 ]; then
  echo "DRIFT DETECTED — infrastructure diverged from Terraform state"
  terraform show -no-color refresh.tfplan | head -100
  rm -f refresh.tfplan
  exit 1
elif [ "$EXIT_CODE" -eq 0 ]; then
  echo "No drift detected"
  rm -f refresh.tfplan
  exit 0
else
  echo "terraform plan failed with exit code $EXIT_CODE"
  rm -f refresh.tfplan
  exit "$EXIT_CODE"
fi
