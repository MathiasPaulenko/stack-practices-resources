# Guía Completa de Seguridad en GraphQL

Configuración endurecida de Apollo Server 4 que acompaña a la guía:
[Guía Completa de Seguridad en GraphQL](https://stackpractices.com/es/guides/complete-guide-graphql-security/) (EN: [Complete Guide to GraphQL Security](https://stackpractices.com/guides/complete-guide-graphql-security/)).

## Archivos

| Archivo | Qué cubre |
| --- | --- |
| `server.js` | Montaje completo del servidor: Express + `expressMiddleware`, contexto de auth, rate limit, tope de body y timeouts, CORS |
| `introspection-gate.js` | Plugin que permite introspección solo a administradores, inspeccionando el AST de la operación |
| `auth-directive.js` | Directiva `@auth(requires: Role!)` vía `mapSchema` + `getDirective` (graphql-tools v8+) |
| `cost-budget.js` | Presupuesto de costo por cliente sobre Redis para rate limiting por costo de consulta |
| `package.json` | Manifiesto de dependencias con las versiones usadas |

## Instalación

```bash
npm install
export NODE_ENV=production
node server.js
```

## Qué se aplica

- `introspection` desactivada en producción, controlada por rol de administrador en el resto
- `hideSchemaDetailsFromClientErrors` para bloquear la enumeración por sugerencias
- `validationRules`: `graphql-depth-limit` + reglas de costo/alias/directivas/tokens de GraphQL Armor
- `allowBatchedHttpRequests` en su valor por defecto `false` + middleware de tope de lote
- `persistedQueries` con TTL limitado
- `express-rate-limit` por IP + presupuesto de costo por identidad en Redis
- Directiva `@auth` de autorización a nivel de campo
- Enmascarado de errores con `formatError` (Apollo Server 4; migra a hooks de plugin en v5)

Es un punto de partida, no un drop-in: conecta tu esquema real, la verificación de tokens y el cliente de Redis.
