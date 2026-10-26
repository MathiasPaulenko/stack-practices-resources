#!/bin/bash
set -euo pipefail

# Automated access review with AWS IAM Access Analyzer
# Usage: ./aws-iam-access-analyzer.sh
# Requires: aws CLI configured, IAM + Access Analyzer read permissions, jq

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ANALYZER_ARN="${ANALYZER_ARN:-}"

# List all IAM users and their last activity
echo "=== IAM Users Last Activity ==="
aws iam get-account-authorization-details --output json | \
  jq -r '.UserDetailList[] | {
    user: .UserName,
    groups: (.Groups | join(", ")),
    policies: (.AttachedManagedPolicies | map(.PolicyName) | join(", ")),
    last_used: .PasswordLastUsed
  }'

# Check for unused access keys
echo ""
echo "=== Unused Access Keys (>90 days) ==="
for user in $(aws iam list-users --query 'Users[].UserName' --output text); do
  aws iam list-access-keys --user-name "$user" --output json | \
    jq -r '.AccessKeyMetadata[] | select(.Status=="Active") | "\(.UserName) \(.AccessKeyId) \(.CreateDate)"'
done

# Generate unused permissions report (requires an existing analyzer ARN)
if [ -n "$ANALYZER_ARN" ]; then
  echo ""
  echo "=== IAM Access Analyzer Findings ==="
  aws accessanalyzer list-findings --analyzer-arn "$ANALYZER_ARN" --output json | \
    jq -r '.findings[] | select(.status=="ACTIVE") | {
      resource: .resource,
      finding: .findingType,
      principal: .principal
    }'
else
  echo ""
  echo "Skipping Access Analyzer findings — set ANALYZER_ARN to enable."
fi
