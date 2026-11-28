-- Redis token bucket, atomic (Lua)
local tokens = tonumber(redis.call("GET", KEYS[1]) or ARGV[1])
local last = tonumber(redis.call("GET", KEYS[2]) or ARGV[2])
local now = tonumber(ARGV[3])
local rate = tonumber(ARGV[4])

tokens = math.min(tonumber(ARGV[1]), tokens + (now - last) * rate)
if tokens >= 1 then
  redis.call("SET", KEYS[1], tokens - 1)
  redis.call("SET", KEYS[2], now)
  return 1
end
return 0
