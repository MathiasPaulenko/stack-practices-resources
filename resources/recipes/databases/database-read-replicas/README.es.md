# Recursos Companion de Read Replicas de Base de Datos

Recurso companion para [Configurar Read Replicas de Base de Datos para Escalado](https://stackpractices.com/es/recipes/database-read-replicas/).

## Archivos

- `routing_session.py` — Sesión de SQLAlchemy con split de lectura/escritura para PostgreSQL.
- `go_router.go` — Router de Go SQL driver con selección round-robin de réplicas.
- `django_routers.py` — Routers de Django (réplica única y round-robin).
- `pgbouncer.ini` — Configuración de PgBouncer para connection pooling con réplicas.
- `proxysql_setup.sql` — Configuración de ProxySQL para split lectura/escritura en MySQL.
- `read_after_write.py` — Handler de lectura-después-de-escritura con fallback por lag.
- `lag_monitoring.sql` — Queries de monitoreo de replication lag para PostgreSQL y MySQL.
- `requirements.txt` — Dependencias de Python.

## Uso

### Python (SQLAlchemy)

```bash
pip install -r requirements.txt
python routing_session.py
```

### Python (lectura-después-de-escritura)

```bash
python read_after_write.py
```

### Go

```bash
go mod init db
go get github.com/lib/pq
# Usa go_router.go en tu aplicación
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
