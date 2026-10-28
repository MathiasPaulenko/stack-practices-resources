#!/bin/bash
set -euo pipefail

echo "=== Filter table ==="
iptables -L -n -v --line-numbers

echo ""
echo "=== NAT table ==="
iptables -t nat -L -n -v --line-numbers

echo ""
echo "=== Mangle table ==="
iptables -t mangle -L -n -v --line-numbers
