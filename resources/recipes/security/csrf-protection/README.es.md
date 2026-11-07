# Protección CSRF — Ejemplos complementarios

Ejemplos ejecutables de la receta [Protección CSRF para formularios web](https://stackpractices.com/es/recipes/csrf-protection/).

## Contenido

- `csrf-middleware.js` — middleware Express que implementa el patrón **cookie double-submit firmada**: emite una cookie de token con firma HMAC y verifica el header `X-CSRF-Token` en cada petición que muta estado, con comparación en tiempo constante.
- `demo-server.js` — servidor Express mínimo que conecta el middleware con un formulario de prueba que lee la cookie y devuelve el token en el header.

## Ejecutar

```bash
npm install express cookie-parser
CSRF_SECRET=dev-secret node demo-server.js
# abrir http://localhost:3000
```

Enviar el formulario dispara `POST /api/transfer` con el header del token — un 200. Repite el mismo POST sin el header (desde curl o una página cross-site) y obtienes un 403.

## Qué demuestra

- Emisión de tokens con firma HMAC (stateless — sin almacenamiento en servidor).
- `SameSite=Strict` + `Secure` en la cookie del token.
- `crypto.timingSafeEqual` con verificación de longitud: las cookies falsificadas reciben 403, no 500.
- Por qué un header personalizado vence a la falsificación cross-site: los navegadores nunca ponen `X-CSRF-Token` en peticiones cross-site con credenciales.
