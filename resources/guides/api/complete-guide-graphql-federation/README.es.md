# Guía Completa de GraphQL Federation — Recursos Companion

Código companion para la [Guía Completa de GraphQL Federation](https://stackpractices.com/es/guides/complete-guide-graphql-federation/) en StackPractices.

## Archivos

- `src/users-subgraph.js` — Subgraph de Users (Node.js, Apollo Server)
- `src/orders-subgraph.js` — Subgraph de Orders (Node.js, Apollo Server)
- `src/products-subgraph.py` — Subgraph de Products (Python, Ariadne)
- `src/gateway.js` — Apollo Gateway que compone los tres subgraphs
- `supergraph.yaml` — Config de composición del Rover CLI
- `package.json` — Dependencias de Node.js
- `requirements.txt` — Dependencias de Python
- `docker-compose.yml` — Setup de Docker para los cuatro servicios

## Inicio Rápido

### Subgraphs y gateway de Node.js

```bash
npm install
npm run start:users   # Subgraph de Users en :4001
npm run start:orders  # Subgraph de Orders en :4002
npm run start:gateway # Gateway en :4000
```

### Subgraph de Python

```bash
pip install -r requirements.txt
uvicorn src.products-subgraph:app --port 4003
```

### Componer el supergraph

```bash
rover supergraph compose --config supergraph.yaml > supergraph.graphql
```

## Consultar el grafo federado

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
