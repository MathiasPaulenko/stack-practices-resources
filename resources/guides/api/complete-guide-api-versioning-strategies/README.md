# API Versioning Strategies — Companion

Runnable examples from the [Complete Guide to API Versioning Strategies](https://stackpractices.com/guides/complete-guide-api-versioning-strategies/).

## Files

- `uri_versioning.py` — v1/v2 routers mounted by path prefix
- `query_param_versioning.py` — `?version=` dispatch with explicit default
- `header_versioning.py` — `X-API-Version` header dispatch
- `content_negotiation.py` — `Accept: application/vnd.*+json` media-type versioning
- `graphql_additive.graphql` / `graphql_deprecation.graphql` — additive and `@deprecated` schema evolution
- `graphql_schemas.js` — parallel schemas / directive options
- `deprecation_headers.py` — `Deprecation` + `Sunset` + `Link` successor headers
- `strangler_fig_router.py` — facade router proxying migrated endpoints to v2
- `parallel_run.py` — shadow-run comparator logging v1/v2 mismatches

## Usage

Requires `fastapi`, `httpx` (Python examples), `graphql` (JS example). Copy the router for your chosen strategy into your app.
