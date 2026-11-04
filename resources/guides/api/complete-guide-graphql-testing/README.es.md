# Guía Completa de Testing en GraphQL — Recursos complementarios

Estructura de tests ejecutable para la guía
[Guía Completa de Testing en GraphQL](https://stackpractices.com/es/guides/complete-guide-graphql-testing/).

## Contenido

| Archivo | Propósito |
| --- | --- |
| `src/typeDefs.js`, `src/resolvers.js` | Esquema mínimo bajo prueba |
| `tests/unit/user.resolver.test.js` | Tests unitarios de resolvers con contexto inyectado |
| `tests/integration/schema.test.js` | Ejecución `graphql()` a través del esquema |
| `tests/contract/persisted-operations.test.js` | Operaciones persistidas validadas contra el esquema candidato |
| `tests/helpers/mock-context.js` | Fábrica de contexto mock compartida |
| `package.json` | Scripts por capas: `test:unit`, `test:integration`, `test:e2e` |

## Uso

```bash
npm install
npm run test:unit
npm run test:integration
```
