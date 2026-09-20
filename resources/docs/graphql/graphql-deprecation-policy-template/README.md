# GraphQL Deprecation Policy Template — Companion Code

Companion resources for [GraphQL Deprecation Policy Template](https://stackpractices.com/docs/graphql-deprecation-policy-template/)
(ES: [Plantilla de Política de Deprecación de GraphQL](https://stackpractices.com/es/docs/graphql-deprecation-policy-template/)).

## What's inside

| File | Description |
|------|-------------|
| `tracking/apollo-server-4-deprecation-plugin.ts` | Apollo Server 4 plugin that walks each query with `TypeInfo`/`visitWithTypeInfo`, reports deprecated field usage to analytics, and injects `extensions.deprecations` into the response |
| `communication/deprecation-email-template.md` | Copy-paste deprecation notice email with usage counts, impact, migration guide link, and the announce → warn → final notice → remove timeline |
| `reports/usage-report-template.txt` | Weekly deprecated-field usage report: per-field counts, top clients, trend, removal eligibility |
| `templates/migration-guide-template.md` | Migration guide skeleton: what changed, before/after queries, migration steps, common issues, timeline |

## Usage

1. Register `deprecationTracker` as an Apollo Server 4 plugin and wire `analytics.track` to your pipeline (Segment, logs, etc.).
2. Deploy it and collect a baseline before announcing any deprecation — the first email should include real per-client numbers.
3. Send `deprecation-email-template.md` to consumers on day 0, 30, 90 and 180; fill the `{placeholders}` from the usage report.
4. Publish one `migration-guide-template.md` per deprecated element and link it from the `@deprecated` reason.
5. Remove an element only after 30 consecutive days of zero usage, following the checklist on the main page.

## License

MIT — see the repository root.
