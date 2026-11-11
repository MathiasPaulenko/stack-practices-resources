# Git Branching Strategy: `<Project/Team Name>`

> Version: ______ | Last updated: ______ | Owner: ______

---

## 1. Branch Types

### Main Branches

| Branch | Purpose | Protection | Lifespan |
|--------|---------|------------|----------|
| `main` | Production-ready code | Requires PR + 2 approvals + CI pass | Permanent |
| `staging` | Pre-production validation | Requires PR + 1 approval + CI pass | Permanent |
| `develop` | Integration branch for features | Requires PR + 1 approval + CI pass | Permanent |

### Supporting Branches

| Prefix | Purpose | Source | Merge Target | Naming |
|--------|---------|--------|--------------|--------|
| `feature/` | New functionality | `develop` | `develop` | `feature/TICKET-short-description` |
| `bugfix/` | Non-urgent fixes | `develop` | `develop` | `bugfix/TICKET-short-description` |
| `hotfix/` | Production-critical fixes | `main` | `main` + `develop` | `hotfix/TICKET-short-description` |
| `release/` | Release preparation | `develop` | `main` + `staging` | `release/v1.2.3` |
| `chore/` | Maintenance, dependencies | `develop` | `develop` | `chore/TICKET-short-description` |
| `docs/` | Documentation only | `develop` | `develop` | `docs/TICKET-short-description` |

---

## 2. Workflow

### Feature Development

```bash
git checkout develop
git pull origin develop

## 2. Create feature branch
git checkout -b feature/PROJ-123-add-user-auth

## 3. Work and commit locally
git commit -m "feat: add OAuth2 login endpoint"
git commit -m "test: add auth integration tests"

## 4. Push and open PR when ready
git push origin feature/PROJ-123-add-user-auth
## Open PR to develop, fill out template

## 5. After approval and CI green, merge
git checkout develop
git merge --no-ff feature/PROJ-123-add-user-auth
## Or use squash merge via GitHub/GitLab UI
```

### Hotfix Workflow

```bash
## 1. Start from main
git checkout main
git pull origin main

## 2. Create hotfix branch
git checkout -b hotfix/PROJ-456-fix-payment-webhook

## 3. Fix, test, commit
git commit -m "fix: validate webhook signature before processing"

## 4. Open PR to main (expedited review)
git push origin hotfix/PROJ-456-fix-payment-webhook
## Request emergency review; target: main

## 5. After merge to main, backport to develop
git checkout develop
git cherry-pick <hotfix-commit>
## Or merge main into develop
```

### Release Workflow

```bash
## 1. Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.3

## 2. Version bump, update changelog, final QA
git commit -m "chore: bump version to 1.2.3"

## 3. Merge to staging for final validation
git checkout staging
git merge --no-ff release/v1.2.3

## 4. After staging validation, merge to main
git checkout main
git merge --no-ff release/v1.2.3

## 5. Tag the release
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3

## 6. Merge back to develop to capture release commits
git checkout develop
git merge --no-ff main
```

---

## 3. Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Use For | Triggers Release |
|------|---------|----------------|
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `docs` | Documentation only | None |
| `style` | Formatting, missing semicolons | None |
| `refactor` | Code change without behavior change | None |
| `perf` | Performance improvement | Patch |
| `test` | Adding or correcting tests | None |
| `chore` | Build process, dependencies | None |
| `ci` | CI/CD changes | None |
| `revert` | Reverting previous commit | Patch |

### Examples

```
feat(auth): add Google OAuth2 login

Implements OAuth2 flow with PKCE for web clients.
Closes PROJ-123

fix(payments): validate webhook signature

Prevents replay attacks by verifying Stripe signature
header before processing events.

Closes PROJ-456
```

---

## 4. Merge Requirements

### Pull Request Requirements

| Requirement | Feature/Bugfix | Hotfix | Release |
|-------------|---------------|--------|---------|
| CI passes | Required | Required | Required |
| Review approvals | 2 | 1 (expedited) | 2 |
| Linked ticket | Required | Required | Required |
| Tests added | Required | Required | N/A |
| Documentation updated | If feature changes | If behavior changes | Changelog updated |
| Security review | If auth/data changes | Required | N/A |

### Merge Strategies

| Target Branch | Strategy | Rationale |
|---------------|----------|-----------|
| `develop` | Squash and merge | Clean history; one commit per feature |
| `main` | Merge commit | Preserves release branch history |
| `hotfix` to `main` | Merge commit | Preserves hotfix identification |

---

## 5. Tagging and Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking API changes
- **MINOR**: New capabilities, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Tag Format

```bash
## Production releases
git tag -a v1.2.3 -m "Release v1.2.3"

## Pre-releases
git tag -a v1.2.3-rc.1 -m "Release candidate 1"

## Hotfixes
git tag -a v1.2.4 -m "Hotfix: fix payment webhook validation"
```

### Version Bump Rules

| Commit Type | Version Bump |
|-------------|-------------|
| `feat` | Minor (x.Y.z) |
| `fix`, `perf`, `revert` | Patch (x.y.Z) |
| `feat` with `BREAKING CHANGE` | Major (X.y.z) |
| `docs`, `style`, `refactor`, `test`, `chore`, `ci` | None |

---

## 6. Rollback Procedures

### Rolling Back a Deployment

Prefer `git revert` when the bad release is already on main — it adds a new commit instead of moving history. Checking out an older tag works for redeploying a known-good build, but it leaves HEAD detached.

```bash
## Identify last known good tag
git log --oneline --decorate --tags

## Revert to previous tag
git checkout v1.2.2

## Create hotfix branch for rollback
git checkout -b hotfix/rollback-v1.2.3

## Deploy rollback
git push origin hotfix/rollback-v1.2.3
## Open emergency PR to main
```

### Reverting a Merge

```bash
## Find the merge commit
git log --oneline --merges

## Revert the merge (creates new revert commit)
git revert -m 1 <merge-commit-hash>

## Open PR with revert commit
```

---

## 7. Protection Rules

### Branch Protection (GitHub/GitLab)

| Rule | main | staging | develop |
|------|--------|---------|---------|
| Require PR | Yes | Yes | Yes |
| Required approvals | 2 | 1 | 1 |
| Dismiss stale approvals | Yes | Yes | No |
| Require status checks | Yes | Yes | Yes |
| Include administrators | Yes | Yes | No |
| Require linear history | No | No | Yes |
| Allow force push | No | No | No |
| Allow deletions | No | No | No |