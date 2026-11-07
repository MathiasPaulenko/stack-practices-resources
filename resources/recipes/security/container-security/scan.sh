#!/usr/bin/env bash
# Local security pipeline: build -> scan -> secrets -> SBOM -> sign -> verify.
# Usage: ./scan.sh myapp:latest
set -euo pipefail

IMAGE="${1:?usage: ./scan.sh <image>}"

echo "==> Scanning $IMAGE for CVEs and secrets (gate: CRITICAL,HIGH with fix)"
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 "$IMAGE"

echo "==> Scanning image layers for committed secrets"
trufflehog docker --image="$IMAGE" --only-verified

echo "==> Generating SBOM (CycloneDX + SPDX)"
syft "$IMAGE" -o cyclonedx-json > sbom.cyclonedx.json
syft "$IMAGE" -o spdx-json > sbom.spdx.json

echo "==> Cross-checking SBOM with Grype"
grype "sbom:sbom.cyclonedx.json" --fail-on high

echo "==> Signing image (keyless OIDC — run inside CI or `cosign sign --key` locally)"
cosign sign --yes "$IMAGE"

echo "==> Attaching SBOM as OCI artifact"
cosign attach sbom --sbom sbom.spdx.json "$IMAGE"

echo "Done. Verify with: cosign verify $IMAGE"
