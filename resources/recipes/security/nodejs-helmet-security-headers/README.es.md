# Headers de Seguridad con Helmet — Código complementario

App Express ejecutable con headers de seguridad de Helmet 8, de la receta de StackPractices:
[Configura headers de seguridad HTTP con Helmet en Node.js](https://stackpractices.com/es/recipes/nodejs-helmet-security-headers/)

## Archivos

| Archivo | Propósito |
| --- | --- |
| `app.js` | App Express con CSP, HSTS, X-Frame-Options y CORS de Helmet configurados |
| `server.js` | Punto de entrada — escucha en `PORT` (3000 por defecto) |
| `headers.test.js` | Suite Jest + supertest que verifica cada header de seguridad |
| `package.json` | Dependencias: express 4, helmet 8, cors; devDeps: jest, supertest |

## Ejecutar

```bash
npm install
npm start          # http://localhost:3000
npm test           # ejecuta las aserciones de headers
```

Verifica los headers contra el servidor en ejecución:

```bash
curl -sI http://localhost:3000 | grep -iE "strict-transport|x-frame|x-content|content-security"
```
