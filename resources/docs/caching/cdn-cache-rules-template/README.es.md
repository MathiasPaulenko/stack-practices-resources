# Plantilla de reglas de caché de CDN

Código companion de [Plantilla de reglas de caché de CDN](https://stackpractices.com/es/docs/cdn-cache-rules-template/).

## Contenido

| Archivo | Qué es |
|---------|--------|
| `cloudflare-purge.py` | Helpers de purge: por URL, por cache tag y purge completo post-deploy (`purge_after_deploy`) |
| `cdn-health-check.py` | Informe de hit ratio y ancho de banda con alerta <90%, vía analytics de Cloudflare |
| `nginx-cache-headers.conf` | Headers `Cache-Control` del origin por tipo de contenido (HTML, assets versionados, API, sitemaps) |

## Cómo usarlo

- Los Python necesitan `pip install requests`; configura `CLOUDFLARE_ZONE_ID` y `CLOUDFLARE_API_TOKEN`.
- Copia los bloques de nginx a la configuración de tu origin.
