# CI/CD Pipeline Security Template Resources

Companion resources for [CI/CD Pipeline Security Template](https://stackpractices.com/docs/ci-cd-pipeline-security-template/).

## Files

| File | Description |
|------|-------------|
| `pipeline/security-controls-template.md` | Six control tables covering source control, pipeline config, secrets management, build, deployment, and incident response — each mapped to a verification method |
| `ci/secure-pipeline.yml` | Hardened GitHub Actions workflow: minimal job permissions, OIDC for cloud auth (no static keys), cosign artifact signing, SBOM generation, CodeQL scanning |
| `ci/slsa-provenance.json` | Example SLSA provenance statement in in-toto format showing how build attestation is structured |
| `audit/pipeline-audit-checklist.md` | Ten-item audit checklist for periodic pipeline security reviews |

## Usage

1. Copy `pipeline/security-controls-template.md` and fill in your platform, owners, and verification evidence.
2. Copy `ci/secure-pipeline.yml` to `.github/workflows/` and adjust the role ARN, region, and build steps.
3. Use `audit/pipeline-audit-checklist.md` quarterly — each row maps to a control in the template.
