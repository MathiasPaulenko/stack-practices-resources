# Error Tracking with Sentry in Express

Companion repository for the [Error Tracking with Sentry in Express](https://stackpractices.com/recipes/nodejs-sentry-error-tracking/) recipe on StackPractices.

## Files

- `instrument.js` — Sentry v8+ initialization (loaded before the app)
- `app.js` — Express app with `setupExpressErrorHandler`, user context, breadcrumbs, and a custom `startSpan`
- `package.json` — minimal dependencies (`@sentry/node` v8+, `express`)
- `.env.example` — environment variables (`SENTRY_DSN`, `SENTRY_RELEASE`, `NODE_ENV`)

## Quick start

```bash
npm install
cp .env.example .env   # fill in your SENTRY_DSN
npm start
```

Then trigger the test error:

```bash
curl http://localhost:3000/debug-sentry
```

The event should appear in your Sentry dashboard within seconds, with the request context, the `alice` user, and any breadcrumbs.

## Notes

- `require("./instrument")` must be the first import — the SDK patches `http` and `express` at load time. Importing it late means errors pass through unreported.
- `setupExpressErrorHandler` only captures 5xx errors by default; 4xx statuses are treated as expected client errors. Customize with `Sentry.expressIntegration({ shouldHandleError })`.
- Express 4 does not forward rejected promises from `async` handlers to error middleware — wrap them or use `next(err)`. Express 5 handles this natively.
