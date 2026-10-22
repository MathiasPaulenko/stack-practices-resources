# Implementar una API GraphQL — Companion

Tres servidores GraphQL ejecutables que implementan la API de libros de la receta, más un archivo de operaciones de ejemplo.

Artículo fuente: [Implementar una API GraphQL](https://stackpractices.com/es/recipes/graphql-api/)

## Estructura

| Ruta | Qué es |
|------|--------|
| `python/server.py` | Servidor Strawberry + FastAPI (code-first) |
| `javascript/index.mjs` | Servidor Apollo Server 4 standalone (schema-first) |
| `java/BookController.java` | Controlador Spring for GraphQL (`@QueryMapping`/`@MutationMapping`) |
| `java/schema.graphqls` | El archivo SDL que Spring lee desde `resources/graphql/` |
| `queries.graphql` | Query + mutación para pegar en GraphiQL / Apollo Sandbox |

## Arranque rápido

**Python** — `pip install fastapi "strawberry-graphql[fastapi]" uvicorn`, luego `uvicorn server:app --reload`. GraphiQL en `http://localhost:8000/graphql`.

**JavaScript** — `npm install && npm start`. Apollo Sandbox en `http://localhost:4000/`.

**Java** — añade `spring-boot-starter-graphql` a un proyecto Spring Boot, coloca `BookController.java` y `schema.graphqls` bajo `src/main/resources/graphql/`. Endpoint en `/graphql`.

## Pruébalo

Ejecuta `ListBooks`, luego `AddBook`, luego `ListBooks` otra vez — verás el libro nuevo. La query `TitlesOnly` demuestra la selección de campos: la misma forma de query con menos campos devuelve menos datos.

## Notas de producción

- `apollo-server` standalone (v3) está EOL — este ejemplo usa `@apollo/server` v4.
- `graphql-java-servlet` / `com.coxautodev.graphql.tools` están sin mantenimiento y usan `javax.servlet` — usa Spring for GraphQL o Netflix DGS en su lugar.
- Antes de producción: límite de profundidad, presupuesto de complejidad, persisted queries, introspection desactivada o protegida — ver el checklist de la receta.
