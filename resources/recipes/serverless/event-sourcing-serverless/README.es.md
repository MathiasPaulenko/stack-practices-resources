# Event Sourcing en Arquitecturas Serverless — Código Companion

Implementación de referencia en TypeScript de las tres piezas de la
[receta event-sourcing-serverless](https://stackpractices.com/es/recipes/event-sourcing-serverless/)
de StackPractices.com:

- `sourcing/eventstore.ts` — event store append-only sobre DynamoDB con versionado
  por agregado y concurrencia optimista (`ConditionExpression`).
- `sourcing/projection.ts` — handler Lambda disparado por un DynamoDB Stream que
  enruta cada evento agregado a la proyección de lectura correspondiente. Incluye
  una nota sobre idempotencia (los streams son at-least-once).
- `sourcing/aggregate.ts` — agregado de orden reconstruido reproduciendo su
  historia de eventos, con `toSnapshot()` para cargas basadas en snapshots.
- `sourcing/eventstore.py` — el mismo event store en Python/boto3
  (`transact_write_items` + `TypeSerializer`).

## Dependencias

```bash
npm install @aws-sdk/client-dynamodb @aws-sdk/lib-dynamodb @aws-sdk/util-dynamodb
npm install -D @types/aws-lambda
```

## Notas

- Los writers de proyección en `projection.ts` son stubs — implementalos contra
  tu store de modelo de lectura (otra tabla DynamoDB, RDS, OpenSearch...).
- El layout de claves del event store es `PK = ORDER#<id>`, `SK = EVENT#<versión>`.
  Activá un DynamoDB Stream (`NEW_IMAGE`) en la tabla para alimentar la Lambda
  de proyección.
- Para agregados con historias largas, hacé snapshot cada 50–100 eventos bajo una
  clave separada (`SK = SNAPSHOT#<versión>`) y reproducí solo los eventos más nuevos.
