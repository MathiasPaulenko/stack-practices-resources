# GraphQL Federated Entity Pattern — Companion Resources

Runnable examples for the [GraphQL Federated Entity Pattern](https://stackpractices.com/patterns/graphql-federated-entity-pattern/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `users-service.ts` | Base subgraph owning `User.id`, `User.name`, `User.email` |
| `orders-service.ts` | Extending subgraph adding `User.orders` |
| `reviews-service.ts` | Extending subgraph adding `User.reviews` |
| `gateway.ts` | Apollo Gateway composing all three subgraphs |
| `client-query.graphql` | Example federated query |
| `docker-compose.yml` | Docker Compose with all services |
| `package.json` | Dependencies |

## Quick start

```bash
npm install
npx tsx users-service.ts &
npx tsx orders-service.ts &
npx tsx reviews-service.ts &
npx tsx gateway.ts
# Gateway ready at http://localhost:4000/graphql
```

### Docker Compose

```bash
docker-compose up -d
# Gateway at http://localhost:4000/graphql
```

## Testing

```bash
# Query the gateway for a user with orders and reviews
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ user(id: \"1\") { id name email orders { id total } reviews { id rating comment } } }"}'
```

Expected response:

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
