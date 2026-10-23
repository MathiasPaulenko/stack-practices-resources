# Encabezados de seguridad para APIs — Recursos complementarios

Herramienta complementaria de la [receta de headers de seguridad para APIs](https://stackpractices.com/es/recipes/api-security-headers/) de StackPractices.

## Contenido

- `audit-headers.sh` — Script Bash que obtiene los headers de respuesta de una URL con `curl` e informa headers de seguridad faltantes, directivas CSP débiles (`unsafe-inline`, `unsafe-eval`) y un HSTS deshabilitado (`max-age=0`).

## Uso

```bash
chmod +x audit-headers.sh
./audit-headers.sh https://tu-dominio.com
```

Ejemplo de salida:

```text
Auditing: https://tu-dominio.com
-----------------------------------
OK: strict-transport-security = max-age=63072000; includeSubDomains
MISSING: content-security-policy
OK: x-content-type-options = nosniff
OK: x-frame-options = DENY
OK: referrer-policy = strict-origin-when-cross-origin
OK: permissions-policy = geolocation=(), microphone=()
OK: cross-origin-opener-policy = same-origin
OK: cross-origin-resource-policy = same-origin
WARNING: CSP contains 'unsafe-inline'
```

Requiere `curl` y `grep`: disponibles en macOS, Linux y Git Bash en Windows.
