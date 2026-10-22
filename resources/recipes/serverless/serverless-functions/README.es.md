# Construir funciones serverless — Companion

Ejemplos ejecutables de la receta, probables en local sin cuenta de nube.

Artículo fuente: [Construir funciones serverless](https://stackpractices.com/es/recipes/serverless-functions/)

## Estructura

| Ruta | Qué es |
|------|--------|
| `lambda/handler.py` | Handler de AWS Lambda — corre en local e imprime la respuesta |
| `lambda/event-api-gateway.json` | Evento proxy de API Gateway para `sam local invoke` |
| `gcf/index.js` | Función HTTP de Google Cloud Functions |
| `sam/template.yaml` | Template SAM para una función disparada por S3 |
| `sam/events/s3-upload.json` | Evento S3 ObjectCreated de muestra |
| `python/event_processor.py` | El bucle de registros S3→SNS con clientes falsos — verificable offline |

## Arranque rápido

**Handler Lambda (sin AWS):** `python lambda/handler.py` — imprime `{"message": "Hello, Mathias!"}`.

**Procesador de eventos (sin AWS):** `python python/event_processor.py` — corre el bucle de registros contra fakes y verifica `processed=2`.

**GCF:** `cd gcf && npm install && npm start`, luego `curl "http://localhost:8080/?name=Mathias"`.

**SAM:** `sam local invoke ProcessUpload --event sam/events/s3-upload.json` (requiere AWS SAM CLI + Docker).

## Notas

- Truco de cold start: los clientes creados *fuera* del handler (`boto3.resource` a nivel de módulo) se reutilizan en invocaciones calientes.
- Las fuentes de eventos son at-least-once — diseña handlers idempotentes; `event_processor.py` publica un resumen seguro de re-emitir.
