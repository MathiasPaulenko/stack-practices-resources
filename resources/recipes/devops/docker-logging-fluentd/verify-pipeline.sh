#!/usr/bin/env bash
# Verifies the Fluentd -> Elasticsearch pipeline end to end.
set -euo pipefail

echo "1. Fluentd is listening:"
docker logs fluentd 2>&1 | tail -5

echo ""
echo "2. Sending a test event through the Forward protocol:"
echo '{"key":"value"}' | fluent-cat docker.test -h localhost -p 24224 || \
    echo "fluent-cat not installed: gem install fluentd (or send from a container)"

echo ""
echo "3. Daily index exists and is growing:"
curl -s "localhost:9200/_cat/indices?v" | grep docker-logs || \
    echo "No docker-logs index yet"

echo ""
echo "4. Sample documents that landed:"
curl -s "localhost:9200/docker-logs-*/_search?q=service:api&size=3" | head -40
