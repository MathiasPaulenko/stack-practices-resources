# API Gateway Serverless — Recursos complementarios

Archivos ejecutables de la receta [Construir APIs Serverless con API Gateway](https://stackpractices.com/es/recipes/serverless-api-gateway/) en StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `handler.py` | Handler Lambda en Python con routing GET/POST sobre `/users` usando el evento proxy de API Gateway. |
| `handler.js` | Equivalente en Node.js, incluida la guarda del body JSON que convierte input malformado en un 400 en lugar de un 502. |
| `main.tf` | Terraform completo para una API funcional: rol IAM, integración `AWS_PROXY`, `aws_lambda_permission`, despliegue con stage `prod` y output `invoke_url`. |

## Uso

1. Comprime el handler que quieras (`zip function.zip handler.js` o `handler.py` renombrado a `index.py` / `index.js` según pida el `handler`).
2. `terraform init && terraform apply` en una carpeta con `main.tf` y `function.zip`.
3. Prueba el `invoke_url` con `curl` — `GET /users` debería devolver el array JSON.

Si el endpoint devuelve `500 Internal Server Error`, revisa `aws lambda get-policy`: API Gateway necesita `aws_lambda_permission` para invocar la función.
