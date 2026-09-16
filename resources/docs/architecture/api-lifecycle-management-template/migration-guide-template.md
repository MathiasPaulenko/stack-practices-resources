# Migration Guide: v2 -> v3 `<Service>` API

## Summary

- Field `name` split into `firstName` and `lastName`
- Endpoint `/v2/users/{id}` replaced by `/v3/users/{id}`
- Error responses now use RFC 7807 Problem Details format

## Before (v2)

```json
GET /v2/users/123
{
  "id": 123,
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

## After (v3)

```json
GET /v3/users/123
{
  "id": 123,
  "firstName": "Alice",
  "lastName": "Johnson",
  "email": "alice@example.com"
}
```

## Error Format Change

```json
// v2 error
{ "error": "User not found", "code": 404 }

// v3 error (RFC 7807)
{
  "type": "https://api.example.com/errors/not-found",
  "title": "User not found",
  "status": 404,
  "detail": "User 123 does not exist"
}
```

## Automated Migration Steps

1. Update base URL from `/v2/` to `/v3/`
2. Replace `name` with `firstName` + `lastName` in request/response models
3. Update error handling to parse RFC 7807 format
4. Test against sandbox at `https://sandbox.api.example.com/v3/`
