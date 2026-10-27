# Plantilla de Documentación de API — Recursos complementarios

Archivos complementarios de la [Plantilla de Documentación de API](https://stackpractices.com/es/docs/api-documentation/) en StackPractices.com.

## Qué incluye

| Archivo | Descripción |
|---------|-------------|
| `api-documentation-template.md` | La plantilla Markdown lista para rellenar — cópiala a tu repo y reemplaza los marcadores `[entre corchetes]` |
| `openapi-fragment.yaml` | Fragmento OpenAPI 3.1 equivalente para los endpoints GET/POST `[recurso]`, el sobre de error y la autenticación bearer |

## Inicio rápido

1. Copia `api-documentation-template.md` a `docs/api/` en tu repositorio.
2. Reemplaza `[recurso]`, `[Service Name]` y `api.example.com` con tus valores.
3. Mete `openapi-fragment.yaml` en tu spec, extiéndelo por endpoint y pásale lint en CI (`spectral lint`).
