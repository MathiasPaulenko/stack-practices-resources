# Endpoint Security Checklist — Companion Files

Assets from the StackPractices template:
[Endpoint Device Security Checklist Template](https://stackpractices.com/docs/endpoint-security-checklist-template/)

## Files

| File | Purpose |
| --- | --- |
| `checklist.md` | Standalone copy-paste version of the 5-category checklist |
| `endpoint-compliance.sql` | osquery fleet-scan queries (encryption, firewall, EDR presence, USB) |
| `ssh-passphrase-audit.sh` | Bash audit for SSH keys without passphrase + credential file permissions |
| `intune-compliance.ps1` | Microsoft Graph PowerShell to pull per-device compliance/encryption state |

## Run

```bash
# osquery fleet scan (works on Linux/macOS/Windows)
osqueryi --json < endpoint-compliance.sql

# SSH key audit
bash ssh-passphrase-audit.sh

# Intune compliance report
pwsh intune-compliance.ps1
```
