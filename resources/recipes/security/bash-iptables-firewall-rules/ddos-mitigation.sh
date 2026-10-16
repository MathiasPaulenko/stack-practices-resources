#!/usr/bin/env bash
# DDoS mitigation: per-IP connection caps, new-connection rate limits,
# SYNPROXY handshake offload (kernel 3.12+), and ICMP throttling.
# Complement for upstream scrubbing — not a replacement under volumetric attack.
set -euo pipefail

# Cap concurrent connections per single IP
iptables -A INPUT -p tcp -m connlimit --connlimit-above 50 --connlimit-mask 32 -j DROP

# New connections: accept up to 20/s with a 40-packet burst, drop the rest
iptables -A INPUT -p tcp -m conntrack --ctstate NEW -m limit --limit 20/s --limit-burst 40 -j ACCEPT
iptables -A INPUT -p tcp -m conntrack --ctstate NEW -j DROP

# Spoofed or malformed packets never belong to a valid connection
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP

# SYNPROXY: validate handshakes without holding sockets
iptables -t raw -A PREROUTING -p tcp -m tcp --syn -j CT --notrack
iptables -A INPUT -p tcp -m tcp --syn -m conntrack --ctstate UNTRACKED,INVALID -j SYNPROXY --sack-perm --timestamp --wscale 7 --mss 1460
iptables -A INPUT -p tcp -m tcp --syn -m conntrack --ctstate UNTRACKED,INVALID -j DROP

# ICMP: enough for diagnostics, not enough for a ping flood
iptables -A INPUT -p icmp -m limit --limit 1/s --limit-burst 3 -j ACCEPT
iptables -A INPUT -p icmp -j DROP

echo "DDoS mitigation rules applied"
