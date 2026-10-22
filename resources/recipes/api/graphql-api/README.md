# Implement a GraphQL API — Companion

Three runnable GraphQL servers implementing the books API from the recipe, plus an example operation file.

Source article: [Implement a GraphQL API](https://stackpractices.com/recipes/graphql-api/)

## Structure

| Path | What it is |
|------|------------|
| `python/server.py` | Strawberry + FastAPI server (code-first) |
| `javascript/index.mjs` | Apollo Server 4 standalone (schema-first) |
| `java/BookController.java` | Spring for GraphQL controller (`@QueryMapping`/`@MutationMapping`) |
| `java/schema.graphqls` | The SDL file Spring picks up from `resources/graphql/` |
| `queries.graphql` | Query + mutation to paste into GraphiQL / Apollo Sandbox |

## Quick start

**Python** — `pip install fastapi "strawberry-graphql[fastapi]" uvicorn`, then `uvicorn server:app --reload`. GraphiQL at `http://localhost:8000/graphql`.

**JavaScript** — `npm install && npm start`. Apollo Sandbox at `http://localhost:4000/`.

**Java** — add `spring-boot-starter-graphql` to a Spring Boot project, drop in `BookController.java` and `schema.graphqls` under `src/main/resources/graphql/`. Endpoint at `/graphql`.

## Try it

Run `ListBooks`, then `AddBook`, then `ListBooks` again — you'll see the new book. The `TitlesOnly` query shows field selection: the same query shape with fewer fields returns less data.

## Production notes

- `apollo-server` standalone (v3) is EOL — this example uses `@apollo/server` v4.
- `graphql-java-servlet` / `com.coxautodev.graphql.tools` are unmaintained and use `javax.servlet` — use Spring for GraphQL or Netflix DGS instead.
- Before production: depth limit, complexity budget, persisted queries, introspection off or gated — see the recipe's checklist.
