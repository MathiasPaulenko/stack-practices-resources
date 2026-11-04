#!/usr/bin/env bash
# Create a monthly AWS budget with an 80% actual-spend email alert.
# Usage: ACCOUNT_ID=123456789012 EMAIL=ops@example.com ./budget-alert.sh
set -euo pipefail

aws budgets create-budget \
  --account-id "${ACCOUNT_ID:?set ACCOUNT_ID}" \
  --budget '{
    "BudgetName": "MonthlyBudget",
    "BudgetLimit": {"Amount": "5000", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers "[
    {
      \"Notification\": {
        \"NotificationType\": \"ACTUAL\",
        \"ComparisonOperator\": \"GREATER_THAN\",
        \"Threshold\": 80
      },
      \"Subscribers\": [{
        \"SubscriptionType\": \"EMAIL\",
        \"Address\": \"${EMAIL:?set EMAIL}\"
      }]
    }
  ]"
