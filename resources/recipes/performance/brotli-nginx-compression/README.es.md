# Compresión Brotli en Nginx — Recursos Companion

Ejemplos ejecutables para la receta [Compresión Brotli en Nginx](https://stackpractices.com/es/recipes/brotli-nginx-compression/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `nginx.conf` | Configuración de Nginx con Brotli + fallback Gzip |
| `pre-compress.sh` | Script de shell para pre-comprimir assets estáticos con Brotli nivel 11 |
| `vite-plugin-brotli.js` | Plugin de Vite para pre-compresión Brotli en build time |
| `Dockerfile` | Build Docker multi-stage para Nginx con módulo ngx_brotli |
| `docker-compose.yml` | Setup de Docker Compose para servir assets estáticos con Brotli |

## Inicio rápido

```bash
# 1. Buildear la imagen Docker con soporte Brotli
docker build -t nginx-brotli .

# 2. Pre-comprimir tus assets estáticos
./pre-compress.sh /path/to/dist

# 3. Servir con Docker Compose
docker-compose up -d

# 4. Verificar que Brotli funciona
curl -H "Accept-Encoding: br" -I http://localhost:8080/app.js
```

## Integración con Vite

```javascript
// vite.config.js
import brotliPlugin from './vite-plugin-brotli.js';

export default {
  plugins: [brotliPlugin()],
};
```

Después de `vite build`, tu directorio `dist/` contendrá archivos `.br` junto a los originales.

## Verificación

```bash
# Checkear el header Content-Encoding
curl -H "Accept-Encoding: br" -I http://localhost:8080/app.js

# Comparar tamaños de transferencia
curl -s -H "Accept-Encoding: br" --compressed -o /dev/null -w "Brotli: %{size_download} bytes\n" http://localhost:8080/app.js
curl -s -H "Accept-Encoding: gzip" --compressed -o /dev/null -w "Gzip: %{size_download} bytes\n" http://localhost:8080/app.js
curl -s -H "Accept-Encoding: identity" -o /dev/null -w "Sin comprimir: %{size_download} bytes\n" http://localhost:8080/app.js
```
