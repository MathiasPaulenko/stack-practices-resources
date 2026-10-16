# Pooling de Conexiones — Recursos complementarios

Configuraciones ejecutables referenciadas en
[Pooling de Conexiones a Base de Datos: Guía Práctica](https://stackpractices.com/es/guides/connection-pooling-deep-dive-guide/).

| Archivo | Propósito |
| --- | --- |
| `pgbouncer.ini` | Config de PgBouncer en modo transaction con pool de reserva y notas de consola admin |
| `HikariPoolConfig.java` | Setup de referencia de HikariCP: dimensionamiento, timeouts, detección de fugas, caché de prepared statements |
| `pool_sqlalchemy.py` | Engine de SQLAlchemy con `pool_size`, `pre_ping` y ejemplo de antipatrón de fuga |
| `pool_monitor.py` | Exportador de métricas de pool a Prometheus (activas/inactivas/waiters/timeouts) |
| `lambda-pool.js` | Pool reutilizado en caliente para AWS Lambda apuntando a un proxy |

Regla práctica usada en toda la guía: `pool_size × instancias < max_connections − margen`,
o pon PgBouncer delante y trata el pool de la app como limitador de concurrencia.
