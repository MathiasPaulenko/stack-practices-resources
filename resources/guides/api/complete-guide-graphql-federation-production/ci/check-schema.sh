#!/usr/bin/env bash
# CI step: check a subgraph schema for breaking changes before publish.
# Note: --routing-url is a `subgraph publish` flag, not valid for `check`.
set -euo pipefail

rover subgraph check my-graph@production \
  --name "${SUBGRAPH_NAME:?set SUBGRAPH_NAME}" \
  --schema "${SCHEMA_PATH:?set SCHEMA_PATH}"

# On merge, publish the schema (routing-url required on first publish):
# rover subgraph publish my-graph@production \
#   --name "$SUBGRAPH_NAME" \
#   --schema "$SCHEMA_PATH" \
#   --routing-url "http://${SUBGRAPH_NAME}-service:4001/graphql"
