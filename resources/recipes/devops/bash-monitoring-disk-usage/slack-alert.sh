#!/usr/bin/env bash
set -euo pipefail

SLACK_WEBHOOK="${SLACK_WEBHOOK:-https://hooks.slack.com/services/XXX}"
THRESHOLD="${1:-80}"
HOSTNAME=$(hostname)

send_slack_alert() {
    local mount="$1" usage="$2" fs="$3"
    local payload
    payload=$(cat <<EOF
{
    "text": "Disk alert on ${HOSTNAME}",
    "attachments": [{
        "color": "danger",
        "fields": [
            {"title": "Mount", "value": "${mount}", "short": true},
            {"title": "Usage", "value": "${usage}", "short": true},
            {"title": "Filesystem", "value": "${fs}", "short": true},
            {"title": "Host", "value": "${HOSTNAME}", "short": true}
        ]
    }]
}
EOF
)
    curl -s -X POST -H 'Content-Type: application/json' -d "$payload" "$SLACK_WEBHOOK"
}

df -Hl | awk 'NR>1 && /^\/dev/{print $1, $5, $6}' | while read -r fs usage mount; do
    usage_val="${usage%\%}"
    if (( usage_val >= THRESHOLD )); then
        send_slack_alert "$mount" "$usage" "$fs"
        echo "[$(date -Iseconds)] WARNING: $mount ($fs) at $usage — Slack alert sent"
    fi
done
