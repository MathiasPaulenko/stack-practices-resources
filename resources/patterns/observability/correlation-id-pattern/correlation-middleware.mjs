// Express correlation ID middleware with AsyncLocalStorage + structured logging.
//
// Usage:
//   node correlation-middleware.mjs
//   curl -i http://localhost:3000/orders -H "x-correlation-id: demo-123"
import { AsyncLocalStorage } from 'node:async_hooks';
import { randomUUID } from 'node:crypto';

const CORRELATION_ID_HEADER = 'x-correlation-id';
const als = new AsyncLocalStorage();

function logInfo(message) {
  const store = als.getStore();
  console.log(
    JSON.stringify({
      timestamp: new Date().toISOString(),
      level: 'info',
      correlationId: store?.correlationId || 'unknown',
      message,
    })
  );
}

export function correlationIdMiddleware(req, res, next) {
  const correlationId = req.headers[CORRELATION_ID_HEADER] || randomUUID();
  req.correlationId = correlationId;
  res.setHeader(CORRELATION_ID_HEADER, correlationId);
  als.run({ correlationId }, () => next());
}

export async function callDownstream(url) {
  const store = als.getStore();
  const response = await fetch(url, {
    headers: { [CORRELATION_ID_HEADER]: store?.correlationId || '' },
  });
  return response.json();
}

// --- minimal demo server (no express dependency needed) ---
import http from 'node:http';

const server = http.createServer((req, res) => {
  const correlationId = req.headers[CORRELATION_ID_HEADER] || randomUUID();
  res.setHeader(CORRELATION_ID_HEADER, correlationId);
  als.run({ correlationId }, () => {
    if (req.url === '/orders') {
      logInfo('Creating order');
      res.end(JSON.stringify({ status: 'created' }));
    } else {
      res.end('ok');
    }
  });
});

if (process.argv[1].endsWith('correlation-middleware.mjs')) {
  server.listen(3000, () => console.log('listening on :3000'));
}
