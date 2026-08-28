# Database Read Replicas Companion Resources

Companion resource for [Set Up Database Read Replicas for Scaling](https://stackpractices.com/recipes/database-read-replicas/).

## Files

- `routing_session.py` — SQLAlchemy read/write splitting session for PostgreSQL.
- `go_router.go` — Go SQL driver router with round-robin replica selection.
- `django_routers.py` — Django database routers (single replica and round-robin).
- `pgbouncer.ini` — PgBouncer configuration for connection pooling with replicas.
- `proxysql_setup.sql` — ProxySQL setup for MySQL read/write splitting.
- `read_after_write.py` — Read-after-write handler with replication lag fallback.
- `lag_monitoring.sql` — Replication lag monitoring queries for PostgreSQL and MySQL.
- `requirements.txt` — Python dependencies.

## Usage

### Python (SQLAlchemy)

```bash
pip install -r requirements.txt
python routing_session.py
```

### Python (read-after-write)

```bash
python read_after_write.py
```

### Go

```bash
go mod init db
go get github.com/lib/pq
# Use go_router.go in your application
```

### PgBouncer

```bash
sudo cp pgbouncer.ini /etc/pgbouncer/pgbouncer.ini
sudo systemctl restart pgbouncer
```

### ProxySQL

```bash
mysql -h 127.0.0.1 -P 6032 -u admin -p < proxysql_setup.sql
```
