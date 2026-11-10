#!/bin/bash
# healthcheck.sh — Simple HTTP probe. Exit 0 = healthy, exit 1 = unhealthy.
set -e

response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$response" = "200" ]; then
    exit 0
else
    echo "Health check failed: HTTP $response"
    exit 1
fi
