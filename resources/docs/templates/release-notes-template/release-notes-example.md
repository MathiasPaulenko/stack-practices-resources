# Release v2.5.0 — CSV Export & Performance Improvements

**Release Date:** 2026-07-15
**Status:** published

## Highlights

Added CSV export for analytics dashboards and improved dashboard load time
by 40%. Fixed a bug where date ranges crossing month boundaries produced
empty exports.

## Breaking Changes

- **Change:** `/api/v1/reports` now returns a `metadata` object instead of flat fields
- **Impact:** Any client parsing the response as flat JSON will break
- **Migration:** Update response parsing to read from `metadata`. See migration guide.

## New Capabilities

- **CSV Export** — export any dashboard chart as CSV. See [docs](https://stackpractices.com/recipes/export-csv-excel/).
- **Saved Filters** — save and name dashboard filter presets for reuse.

## Improvements

- **Dashboard load time** — reduced from 3.2s to 1.9s (p95) by lazy-loading charts
- **API rate limits** — increased from 100 to 200 req/min for Pro tier

## Bug Fixes

- **#234** — CSV export downloads empty file when date range crosses a month boundary
- **#231** — saved filter names truncate at 20 characters
- **#228** — dashboard crashes when switching from table to bar chart with 0 rows

## Security

- **CVE-2026-1234** — XSS in chart tooltip rendering (High). Fixed by escaping
  user input in tooltip templates.

## Deprecations

- **`/api/v1/reports` flat response format** — removed in v3.0.0. Use `metadata`.
  See API Deprecation Notice.

## Upgrade Instructions

1. Update the SDK: `npm install @stackpractices/sdk@2.5.0`
2. If using `/api/v1/reports`, update response parsing (see migration guide)
3. Verify: `curl -H "Authorization: Bearer $TOKEN" https://api.example.com/v1/reports | jq .metadata`

## Known Issues

- **#240** — CSV export fails for charts with more than 10,000 rows.
  Workaround: narrow the date range. Fix targeted for v2.5.1.

## Release Metrics

- Commits: 47 · Contributors: 6 · Issues closed: 12 · PRs merged: 31

## Full Changelog

https://github.com/example/repo/compare/v2.4.1...v2.5.0
