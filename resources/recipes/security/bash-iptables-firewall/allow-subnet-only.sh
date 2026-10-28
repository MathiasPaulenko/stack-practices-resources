#!/bin/bash
set -euo pipefail

# Only allow SSH from 10.0.0.0/24
iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP

echo "SSH restricted to 10.0.0.0/24"
