// Stale-while-revalidate on Redis.
// Serves the cached value even when stale, and refreshes it in the background.
const redis = require('redis');

const client = redis.createClient();

async function swr(key, ttl, builder) {
  const cached = await client.get(key);
  const staleFlag = await client.get(`${key}:stale`);

  if (cached) {
    const data = JSON.parse(cached);

    if (staleFlag === '1') {
      builder()
        .then((value) => {
          client.setEx(key, ttl, JSON.stringify(value));
          client.del(`${key}:stale`);
        })
        .catch((err) => console.error('SWR refresh failed:', err));
    }
    return data;
  }

  const value = await builder();
  await client.setEx(key, ttl, JSON.stringify(value));
  return value;
}

// Call this from a scheduler at ~80% of the TTL to mark keys as stale
async function markStale(key) {
  await client.set(`${key}:stale`, '1', { EX: 60 });
}

module.exports = { swr, markStale };
