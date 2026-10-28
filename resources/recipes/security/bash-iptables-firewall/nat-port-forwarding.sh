#!/bin/bash

# Enable IP forwarding (runtime) — persist it in /etc/sysctl.conf
# or a file under /etc/sysctl.d/ so it survives reboots
echo 1 > /proc/sys/net/ipv4/ip_forward

# Forward port 8080 to port 80 on 192.168.1.100
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.100:80
iptables -t nat -A POSTROUTING -p tcp -d 192.168.1.100 --dport 80 -j MASQUERADE
# On a static public IP prefer: -j SNAT --to-source <public-ip> (less overhead)

# Allow forwarding in BOTH directions — without this, replies from the
# backend hit the FORWARD DROP policy and the forward only works one way
iptables -A FORWARD -p tcp -d 192.168.1.100 --dport 80 -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

echo "Port forwarding: 8080 -> 192.168.1.100:80"
