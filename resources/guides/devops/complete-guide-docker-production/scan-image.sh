#!/usr/bin/env bash
# scan-image.sh — build + Trivy gate for CI
set -euo pipefail
IMAGE="${1:?usage: scan-image.sh <image:tag>}"
docker build -t "$IMAGE" .
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 "$IMAGE"
