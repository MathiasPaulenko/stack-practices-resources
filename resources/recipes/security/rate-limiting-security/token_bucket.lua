-- token_bucket.lua
-- Atomic token-bucket rate limiter for Redis.
-- KEYS[1] = rate limit key (e.g. "rl:login:1.2.3.4")
-- ARGV[1] = capacity, ARGV[2] = refill rate (tokens/sec)
-- ARGV[3] = current unix timestamp, ARGV[4] = key TTL (sec)
-- Returns: 1 if allowed, 0 if rate limited.

local bucket = redis.call('HMGET', KEYS[1], 'tokens', 'last_refill')
local tokens = tonumber(bucket[1]) or tonumber(ARGV[1])
local last_refill = tonumber(bucket[2]) or tonumber(ARGV[3])

tokens = math.min(tonumber(ARGV[1]),
  tokens + (tonumber(ARGV[3]) - last_refill) * tonumber(ARGV[2]))

local allowed = 0
if tokens >= 1 then
  tokens = tokens - 1
  allowed = 1
end

redis.call('HMSET', KEYS[1], 'tokens', tokens, 'last_refill', ARGV[3])
redis.call('EXPIRE', KEYS[1], ARGV[4])
return allowed
