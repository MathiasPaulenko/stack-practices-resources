# Advanced iptables Firewall Rules and Hardening

Companion scripts and configs for the StackPractices recipe
[Advanced iptables Firewall Rules and Hardening](https://stackpractices.com/recipes/bash-iptables-firewall-rules/).

## Files

| File | Purpose |
|------|---------|
| `firewall-basic.sh` | Baseline ruleset: default-deny, rate-limited SSH, persisted via `iptables-save` |
| `firewall-ipv6.sh` | Same policy for IPv6 (`ip6tables`), including mandatory ICMPv6 |
| `ddos-mitigation.sh` | `connlimit` caps, new-connection rate limits, SYNPROXY, ICMP throttling |
| `logging-setup.sh` | Rate-limited `LOG` target plus rsyslog routing to `/var/log/iptables.log` |
| `fail2ban/jail.local` | fail2ban jails for sshd, nginx-http-auth, and recidive offenders |
| `nftables.conf` | Equivalent ruleset in nftables (`inet` table, IPv4+IPv6 unified) |
| `knockd.conf` | Port knocking config that opens/closes SSH on a knock sequence |

## Usage

All scripts require root and assume `iptables`/`ip6tables` are installed.

```bash
# Baseline first — apply it while you still have an open SSH session
sudo bash firewall-basic.sh
sudo bash firewall-ipv6.sh

# Optional layers
sudo bash ddos-mitigation.sh
sudo bash logging-setup.sh

# fail2ban
sudo apt install fail2ban
sudo cp fail2ban/jail.local /etc/fail2ban/jail.local
sudo systemctl enable --now fail2ban

# nftables migration (replaces the iptables scripts)
sudo nft -f nftables.conf
sudo systemctl enable --now nftables

# Port knocking
sudo apt install knockd
sudo cp knockd.conf /etc/knockd.conf
sudo systemctl enable --now knockd
```

**Warning:** the default-deny policy takes effect the instant `iptables -P INPUT DROP`
runs. Apply rules with a verified session open, or schedule an `iptables-restore`
of a known-good ruleset as a fallback.
