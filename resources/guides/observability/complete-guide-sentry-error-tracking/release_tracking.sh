#!/usr/bin/env bash
# release_tracking.sh — Sentry release tracking and source map upload.
#
# Usage:
#   SENTRY_AUTH_TOKEN=your_token ./release_tracking.sh
#
# Requires: sentry-cli installed (npm install -g @sentry/cli)

set -euo pipefail

RELEASE="order-service@1.2.3"
ORG="your-org"
PROJECT="order-service"

echo "Creating Sentry release: ${RELEASE}"
sentry-cli releases new "${RELEASE}"

echo "Associating commits with the release"
sentry-cli releases set-commits "${RELEASE}" --auto

echo "Uploading source maps"
sentry-cli releases files "${RELEASE}" upload-sourcemaps ./dist \
    --url-prefix "~/static/js"

echo "Finalizing the release"
sentry-cli releases finalize "${RELEASE}"

echo "Marking deployment"
sentry-cli releases deploys "${RELEASE}" new \
    --env production \
    --url "https://order-service.example.com"

echo "Release ${RELEASE} deployed successfully."
