# Connect to Redis

Runnable companion for the [Connect to Redis](https://stackpractices.com/recipes/connect-to-redis/) recipe: connection via URL, pools, pipelines, rate limiting, sorted sets, and pub/sub in Python, JavaScript, and Java.

## Contents

- `docker-compose.yml` + `redis.conf` — local Redis 7 with `maxmemory` + `allkeys-lru` + AOF
- `connect.py` — `redis-py` `from_url` + `decode_responses` + pipeline + `INCR`/`EXPIRE` rate limit
- `connect.js` — `ioredis` URL config + `retryStrategy` + sorted sets + pub/sub with a second connection
- `RedisExample.java` — `JedisPooled` + `setex`/`hset` + Lua rate limiter
- `requirements.txt`, `package.json`

## Run it

```bash
docker compose up -d          # starts Redis on localhost:6379

# Python
pip install -r requirements.txt
python connect.py

# JavaScript
npm install
npm start

# Java — needs jedis on the classpath
javac -cp ".:jedis.jar" RedisExample.java
java -cp ".:jedis.jar" RedisExample
```

## Notes

- The connection string comes from `REDIS_URL` (`redis://host:6379/0` locally). Never hardcode production credentials — use `rediss://user:password@host:6379` for AUTH + TLS.
- Local dev has no password. Production requires ACL users (`ACL SETUSER`) and TLS; managed services hand you a `rediss://` endpoint.
- `maxmemory` + an eviction policy are mandatory in production — without them Redis grows until the OOM killer picks it. `allkeys-lru` for caches, `noeviction` for durable data.
- Use `SCAN`/`HSCAN` over `KEYS`/`HGETALL` on large keyspaces — the blocking commands freeze the single thread.
