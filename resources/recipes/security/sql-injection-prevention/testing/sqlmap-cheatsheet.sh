#!/usr/bin/env bash
# sqlmap quick reference — only ever point this at environments you own.
# https://sqlmap.org/

# Single GET endpoint
sqlmap -u "https://staging.example.com/api/users?id=1" \
  --batch --level=3 --risk=2 \
  --output-dir=/tmp/sqlmap-results

# Authenticated request
sqlmap -u "https://staging.example.com/api/users?id=1" \
  --cookie="session=$SESSION_TOKEN" \
  --batch --level=5

# POST parameters
sqlmap -u "https://staging.example.com/api/login" \
  --data="email=test@example.com&password=test" \
  --batch --level=3
