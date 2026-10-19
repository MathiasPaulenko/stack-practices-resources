// Structured logging with Winston: JSON output, size rotation, metadata fields.
// Run: npm install && node javascript_winston.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log', maxsize: 10_000_000, maxFiles: 5 }),
  ],
});

const userId = 'u-42';
const apiKey = 'sk-live-abcdef123456';

logger.debug('Processing user', { userId });
logger.info('User logged in', { userId });
logger.warn('Rate limit at 90%', { apiKey: apiKey.slice(0, 4) });

try {
  throw new Error('database timeout');
} catch (error) {
  logger.error('Database connection failed', { error });
}

// Child logger carries request context on every line
const requestLogger = logger.child({ requestId: 'abc-123' });
requestLogger.info('Request completed', { durationMs: 45 });
