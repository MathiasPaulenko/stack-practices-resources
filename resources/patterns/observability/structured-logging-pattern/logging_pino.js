// Structured logging with pino (Node.js). Install: npm install pino
const pino = require('pino');

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  timestamp: pino.stdTimeFunctions.isoTime,
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: { service: 'order-service', version: '1.0.0' },
});

// Metadata object first, message second
logger.info({ orderId: 123, customerId: 456, total: 99.99 }, 'order_created');
logger.error({ orderId: 123, reason: 'insufficient_funds' }, 'payment_failed');

// Child loggers carry persistent context
const requestLogger = logger.child({ requestId: 'abc-123', userId: 42 });
requestLogger.info('processing request');
requestLogger.info({ durationMs: 150 }, 'request completed');

// Sample noisy endpoints; keep the ones that matter
let requestCount = 0;
function logRequest(req) {
  if (req.path === '/health') return; // always skip health checks
  requestCount++;
  if (requestCount % 100 === 0) {
    logger.debug({ path: req.path, method: req.method }, 'request_received');
  }
}

for (let i = 0; i < 250; i++) {
  logRequest({ path: i % 2 ? '/health' : '/api/orders', method: 'GET' });
}
