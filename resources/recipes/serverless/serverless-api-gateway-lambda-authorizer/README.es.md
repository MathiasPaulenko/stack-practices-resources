# Lambda Authorizers de API Gateway — Recursos Complementarios

Ejemplos ejecutables de authorizers correspondientes a la receta [Securizar API Gateway con Lambda Authorizers](https://stackpractices.com/es/recipes/serverless-api-gateway-lambda-authorizer/).

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `src/authorizer.py` | Authorizer JWT — valida el Bearer token, devuelve política IAM + contexto |
| `src/authorizer_rbac.py` | Variante por roles — permisos por método para admin/editor/user |
| `src/authorizer_apikey.py` | Authorizer de API key con lookup en DynamoDB (keys hasheadas) |
| `template.yaml` | Template SAM: authorizer + recurso protegido + caché de 300s |

Devuelve `Deny` — nunca lances excepciones — ante cualquier fallo de validación, o API Gateway devolverá un 500 en lugar de un 403.
