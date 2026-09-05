# Brotli Nginx Compression — Companion Resources

Runnable examples for the [Brotli Nginx Compression](https://stackpractices.com/recipes/brotli-nginx-compression/) recipe on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `nginx.conf` | Nginx configuration with Brotli + Gzip fallback |
| `pre-compress.sh` | Shell script to pre-compress static assets with Brotli level 11 |
| `vite-plugin-brotli.js` | Vite plugin for build-time Brotli pre-compression |
| `Dockerfile` | Multi-stage Docker build for Nginx with ngx_brotli module |
| `docker-compose.yml` | Docker Compose setup to serve static assets with Brotli |

## Quick start

```bash
# 1. Build the Docker image with Brotli support
docker build -t nginx-brotli .

# 2. Pre-compress your static assets
./pre-compress.sh /path/to/dist

# 3. Serve with Docker Compose
docker-compose up -d

# 4. Verify Brotli is working
curl -H "Accept-Encoding: br" -I http://localhost:8080/app.js
```

## Vite integration

```javascript
// vite.config.js
import brotliPlugin from './vite-plugin-brotli.js';

export default {
  plugins: [brotliPlugin()],
};
```

After `vite build`, your `dist/` directory will contain `.br` files alongside the originals.

## Verification

```bash
# Check Content-Encoding header
curl -H "Accept-Encoding: br" -I http://localhost:8080/app.js

# Compare transfer sizes
curl -s -H "Accept-Encoding: br" --compressed -o /dev/null -w "Brotli: %{size_download} bytes\n" http://localhost:8080/app.js
curl -s -H "Accept-Encoding: gzip" --compressed -o /dev/null -w "Gzip: %{size_download} bytes\n" http://localhost:8080/app.js
curl -s -H "Accept-Encoding: identity" -o /dev/null -w "Uncompressed: %{size_download} bytes\n" http://localhost:8080/app.js
```
