# GraphQL Mutation Validation Pattern: Centralized Input Checks

Companion code for the [GraphQL Mutation Validation pattern](https://stackpractices.com/patterns/graphql-mutation-validation-pattern/) on StackPractices.

## Files

| File | Description |
| --- | --- |
| `validation.ts` | Validation framework: `validateInput` and `collectErrors` |
| `rules.ts` | Reusable validation rule factories (required, minLength, email, range, url) |
| `scalars.ts` | Custom Email scalar helpers (dependency-free) |
| `test_validation.ts` | Unit tests for all modules (15 tests) |

## Setup

```bash
npm install -g ts-node typescript
```

## Running the Tests

```bash
npx ts-node test_validation.ts
```

## Usage

```typescript
import { validateInput } from "./validation";
import { rules } from "./rules";

validateInput(input, [
  rules.required("name"),
  rules.minLength("name", 2),
  rules.email("email"),
]);
// throws if validation fails, passes silently if valid
```

## Production Usage

In production with the `graphql` package installed, replace the plain `Error`
in `validation.ts` with a `GraphQLError`:

```typescript
import { GraphQLError } from "graphql";

throw new GraphQLError("Validation failed", {
  extensions: {
    code: "VALIDATION_ERROR",
    fields: errors.map(e => e.field),
    errors,
    timestamp: new Date().toISOString(),
  },
});
```
