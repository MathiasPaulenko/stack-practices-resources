#!/usr/bin/env bash
# smoke-test.sh — run after every deploy to verify the system is up.
# Usage: BASE_URL=https://api.example.com ./smoke-test.sh
set -euo pipefail

BASE_URL="${BASE_URL:-https://api.example.com}"

curl -sf "$BASE_URL/health" > /dev/null || exit 1
curl -sf "$BASE_URL/api/status" | jq -e '.db == "up"' > /dev/null || exit 1
echo "Smoke tests passed"
