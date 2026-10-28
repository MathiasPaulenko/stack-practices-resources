#!/bin/bash

# Use this INSTEAD of the plain `--dport 22 ACCEPT` from the basic setup —
# that earlier rule matches first and the limiter would never trigger
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT

echo "SSH rate limiting configured: max 3 new connections per minute"
