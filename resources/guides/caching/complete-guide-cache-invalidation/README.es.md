# Guía Completa de Invalidación de Caché — Código de acompañamiento

Patrones ejecutables de invalidación en Redis para la guía
[Guía Completa de Invalidación de Caché](https://stackpractices.com/es/guides/complete-guide-cache-invalidation/)
de StackPractices.

## Archivos

| Archivo | Qué implementa |
| --- | --- |
| `ttl_cache.py` | TTL con jitter + config por tipo |
| `event_driven.py` | Escribir-luego-borrar + difusión pub/sub a L1 |
| `versioned_keys.py` | Claves versionadas con `.decode()` seguro |
| `tag_based.py` | Índice por tags + purga por tag |
| `multi_tier.py` | Propagación L2 + L1 vía pub/sub |
| `race_safe.py` | Lecturas con lock + doble chequeo, doble borrado diferido |
| `test_invalidation.py` | Tests con pytest (fakeredis) incl. regresión `vb'2'` |

## Puesta en marcha

```bash
pip install -r requirements.txt
pytest test_invalidation.py -v
```

`r` es un cliente Redis (`fakeredis` en tests), `db_users` tu capa de datos.
