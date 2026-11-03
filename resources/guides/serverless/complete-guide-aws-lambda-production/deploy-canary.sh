#!/usr/bin/env bash
# Canary deploy via alias traffic shifting.
# Source: https://stackpractices.com/guides/complete-guide-aws-lambda-production/
set -euo pipefail

FUNCTION="${1:?function name required}"

aws lambda publish-version --function-name "$FUNCTION"

# 10% canary on the new version
aws lambda update-alias \
  --function-name "$FUNCTION" \
  --name live \
  --function-version "$(aws lambda list-versions-by-function \
      --function-name "$FUNCTION" \
      --query 'Versions[-1].Version' --output text)" \
  --routing-config '{"AdditionalVersionWeights": {"1": 0.9}}'

echo "Canary live at 10%. Monitor CloudWatch, then promote with:"
echo "  aws lambda update-alias --function-name $FUNCTION \\"
echo "    --name live --function-version <v> --routing-config '{}'"
