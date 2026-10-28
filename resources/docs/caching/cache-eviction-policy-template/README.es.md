# Plantilla de política de eviction de caché

Código companion de [Plantilla de política de eviction de caché](https://stackpractices.com/es/docs/cache-eviction-policy-template/).

## Contenido

| Archivo | Qué es |
|---------|--------|
| `redis-local.conf` | Config de Redis local L2: `allkeys-lru`, 4 GB de `maxmemory` |
| `redis-cluster.conf` | Config de cluster compartido L3: `volatile-ttl`, 32 GB |
| `monitor_eviction.py` | Monitor de tasa de eviction y memoria con umbrales de alerta (`evicted_keys`, hit rate, uso %) |

## Cómo usarlo

- Copia un conf a tu despliegue de Redis y ajusta `maxmemory` al host (máx. ~75% de la RAM).
- `python monitor_eviction.py` — necesita `pip install redis` y una instancia accesible.
