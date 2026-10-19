# Réplicas de Lectura — Recursos Complementarios

Configuración y código ejecutable para la guía
[Réplicas de Lectura: Escala Lecturas Sin Tocar tu App](https://stackpractices.com/es/guides/read-replica-guide/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `postgresql_primary.ini` | Ajustes de `postgresql.conf` + `pg_hba.conf` para el primario, con bootstrap `pg_basebackup` |
| `postgresql_replica.ini` | Ajustes de hot standby para la réplica |
| `mysql_replication.cnf` | `my.cnf` para primario y réplica más el fragmento `CHANGE REPLICATION SOURCE` |
| `read_write_router.py` | Separación lectura/escritura con dos pools de psycopg2 |
| `sqlalchemy_router.py` | Sesión de SQLAlchemy que enruta lecturas a una réplica aleatoria |
| `django_router.py` | Implementación de `DATABASE_ROUTERS` en Django |
| `SpringRoutingDataSource.java` | `AbstractRoutingDataSource` de Spring enrutado por `@Transactional(readOnly)` |
| `lag_aware_router.py` | Enrutamiento consciente del lag + fallback al primario tras escritura |
| `pgbouncer.ini` | Config multi-backend de PgBouncer (primario + réplicas como alias) |
| `proxysql_setup.sql` | Hostgroups y reglas de consultas de ProxySQL para separación en MySQL |
| `replication_monitoring.sql` | Consultas de lag y salud para PostgreSQL y MySQL |
| `prometheus_replication_alerts.yaml` | Reglas de alertas de Prometheus para lag y replicación detenida |

## Uso

Ajusta hosts, credenciales y umbrales a tu entorno. Empieza con una réplica,
alerta sobre el lag desde el día uno y ensaya la promoción antes de necesitarla.
