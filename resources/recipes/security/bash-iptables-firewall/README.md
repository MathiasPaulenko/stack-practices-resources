# Configure iptables Firewall Rules with Bash

Companion scripts for the [iptables firewall recipe](https://stackpractices.com/recipes/bash-iptables-firewall/) on StackPractices.

Each `.sh` file is self-contained: adjust the variables at the top and run as root (or via sudo). Scripts use `set -euo pipefail` and order allow-rules before drop policies so a line-by-line paste over SSH can't lock you out.

## Prerequisites

- Linux with iptables (or `iptables-nft` on nftables-based distros)
- Root privileges (`sudo` or a root shell)
- Debian/Ubuntu: `iptables-persistent` for `persist-rules.sh`; RHEL/Fedora: `iptables-services`
- **Always** keep a second SSH session open while testing — a wrong rule can cut your own access

## Scripts

| File | What it does |
| --- | --- |
| `basic-firewall-setup.sh` | Baseline ruleset: loopback, ESTABLISHED, INVALID drop, SSH/HTTP/HTTPS, then DROP policies |
| `ssh-rate-limit.sh` | Replaces the plain SSH ACCEPT with `-m recent` rate limiting (max 3 new/min) |
| `nat-port-forwarding.sh` | DNAT port forward + MASQUERADE/SNAT + bidirectional FORWARD |
| `block-ip-addresses.sh` | Inserts DROP rules for a list of IPs (before the port allows) |
| `allow-subnet-only.sh` | Restricts SSH to one subnet |
| `persist-rules.sh` | `iptables-persistent`/`netfilter-persistent` + systemd unit restoring v4 and v6 |
| `firewall-reset.sh` | Flushes all rules and restores ACCEPT policies |
| `list-verify-rules.sh` | Dumps filter/nat/mangle tables with counters and line numbers |

## License

MIT — same as the StackPractices resources repository.
