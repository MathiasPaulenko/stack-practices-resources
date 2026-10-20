#!/bin/bash
# Export AWS IAM Access Analyzer findings for an access review audit trail.
# Usage: ./aws-access-analyzer.sh [region]
set -euo pipefail

REGION="${1:-us-east-1}"
ANALYZER_NAME="org-access-analyzer"

# Create an analyzer if it doesn't already exist
ANALYZER_ARN=$(aws accessanalyzer list-analyzers \
  --type ORGANIZATION \
  --region "$REGION" \
  --query 'analyzers[?analyzerName==`'"$ANALYZER_NAME"'`].arn | [0]' \
  --output text)

if [ -z "$ANALYZER_ARN" ] || [ "$ANALYZER_ARN" = "None" ]; then
  echo "Creating analyzer $ANALYZER_NAME..."
  ANALYZER_ARN=$(aws accessanalyzer create-analyzer \
    --analyzer-name "$ANALYZER_NAME" \
    --type ORGANIZATION \
    --region "$REGION" \
    --query 'analyzer.arn' \
    --output text)
fi

echo "Analyzer: $ANALYZER_ARN"

# List all active findings
echo "=== Active Findings ==="
aws accessanalyzer list-findings \
  --analyzer-arn "$ANALYZER_ARN" \
  --region "$REGION" \
  --filter '{"status":{"eq":["ACTIVE"]}}' \
  --query 'findings[*].{id:id,resource:resource.resourceArn,type:findingType,createdAt:createdAt}' \
  --output table

# Export findings to JSON for audit trail
OUT_FILE="iam-findings-$(date +%Y%m%d).json"
aws accessanalyzer list-findings \
  --analyzer-arn "$ANALYZER_ARN" \
  --region "$REGION" \
  --query 'findings[*].{id:id,resource:resource.resourceArn,type:findingType,createdAt:createdAt}' \
  --output json > "$OUT_FILE"

echo "Findings exported to $OUT_FILE"
