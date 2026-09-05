# Patrón de Entidades Federadas en GraphQL — Recursos Companion

Ejemplos ejecutables para el [Patrón de Entidades Federadas en GraphQL](https://stackpractices.com/es/patterns/graphql-federated-entity-pattern/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `users-service.ts` | Subgraph base que posee `User.id`, `User.name`, `User.email` |
| `orders-service.ts` | Subgraph extensor que agrega `User.orders` |
| `reviews-service.ts` | Subgraph extensor que agrega `User.reviews` |
| `gateway.ts` | Apollo Gateway que compone los tres subgraphs |
| `client-query.graphql` | Query federada de ejemplo |
| `docker-compose.yml` | Docker Compose con todos los servicios |
| `package.json` | Dependencias |

## Inicio rápido

```bash
npm install
npx tsx users-service.ts &
npx tsx orders-service.ts &
npx tsx reviews-service.ts &
npx tsx gateway.ts
# Gateway listo en http://localhost:4000/graphql
```

### Docker Compose

```bash
docker-compose up -d
# Gateway en http://localhost:4000/graphql
```

## Testing

```bash
# Query al gateway por un usuario con órdenes y reseñas
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: \"1\") { id name email orders { id total } reviews { id rating comment } } }"}'
```

Respuesta esperada:

```json
{
  "data": {
    "user": {
      "id": "1",
      "name": "Ada Lovelace",
      "email": "ada@example.com",
      "orders": [{"id": "o1", "total": 99.9}, {"id": "o2", "total": 45.5}],
      "reviews": [{"id": "r1", "rating": 5, "comment": "Excellent"}, {"id": "r2", "rating": 3, "comment": "OK"}]
    }
  }
}
```
