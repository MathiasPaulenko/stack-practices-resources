# Almacenar Terraform Remote State en S3 con Bloqueo

Código companion de la receta de StackPractices:
<https://stackpractices.com/es/recipes/terraform-remote-state-s3-backend/>

## Qué hay acá

- `bootstrap.tf` — configuración de una sola vez que crea el bucket de state en S3 con versionado, cifrado SSE-S3, acceso público bloqueado y `prevent_destroy`. Aplicalo desde un root module separado antes que cualquier otra cosa.
- `backend.tf` — bloque de backend S3 con locking nativo (`use_lockfile = true`, Terraform >= 1.10) y notas de migración para configuraciones con `dynamodb_table`.
- `environments.tf` — estrategia de `key` por entorno (ejemplos comentados) y la alternativa con workspaces.

## Uso

```bash
# 1. Bootstrap del bucket (módulo separado, state local)
terraform init && terraform apply   # en el módulo de bootstrap

# 2. Conectá el backend en tu root module, después
terraform init -migrate-state       # primera vez
terraform plan && terraform apply
```

En CI preferí OIDC (`aws-actions/configure-aws-credentials` con
`role-to-assume`) en vez de access keys estáticas.
