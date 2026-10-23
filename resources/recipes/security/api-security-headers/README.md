# API Security Headers — Companion Resources

Companion tool for the [API security headers recipe](https://stackpractices.com/recipes/api-security-headers/) on StackPractices.

## Contents

- `audit-headers.sh` — Bash script that fetches a URL's response headers with `curl` and reports missing security headers, weak CSP directives (`unsafe-inline`, `unsafe-eval`), and a disabled HSTS (`max-age=0`).

## Usage

```bash
chmod +x audit-headers.sh
./audit-headers.sh https://your-domain.com
```

Example output:

```text
Auditing: https://your-domain.com
-----------------------------------
OK: strict-transport-security = max-age=63072000; includeSubDomains
MISSING: content-security-policy
OK: x-content-type-options = nosniff
OK: x-frame-options = DENY
OK: referrer-policy = strict-origin-when-cross-origin
OK: permissions-policy = geolocation=(), microphone=()
OK: cross-origin-opener-policy = same-origin
OK: cross-origin-resource-policy = same-origin
WARNING: CSP contains 'unsafe-inline'
```

Requires `curl` and `grep` — available on macOS, Linux, and Git Bash on Windows.
