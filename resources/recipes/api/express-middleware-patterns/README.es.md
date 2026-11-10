# Patrones de Composición de Middleware en Express

Demo sin dependencias de los cinco patrones de composición de la receta, implementada sobre `node:http` para correr en cualquier lado — sin `npm install`. El modelo de middleware replica el contrato `(req, res, next)` de Express, así que el código se porta directamente.

## Archivos

| Archivo | Qué muestra |
|---------|-------------|
| `middleware_pipeline.js` | `compose()` aplanando stacks de middleware, `asyncHandler()` reenviando rejections, contexto de request con `AsyncLocalStorage` y trace IDs, error handler unificado y un mini validador de schema — todo dentro de un servidor `node:http` funcional |
| `pipeline.test.js` | `node:test` + `fetch` ejercitando el pipeline real: happy path, fallo de validación (400), mapeo de `AppError` (403) y captura de rejection no manejada (500) con propagación de trace ID |

## Ejecutar

```bash
node middleware_pipeline.js   # levanta el servidor en :3000
node --test pipeline.test.js  # corre la suite de integración
```

Pruébalo:

```bash
curl -i http://localhost:3000/users/1
curl -i -X POST http://localhost:3000/users -d '{"name": 42}'
curl -i -H "X-Trace-Id: my-trace" http://localhost:3000/users/1  # el trace vuelve en el header
```

Fuente: https://stackpractices.com/recipes/express-middleware-patterns/
