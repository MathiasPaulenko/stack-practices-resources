#!/usr/bin/env bash
set -euo pipefail

# Purge cached content on CloudFront, Cloudflare, or Fastly.
# Usage: ./purge.sh <cloudfront|cloudflare|fastly> <target>
# Env: CF_DISTRIBUTION_ID / CF_ZONE_ID + CF_API_TOKEN / FASTLY_SERVICE_ID + FASTLY_API_TOKEN

provider="$1"
target="$2"

case "$provider" in
  cloudfront)
    aws cloudfront create-invalidation \
      --distribution-id "${CF_DISTRIBUTION_ID}" \
      --paths "${target}"
    ;;
  cloudflare)
    curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
      -H "Authorization: Bearer ${CF_API_TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{\"files\": [\"${target}\"]}"
    ;;
  fastly)
    curl -X POST "https://api.fastly.com/service/${FASTLY_SERVICE_ID}/purge/${target}" \
      -H "Fastly-Key: ${FASTLY_API_TOKEN}"
    ;;
  *)
    echo "Unknown provider: $provider" >&2
    exit 1
    ;;
esac
