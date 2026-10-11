// Publishes a test notification to a room.
// Usage: node publish.js [room] [message]
const Redis = require('ioredis');

const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const [, , room = 'orders', ...rest] = process.argv;
const text = rest.join(' ') || 'New order!';

const redis = new Redis(REDIS_URL);

redis
  .publish('notifications', JSON.stringify({ room, text }))
  .then((receivers) => {
    console.log(`published to "${room}" -> ${receivers} subscriber(s)`);
    redis.disconnect();
  });
