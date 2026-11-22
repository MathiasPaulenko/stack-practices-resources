# CRUD Operations with MongoDB and Mongoose — Offline Companion

Runnable, dependency-free companion for the StackPractices recipe
[CRUD Operations with MongoDB and Mongoose](https://stackpractices.com/recipes/mongodb-crud-mongoose/).

The recipe uses Mongoose + a real MongoDB. This companion reproduces the same
semantics — validation, soft delete with hidden queries, and multi-write
transaction rollback — against an in-memory `DocumentStore`, so you can study
and test the patterns without a database.

## Run the tests

```bash
node --test user_store.test.mjs
```

## What it covers

- `create` / `find` / `findById` / `findByIdAndUpdate` — the CRUD round-trip.
- Field validators that throw readable errors, like Mongoose validators.
- `softDelete` — deleted docs disappear from `find()` but stay queryable with
  `includeDeleted`.
- `withTransaction` — commits every op or rolls the whole batch back on error.

## Related

- Recipe: https://stackpractices.com/recipes/mongodb-crud-mongoose/
- Spanish: https://stackpractices.com/es/recipes/mongodb-crud-mongoose/
