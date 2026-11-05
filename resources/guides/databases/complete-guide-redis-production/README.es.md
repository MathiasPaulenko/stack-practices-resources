# Redis en Producción — Configuraciones

Archivos de configuración de producción para la [Guía de Redis en Producción](https://stackpractices.com/es/guides/complete-guide-redis-production/).

## Archivos

-  — redis.conf endurecido: bind, auth, maxmemory+expulsión, AOF+RDB, comandos peligrosos renombrados.
-  — configuración mínima de quórum de 3 sentinels para failover automático.
-  — snapshot de salud: memoria, hit rate, expulsiones, lag de replicación, slow log.
-  — BGSAVE en una réplica + copia fuera de la máquina.

Ajusta , ,  y los hostnames antes de usar.
