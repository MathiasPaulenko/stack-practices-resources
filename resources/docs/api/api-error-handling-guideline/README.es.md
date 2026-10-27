# Guía de Manejo de Errores de API — Recursos complementarios

Archivos complementarios de la [Guía de Manejo de Errores de API](https://stackpractices.com/es/docs/api-error-handling-guideline/) en StackPractices.com.

## Qué incluye

| Archivo | Descripción |
|---------|-------------|
| `error-handler-express.js` | Manejador central de errores para Express.js + clase `ApiError` (listo para `app.use`) |
| `error-handler-flask.py` | Excepción `ApiError` de Flask + implementación con `@app.errorhandler` |
| `error-registry.json` | Registro de códigos de error legible por máquina — status, flags de reintento, descripciones |
| `api-client-error.js` | Consumidor tipado de errores en el cliente que respeta `Retry-After` |

## Inicio rápido

1. Mete el handler de tu stack en el proyecto y regístralo tras las rutas.
2. Importa `error-registry.json` donde se crean los errores — los códigos son constantes, no strings.
3. Extiende el registro con códigos de dominio; retíralos con `deprecated: true`, nunca los borres.
