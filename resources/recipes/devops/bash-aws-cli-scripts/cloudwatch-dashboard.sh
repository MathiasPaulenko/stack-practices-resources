#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
DASHBOARD_NAME="${1:-app-overview}"

DASHBOARD_BODY=$(cat <<EOF
{
    "widgets": [
        {
            "type": "metric",
            "x": 0, "y": 0, "width": 12, "height": 6,
            "properties": {
                "metrics": [
                    ["AWS/EC2", "CPUUtilization", "AutoScalingGroupName", "app-asg"],
                    [".", "NetworkIn", ".", "."]
                ],
                "period": 300,
                "stat": "Average",
                "region": "$REGION",
                "title": "EC2 CPU and Network"
            }
        },
        {
            "type": "metric",
            "x": 12, "y": 0, "width": 12, "height": 6,
            "properties": {
                "metrics": [
                    ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "app-db"],
                    [".", "DatabaseConnections", ".", "."]
                ],
                "period": 300,
                "stat": "Average",
                "region": "$REGION",
                "title": "RDS CPU and Connections"
            }
        },
        {
            "type": "log",
            "x": 0, "y": 6, "width": 24, "height": 6,
            "properties": {
                "query": "SOURCE 'app-logs' | fields @timestamp, level, message | filter level = \"ERROR\" | sort @timestamp desc | limit 20",
                "region": "$REGION",
                "title": "Recent Errors"
            }
        }
    ]
}
EOF
)

aws cloudwatch put-dashboard \
    --dashboard-name "$DASHBOARD_NAME" \
    --dashboard-body "$DASHBOARD_BODY" \
    --region "$REGION"

echo "Dashboard $DASHBOARD_NAME created"
