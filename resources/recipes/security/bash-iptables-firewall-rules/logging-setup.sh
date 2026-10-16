#!/usr/bin/env bash
# Rate-limited packet logging plus a dedicated log file via rsyslog.
# Without the `limit` match, one port scan fills your disk.
set -euo pipefail

# Log drops, rate-limited: 5/min with a 10-packet burst
iptables -A INPUT -m limit --limit 5/min --limit-burst 10 -j LOG \
    --log-prefix "iptables-DROP: " \
    --log-level 4 \
    --log-ip-options \
    --log-tcp-options

# Read the drops
# journalctl -k | grep "iptables-DROP"
# or: dmesg | grep "iptables-DROP"

# Dedicated log file via rsyslog
cat > /etc/rsyslog.d/10-iptables.conf << 'EOF'
:msg, contains, "iptables-DROP" /var/log/iptables.log
& stop
EOF
systemctl restart rsyslog

echo "iptables logging configured"
