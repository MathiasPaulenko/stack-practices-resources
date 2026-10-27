-- Atomic token bucket on Redis.
-- KEYS[1]=bucket key; ARGV: capacity, refill_rate, tokens_requested, now
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local tokens_requested = tonumber(ARGV[3])
local now = tonumber(ARGV[4])
local bucket = redis.call('HMGET', KEYS[1], 'tokens', 'last_refill')
local current_tokens = tonumber(bucket[1]) or capacity
local last_refill = tonumber(bucket[2]) or now
local elapsed = now - last_refill
local new_tokens = math.min(capacity, current_tokens + elapsed * refill_rate)
local allowed = 0
if new_tokens >= tokens_requested then
    new_tokens = new_tokens - tokens_requested
    allowed = 1
end
redis.call('HMSET', KEYS[1], 'tokens', new_tokens, 'last_refill', now)
redis.call('EXPIRE', KEYS[1], 60)
return allowed
