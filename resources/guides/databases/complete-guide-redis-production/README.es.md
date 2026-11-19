# Redis en Producción — Configuraciones

Archivos de configuración de producción para la [Guía de Redis en Producción](https://stackpractices.com/es/guides/complete-guide-redis-production/).

## Archivos

- `redis-prod.conf` — redis.conf endurecido: bind, auth, maxmemory+expulsión, AOF+RDB, comandos peligrosos renombrados.
- `sentinel.conf` — configuración mínima de quórum de 3 procesos Sentinel para failover automático.
- `monitor.sh` — snapshot de salud: memoria, hit rate, expulsiones, lag de replicación, slow log.
- `backup.sh` — BGSAVE en una réplica + copia fuera de la máquina.

Ajusta `requirepass`, `maxmemory`, `bind` y los hostnames antes de usar.
