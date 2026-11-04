# Guía Completa de Diseño de Esquemas GraphQL — Recursos complementarios

Archivos de referencia de la guía
[Guía Completa de Diseño de Esquemas GraphQL](https://stackpractices.com/es/guides/complete-guide-graphql-schema-design/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `schema.graphql` | SDL completo: interfaces, enums, connections, mutaciones input/payload, deprecation |
| `.graphql-schema-linterrc` | Reglas del linter que aplican las convenciones de la guía |
| `resolvers.ts` | Mutación con errores en payload + fábrica de DataLoader por petición |

## Uso

- Lleva `schema.graphql` a un proyecto schema-first o úsalo como material de revisión.
- Ejecuta el linter: `npx graphql-schema-linter schema.graphql`.
- `resolvers.ts` muestra los dos patrones que recomienda la guía: errores
  estructurados en payloads y batching con DataLoader con ámbito de petición.
