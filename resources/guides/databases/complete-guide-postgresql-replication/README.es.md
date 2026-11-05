# Replicación en PostgreSQL — Archivos Companion

Companion ejecutable de la guía
[Guía Completa de Replicación en PostgreSQL](https://stackpractices.com/es/guides/complete-guide-postgresql-replication/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `docker-compose.yml` | Laboratorio local: primario PostgreSQL 16 + réplica streaming que se autoinicializa con `pg_basebackup` |
| `postgresql-primary.conf` | Configuración del primario para replicación streaming, con notas de reinicio vs reload |
| `postgresql-replica.conf` | Configuración hot-standby (`hot_standby_feedback`, `max_standby_streaming_delay`) |
| `pg_hba.conf` | Reglas de acceso solo para replicación (`hostssl` + `scram-sha-256`, sin SSL rechazado) |
| `01-create-replication-user.sql` | Crea el rol `replicator` y el slot físico `replica1_slot` |
| `patroni.yml` | Plantilla de cluster Patroni + etcd de tres nodos para failover automático |
| `monitoring-queries.sql` | Las consultas de lag, slots y wal-receiver de la guía, listas para ejecutar |

## Inicio rápido — laboratorio de réplica streaming

```bash
docker compose up -d

# Observa cómo se conecta la réplica y comprueba el estado en el primario
docker compose exec primary psql -U postgres \
  -c "SELECT application_name, state, sync_state FROM pg_stat_replication;"

# Escribe en el primario y léelo en la réplica
docker compose exec primary psql -U postgres -c "CREATE TABLE t(i int); INSERT INTO t VALUES (1);"
docker compose exec replica psql -U postgres -c "SELECT * FROM t;"
```

El servicio de la réplica vacía su directorio de datos y repite `pg_basebackup -R`
en cada arranque: es un laboratorio, no un setup de producción. `PGPASSWORD` en
`docker-compose.yml` debe coincidir con la contraseña de `01-create-replication-user.sql`.

## Cluster Patroni

`patroni.yml` es por nodo: cópialo a cada uno de los tres hosts, ajusta `name`,
`connect_address` y apunta `etcd.hosts` a tu DCS. Consulta la sección
*Failover con Patroni* de la guía para afinar `ttl`, `loop_wait` y
`maximum_lag_on_failover`.

## Notas de seguridad

- Cambia todas las contraseñas `change_me_before_production`.
- En producción no pongas la contraseña de replicación en `primary_conninfo`:
  usa `.pgpass` (permisos 0600) o un gestor de secretos.
- `pg_hba.conf` rechaza la replicación sin SSL; emite los certificados antes de activarlo.
