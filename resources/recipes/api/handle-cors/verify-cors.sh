#!/usr/bin/env bash
# Verify CORS behavior of a running API with curl.
# Usage: bash verify-cors.sh http://localhost:5000
set -euo pipefail

BASE="${1:-http://localhost:5000}"
ALLOWED="https://app.example.com"
DENIED="https://evil.example.com"

echo "== 1. Simple request with an allowed origin =="
curl -si "$BASE/api/users" -H "Origin: $ALLOWED" | grep -iE "^HTTP|access-control|vary"

echo
echo "== 2. Preflight with an allowed origin =="
curl -si -X OPTIONS "$BASE/api/users" \
    -H "Origin: $ALLOWED" \
    -H "Access-Control-Request-Method: PUT" \
    -H "Access-Control-Request-Headers: Content-Type,Authorization" \
    | grep -iE "^HTTP|access-control|vary"

echo
echo "== 3. Request from a disallowed origin (expect NO Access-Control-Allow-Origin) =="
curl -si "$BASE/api/users" -H "Origin: $DENIED" | grep -iE "^HTTP|access-control|vary" \
    || echo "OK: no CORS headers returned for a disallowed origin"
