// Health check endpoints for Kubernetes probes (Express + TypeScript).
// Companion to https://stackpractices.com/recipes/microservices-patterns/
// Pair with deployment.yaml: /health/live, /health/ready, /health/startup.

import express from 'express';

const app = express();

declare function checkDatabaseConnection(): Promise<void>;
declare function checkRedisConnection(): Promise<void>;
declare function checkDownstreamServices(): Promise<void>;

// Liveness: is the process running?
app.get('/health/live', (req, res) => {
  res.status(200).json({ status: 'alive' });
});

// Readiness: can we handle traffic?
app.get('/health/ready', async (req, res) => {
  const checks = await Promise.allSettled([
    checkDatabaseConnection(),
    checkRedisConnection(),
    checkDownstreamServices(),
  ]);

  const allHealthy = checks.every(c => c.status === 'fulfilled');
  if (allHealthy) {
    res.status(200).json({ status: 'ready' });
  } else {
    res.status(503).json({
      status: 'not ready',
      failures: checks
        .filter(c => c.status === 'rejected')
        .map(c => (c as PromiseRejectedResult).reason.message),
    });
  }
});

// Startup: has the app finished initializing?
app.get('/health/startup', (req, res) => {
  if (app.locals.initialized) {
    res.status(200).json({ status: 'started' });
  } else {
    res.status(503).json({ status: 'starting' });
  }
});

export default app;
