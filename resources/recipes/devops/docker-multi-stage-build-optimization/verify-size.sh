#!/usr/bin/env bash
# Builds the Go images single- and multi-stage, then compares sizes.
set -euo pipefail

echo "==> Building multi-stage Go image (scratch runtime)"
docker build -f Dockerfile.go -t msdemo:scratch .

echo "==> Sizes"
docker images --format "{{.Repository}}:{{.Tag}}\t{{.Size}}" | grep msdemo

echo "==> Layer breakdown"
docker history msdemo:scratch --no-trunc --format "{{.Size}}\t{{.CreatedBy}}"

echo "==> Try: dive msdemo:scratch for an interactive per-layer view"
