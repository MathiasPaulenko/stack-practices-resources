#!/bin/bash
set -euo pipefail

# Evidence collection for SOC 2 / ISO 27001 gap analysis
# Usage: ./collect-evidence.sh
# Requires: aws CLI configured (read-only permissions are enough), kubectl optional

OUT="compliance-evidence/$(date +%Y-%m)"
mkdir -p "$OUT"

echo "=== AWS Config compliance ==="
aws configservice get-discovery-summary > "$OUT/config-summary.json" || \
  echo "AWS Config not enabled in this account" > "$OUT/config-summary.json"

echo "=== IAM evidence (CC6.1) ==="
aws iam get-account-summary > "$OUT/iam-account-summary.json"
aws iam list-virtual-mfa-devices > "$OUT/mfa-devices.json"
aws iam get-account-summary --query 'SummaryMap.AccountMFAEnabled' --output text \
  > "$OUT/root-mfa-status.txt"

echo "=== S3 encryption evidence (CC6.7) ==="
aws s3api list-buckets --query 'Buckets[].Name' --output text | tr '\t' '\n' | \
  while read -r bucket; do
    ENC=$(aws s3api get-bucket-encryption --bucket "$bucket" \
      --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' \
      --output text 2>/dev/null || echo "None")
    echo "$bucket: $ENC" >> "$OUT/s3-encryption-evidence.txt"
  done

echo "=== CloudTrail evidence (CC7.2) ==="
aws cloudtrail describe-trails \
  --query 'trailList[].{Name:Name,IsLogging:IsLogging,S3Bucket:S3BucketName}' \
  --output table > "$OUT/cloudtrail-evidence.txt" || \
  echo "No CloudTrail trails found" > "$OUT/cloudtrail-evidence.txt"

echo "=== Dependency evidence ==="
if command -v npm >/dev/null 2>&1; then
  npm audit --json > "$OUT/npm-audit.json" 2>/dev/null || true
fi
if command -v trivy >/dev/null 2>&1; then
  trivy image --format json "${TRIVY_IMAGE:-myapp:latest}" > "$OUT/trivy-scan.json" 2>/dev/null || true
fi

echo "Done. Evidence written to $OUT/"
echo "Commit it: git add $OUT && git commit -m 'compliance: monthly evidence snapshot'"
