# OWASP Top 10 2025 - Remediation Checklist

Printable/copyable remediation checks per category, ordered by priority (P0 first). Full context and code examples: https://stackpractices.com/docs/owasp-top-10-remediation-checklist/

## 1. A01:2025 — Broken Access Control

| Status | Check | Priority |
|---|---|---|
| ☐ | Enforce deny-by-default authorization on every route, not just the sensitive ones | P0 |
| ☐ | Verify resource ownership server-side before read/write/delete (IDOR check) | P0 |
| ☐ | Re-check authorization on every request — never trust a role cached client-side | P0 |
| ☐ | Use unguessable identifiers (UUIDs) for resources exposed in URLs | P1 |
| ☐ | Invalidate sessions on logout and on idle timeout | P1 |
| ☐ | Apply rate limiting per user and per IP on sensitive endpoints | P1 |
| ☐ | Disable directory listing and public file indexes | P1 |
| ☐ | Validate redirect targets against an allowlist | P1 |
| ☐ | For SSRF: allowlist outbound domains, block internal IP ranges and `file://`/`gopher://` schemes | P0 |
| ☐ | For SSRF: disable redirect following on outbound server-side requests | P1 |
| ☐ | Log every access-denied event with user, resource, and reason | P2 |

## 2. A02:2025 — Security Misconfiguration

| Status | Check | Priority |
|---|---|---|
| ☐ | Remove or rotate every default credential (databases, admin panels, message brokers) | P0 |
| ☐ | Turn off debug mode and stack-trace error pages in production | P0 |
| ☐ | Close cloud storage to the public (S3 buckets, blobs) and scope IAM to least privilege | P0 |
| ☐ | Send the security headers below on every response | P1 |
| ☐ | Remove unused endpoints, dead code paths, and dependencies from the deploy artifact | P1 |
| ☐ | Pin CORS to explicit origins — never `*` with credentials | P1 |
| ☐ | Separate configuration per environment; prod secrets never reach dev/staging | P1 |
| ☐ | Schedule automated config scans (Prowler, Scout Suite, Trivy) and review output weekly | P2 |
| ☐ | Document every intentional deviation from hardening baselines | P2 |

## 3. A03:2025 — Software Supply Chain Failures

| Status | Check | Priority |
|---|---|---|
| ☐ | Generate an SBOM for every release artifact (CycloneDX or SPDX) | P1 |
| ☐ | Scan dependencies in CI on every PR; block merges on critical CVEs | P0 |
| ☐ | Pin versions exactly — no floating ranges on production dependencies | P0 |
| ☐ | Verify package provenance: lockfiles committed, checksums or signatures checked | P1 |
| ☐ | Restrict which registries builds can pull from; proxy public registries internally | P1 |
| ☐ | Protect the pipeline: signed commits or protected branches, secrets out of CI logs | P1 |
| ☐ | Remove unused dependencies — every package you don't need is attack surface | P1 |
| ☐ | Track end-of-life dates of frameworks and plan upgrades before they lapse | P2 |
| ☐ | Subscribe to advisories for your critical stack (GitHub advisories, vendor lists) | P2 |
| ☐ | Review transitive dependencies on major version bumps | P2 |

## 4. A04:2025 — Cryptographic Failures

| Status | Check | Priority |
|---|---|---|
| ☐ | Enforce TLS 1.2+ everywhere; disable SSLv3, TLS 1.0, and 1.1 | P0 |
| ☐ | Encrypt sensitive data at rest (AES-256-GCM or provider-managed equivalents) | P0 |
| ☐ | Hash passwords with Argon2id or bcrypt — never fast hashes like SHA-256 alone | P0 |
| ☐ | Move every secret out of source code into a secrets manager | P0 |
| ☐ | Rotate keys on a schedule and after any suspected exposure | P1 |
| ☐ | Classify data so you know what actually needs encryption (don't encrypt everything blindly) | P1 |
| ☐ | Enable HSTS with preload on public properties | P1 |
| ☐ | Avoid inventing crypto — use audited libraries and their recommended parameters | P1 |
| ☐ | Audit where randomness is used; security tokens need a CSPRNG | P1 |
| ☐ | Plan key custody: who can decrypt, and how that's logged | P2 |

## 5. A05:2025 — Injection

| Status | Check | Priority |
|---|---|---|
| ☐ | Parameterize every database query — zero string-built SQL anywhere | P0 |
| ☐ | Audit ORM usage for raw-escape hatches (`raw()`, `extra()`, template queries) | P0 |
| ☐ | Run subprocesses with `shell=False` and argument arrays, never interpolated strings | P0 |
| ☐ | Validate input against allowlists (type, length, format) at the trust boundary | P1 |
| ☐ | Escape output for its context — HTML, JS, URL, and CSS contexts differ | P1 |
| ☐ | Limit query results (`LIMIT`/`OFFSET`) so a successful injection can't dump the table | P1 |
| ☐ | Give database users minimum privileges; the web app shouldn't be able to `DROP` | P1 |
| ☐ | Alert on SQL syntax errors reaching production logs — they're probe signatures | P2 |
| ☐ | Add the injection payloads from your pentest report as regression tests | P2 |

## 6. A06:2025 — Insecure Design

| Status | Check | Priority |
|---|---|---|
| ☐ | Threat-model anything that moves money, data, or permissions before building it | P1 |
| ☐ | Write abuse cases alongside user stories (how would an attacker use this?) | P1 |
| ☐ | Rate-limit every action that costs money or resources — signup, reset, search, export | P0 |
| ☐ | Separate tenant data architecturally, not just by a `WHERE` clause | P1 |
| ☐ | Design state-changing flows to require step-up verification for sensitive steps | P1 |
| ☐ | Fail closed: when a check can't run, deny rather than allow | P0 |
| ☐ | Cap recoverable operations — unlimited password-reset attempts is a design bug | P1 |
| ☐ | Log business events, not just technical ones (who transferred what, when) | P2 |
| ☐ | Review designs for data minimization — you can't leak what you never collected | P2 |

## 7. A07:2025 — Authentication Failures

| Status | Check | Priority |
|---|---|---|
| ☐ | Offer MFA everywhere, require it for admins and sensitive actions | P0 |
| ☐ | Check passwords against breach lists at signup and reset (e.g., HaveIBeenPwned-style) | P1 |
| ☐ | Rate-limit login and recovery endpoints; add progressive delays or lockout | P0 |
| ☐ | Regenerate session IDs on login, privilege change, and logout | P0 |
| ☐ | Keep session tokens long, random, and server-revocable | P1 |
| ☐ | Make password-reset tokens single-use, short-lived, and bound to the account | P1 |
| ☐ | Set explicit session timeouts (idle and absolute) and honor them server-side | P1 |
| ☐ | Alert on credential-stuffing patterns — many failed logins across many accounts | P1 |
| ☐ | Log every auth event with outcome; silence here means you can't detect A09 either | P2 |
| ☐ | Avoid rolling your own — use the framework's session/auth machinery | P2 |

## 8. A08:2025 — Software or Data Integrity Failures

| Status | Check | Priority |
|---|---|---|
| ☐ | Sign release artifacts and verify signatures at deploy time | P1 |
| ☐ | Add subresource integrity (SRI) to every third-party script tag | P1 |
| ☐ | Treat deserialization as untrusted input; avoid native object deserialization entirely | P0 |
| ☐ | Verify webhook signatures before acting on them | P0 |
| ☐ | Use immutable, digest-pinned container images — no `latest` in production | P1 |
| ☐ | Protect branch and tag namespaces so release refs can't be moved silently | P1 |
| ☐ | Record build provenance (SLSA-style attestations) for release binaries | P2 |
| ☐ | Detect drift: alert when running artifacts differ from signed releases | P2 |

## 9. A09:2025 — Security Logging & Alerting Failures

| Status | Check | Priority |
|---|---|---|
| ☐ | Log authentication, authorization, and input-validation failures with context | P0 |
| ☐ | Centralize logs off the app hosts (an attacker who owns the box owns its logs) | P0 |
| ☐ | Alert on the patterns that matter: brute force, privilege changes, unusual egress | P1 |
| ☐ | Include actor, timestamp, source IP, and outcome in every security event | P1 |
| ☐ | Protect log integrity — append-only or WORM storage for audit trails | P1 |
| ☐ | Sanitize data written to logs to prevent log injection and forged entries | P1 |
| ☐ | Set and enforce retention that matches your compliance needs (90+ days typical) | P1 |
| ☐ | Test alerts end-to-end — a paging rule that never fired is unverified | P2 |
| ☐ | Schedule log review: automated daily, human review on a real cadence | P2 |

## 10. A10:2025 — Mishandling of Exceptional Conditions

| Status | Check | Priority |
|---|---|---|
| ☐ | Fail closed in security-relevant paths — an error during a check means deny | P0 |
| ☐ | Never swallow exceptions silently; log with enough context to debug later | P1 |
| ☐ | Set timeouts on every outbound call — an unbounded wait is a resource-exhaustion DoS | P0 |
| ☐ | Return generic errors to clients; keep internals (stack traces, hostnames) server-side | P1 |
| ☐ | Handle partial failure explicitly: what happens when payment succeeds but email fails? | P1 |
| ☐ | Bound resource use — input sizes, retries, queue depths, file uploads | P1 |
| ☐ | Test error paths in staging, including the ones "that never happen" | P1 |
| ☐ | Alert on error-rate spikes; a sudden flood of 500s is often an attack signature | P2 |
