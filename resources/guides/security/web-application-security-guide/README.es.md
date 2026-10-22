# Seguridad de Aplicaciones Web (OWASP Top 10)

Archivos complementarios de la guía [Seguridad de Aplicaciones Web (OWASP Top 10)](https://stackpractices.com/es/guides/web-application-security-guide/).

Piezas ejecutables para los controles que cubre la guía — sin dependencias más allá de Node y la stdlib de Python.

## Contenido

| Archivo | Item OWASP | Qué hace |
| ------- | ---------- | -------- |
| `headers_server.js` | A05 | Servidor Node sin deps que envía el set completo de security headers |
| `security_headers.conf` | A05 | Snippet nginx: headers, restricción de métodos, `server_tokens off` |
| `ssrf_safe_fetch.py` | A10 | Allowlist de host + scheme + IP resuelta antes de cualquier fetch |
| `dependency_scan.sh` | A06 | Ejecuta `npm audit` / `pip-audit` / `snyk test` donde existan |

## Ejecutar

```bash
# Security headers — luego curl -i http://localhost:3000/
node headers_server.js

# Demo del allowlist SSRF (solo stdlib — imprime BLOCKED/ALLOWED por URL)
python ssrf_safe_fetch.py

# Auditoría de dependencias (déjalo en la raíz del proyecto o en CI)
bash dependency_scan.sh
```

`ssrf_safe_fetch.py` valida seis URLs: una permitida (`api.github.com` — el fetch real puede fallar sin red, la validación corre igual) y cinco bloqueadas (scheme http, host fuera de allowlist, IP de metadata de AWS, loopback, `file://`).

## Notas

- La CSP en `headers_server.js`/`security_headers.conf` es un punto de partida — ajusta `default-src 'self'` a lo que la app realmente carga.
- `security_headers.conf` va dentro de un bloque `server {}` de nginx o en un include; combínalo con el redirect HTTP→HTTPS del comentario.
- El chequeo SSRF resuelve el hostname y rechaza IPs no globales, cubriendo los trucos de endpoint de metadata y DNS rebinding que explica la guía.
