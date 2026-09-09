const Redis = require('ioredis');

/**
 * Distributed lock using Redis SET NX with TTL and a fencing token.
 */
class RedisDistributedLock {
  constructor(redisClient, lockKey, ttlSeconds = 30, retryDelay = 100) {
    this.redis = redisClient;
    this.lockKey = `distlock:${lockKey}`;
    this.ttl = ttlSeconds;
    this.retryDelay = retryDelay;
    this.token = null;
    this._acquired = false;
  }

  async acquire(blocking = true, timeoutMs = null) {
    this.token = crypto.randomUUID();
    const start = Date.now();

    while (true) {
      const result = await this.redis.set(
        this.lockKey, this.token, 'NX', 'EX', this.ttl
      );
      if (result === 'OK') {
        this._acquired = true;
        return true;
      }

      if (!blocking) return false;
      if (timeoutMs && Date.now() - start >= timeoutMs) return false;

      await new Promise((r) => setTimeout(r, this.retryDelay));
    }
  }

  async release() {
    if (!this._acquired) return false;

    const luaScript = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    const result = await this.redis.eval(luaScript, 1, this.lockKey, this.token);
    this._acquired = false;
    return result === 1;
  }

  async extend(additionalTtl) {
    if (!this._acquired) return false;

    const luaScript = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("expire", KEYS[1], ARGV[2])
      else
        return 0
      end
    `;
    const result = await this.redis.eval(
      luaScript, 1, this.lockKey, this.token, additionalTtl
    );
    return result === 1;
  }
}

const crypto = require('crypto');

module.exports = { RedisDistributedLock };
