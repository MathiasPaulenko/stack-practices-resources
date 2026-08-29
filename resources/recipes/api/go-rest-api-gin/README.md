# Go REST API with Gin and Middleware

Companion code for [Go REST API with Gin and Middleware](https://stackpractices.com/recipes/go-rest-api-gin/).

## Files

| File | Description |
| --- | --- |
| `main.go` | Entry point, router setup, and middleware registration |
| `middleware/logger.go` | Request logging middleware |
| `middleware/auth.go` | Simple Authorization header middleware |
| `middleware/auth_test.go` | Tests for the auth middleware |
| `middleware/error.go` | `APIError` type and error-handling middleware |
| `middleware/error_test.go` | Tests for the error middleware |
| `handlers/user.go` | Sample handlers with request validation |
| `handlers/user_test.go` | Tests for the user handlers |
| `server/server.go` | Graceful shutdown wrapper |
| `go.mod` | Module and dependencies |

## Quick start

```bash
cd resources/recipes/api/go-rest-api-gin
go mod tidy
go run main.go
```

The server starts on `http://localhost:8080`.

### Example requests

```bash
# Health check
curl http://localhost:8080/health

# List users
curl -H "Authorization: Bearer token" http://localhost:8080/api/v1/users

# Create a user
curl -X POST -H "Authorization: Bearer token" -H "Content-Type: application/json" \
  -d '{"name":"alice","email":"alice@example.com","age":30}' \
  http://localhost:8080/api/v1/users
```

## Running tests

```bash
go test ./...
```
