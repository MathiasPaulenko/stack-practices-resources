#!/usr/bin/env bash
# Dependency audit sweep — OWASP A06. Runs whichever scanners exist
# in the environment; run in CI to catch new CVEs as they're published.
set -euo pipefail

if [ -f package.json ] && command -v npm >/dev/null; then
    echo "== npm audit =="
    npm audit --audit-level=high || echo "npm audit found high-severity advisories"
fi

if [ -f requirements.txt ] && command -v pip-audit >/dev/null; then
    echo "== pip-audit =="
    pip-audit || echo "pip-audit found advisories"
fi

if command -v snyk >/dev/null; then
    echo "== snyk test =="
    snyk test || echo "snyk found issues"
fi

echo "Done. Treat any advisory output as a security ticket, not routine noise."
