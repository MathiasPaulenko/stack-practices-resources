# Docker Basics — Companion Files

Runnable examples from the [Docker Basics recipe](https://stackpractices.com/recipes/docker-basics/) on StackPractices.com.

## Contents

| File | Purpose |
| --- | --- |
| `Dockerfile.node` | Multi-stage build for a Node.js app (deps cached, non-root runner) |
| `Dockerfile.python` | Single-stage build for a Python/uvicorn app |
| `Dockerfile.java` | Multi-stage Gradle build for a Spring Boot app |
| `docker-compose.yml` | Web app + PostgreSQL with a named volume |
| `.dockerignore` | Keeps the build context small and secrets out |

## Usage

```bash
# Build one of the Dockerfiles
docker build -f Dockerfile.node -t myapp:latest .

# Start the Compose stack (uses Dockerfile.node)
docker compose up --build

# Stop and clean up
docker compose down -v
```

Adapt the build context, ports, and environment variables to your project. Do not commit real credentials — the `user`/`pass` values are placeholders for local development.
