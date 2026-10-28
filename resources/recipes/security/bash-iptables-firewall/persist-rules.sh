#!/bin/bash
set -euo pipefail

# The dir doesn't exist until the package is installed (or created)
mkdir -p /etc/iptables

# Debian/Ubuntu: install first, then save — netfilter-persistent reloads
# these files on boot
apt-get install -y iptables-persistent
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6
netfilter-persistent save

# RHEL/Fedora equivalent: install iptables-services and run
#   service iptables save   (writes /etc/sysconfig/iptables)
# — or use firewalld, which those distros ship by default.

# Or restore manually on boot via systemd
cat > /etc/systemd/system/iptables-restore.service << 'EOF'
[Unit]
Description=Restore iptables rules
Wants=network-pre.target
Before=network-pre.target

[Service]
Type=oneshot
ExecStart=/sbin/iptables-restore /etc/iptables/rules.v4
ExecStart=/sbin/ip6tables-restore /etc/iptables/rules.v6

[Install]
WantedBy=multi-user.target
EOF

systemctl enable iptables-restore.service

echo "Rules persisted to /etc/iptables/rules.v4 and rules.v6"
