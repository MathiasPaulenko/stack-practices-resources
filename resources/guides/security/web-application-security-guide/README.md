# Web Application Security (OWASP Top 10)

Companion files for the guide [Web Application Security (OWASP Top 10)](https://stackpractices.com/guides/web-application-security-guide/).

Runnable pieces for the controls the guide covers — no dependencies beyond Node and Python stdlib.

## Contents

| File | OWASP item | What it does |
| ---- | ---------- | ------------ |
| `headers_server.js` | A05 | Zero-dep Node server sending the full security header set |
| `security_headers.conf` | A05 | nginx snippet: headers, method restriction, `server_tokens off` |
| `ssrf_safe_fetch.py` | A10 | Host + scheme + resolved-IP allowlist before fetching |
| `dependency_scan.sh` | A06 | Runs `npm audit` / `pip-audit` / `snyk test` wherever they exist |

## Run it

```bash
# Security headers — then curl -i http://localhost:3000/
node headers_server.js

# SSRF allowlist demo (stdlib only — prints BLOCKED/ALLOWED per URL)
python ssrf_safe_fetch.py

# Dependency audit (drop into your project root or CI)
bash dependency_scan.sh
```

`ssrf_safe_fetch.py` exits having validated six URLs: one allowed (`api.github.com` — the actual fetch may fail without network, validation still runs) and five blocked (http scheme, off-allowlist host, AWS metadata IP, loopback, `file://`).

## Notes

- The CSP in `headers_server.js`/`security_headers.conf` is a starting point — adjust `default-src 'self'` to what the app actually loads.
- `security_headers.conf` goes inside an nginx `server {}` block or an include; pair it with the HTTP→HTTPS redirect shown in the comment.
- The SSRF check resolves the hostname and rejects non-global IPs, covering the metadata-endpoint and DNS-rebinding tricks the guide explains.
