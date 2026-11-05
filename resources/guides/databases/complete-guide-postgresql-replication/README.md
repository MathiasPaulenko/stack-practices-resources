# PostgreSQL Replication — Companion Files

Runnable companion for the guide
[Complete Guide to PostgreSQL Replication](https://stackpractices.com/guides/complete-guide-postgresql-replication/).

## Contents

| File | Purpose |
| --- | --- |
| `docker-compose.yml` | Local lab: PostgreSQL 16 primary + streaming replica that bootstraps itself with `pg_basebackup` |
| `postgresql-primary.conf` | Primary settings for streaming replication, with restart vs reload notes |
| `postgresql-replica.conf` | Hot-standby settings (`hot_standby_feedback`, `max_standby_streaming_delay`) |
| `pg_hba.conf` | Replication-scoped access rules (`hostssl` + `scram-sha-256`, non-SSL rejected) |
| `01-create-replication-user.sql` | Creates the `replicator` role and the `replica1_slot` physical slot |
| `patroni.yml` | Three-node Patroni + etcd cluster template for automatic failover |
| `monitoring-queries.sql` | The lag, slot, and wal-receiver queries from the guide, ready to run |

## Quick start — streaming replica lab

```bash
docker compose up -d

# Watch the replica connect, then check status on the primary
docker compose exec primary psql -U postgres \
  -c "SELECT application_name, state, sync_state FROM pg_stat_replication;"

# Write on the primary, read it back on the replica
docker compose exec primary psql -U postgres -c "CREATE TABLE t(i int); INSERT INTO t VALUES (1);"
docker compose exec replica psql -U postgres -c "SELECT * FROM t;"
```

The replica service wipes its data directory and re-runs `pg_basebackup -R`
on every start — it's a lab, not a production setup. `PGPASSWORD` in
`docker-compose.yml` must match the password in `01-create-replication-user.sql`.

## Patroni cluster

`patroni.yml` is per-node: copy it to each of the three hosts, adjust `name`,
`connect_address`, and point `etcd.hosts` at your DCS. See the guide's
*Failover with Patroni* section for `ttl`, `loop_wait`, and
`maximum_lag_on_failover` tuning.

## Security notes

- Change every `change_me_before_production` password.
- In production keep the replication password out of `primary_conninfo` —
  use `.pgpass` (mode 0600) or a secrets manager.
- `pg_hba.conf` rejects non-SSL replication; issue certs before enabling it.
