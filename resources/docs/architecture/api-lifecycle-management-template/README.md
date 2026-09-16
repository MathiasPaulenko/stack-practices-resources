# API Lifecycle Management — Companion Resources

Companion files for the [API Lifecycle Management Template](https://stackpractices.com/docs/api-lifecycle-management-template/) on StackPractices.com.

## What's included

| File | Format | Description |
|------|--------|-------------|
| `api-lifecycle-checklist.md` | Markdown | Master checklist: metadata, deprecation, versioning, and sunset checklists |
| `migration-guide-template.md` | Markdown | Structured migration guide template with before/after and RFC 7807 error format |
| `deprecation-notice-example.md` | Markdown | Filled-in deprecation notice ready to adapt and send to consumers |
| `sunset-readiness-check.py` | Python | Zero-traffic readiness check against Prometheus via Grafana datasource proxy |

## Quick start

### 1. Copy the master checklist

```bash
cp api-lifecycle-checklist.md my-api-lifecycle.md
```

Edit `my-api-lifecycle.md` and replace `<API Name>`, versions, and placeholder values with your API's data.

### 2. Adapt the migration guide and notice

Copy `migration-guide-template.md` per breaking change and `deprecation-notice-example.md` per announcement. Keep the same dates across changelog, portal, email, and the `Deprecation`/`Sunset` headers.

### 3. Run the sunset readiness check

```bash
pip install requests
export GRAFANA_URL=https://grafana.example.com
export GRAFANA_TOKEN=<service-account-token>
python sunset-readiness-check.py
```

Exit code `0` means the deprecated version served zero traffic for 7 consecutive days; `1` means it is not ready; `2` means missing configuration.

## Deprecation/Sunset headers

Emit on every response of a deprecated endpoint ([RFC 9745](https://www.rfc-editor.org/rfc/rfc9745), [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594)):

```http
Deprecation: @1789430400
Sunset: Sat, 31 Dec 2026 23:59:59 GMT
Link: <https://api.example.com/v3/users>; rel="successor-version",
      <https://api.example.com/docs/deprecation-notice>; rel="deprecation"
```

## References

- [RFC 9745 — The Deprecation HTTP Header Field](https://www.rfc-editor.org/rfc/rfc9745)
- [RFC 8594 — The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594)
- [RFC 7807 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc7807)
- [Semantic Versioning 2.0.0](https://semver.org/)
