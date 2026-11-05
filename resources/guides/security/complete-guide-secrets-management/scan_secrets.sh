#!/usr/bin/env bash
# Scan repo history for leaked secrets (run locally and in CI)
set -euo pipefail
command -v gitleaks >/dev/null || { echo "install gitleaks: https://github.com/gitleaks/gitleaks"; exit 1; }
gitleaks detect --source . --verbose --redact
echo "Reminder: a hit means ROTATE the credential — deleting the line does not remove it from history."
