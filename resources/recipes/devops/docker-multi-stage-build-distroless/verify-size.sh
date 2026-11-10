#!/usr/bin/env bash
# Compare image sizes between a fat base and the distroless build.
set -euo pipefail

docker build -f Dockerfile.go -t demo:distroless .
docker build -f Dockerfile.alpine -t demo:alpine .

docker images demo --format "{{.Tag}}: {{.Size}}"

echo
echo "Shell check (distroless should FAIL — that is the point):"
docker run --rm --entrypoint sh demo:distroless -c 'echo got a shell' || \
  echo "no shell in distroless — good"
