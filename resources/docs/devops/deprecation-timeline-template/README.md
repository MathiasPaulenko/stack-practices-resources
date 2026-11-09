# Deprecation Timeline Template — Companion Files

Fillable files for the StackPractices guide:
[Deprecation Timeline Template](https://stackpractices.com/docs/deprecation-timeline-template/)

| File | What it is |
|------|-----------|
| `deprecation-timeline-template.md` | The blank template — copy it into your repo docs and fill in the blanks |
| `filled-example.md` | The same template completed for a real scenario: payments-api v1 → v2 with contractual notice clauses |
| `migration-tracker.csv` | Consumer tracking spreadsheet — status, last contact, risk level per consumer |
| `express-deprecation-headers.js` | Express middleware adding RFC 9745 `Deprecation` + RFC 8594 `Sunset` headers, plus a 410 Gone handler |
| `nginx-deprecation-headers.conf` | Same headers in nginx config, including the post-cutoff 410 block |

## Quick start

1. Copy `deprecation-timeline-template.md` into your project and fill in every `______`.
2. Track consumers in `migration-tracker.csv` — update it weekly.
3. When the soft warning milestone arrives, wire the header middleware into the deprecated routes so clients get machine-readable warnings.
4. On cutoff day, swap the proxy block for the 410 handler (or the commented nginx block).

The HTTP-date format matters: `Sunset` expects an HTTP-date like
`Thu, 15 Oct 2027 00:00:00 GMT`, not an ISO string.
