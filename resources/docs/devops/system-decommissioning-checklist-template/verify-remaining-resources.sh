#!/bin/bash
# Verify remaining resources after decommissioning
# Usage: SERVICE_NAME=legacy-auth-service AWS_REGION=us-east-1 ./verify-remaining-resources.sh
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-legacy-auth-service}"
AWS_REGION="${AWS_REGION:-us-east-1}"

echo "=== Remaining Resource Verification ==="
echo "Service: $SERVICE_NAME"
echo "Date: $(date)"
echo ""

# Check DNS records
echo "--- DNS Records ---"
dig +short "$SERVICE_NAME.internal.example.com" && echo "WARNING: DNS record still exists" || echo "OK: No DNS record"

# Check AWS resources
echo "--- AWS Resources ---"
aws ec2 describe-instances --region "$AWS_REGION" --filters "Name=tag:Service,Values=$SERVICE_NAME" --query 'Reservations[*].Instances[*].InstanceId' --output text 2>/dev/null | while read -r id; do
  [ -n "$id" ] && echo "WARNING: EC2 instance found: $id"
done

aws rds describe-db-instances --region "$AWS_REGION" --query 'DBInstances[?DBInstanceIdentifier.contains(@, `'$SERVICE_NAME'`)].DBInstanceIdentifier' --output text 2>/dev/null | while read -r id; do
  [ -n "$id" ] && echo "WARNING: RDS instance found: $id"
done

aws s3 ls --region "$AWS_REGION" 2>/dev/null | grep "$SERVICE_NAME" && echo "WARNING: S3 bucket found" || echo "OK: No S3 buckets"

# Check certificates
echo "--- Certificates ---"
aws acm list-certificates --region "$AWS_REGION" --query 'CertificateSummaryList[*].DomainName' --output text 2>/dev/null | tr '\t' '\n' | grep -i "$SERVICE_NAME" && echo "WARNING: ACM certificate found" || echo "OK: No certificates"

# Check CloudWatch alarms
echo "--- CloudWatch Alarms ---"
aws cloudwatch describe-alarms --region "$AWS_REGION" --query 'MetricAlarms[?AlarmName.contains(@, `'$SERVICE_NAME'`)].AlarmName' --output text 2>/dev/null | while read -r alarm; do
  [ -n "$alarm" ] && echo "WARNING: CloudWatch alarm found: $alarm"
done

echo ""
echo "=== Verification Complete ==="
echo "Extend this script with your stack: Kubernetes namespaces, Datadog monitors, Vault policies, etc."
