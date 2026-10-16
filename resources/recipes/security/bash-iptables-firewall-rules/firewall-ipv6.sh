#!/usr/bin/env bash
# IPv6 twin of the baseline ruleset. ICMPv6 is mandatory: neighbor discovery
# and path MTU discovery break without it.
set -euo pipefail

ip6tables -F
ip6tables -X
ip6tables -Z

ip6tables -P INPUT DROP
ip6tables -P FORWARD DROP
ip6tables -P OUTPUT ACCEPT

ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# ICMPv6 is required — neighbor discovery, path MTU, MLD all break without it
ip6tables -A INPUT -p icmpv6 -j ACCEPT

ip6tables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
ip6tables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT

ip6tables -A INPUT -p tcp --dport 80 -j ACCEPT
ip6tables -A INPUT -p tcp --dport 443 -j ACCEPT

mkdir -p /etc/iptables
ip6tables-save > /etc/iptables/rules.v6

echo "IPv6 firewall rules applied"
