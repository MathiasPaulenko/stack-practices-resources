# Container Security — runnable artifacts

Companion resources for [Container Security: Scan, Harden, and Sign Docker Images](https://stackpractices.com/recipes/container-security/).

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Hardened multi-stage build — distroless runtime, non-root uid 65532 |
| `Dockerfile.alpine` | Alternative that keeps a shell (`dumb-init` + created user) |
| `security-scan.yml` | GitHub Actions gate: Trivy scan, SARIF upload, SBOM artifact, weekly rescan |
| `.gitlab-ci.yml` | GitLab CI equivalent |
| `trivy.yaml` | Scanner config — severity gate, ignore-unfixed, skip dirs |
| `.trivyignore` | Reviewed-CVE exceptions with justification template |
| `k8s-deployment.yaml` | Locked-down pod securityContext (read-only root, no caps, seccomp) |
| `kyverno-policy.yaml` | Admission control — only Cosign-signed images may run |
| `scan.sh` | Local pipeline: build → Trivy → TruffleHog → Syft → Grype → Cosign |

## Quick start

```bash
# Scan a local image (gate on fixable HIGH/CRITICAL)
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 myapp:latest

# Full local pipeline
chmod +x scan.sh && ./scan.sh myapp:latest

# Deploy with the hardened context (replace the digest first)
kubectl apply -f k8s-deployment.yaml
```

Requires: Docker, Trivy, Syft, Grype, Cosign, TruffleHog.
