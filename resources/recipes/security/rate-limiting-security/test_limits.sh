#!/usr/bin/env bash
# Burst-test a rate-limited endpoint: expects 2xx/401 then 429 responses.
# Usage: ./test_limits.sh https://api.example.com/api/auth/login

URL="${1:?Usage: $0 <endpoint-url>}"
COUNT="${2:-10}"

for i in $(seq 1 "$COUNT"); do
  curl -s -o /dev/null -w "attempt $i: %{http_code}\n" \
    -X POST "$URL" \
    -H "Content-Type: application/json" \
    -d '{"email":"a@b.c","password":"x"}'
done

echo "Expected: a few 200/401, then 429 responses with Retry-After header."
