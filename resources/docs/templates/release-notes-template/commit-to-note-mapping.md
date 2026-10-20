# Conventional Commit → Release Note Mapping

Quick reference for turning commit prefixes into release note entries.
Include anything a user can see or must act on; leave internal work in the changelog.

| Commit prefix | Section | Include? | Example entry |
|---------------|---------|----------|---------------|
| `feat:` | New Capabilities | Yes | **Capability name** — what it does and where to find it |
| `fix:` | Bug Fixes | Yes | **#issue** — symptom the user experienced |
| `feat!:` / `BREAKING CHANGE:` | Breaking Changes | Yes, first | **Change/Impact/Migration** — exact adaptation steps |
| `fix(security):` / CVE | Security | Yes | **CVE-YYYY-NNNN** — severity and fix summary |
| `perf:` | Improvements | Yes, if measurable | **Area** — from X to Y (metric) |
| `deprecate:` / deprecation PRs | Deprecations | Yes | **Capability** — removal version and replacement |
| `chore:` / `ci:` / `build:` | — | No (internal) | — |
| `refactor:` | — | No (internal) | — |
| `docs:` | — | No, unless user-facing docs shipped | — |
| `style:` / `test:` | — | No (internal) | — |

## Triage rule

Tag each merged PR title as **user-facing**, **internal**, or **needs migration**.
If the title doesn't tell you which, it's probably internal — or the title itself
needs a rewrite before the next release.
