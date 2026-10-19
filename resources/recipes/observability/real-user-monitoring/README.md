# Real User Monitoring (RUM) Setup with web-vitals

Companion code for the StackPractices recipe:
<https://stackpractices.com/recipes/real-user-monitoring/>

Collect Core Web Vitals from real browsers, ship them with `sendBeacon`, and layer session replay on top.

## Files

| File | Stack | What it shows |
| --- | --- | --- |
| `vitals-collector.js` | web-vitals v4 | `onCLS`/`onINP`/`onFCP`/`onLCP`/`onTTFB` with `sendBeacon` fallback to `fetch` |
| `sentry-replay.js` | `@sentry/browser` | `replayIntegration()` with privacy masking and per-session sampling |
| `performance-observer.js` | PerformanceObserver | Custom metrics: slow resources and long tasks |
| `ingest-server.js` | Node.js | Minimal beacon endpoint that logs vitals as JSONL |

## Run

```bash
npm install
npm run ingest   # minimal /analytics/vitals endpoint on :8899
```

Import `vitals-collector.js` (and optionally `sentry-replay.js` and `performance-observer.js`) from your app's entry point. Replace `/analytics/vitals` and the Sentry DSN with your own values.

## Notes

- `web-vitals` v4 reports INP (FID was retired from Core Web Vitals in March 2024).
- The standalone `@sentry/replay` package is deprecated; replay ships in `@sentry/browser` since SDK v7.
- `sendBeacon` keeps events alive when the user closes the tab mid-measurement.
- Sample replay at ~1% of sessions (100% on error sessions) — it's heavier than vitals.
