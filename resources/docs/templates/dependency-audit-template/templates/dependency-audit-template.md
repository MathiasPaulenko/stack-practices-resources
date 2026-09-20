# Dependency Audit: [Library Name]

## Overview
| Field | Value |
|-------|-------|
| **Library** | [name] v[x.y.z] |
| **Purpose** | [what problem it solves] |
| **Replaces** | [internal code / another library] |
| **Auditor** | [name] |
| **Date** | [YYYY-MM-DD] |

## Security

| Check | Result | Evidence |
|-------|--------|----------|
| Known CVEs | [none / list] | Snyk / OSV report link |
| SAST available | [yes / no] | Link to security audit |
| Bug bounty program | [yes / no] | Link |
| Release signing | [yes / no] | GPG / Sigstore verification |

## Maintenance Health

| Metric | Value | Threshold |
|--------|-------|-----------|
| Last release | [date] | < 12 months |
| Open issues | [count] | < 500 |
| Open PRs | [count] | < 100 |
| Contributors | [count] | > 2 (bus factor) |
| License | [SPDX identifier] | [approved list] |

## Supply Chain Risk

| Check | Result |
|-------|--------|
| Download count | [npm / PyPI stats] |
| Corporate backing | [yes / no — who] |
| Transitive dependencies | [count] |
| Native code / compiled binaries | [yes / no] |

## Decision

| Outcome | Conditions |
|---------|-----------|
| **Approved** | All checks pass |
| **Approved with monitoring** | Minor risks, track quarterly |
| **Rejected** | Critical risk, find alternative |
