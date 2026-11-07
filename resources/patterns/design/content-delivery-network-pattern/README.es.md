# Patrón Content Delivery Network (CDN) — Código complementario

Snippets ejecutables del
[Patrón Content Delivery Network (CDN)](https://stackpractices.com/es/patterns/content-delivery-network-pattern/)
en StackPractices. Las tres piezas móviles de un despliegue CDN: la distribución,
los headers cache-control y la ruta de invalidación.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `invalidate_cache.mjs` | Invalidación de CloudFront con AWS SDK v3 — llámalo desde tu pipeline de deploy para purgar paths o wildcards |
| `cdn_manager.py` | `CDNManager` con warmup de cache en paralelo, purge y verificación HIT/MISS (headers `X-Cache`, `Age`) |
| `cloudfront.tf` | Distribución CloudFront en Terraform — orígenes S3 + ALB, tres cache behaviors, TLS 1.2, compresión |
| `cache-control-headers.http` | Recetas de `Cache-Control` por tipo de contenido: assets con fingerprint, HTML, personalizado, APIs |

## Requisitos

- `invalidate_cache.mjs`: Node 18+ y `@aws-sdk/client-cloudfront`
- `cdn_manager.py`: Python 3.10+ y `requests`
- `cloudfront.tf`: Terraform 1.x con el provider AWS y los recursos referenciados (`aws_s3_bucket.assets`, `aws_lb.main`, `aws_acm_certificate.cdn`, `aws_cloudfront_origin_access_identity.oai`)

## Uso

```bash
# Purgar paths después de un deploy
node invalidate_cache.mjs

# Calentar los caches edge y verificar HIT/MISS
python cdn_manager.py

# Planificar la distribución
terraform plan
```
