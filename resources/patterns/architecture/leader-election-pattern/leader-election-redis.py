"""Redis-based leader election with SET NX PX and Lua release/renew.

Companion code for https://stackpractices.com/patterns/leader-election-pattern/

Requires: pip install redis, and a Redis server on localhost:6379.
Run:      python leader-election-redis.py

Two rules this example enforces:
- Acquire is a single atomic command (SET key token NX PX ttl).
- Release/renew go through Lua so the compare can't race another leader.
"""
import time
import uuid

import redis

RELEASE_LUA = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
end
return 0
"""

RENEW_LUA = """
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("pexpire", KEYS[1], ARGV[2])
end
return 0
"""


class RedisLeaderElection:
    def __init__(self, redis_client, lock_key="leader_lock", ttl_ms=10000):
        self.redis = redis_client
        self.lock_key = lock_key
        self.ttl_ms = ttl_ms
        self.node_id = uuid.uuid4().hex
        self.token = None

    def acquire(self):
        # One atomic command — no check-then-set race.
        self.token = f"{self.node_id}:{int(time.time() * 1000)}"
        return self.redis.set(
            self.lock_key, self.token, nx=True, px=self.ttl_ms
        ) is not None

    def renew(self):
        # Lua: extend only if we still hold it.
        return self.redis.eval(
            RENEW_LUA, 1, self.lock_key, self.token, self.ttl_ms
        ) == 1

    def release(self):
        # Lua: delete only our own token — never someone else's lease.
        self.redis.eval(RELEASE_LUA, 1, self.lock_key, self.token)


if __name__ == "__main__":
    client = redis.Redis(host="localhost", port=6379, db=0)
    election = RedisLeaderElection(client, ttl_ms=2000)
    if election.acquire():
        print("acquired leadership, renewing once...")
        time.sleep(0.5)
        print("renewed:", election.renew())
        election.release()
        print("released cleanly")
    else:
        print("another node holds the lease")
