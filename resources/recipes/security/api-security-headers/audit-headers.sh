#!/bin/bash
# audit-headers.sh — Check security headers on a URL
# Usage: ./audit-headers.sh https://example.com

URL="${1:-https://example.com}"
REQUIRED_HEADERS=(
  "strict-transport-security"
  "content-security-policy"
  "x-content-type-options"
  "x-frame-options"
  "referrer-policy"
  "permissions-policy"
  "cross-origin-opener-policy"
  "cross-origin-resource-policy"
)

echo "Auditing: $URL"
echo "-----------------------------------"

HEADERS=$(curl -sI "$URL")

for header in "${REQUIRED_HEADERS[@]}"; do
  VALUE=$(echo "$HEADERS" | grep -i "^$header:" | sed 's/^[^:]*: *//')
  if [ -z "$VALUE" ]; then
    echo "MISSING: $header"
  else
    echo "OK: $header = $VALUE"
  fi
done

# Check for weak CSP
CSP=$(echo "$HEADERS" | grep -i "^content-security-policy:" | sed 's/^[^:]*: *//')
if echo "$CSP" | grep -q "unsafe-inline"; then
  echo "WARNING: CSP contains 'unsafe-inline'"
fi
if echo "$CSP" | grep -q "unsafe-eval"; then
  echo "WARNING: CSP contains 'unsafe-eval'"
fi

# Check HSTS max-age
HSTS=$(echo "$HEADERS" | grep -i "^strict-transport-security:" | sed 's/^[^:]*: *//')
if echo "$HSTS" | grep -q "max-age=0"; then
  echo "WARNING: HSTS max-age is 0 (disabled)"
fi
