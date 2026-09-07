# Mocks de resolvers GraphQL para desarrollo frontend

Código complementario para [StackPractices: Mocks de resolvers GraphQL](https://stackpractices.com/es/recipes/graphql-mocking-apollo-server/).

## Requisitos

- Node.js 20+
- `@apollo/server` 4.x
- `@faker-js/faker` 8.x
- `msw` 2.x (opcional, para mocking del lado del cliente)

## Archivos

| Archivo | Descripción |
| --------- | ------------- |
| `mock-server.ts` | Apollo Server básico con `mocks: true` |
| `custom-mocks.ts` | Mocks de escalares personalizados (ID, String, Int, Boolean) |
| `type-mocks.ts` | Mocks a nivel de tipo con faker para datos realistas |
| `env-toggle.ts` | Alternar mocking por variable de entorno |
| `custom-scalars.ts` | Mockear escalares personalizados (Date) y enums (Role) |
| `relay-pagination.ts` | Mockear paginación por cursor estilo Relay |
| `msw-handlers.ts` | Handlers de MSW 2.x para mocking GraphQL del lado del cliente |
| `seeded-mocks.ts` | Faker con seed para snapshot tests reproducibles |
| `error-mocks.ts` | Simular respuestas de error para manejo de errores en UI |

## Uso

```bash
npm install @apollo/server @faker-js/faker
npx tsx mock-server.ts
```

El servidor mock arranca en `http://localhost:4000`.
