// prom-client + Express — request metrics middleware and /metrics endpoint.
//
// Run:
//   npm install prom-client express
//   node prom_client_express.js
//
// App on http://localhost:3000 — metrics on http://localhost:3000/metrics
const express = require('express');
const promClient = require('prom-client');

const register = new promClient.Registry();

// Default metrics (CPU, memory, GC)
promClient.collectDefaultMetrics({ register });

const httpRequestTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'endpoint', 'status'],
  registers: [register],
});

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'endpoint'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
  registers: [register],
});

const activeConnections = new promClient.Gauge({
  name: 'active_connections',
  help: 'Currently active connections',
  registers: [register],
});

const app = express();

app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestTotal.labels(req.method, req.path, String(res.statusCode)).inc();
    httpRequestDuration.labels(req.method, req.path).observe(duration);
  });
  next();
});

app.get('/api/orders', (req, res) => res.json({ orders: [] }));

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

activeConnections.set(42);

app.listen(3000, () => {
  console.log('App on http://localhost:3000 — metrics at /metrics');
});
