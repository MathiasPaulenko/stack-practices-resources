"""Leader election demo over an atomic store with CAS + fencing tokens.

Companion code for https://stackpractices.com/patterns/leader-election-pattern/

Run:  python leader_election.py

Simulates three nodes competing for a lease: node-1 wins, renews twice,
then "crashes" (stops renewing). The lease expires and a follower wins the
next campaign with a higher fencing token. Works the same against etcd's
transaction API, ZooKeeper, or SQL UPDATE ... WHERE.
"""
import threading
import time
import uuid


class AtomicStore:
    """Minimal stand-in for etcd/ZooKeeper: atomic ops only."""

    def __init__(self):
        self._data, self._fence, self._lock = {}, 0, threading.Lock()

    def get(self, key):
        return self._data.get(key)

    def cas(self, key, expected, value):
        """Write only if current == expected. Return a fencing token."""
        with self._lock:
            if self._data.get(key) != expected:
                return None
            self._fence += 1
            value["fence"] = self._fence
            self._data[key] = value
            return self._fence


class LeaderElection:
    def __init__(self, store, node_id=None, lease_seconds=1.0):
        self.store = store
        self.lease_seconds = lease_seconds
        self.node_id = node_id or uuid.uuid4().hex[:8]

    def campaign(self):
        """Return a fencing token once this node wins the lease."""
        now = time.monotonic()  # elapsed time, immune to wall-clock jumps
        current = self.store.get("leader")
        if current and current["expires"] > now:
            return None
        return self.store.cas(
            "leader", current,
            {"node": self.node_id, "expires": now + self.lease_seconds},
        )

    def renew(self, token):
        now = time.monotonic()
        current = self.store.get("leader")
        if not current or current["fence"] != token:
            return False  # lost leadership
        current["expires"] = now + self.lease_seconds
        return True


def main():
    store = AtomicStore()
    nodes = [LeaderElection(store, f"node-{i}", lease_seconds=1.0)
             for i in range(1, 4)]

    leader = nodes[0]
    token = leader.campaign()
    print(f"{leader.node_id} won the lease (fence={token})")

    for _ in range(2):
        time.sleep(0.4)
        leader.renew(token)
        print(f"{leader.node_id} renewed; "
              f"expires={store.get('leader')['expires']:.3f}")

    print(f"{leader.node_id} crashes — no more renewals")
    time.sleep(1.1)  # lease TTL expires

    winner = None
    while winner is None:
        for node in nodes[1:]:
            token = node.campaign()
            if token:
                winner = node
                break
        time.sleep(0.05)

    print(f"{winner.node_id} takes over (fence={token}); "
          f"old leader fence=1 is now stale")


if __name__ == "__main__":
    main()
