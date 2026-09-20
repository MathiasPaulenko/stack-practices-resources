#!/usr/bin/env bash
# Flags copyleft / restrictive licenses hiding in the *production*
# dependency tree. Requires: license-checker (npm i -g license-checker).
# For Python projects use: pip-licenses --format=json
set -euo pipefail

DENY='GPL|AGPL|LGPL|SSPL|Commons Clause|CC-BY-SA|EUPL|OSL'

echo "Scanning production dependency licenses..."
if ! license-checker --production --json > /tmp/licenses.json 2>/dev/null; then
  echo "license-checker failed — is it installed? (npm i -g license-checker)" >&2
  exit 1
fi

node -e '
const deps = require("/tmp/licenses.json");
const deny = /GPL|AGPL|LGPL|SSPL|Commons Clause|CC-BY-SA|EUPL|OSL/i;
const hits = Object.entries(deps)
  .filter(([, v]) => deny.test(String(v.licenses)))
  .map(([name, v]) => `${name} -> ${v.licenses}`);
if (hits.length) {
  console.log("RESTRICTIVE LICENSES FOUND:");
  hits.forEach(h => console.log("  " + h));
  process.exit(2);
}
console.log("OK — no copyleft licenses in production dependencies.");
'
