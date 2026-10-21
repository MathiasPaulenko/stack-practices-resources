#!/usr/bin/env bash
# CI compatibility check for Confluent Schema Registry.
# Fails the build if a candidate schema is not compatible with the latest
# registered version of a subject.
#
# Usage: ./schema-compatibility-check.sh <schema-file> <subject> [registry-url]
# Example: ./schema-compatibility-check.sh order-created-v2.avsc prod.orders.order-created.v1-value

set -euo pipefail

SCHEMA_FILE="${1:?Usage: $0 <schema-file> <subject> [registry-url]}"
SUBJECT="${2:?Usage: $0 <schema-file> <subject> [registry-url]}"
REGISTRY="${3:-http://schema-registry:8081}"

if [[ ! -f "$SCHEMA_FILE" ]]; then
  echo "Schema file not found: $SCHEMA_FILE" >&2
  exit 2
fi

# Escape the schema into a single JSON string for the request payload
SCHEMA_JSON=$(python3 -c "import json,sys; print(json.dumps(open(sys.argv[1]).read()))" "$SCHEMA_FILE")

RESPONSE=$(curl -sf -X POST \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data "{\"schema\": $SCHEMA_JSON}" \
  "$REGISTRY/compatibility/subjects/$SUBJECT/versions/latest")

COMPATIBLE=$(echo "$RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('is_compatible'))")

if [[ "$COMPATIBLE" == "True" ]]; then
  echo "PASS: $SCHEMA_FILE is compatible with $SUBJECT"
  exit 0
else
  echo "FAIL: $SCHEMA_FILE is NOT compatible with $SUBJECT" >&2
  echo "Registry response: $RESPONSE" >&2
  echo "Follow the breaking change procedure: new versioned topic, dual-write, migrate consumers." >&2
  exit 1
fi
