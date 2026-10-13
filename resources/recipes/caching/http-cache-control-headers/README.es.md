# Headers HTTP Cache-Control — Archivos complementarios

Configuraciones funcionales de los patrones principales de la receta: caché `immutable` de larga duración para assets hasheados, `max-age` corto con `stale-while-revalidate` para respuestas de API públicas, peticiones condicionales con `ETag` y `Last-Modified`, y `no-store`/`private` para datos sensibles.

Artículo original: [Headers HTTP Cache-Control para APIs y assets](https://stackpractices.com/es/recipes/http-cache-control-headers/)

## Archivos

| Archivo | Rol |
|------|------|
| `nginx.conf` | Bloque server con `Cache-Control` por location: assets `immutable`, HTML `no-cache`, API con `stale-while-revalidate`, rutas auth `private`/`no-store`. |
| `express-cache-headers.js` | App Express con todas las variantes: `maxAge` estático, respuestas condicionales con ETag, comparación de fechas con `Last-Modified`, `s-maxage` dividido, `Vary`. |
| `fastapi-cache-headers.py` | App FastAPI con un middleware que pone `Cache-Control` en `/static/` (porque `StaticFiles` no acepta `max_age`) más un ejemplo de ETag. |

## Uso

```bash
# Express (Node 18+)
npm install express
node express-cache-headers.js
curl -I http://localhost:3000/api/products            # ver Cache-Control + ETag
curl -I -H 'If-None-Match: "<etag>"' http://localhost:3000/api/products  # 304

# FastAPI
pip install fastapi uvicorn
uvicorn fastapi-cache-headers:app
curl -I http://localhost:8000/api/products

# nginx — copia el bloque server en tu config y recarga
nginx -t && nginx -s reload
curl -I http://localhost/api/products
```

Verifica los headers con `curl -I` o la pestaña Network de DevTools: busca `Cache-Control`, `ETag`, `Last-Modified`, `Age` y `X-Cache`.
