// Gateway Routing Pattern — runnable Express gateway.
// Routes path prefixes to upstream services, injects a correlation ID,
// and returns 502 on upstream errors.
//
// Run:  npm install && npm start
// Test: curl http://localhost:3000/users   (needs an upstream on :3001)

import express from 'express';
import { randomUUID } from 'node:crypto';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

// Correlation ID middleware must run before any proxy route so the
// same ID reaches every upstream.
app.use((req, _res, next) => {
  req.headers['x-request-id'] ??= randomUUID();
  next();
});

const routes: Array<[string, string]> = [
  ['/users', process.env.USERS_URL ?? 'http://localhost:3001'],
  ['/orders', process.env.ORDERS_URL ?? 'http://localhost:3002'],
  ['/inventory', process.env.INVENTORY_URL ?? 'http://localhost:3003'],
];

for (const [path, target] of routes) {
  app.use(
    path,
    createProxyMiddleware({
      target,
      changeOrigin: true,
      on: {
        proxyReq: (proxyReq, req) => {
          proxyReq.setHeader('X-Request-ID', req.headers['x-request-id']);
        },
        error: (_err, _req, res) => {
          (res as express.Response).status(502).json({ error: 'Bad Gateway' });
        },
      },
    }),
  );
}

// Gateway health endpoint so the platform can monitor the router itself.
app.get('/healthz', (_req, res) => res.json({ status: 'ok' }));

app.listen(3000, () => console.log('Gateway listening on port 3000'));
