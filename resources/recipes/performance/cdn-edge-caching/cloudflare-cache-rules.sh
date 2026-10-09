#!/usr/bin/env bash
set -euo pipefail

# Creates a Cloudflare zone ruleset with a cache rule for static assets
# (Ruleset Engine — Page Rules are deprecated).
# Requires: ZONE_ID, API_TOKEN env vars.

curl -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/rulesets" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "static-asset-caching",
    "kind": "zone",
    "phase": "http_request_cache_settings",
    "rules": [{
      "expression": "(http.request.uri.path.extension in {\"css\" \"js\" \"png\" \"jpg\" \"woff2\"})",
      "action": "set_cache_settings",
      "action_parameters": {
        "edge_ttl": { "mode": "override_origin", "default": 2592000 },
        "browser_ttl": { "mode": "override_origin", "default": 86400 }
      },
      "enabled": true
    }]
  }'
