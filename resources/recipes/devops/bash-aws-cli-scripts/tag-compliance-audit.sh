#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
REQUIRED_TAGS=("Project" "Environment" "Owner" "CostCenter")

# Audit EC2 instances for missing required tags
INSTANCES=$(aws ec2 describe-instances \
    --query 'Reservations[*].Instances[?State.Name==`running`].[InstanceId,Tags]' \
    --output json \
    --region "$REGION")

echo "$INSTANCES" | jq -c '.[]' | while read -r instance; do
    instance_id=$(echo "$instance" | jq -r '.[0]')
    tags=$(echo "$instance" | jq -r '.[1] // [] | map(.Key)')
    missing=()
    for req_tag in "${REQUIRED_TAGS[@]}"; do
        if ! echo "$tags" | grep -q "\"$req_tag\""; then
            missing+=("$req_tag")
        fi
    done
    if [ ${#missing[@]} -gt 0 ]; then
        echo "VIOLATION: $instance_id missing tags: ${missing[*]}"
    fi
done

# Audit S3 buckets for missing tags
# Buckets can live in other regions — resolve each one's location first,
# otherwise get-bucket-tagging fails with PermanentRedirect and reports false positives
BUCKETS=$(aws s3api list-buckets --query 'Buckets[*].Name' --output text --region "$REGION")
for bucket in $BUCKETS; do
    BUCKET_REGION=$(aws s3api get-bucket-location --bucket "$bucket" \
        --query 'LocationConstraint' --output text 2>/dev/null || echo "")
    [ "$BUCKET_REGION" = "None" ] && BUCKET_REGION="us-east-1"
    bucket_tags=$(aws s3api get-bucket-tagging --bucket "$bucket" \
        --region "${BUCKET_REGION:-$REGION}" \
        --query 'TagSet[*].Key' --output text 2>/dev/null || echo "")
    missing=()
    for req_tag in "${REQUIRED_TAGS[@]}"; do
        if ! echo "$bucket_tags" | grep -qw "$req_tag"; then
            missing+=("$req_tag")
        fi
    done
    if [ ${#missing[@]} -gt 0 ]; then
        echo "VIOLATION: bucket $bucket missing tags: ${missing[*]}"
    fi
done
