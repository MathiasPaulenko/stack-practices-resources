# Complete Guide to GraphQL Federation — Companion Resources

Companion code for the [Complete Guide to GraphQL Federation](https://stackpractices.com/guides/complete-guide-graphql-federation/) on StackPractices.

## Files

- `src/users-subgraph.js` — Users subgraph (Node.js, Apollo Server)
- `src/orders-subgraph.js` — Orders subgraph (Node.js, Apollo Server)
- `src/products-subgraph.py` — Products subgraph (Python, Ariadne)
- `src/gateway.js` — Apollo Gateway that composes the three subgraphs
- `supergraph.yaml` — Rover CLI composition config
- `package.json` — Node.js dependencies
- `requirements.txt` — Python dependencies
- `docker-compose.yml` — Docker setup for all four services

## Quick Start

### Node.js subgraphs and gateway

```bash
npm install
npm run start:users   # Users subgraph on :4001
npm run start:orders  # Orders subgraph on :4002
npm run start:gateway # Gateway on :4000
```

### Python subgraph

```bash
pip install -r requirements.txt
uvicorn src.products-subgraph:app --port 4003
```

### Compose the supergraph

```bash
rover supergraph compose --config supergraph.yaml > supergraph.graphql
```

## Query the federated graph

```graphql
query GetUserWithOrders {
  user(id: "1") {
    id
    name
    email
    orders {
      id
      total
      status
      items {
        quantity
        product {
          name
          price
        }
      }
    }
  }
}
```
