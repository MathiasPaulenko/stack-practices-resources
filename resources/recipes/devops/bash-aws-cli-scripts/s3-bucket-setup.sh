#!/bin/bash

set -euo pipefail

BUCKET_NAME="my-app-backups-$(date +%Y%m%d)"
REGION="us-east-1"

# Create bucket — us-east-1 takes no LocationConstraint
if [ "$REGION" = "us-east-1" ]; then
    aws s3api create-bucket --bucket "$BUCKET_NAME"
else
    aws s3api create-bucket \
        --bucket "$BUCKET_NAME" \
        --region "$REGION" \
        --create-bucket-configuration LocationConstraint="$REGION"
fi

echo "Created bucket: $BUCKET_NAME"

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket "$BUCKET_NAME" \
    --versioning-configuration Status=Enabled

# Lifecycle: logs move to Infrequent Access at 30 days, Glacier at 90, expire at 365
cat > /tmp/lifecycle.json << 'EOF'
{
    "Rules": [
        {
            "ID": "LogLifecycleRule",
            "Status": "Enabled",
            "Filter": { "Prefix": "logs/" },
            "Transitions": [
                { "Days": 30, "StorageClass": "STANDARD_IA" },
                { "Days": 90, "StorageClass": "GLACIER" }
            ],
            "Expiration": { "Days": 365 },
            "NoncurrentVersionExpiration": { "NoncurrentDays": 30 }
        }
    ]
}
EOF

aws s3api put-bucket-lifecycle-configuration \
    --bucket "$BUCKET_NAME" \
    --lifecycle-configuration file:///tmp/lifecycle.json

echo "Versioning and lifecycle policy configured"

# Audit: list objects under the prefix older than 90 days
# date -d is GNU date — on macOS install coreutils and use gdate
aws s3api list-objects-v2 \
    --bucket "$BUCKET_NAME" \
    --prefix "logs/" \
    --query "Contents[?LastModified<='$(date -d '90 days ago' -I)'].[Key,LastModified,Size]" \
    --output table
