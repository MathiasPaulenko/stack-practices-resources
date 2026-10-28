#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
ACCOUNTS=("dev:111111111111" "staging:222222222222" "prod:333333333333")  # replace with your account IDs
ROLE_NAME="DeploymentRole"

for account in "${ACCOUNTS[@]}"; do
    ENV="${account%%:*}"
    ACCOUNT_ID="${account##*:}"

    echo "=== Deploying to $ENV ($ACCOUNT_ID) ==="

    # Assume the deployment role in this account
    CREDS=$(aws sts assume-role \
        --role-arn "arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME" \
        --role-session-name "deploy-$ENV-$(date +%s)" \
        --query 'Credentials' \
        --output json)

    export AWS_ACCESS_KEY_ID=$(echo "$CREDS" | jq -r '.AccessKeyId')
    export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS" | jq -r '.SecretAccessKey')
    export AWS_SESSION_TOKEN=$(echo "$CREDS" | jq -r '.SessionToken')

    # Deploy: update Lambda function
    aws lambda update-function-code \
        --function-name "app-handler" \
        --zip-file "fileb://dist/handler.zip" \
        --region "$REGION"

    # Verify deployment
    STATUS=$(aws lambda get-function \
        --function-name "app-handler" \
        --query 'Configuration.LastUpdateStatus' \
        --output text)

    echo "Deployment to $ENV: $STATUS"

    # Clear credentials before the next account
    unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
done
