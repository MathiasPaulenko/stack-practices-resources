# Fundamentos de Docker — Archivos de apoyo

Ejemplos ejecutables de la [receta Fundamentos de Docker](https://stackpractices.com/es/recipes/docker-basics/) en StackPractices.com.

## Contenido

| Archivo | Propósito |
| --- | --- |
| `Dockerfile.node` | Build multi-etapa para una app Node.js (deps cacheadas, runner sin root) |
| `Dockerfile.python` | Build de una etapa para una app Python/uvicorn |
| `Dockerfile.java` | Build multi-etapa con Gradle para una app Spring Boot |
| `docker-compose.yml` | App web + PostgreSQL con volumen nombrado |
| `.dockerignore` | Mantiene pequeño el contexto de build y los secretos fuera |

## Uso

```bash
# Construir uno de los Dockerfiles
docker build -f Dockerfile.node -t myapp:latest .

# Levantar el stack de Compose (usa Dockerfile.node)
docker compose up --build

# Detener y limpiar
docker compose down -v
```

Adapta el contexto de build, los puertos y las variables de entorno a tu proyecto. No subas credenciales reales — los valores `user`/`pass` son placeholders para desarrollo local.
