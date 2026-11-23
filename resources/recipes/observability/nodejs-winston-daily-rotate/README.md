# Winston Daily Log Rotation — Companion Project

Runnable companion to the StackPractices recipe [Rotate Logs Daily with Winston](https://stackpractices.com/recipes/nodejs-winston-daily-rotate/).

## What's inside

- `logger.js` — Winston configured with two `winston-daily-rotate-file` transports (info 14d + error 30d), `zippedArchive`, `auditFile`, rotation event listeners, and a dev-only console transport.
- `server.js` — Express app piping morgan's `combined` access log into Winston, with a normal route and a forced-error route.
- `demo.js` — writes a burst of 100+ entries so you can see files appear in `logs/`.

## Run it

```bash
npm install
npm run demo      # writes entries to logs/application-*.log and logs/error-*.log
npm start         # Express on :3000 — hit /api/users/1 and /api/error
```

Check `logs/` for `application-YYYY-MM-DD.log`, `error-YYYY-MM-DD.log`, and `audit.json`. Shrink `maxSize` (e.g. `"1k"`) temporarily if you want to watch a rotation happen in one run.
