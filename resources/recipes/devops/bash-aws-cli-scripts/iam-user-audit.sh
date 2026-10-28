#!/bin/bash

set -euo pipefail

echo "=== IAM User Audit ==="
echo "Date: $(date)"
echo ""

# List all users
USERS=$(aws iam list-users --query 'Users[*].UserName' --output text)

for user in $USERS; do
    echo "--- User: $user ---"

    # Get access keys (tolerate per-user permission failures)
    KEYS=$(aws iam list-access-keys --user-name "$user" --output text 2>/dev/null || echo "")
    if [ -n "$KEYS" ]; then
        echo "Access keys:"
        echo "$KEYS" | tr '\t' '\n'
    else
        echo "No access keys"
    fi

    # Get attached policies
    POLICIES=$(aws iam list-attached-user-policies --user-name "$user" \
        --query 'AttachedPolicies[*].PolicyName' --output text 2>/dev/null || echo "")
    if [ -n "$POLICIES" ]; then
        echo "Attached policies: $POLICIES"
    fi

    # Get groups
    GROUPS=$(aws iam list-groups-for-user --user-name "$user" \
        --query 'Groups[*].GroupName' --output text 2>/dev/null || echo "")
    if [ -n "$GROUPS" ]; then
        echo "Groups: $GROUPS"
    fi

    echo ""
done
