# Patrón Gatekeeper — Recursos Companion

Ejemplos ejecutables del [patrón Gatekeeper](https://stackpractices.com/es/patterns/gatekeeper-pattern/) en StackPractices.

El patrón coloca un único punto de inspección en el borde del sistema: bloqueo de rutas, rate limiting, detección de inyección y autenticación JWT corren antes de que cualquier petición toque un servicio backend. Los rechazos se mapean a códigos distintos (403 / 429 / 400 / 401) para que los patrones de ataque aparezcan en el monitoreo.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `gatekeeper.py` | Clase `Gatekeeper` sin frameworks en Python — cuatro capas de inspección más un firmante/verificador JWT HS256 mínimo sobre `hmac` de la stdlib |
| `test_gatekeeper.py` | Suite pytest: 8 tests que cubren cada ruta de rechazo, rutas públicas que omiten auth, y tokens falsificados/expirados |
| `gatekeeper.js` | El mismo validador en JavaScript, con métodos `check*()` por capa que un stack de middleware puede llamar individualmente |
| `gatekeeper.test.js` | Suite `node:test`: 10 tests para la clase más el pipeline estilo Express |
| `express_app.js` | Las capas como middleware estilo Express con un motor `(req, res, next)` sin dependencias — funciona igual en Express real |

## Ejecutar

```bash
# Demo + tests Python
python gatekeeper.py
python -m pytest test_gatekeeper.py -v

# Demo + tests JavaScript (Node 18+)
node gatekeeper.js
node --test gatekeeper.test.js

# Servidor estilo Express
node express_app.js   # luego curl http://localhost:3000/api/public/products
```

## Ideas clave

- Rechazo más barato primero: bloqueo de rutas, luego rate limiting, luego detección de inyección, luego JWT — un token falsificado nunca quema una comprobación de firma que no necesita.
- Las rutas públicas (`/api/public/*`, `/health`) omiten solo la *autenticación* — el resto de capas sigue aplicando.
- El secret JWT viene de `GATEKEEPER_JWT_SECRET`; los demos usan un fallback `dev-secret-for-demo-only`, los ejemplos del artículo fallan al arrancar en su lugar — nunca despliegues ninguno de los dos patrones con un secret real en el archivo.
- `checkAuth` adjunta el payload verificado a `req.user`, así los manejadores aguas abajo reciben la identidad gratis.
- Los contadores de rate limit viven en memoria del proceso aquí; cambia el map por Redis antes de ejecutar más de una réplica.

CI: `.github/workflows/test.yml` ejecuta ambas suites de tests en cada cambio a esta carpeta.
