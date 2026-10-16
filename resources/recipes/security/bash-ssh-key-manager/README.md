# SSH Key Management in Bash — Companion Resources

Runnable scripts for the [SSH Key Management in Bash](https://stackpractices.com/recipes/bash-ssh-key-manager/) recipe on StackPractices.

## Files

| File | Purpose |
| --- | --- |
| `generate-key.sh` | Generate an ed25519 key with sane `~/.ssh` permissions. |
| `distribute-key.sh` | Push a public key to a list of servers (`ssh-copy-id` with manual fallback). |
| `rotate-key-verified.sh` | Fleet-wide rotation that installs the new key, verifies login, then removes the old one. Safe to rerun. |
| `audit-keys-fleet.sh` | Audit `authorized_keys` across servers into a CSV report and flag weak keys (DSA, ECDSA, RSA < 4096). |
| `ssh-agent-ci.sh` | Non-interactive `ssh-agent` setup for CI runners; loads a base64-encoded key from `SSH_KEY`. |
| `sshd-hardening.sh` | Disable password authentication in `sshd_config` (validates config with `sshd -t` before restart). |
| `ssh-key-manager.py` | Python wrapper around `ssh-keygen` for inventory and weak-key audits. |

## Usage

```bash
./generate-key.sh id_ed25519
./distribute-key.sh servers.txt
./rotate-key-verified.sh servers.txt
./audit-keys-fleet.sh web-01 web-02 db-01
python ssh-key-manager.py
```

`servers.txt` holds one `user@host` per line; `#` comments and blank lines are skipped.

Test on a disposable VM first — these scripts modify `~/.ssh` and remote `authorized_keys` files.
