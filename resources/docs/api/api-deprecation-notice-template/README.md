# API Deprecation Notice Template — Companion Code

Companion resources for [API Deprecation Notice Template](https://stackpractices.com/docs/api-deprecation-notice-template/)
(ES: [Plantilla de Aviso de Deprecación de API](https://stackpractices.com/es/docs/api-deprecation-notice-template/)).

## What's inside

| File | Description |
|------|-------------|
| `notice/deprecation-notice-template.md` | The copy-paste deprecation notice: change summary, before/after, migration steps, timeline table, support contacts, exceptions |
| `middleware/express.js` | Express middleware emitting `Deprecation`, `Sunset`, and `Link` headers on deprecated paths |
| `middleware/flask.py` | The same middleware as Flask `before_request` / `after_request` hooks |
| `tracking/deprecation-traffic.sql` | SQL query listing request volume per deprecated endpoint per client |
| `tracking/alert-rule.yaml` | Prometheus alert that fires when a high-traffic client still hasn't migrated |

## Usage

1. Copy `notice/deprecation-notice-template.md`, fill the `<placeholders>`, and send it to consumers at T-90.
2. Mount the middleware that matches your stack so deprecated endpoints self-report via response headers.
3. Run the SQL query (or the Prometheus alert) weekly to find consumers who haven't started migrating.
4. Follow the T-90 → T-0 communication plan on the main page; at sunset the old version returns `410 Gone`.

## License

MIT — see the repository root.
