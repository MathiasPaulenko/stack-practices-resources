# CI/CD Pipeline Security Controls — `<Project Name>`

## 1. Source Control Security

| Control | Requirement | Verification |
|---------|-------------|--------------|
| Branch protection | Required reviews before merge to main | Repository settings |
| Signed commits | Require verified commits for privileged accounts | Git configuration |
| Access control | Least-privilege access to repositories | RBAC review |
| Audit logging | All pushes, merges, and permission changes logged | Platform logs |
| Dependency pinning | Lockfiles and pinned versions for reproducible builds | Repository files |
| Secret scanning | Automated detection of secrets in commits | Pre-commit hooks + CI |

## 2. Pipeline Configuration

| Control | Requirement | Verification |
|---------|-------------|--------------|
| Immutable pipeline definitions | Pipelines stored as code and reviewed | Repository files |
| No secrets in code | Secrets loaded from vault, CI variables, or OIDC | Secret scanning |
| Input validation | Pipeline parameters validated and sanitized | Code review |
| Self-hosted runner isolation | Production runners isolated from dev runners | Runner configuration |
| Ephemeral runners | Fresh runner per build to reduce persistence | Runner settings |
| Pipeline provenance | SLSA provenance generated for artifacts | Attestation tool |

## 3. Secrets Management

| Secret Type | Storage | Rotation | Scope |
|-------------|---------|----------|-------|
| Cloud credentials | External vault or OIDC | 90 days | Per environment |
| Container registry tokens | Vault or short-lived CI tokens | 90 days | Per pipeline |
| Signing keys | Hardware-backed or KMS | 180 days | Limited service accounts |
| API keys | Vault or secret manager | 90 days | Minimum required permissions |
| Database passwords | Vault dynamic secrets | 24 hours | Per pipeline run |

## 4. Build Security

| Control | Requirement | Verification |
|---------|-------------|--------------|
| Dependency scanning | All dependencies scanned for known CVEs | Scanner in CI |
| Static analysis | SAST run on every pull request | CI job |
| Container image scanning | Base image and layers scanned before push | Registry scan |
| Reproducible builds | Same source produces same artifact | Build verification |
| Artifact signing | All artifacts signed with build identity | Signature verification |
| SBOM generation | Bill of materials generated per build | CI output |

## 5. Deployment Security

| Control | Requirement | Verification |
|---------|-------------|--------------|
| Deployment gates | Manual or automated approval before production | Pipeline rules |
| Environment separation | Production credentials not available in dev | Secret scoping |
| Rollback plan | Automated rollback trigger on failure | Pipeline definition |
| Immutable deployments | Artifacts deployed by reference, not rebuilt | Deployment logs |
| Drift detection | Unauthorized production changes detected | Monitoring tool |
| Audit trail | Who deployed what, when, and why | Deployment logs |

## 6. Incident Response

| Scenario | Response | Owner |
|----------|----------|-------|
| Secret leaked | Rotate secret, revoke tokens, audit usage | Security team |
| Malicious commit | Revert, investigate, revoke credentials | Platform team |
| Compromised runner | Terminate runner, rebuild, review logs | Platform team |
| Unauthorized deployment | Rollback, freeze pipeline, audit | Release manager |
| Tampered artifact | Block deployment, trace provenance | Security team |
