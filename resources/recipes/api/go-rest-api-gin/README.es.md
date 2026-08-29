# REST API en Go con Gin y Middleware

Código companion para [REST API en Go con Gin y Middleware](https://stackpractices.com/es/recipes/go-rest-api-gin/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `main.go` | Punto de entrada, setup del router y registro de middleware |
| `middleware/logger.go` | Middleware de logging de requests |
| `middleware/auth.go` | Middleware simple con header Authorization |
| `middleware/auth_test.go` | Tests para el middleware de auth |
| `middleware/error.go` | Tipo `APIError` y middleware de manejo de errores |
| `middleware/error_test.go` | Tests para el middleware de errores |
| `handlers/user.go` | Handlers de ejemplo con validación de requests |
| `handlers/user_test.go` | Tests para los handlers de usuarios |
| `server/server.go` | Wrapper de graceful shutdown |
| `go.mod` | Módulo y dependencias |

## Inicio rápido

```bash
cd resources/recipes/api/go-rest-api-gin
go mod tidy
go run main.go
```

El server inicia en `http://localhost:8080`.

### Requests de ejemplo

```bash
# Health check
curl http://localhost:8080/health

# Listar usuarios
curl -H "Authorization: Bearer token" http://localhost:8080/api/v1/users

# Crear un usuario
curl -X POST -H "Authorization: Bearer token" -H "Content-Type: application/json" \
  -d '{"name":"alice","email":"alice@example.com","age":30}' \
  http://localhost:8080/api/v1/users
```

## Correr tests

```bash
go test ./...
```
