-- token_bucket.lua — atomic token bucket for Redis
--
-- KEYS[1] = bucket key (e.g. "rate_limit:user:u_4812")
-- ARGV[1] = capacity (max tokens)
-- ARGV[2] = refill_rate (tokens per second)
-- ARGV[3] = now (unix timestamp, seconds — pass from the caller, not TIME, for testability)
--
-- Returns: { allowed (0|1), remaining_tokens, retry_after_seconds }
--
-- Atomicity: the whole read-check-update runs inside Redis, so concurrent
-- requests can't race on the counter the way hgetall + hset can.

local bucket_key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local bucket = redis.call('HMGET', bucket_key, 'tokens', 'last_refill')
local tokens = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now

local elapsed = math.max(0, now - last_refill)
tokens = math.min(capacity, tokens + elapsed * refill_rate)

if tokens < 1 then
  redis.call('HMSET', bucket_key, 'tokens', tokens, 'last_refill', now)
  redis.call('EXPIRE', bucket_key, math.ceil(capacity / refill_rate) + 1)
  local retry_after = math.ceil((1 - tokens) / refill_rate)
  return { 0, math.floor(tokens), retry_after }
end

tokens = tokens - 1
redis.call('HMSET', bucket_key, 'tokens', tokens, 'last_refill', now)
redis.call('EXPIRE', bucket_key, math.ceil(capacity / refill_rate) + 1)
return { 1, math.floor(tokens), 0 }
