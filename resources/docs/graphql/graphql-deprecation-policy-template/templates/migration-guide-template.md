## Migrating from {deprecated} to {replacement}

### What changed

{Description of what was deprecated and why}

### Before

```graphql
query {
  user(id: "1") {
    name
    email
  }
}
```

### After

```graphql
query {
  user(id: "1") {
    firstName
    lastName
    contactEmail
  }
}
```

### Migration steps

1. Update all queries that select {deprecated field}
2. Update all response parsing logic
3. Update all tests
4. Deploy to staging and verify
5. Deploy to production

### Common issues

- **Issue**: {common problem}
  **Fix**: {solution}

### Timeline

- Deprecated: {date}
- Rate limited: {date}
- Removed: {date}
