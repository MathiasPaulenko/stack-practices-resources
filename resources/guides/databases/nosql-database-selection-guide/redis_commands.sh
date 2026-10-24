#!/usr/bin/env bash
# Redis patterns from the NoSQL selection guide.
# Companion to https://stackpractices.com/guides/nosql-database-selection-guide/
# Run against a local redis-cli or paste line by line.

# Cache a computed value for 5 minutes
SET user:123:profile '{"name":"Alice"}' EX 300

# Atomic increment for rate limiting
INCR rate_limit:ip:192.168.1.1
EXPIRE rate_limit:ip:192.168.1.1 60

# Fan-out-on-write follower feed (social platform scenario)
ZADD feed:user:follower-42 1719160000 post-9001
EXPIRE feed:user:follower-42 86400
ZREVRANGE feed:user:follower-42 0 49 WITHSCORES
