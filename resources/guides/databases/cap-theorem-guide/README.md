# CAP Theorem Lab

Companion files for the guide [CAP Theorem and Database Trade-offs](https://stackpractices.com/guides/cap-theorem-guide/).

A small, runnable lab to see the CP/AP trade-off instead of just reading about it: a 3-node etcd cluster you can partition with one script, plus the consistency-tuning snippets the guide uses for PostgreSQL, Cassandra and MongoDB.

## Contents

| File | What it shows |
| ---- | ------------- |
| `docker-compose.yml` | 3-node etcd cluster (PC/EC — needs quorum to write) |
| `simulate-partition.sh` | Cut/heal a node from the cluster network, check quorum |
| `postgresql.conf` | Synchronous replication: CP trade-off for Postgres |
| `notifications.cql` | Cassandra keyspace/table: AP setup with tunable consistency |
| `mongo_consistency.js` | MongoDB `writeConcern` / `readConcern` / `readPreference` examples |

## Run the etcd partition lab

```bash
docker compose up -d

# write through the majority side
./simulate-partition.sh write

# isolate etcd3 — the minority side
./simulate-partition.sh cut etcd3

# majority side (etcd1+etcd2) still has quorum
./simulate-partition.sh status

# writes to the isolated node fail: no quorum on its side
docker exec etcd3 etcdctl put isolated-write nope   # times out / errors

# heal and watch it catch up via Raft
./simulate-partition.sh heal etcd3
```

What you just saw: the majority partition keeps serving because it holds quorum (CP). The isolated node refuses consensus operations rather than diverge — availability sacrificed for consistency.

Try it again cutting two nodes (`cut etcd2` then `cut etcd3`): now no side has quorum and every write fails. That is the theorem, not a bug.

## Adapting it

- Asymmetric partitions need `iptables`/`tc` inside the containers — `docker network disconnect` produces a full cut only.
- The same script pattern works for a MongoDB replica set or a Cassandra multi-DC cluster if you swap the compose services.
- `simulate-partition.sh` targets Docker's bridge network naming; if your compose project name differs, adjust `NETWORK`.
