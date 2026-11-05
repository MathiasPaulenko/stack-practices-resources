# Estrategias de Caché con Redis — Ejemplos

Implementaciones en Python ejecutables de los cinco patrones de caché Redis cubiertos en
[Guía completa de estrategias de caché con Redis](https://stackpractices.com/es/guides/complete-guide-redis-caching-strategies/).

## Instalación

```bash
pip install -r requirements.txt
redis-server  # o apunta REDIS_URL a tu instancia
```

## Archivos

- `caching_patterns.py` — los cinco patrones en un solo módulo:
  - `get_user` / `update_user` — cache-aside con TTL e invalidación
  - `get_user_safe` — cache-aside con lock anti-estampida acotado
  - `ReadThroughCache` — la capa de caché es dueña del miss
  - `WriteThroughCache` — escrituras síncronas DB-luego-caché
  - `write_behind_set` + `flush_worker` — escrituras async por lotes con logging
  - `refresh_ahead` — refresco proactivo antes del vencimiento del TTL vía `scan_iter`
  - `set_with_jitter` — jitter de TTL para evitar expiraciones sincronizadas

Los ejemplos esperan un objeto `db` con `users.find_by_id()` / `users.update()`
— sustituye por tu ORM o repositorio. Requiere `redis-py >= 4.1`.
