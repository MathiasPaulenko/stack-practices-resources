// Structured logger demo: writes one JSON line per simulated request
// to stdout AND to /var/log/app/app.log (tailed by Fluent Bit).
const fs = require('fs');
const pino = require('pino');

const stream = pino.multistream([
  { stream: process.stdout },
  { stream: fs.createWriteStream('/var/log/app/app.log', { flags: 'a' }) },
]);
const logger = pino({ level: process.env.LOG_LEVEL || 'info' }, stream);

const levels = ['info', 'info', 'info', 'warn', 'error'];
let i = 0;

setInterval(() => {
  const level = levels[i % levels.length];
  logger[level]({
    msg: 'request_handled',
    request_id: `req-${i}`,
    trace_id: `trace-${Math.floor(i / 5)}`,
    path: ['/api/orders', '/api/users', '/health'][i % 3],
    status: level === 'error' ? 500 : 200,
    duration_ms: Math.floor(Math.random() * 800),
  });
  i += 1;
}, 500);
