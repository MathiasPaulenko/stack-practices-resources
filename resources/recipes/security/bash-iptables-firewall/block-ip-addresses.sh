#!/bin/bash
set -euo pipefail

BLOCKED_IPS=(
    "203.0.113.50"
    "198.51.100.23"
    "192.0.2.100"
)

# Insert (-I), don't append (-A): a block rule must be evaluated BEFORE
# the port allows, otherwise SSH/HTTP/HTTPS from that IP is accepted first
for ip in "${BLOCKED_IPS[@]}"; do
    iptables -I INPUT -s "$ip" -j DROP
    echo "Blocked: $ip"
done
