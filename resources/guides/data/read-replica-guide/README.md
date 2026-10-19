# Read Replicas — Companion Resources

Runnable configuration and code for the guide
[Read Replicas: Scale Reads Without Changing Your App](https://stackpractices.com/guides/read-replica-guide/).

## Files

| File | Purpose |
|------|---------|
| `postgresql_primary.ini` | `postgresql.conf` + `pg_hba.conf` settings for the primary, with `pg_basebackup` bootstrap |
| `postgresql_replica.ini` | Hot-standby settings for the replica |
| `mysql_replication.cnf` | `my.cnf` for primary and replica plus `CHANGE REPLICATION SOURCE` snippet |
| `read_write_router.py` | Read/write splitting with two psycopg2 pools |
| `sqlalchemy_router.py` | SQLAlchemy session routing reads to a random replica |
| `django_router.py` | Django `DATABASE_ROUTERS` implementation |
| `SpringRoutingDataSource.java` | Spring `AbstractRoutingDataSource` routed by `@Transactional(readOnly)` |
| `lag_aware_router.py` | Lag-aware routing + read-after-write fallback to primary |
| `pgbouncer.ini` | PgBouncer multi-backend config (master + replicas as aliases) |
| `proxysql_setup.sql` | ProxySQL hostgroups and query rules for MySQL splitting |
| `replication_monitoring.sql` | Lag and health queries for PostgreSQL and MySQL |
| `prometheus_replication_alerts.yaml` | Prometheus alert rules for lag and stopped replication |

## Usage

Adjust hosts, credentials and thresholds to your environment. Start with one
replica, alert on lag from day one, and rehearse promotion before you need it.
