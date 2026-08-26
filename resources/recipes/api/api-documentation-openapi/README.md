# OpenAPI Docs with Swagger UI and Redoc

Companion code for [OpenAPI Docs with Swagger UI and Redoc: A Practical Guide](https://stackpractices.com/recipes/api-documentation-openapi/).

## Files

| File | Description |
| --- | --- |
| `openapi.yaml` | Sample OpenAPI 3.0 spec for a Book API |
| `python_fastapi.py` | FastAPI code-first example (auto-generates spec) |
| `javascript_express.js` | Express + swagger-ui-express design-first example |
| `java_springdoc.java` | Spring Boot + SpringDoc code-first example |
| `redocly_ruleset.yaml` | Custom Redocly CLI linting rules |
| `github_actions_lint.yml` | GitHub Actions workflow for CI linting |

## Quick start

### Python (FastAPI)

```bash
pip install fastapi uvicorn
uvicorn python_fastapi:app --reload
# Open http://localhost:8000/docs
```

### JavaScript (Express)

```bash
npm install express swagger-ui-express yamljs
node javascript_express.js
# Open http://localhost:3000/api-docs
```

### Lint the spec

```bash
npm install -g @redocly/cli
redocly lint --config=redocly_ruleset.yaml openapi.yaml
```
