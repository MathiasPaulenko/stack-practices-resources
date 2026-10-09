# CDN Edge Caching — Código complementario

Configuración de edge caching multi-proveedor para Cloudflare, AWS
CloudFront y Fastly. Fuente: <https://stackpractices.com/es/recipes/cdn-edge-caching/>

## Archivos

| Archivo | Proveedor | Qué hace |
| --- | --- | --- |
| `cloudfront.tf` | AWS CloudFront | Distribución + cache policy con `parameters_in_cache_key` vacío — headers, cookies y query strings excluidos para mantener alto el hit ratio |
| `cloudflare-cache-rules.sh` | Cloudflare | Crea un ruleset de zona (fase `http_request_cache_settings`) que fija un TTL edge de 30 días para assets estáticos |
| `fastly.vcl` | Fastly | `vcl_recv`/`vcl_fetch` que marcan extensiones estáticas como inmutables + `Surrogate-Key: static` para purgas acotadas |
| `purge.sh` | Los tres | Purga por ruta (CloudFront), URL (Cloudflare) o surrogate key (Fastly) |

## Uso

```bash
# CloudFront
terraform plan && terraform apply
aws cloudfront create-invalidation --distribution-id E1EXAMPLE --paths "/assets/*"

# Cloudflare
export ZONE_ID=... API_TOKEN=...
./cloudflare-cache-rules.sh

# Fastly
# sube fastly.vcl a la versión de tu servicio, luego:
./purge.sh fastly static
```

## Notas

- Las Page Rules están deprecadas; el script de Cloudflare usa el Ruleset Engine.
- La purga por tags de Cloudflare requiere plan Enterprise; el script purga por URL.
- `stale-while-revalidate` / `stale-if-error` van en el header
  `Cache-Control` del origen, no en la configuración de la CDN.
