# Guía Completa de Estrategia de Caché en CDN — Código de acompañamiento

Bloques ejecutables para la guía
[Guía Completa de Estrategia de Caché en CDN](https://stackpractices.com/es/guides/complete-guide-cdn-caching-strategy/)
de StackPractices.

## Archivos

| Archivo | Qué implementa |
| --- | --- |
| `nginx-cache-headers.conf` | Matriz de headers por tipo de contenido |
| `worker-cache-key-normalizer.js` | Worker de Cloudflare: quita params de tracking |
| `surrogate_key_purge.py` | Purga por surrogate key (Fastly) y por URL (Cloudflare) |
| `event_purge.py` | Purga tras escribir (invalidación por eventos) |
| `hit_ratio.py` | Calculadora de hit ratio + objetivos por tipo |
| `cdn_failover.sh` | Failover DNS Route53 con health check |
| `test_hit_ratio.py` | Tests de humo con pytest |

## Puesta en marcha

```bash
pip install -r requirements.txt
pytest test_hit_ratio.py -v
```

Las claves API vienen de variables de entorno (`FASTLY_API_KEY`, `CF_API_TOKEN`); `db_products` es tu capa de datos.
