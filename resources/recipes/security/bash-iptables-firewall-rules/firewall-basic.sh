#!/usr/bin/env bash
# Baseline iptables ruleset: default-deny inbound, rate-limited SSH, persisted.
# Apply while you have an open session — INPUT DROP takes effect immediately.
set -euo pipefail

# Reset rules and counters
iptables -F
iptables -X
iptables -Z

# Default policies: deny inbound/forward, allow outbound
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Loopback — local services depend on it
iptables -A INPUT -i lo -j ACCEPT

# Replies to connections we initiated
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# SSH, rate-limited: >4 new connections per 60s from one IP get dropped
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Web traffic
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Persist (iptables-persistent writes here; create the dir if missing)
mkdir -p /etc/iptables
iptables-save > /etc/iptables/rules.v4

echo "Firewall rules applied"
