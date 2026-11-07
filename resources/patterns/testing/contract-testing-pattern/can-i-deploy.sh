#!/usr/bin/env bash
# Deploy gate: asks the broker whether this version is compatible with
# every contract it participates in. Run before deploying to production.
# Usage: GIT_SHA=$(git rev-parse HEAD) ./can-i-deploy.sh order-service production
set -euo pipefail

PARTICIPANT="${1:?participant name required, e.g. order-service}"
ENVIRONMENT="${2:-production}"
GIT_SHA="${GIT_SHA:?set GIT_SHA to the commit being deployed}"

npx pact-broker can-i-deploy \
  --broker-base-url "$PACT_BROKER_URL" \
  --broker-token "$PACT_BROKER_TOKEN" \
  --participant "$PARTICIPANT" \
  --version "$GIT_SHA" \
  --to-environment "$ENVIRONMENT"

# Exit 0: safe to deploy — all contracts satisfied
# Exit 1: unsafe — a consumer contract is broken
