// Structured logger with correlation IDs.
// Sends JSON lines to stdout (Docker/Kubernetes friendly) and to app.log
// (readable by a node-level agent like Fluent Bit or Promtail).
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log' })
  ]
});

function logWithContext(req, message, meta = {}) {
  logger.info(message, {
    traceId: req.headers?.['x-trace-id'],
    userId: req.user?.id,
    service: 'order-service',
    ...meta
  });
}

// Demo: emits three correlated lines for a fake request.
const fakeReq = { headers: { 'x-trace-id': 'abc123' }, user: { id: 'u-42' } };
logWithContext(fakeReq, 'Order received', { orderId: '123', amount: 99.99 });
logWithContext(fakeReq, 'Payment authorized', { orderId: '123', provider: 'stripe' });
logWithContext(fakeReq, 'Order placed', { orderId: '123' });
