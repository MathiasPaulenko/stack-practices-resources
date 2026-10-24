// Express audit middleware: correlation ID + structured JSON audit entry per request.
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
  });
  next();
}

const app = express();
app.use(auditMiddleware);
app.get('/health', (_req, res) => res.json({ status: 'ok' }));
app.listen(3000, () => console.log('http://127.0.0.1:3000/health'));
