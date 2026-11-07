// Connect to Redis with ioredis: URL, retry strategy, sorted sets, pub/sub.
// npm install ioredis
const Redis = require('ioredis');

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379', {
    // rediss:// URLs enable TLS automatically; add tls: {} for custom certs.
    maxRetriesPerRequest: 3,
    retryStrategy: (times) => Math.min(times * 200, 2000),
    enableReadyCheck: true,
});

async function main() {
    await redis.set('user:1:name', 'Alice', 'EX', 3600);
    console.log(await redis.get('user:1:name'));

    await redis.hset('user:1', 'email', 'alice@example.com', 'role', 'admin');
    console.log(await redis.hgetall('user:1'));

    // Sorted set: leaderboard.
    await redis.zadd('leaderboard', 100, 'alice', 85, 'bob', 120, 'charlie');
    console.log(await redis.zrevrange('leaderboard', 0, 2, 'WITHSCORES'));

    // Pub/sub needs a second connection for the subscriber.
    const subscriber = new Redis(process.env.REDIS_URL || 'redis://localhost:6379');
    await subscriber.subscribe('notifications');
    subscriber.on('message', (channel, message) => {
        console.log(`received on ${channel}: ${message}`);
    });
    await redis.publish('notifications', 'hello');

    await new Promise((resolve) => setTimeout(resolve, 200));
    await subscriber.quit();
    await redis.quit();
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
