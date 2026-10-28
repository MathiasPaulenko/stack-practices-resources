#!/bin/bash

set -euo pipefail

START_DATE=$(date -d "30 days ago" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

aws ce get-cost-and-usage \
    --time-period Start="$START_DATE",End="$END_DATE" \
    --granularity DAILY \
    --metrics UnblendedCost \
    --group-by Type=DIMENSION,Key=SERVICE \
    --query 'ResultsByTime[*].[TimePeriod.Start,Groups[*].[Keys[0],Metrics.UnblendedCost.Amount]]' \
    --output table
