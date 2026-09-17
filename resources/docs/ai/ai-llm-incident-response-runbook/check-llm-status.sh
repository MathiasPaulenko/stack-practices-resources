#!/usr/bin/env bash
# check-llm-status.sh — quick health check for LLM providers during an incident.
# Polls public status endpoints and tests API connectivity.
# Exit 0 = all reachable, 1 = provider degradation/outage detected.

set -u

fail=0

check_status_page() {
  local name="$1" url="$2"
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url")
  if [ "$code" = "200" ]; then
    echo "OK   $name status page reachable"
  else
    echo "FAIL $name status page returned $code"
    fail=1
  fi
}

check_api() {
  local name="$1" url="$2" key_env="$3"
  local key="${!key_env:-}"
  if [ -z "$key" ]; then
    echo "SKIP $name ($key_env not set)"
    return
  fi
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url" \
    -H "Authorization: Bearer $key")
  if [ "$code" = "200" ] || [ "$code" = "401" ]; then
    # 401 still proves reachability — the service responded
    echo "OK   $name API reachable (HTTP $code)"
  else
    echo "FAIL $name API returned $code"
    fail=1
  fi
}

check_status_page "OpenAI"    "https://status.openai.com/api/v2/status.json"
check_status_page "Anthropic" "https://status.anthropic.com/api/v2/status.json"

check_api "OpenAI"    "https://api.openai.com/v1/models"    OPENAI_API_KEY
check_api "Anthropic" "https://api.anthropic.com/v1/models" ANTHROPIC_API_KEY

exit "$fail"
