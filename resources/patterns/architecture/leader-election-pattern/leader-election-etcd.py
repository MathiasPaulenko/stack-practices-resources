"""Leader election with etcd's transaction API (python-etcd3, synchronous).

Companion code for https://stackpractices.com/patterns/leader-election-pattern/

Requires: pip install etcd3, and etcd on localhost:2379.
Run:      python leader-election-etcd.py

The safe primitive is client.transaction — one atomic compare-then-put
guarded by a lease. Never implement election as separate get + put calls.
"""
import time

import etcd3

client = etcd3.client(host="localhost", port=2379)
ELECTION_KEY = "/app/leader"
NODE_ID = "node-42"


def campaign():
    """One atomic op: write our ID only if the key doesn't exist yet."""
    lease = client.lease(ttl=10)
    won = client.transaction(
        compare=[client.transactions.version(ELECTION_KEY) == 0],
        success=[client.transactions.put(ELECTION_KEY, NODE_ID, lease=lease)],
        failure=[],
    )
    return lease if won else None


def main():
    lease = campaign()
    if lease is None:
        print("another node holds the lease — watch and retry")
        events, cancel = client.watch(ELECTION_KEY)
        for _ in events:
            break  # demo: stop after the first change
        cancel()
        return

    try:
        for _ in range(3):
            lease.refresh()      # keep the lease alive
            print("renewed lease")
            time.sleep(3)        # renew well before the TTL
    finally:
        lease.revoke()           # step down cleanly on exit
        print("resigned leadership")


if __name__ == "__main__":
    main()
