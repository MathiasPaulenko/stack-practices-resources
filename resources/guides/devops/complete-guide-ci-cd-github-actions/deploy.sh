#!/usr/bin/env bash
# Placeholder deploy script used by the ci.yml workflow.
# Replace the body with your real deployment: rsync, kubectl, cloud CLI, etc.
set -euo pipefail

ENV="${1:-staging}"

case "$ENV" in
  staging|production)
    echo "Deploying to $ENV..."
    # rsync -avz dist/ "deploy@$ENV.example.com:/var/www/app/"
    # kubectl set image deployment/app "app=ghcr.io/org/app:${GITHUB_SHA}"
    ;;
  *)
    echo "Unknown environment: $ENV" >&2
    exit 1
    ;;
esac

echo "Deploy to $ENV finished."
