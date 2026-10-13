import express from 'express';
import { cspNonceMiddleware } from './csp-nonce-middleware.js';
import { cspReportRouter } from './csp-report-endpoint.js';

const app = express();

// 1. Report endpoint first, so it works even if CSP blocks something later
app.use('/api/csp-reports', cspReportRouter);

// 2. Reporting-Endpoints header for the Reporting API (report-to csp-endpoint)
app.use((req, res, next) => {
  res.setHeader('Reporting-Endpoints', 'csp-endpoint="/api/csp-reports"');
  next();
});

// 3. Per-request nonce + enforcing CSP policy
app.use(cspNonceMiddleware);

app.get('/', (req, res) => {
  const nonce = res.locals.nonce as string;
  res.send(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>CSP nonce demo</title>
    <script nonce="${nonce}">console.log('allowed: this inline script carries the nonce');</script>
    <script>console.log('blocked: no nonce — check the browser console and /api/csp-reports');</script>
  </head>
  <body>
    <h1>CSP nonce demo</h1>
    <p>One inline script runs, the other is blocked. Check DevTools console.</p>
  </body>
</html>`);
});

const port = process.env.PORT ?? 3000;
app.listen(port, () => {
  console.log(`Listening on http://localhost:${port}`);
});
