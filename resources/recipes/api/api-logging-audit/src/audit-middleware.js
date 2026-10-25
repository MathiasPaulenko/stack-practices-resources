// Express audit middleware: correlation ID + request log + audit record for non-GET ops.
// Run: node audit-middleware.js  (needs: npm i express winston uuid)
const express = require('express');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.json(),
  transports: [new winston.transports.Console()],
});

function auditMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id'] || uuidv4();
  req.correlationId = correlationId;
  res.setHeader('X-Correlation-Id', correlationId);

  const start = Date.now();
  res.on('finish', () => {
    logger.info('api_request', {
      correlation_id: correlationId,
      method: req.method,
      path: req.path,
      status_code: res.statusCode,
      duration_ms: Date.now() - start,
      client_ip: req.ip,
      user_agent: req.get('user-agent'),
    });

    // Audit record: only for state-changing or sensitive operations
    if (!['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
      logger.info('api_audit', {
        timestamp: new Date().toISOString(),
        correlation_id: correlationId,
        actor: (req.user && req.user.id) || 'anonymous',
        action: req.method,
        resource: req.path,
        outcome: res.statusCode < 400 ? 'success' : 'failure',
        client_ip: req.ip,
      });
    }
  });
  next();
}

const app = express();
app.use(auditMiddleware);
app.get('/health', (_req, res) => res.json({ status: 'ok' }));
app.post('/echo', (_req, res) => res.json({ status: 'created' }));
app.listen(3000, () => console.log('http://127.0.0.1:3000/health'));
