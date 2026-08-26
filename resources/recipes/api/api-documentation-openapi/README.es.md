# OpenAPI con Swagger UI y Redoc

Código complementario para [OpenAPI con Swagger UI y Redoc: guía práctica](https://stackpractices.com/es/recipes/api-documentation-openapi/).

## Archivos

| Archivo | Descripción |
| --- | --- |
| `openapi.yaml` | Spec OpenAPI 3.0 de ejemplo para una API de libros |
| `python_fastapi.py` | Ejemplo code-first con FastAPI (auto-genera el spec) |
| `javascript_express.js` | Ejemplo design-first con Express + swagger-ui-express |
| `java_springdoc.java` | Ejemplo code-first con Spring Boot + SpringDoc |
| `redocly_ruleset.yaml` | Reglas de linting personalizadas para Redocly CLI |
| `github_actions_lint.yml` | Workflow de GitHub Actions para linting en CI |

## Inicio rápido

### Python (FastAPI)

```bash
pip install fastapi uvicorn
uvicorn python_fastapi:app --reload
# Abre http://localhost:8000/docs
```

### JavaScript (Express)

```bash
npm install express swagger-ui-express yamljs
node javascript_express.js
# Abre http://localhost:3000/api-docs
```

### Lint del spec

```bash
npm install -g @redocly/cli
redocly lint --config=redocly_ruleset.yaml openapi.yaml
```
