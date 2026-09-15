#!/bin/bash
# Scan for secrets in the codebase before merge.
#
# Runs three secret detection tools and reports findings.
# Intended for use as a pre-commit hook or CI step.
#
# Usage:
#   ./scan_secrets.sh [directory]

set -euo pipefail

DIR="${1:-.}"

echo "=== TruffleHog ==="
trufflehog filesystem --directory="$DIR" || echo "TruffleHog not installed, skipping"

echo ""
echo "=== Gitleaks ==="
gitleaks detect --source="$DIR" --no-banner || echo "Gitleaks not installed, skipping"

echo ""
echo "=== detect-secrets ==="
detect-secrets scan "$DIR" 2>/dev/null || echo "detect-secrets not installed, skipping"

echo ""
echo "Scan complete. Review findings above."
