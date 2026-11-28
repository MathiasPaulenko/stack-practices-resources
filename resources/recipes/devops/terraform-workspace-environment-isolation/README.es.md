# Aislar Entornos con Terraform Workspaces

Configuración de Terraform ejecutable para aislar entornos con workspaces de CLI: backend S3 con lockfile nativo, locals `env_config` por workspace y `.tfvars` por entorno.

## Archivos

- `backend.tf` — backend S3 con `use_lockfile` (Terraform >= 1.10). Un solo `key` para todos los workspaces; los states quedan bajo `env:/<workspace>/`.
- `environments.tf` — mapa `env_config` indexado por `terraform.workspace` con un ejemplo comentado de recurso condicional.
- `dev.tfvars` / `staging.tfvars` / `production.tfvars` — archivos de variables por entorno.

## Uso

```bash
terraform init
terraform workspace new dev
terraform workspace new production

terraform workspace select dev
terraform apply -var-file="dev.tfvars"

terraform workspace select production
terraform apply -var-file="production.tfvars"
```

## Notas

- No interpolés `terraform.workspace` en el bloque backend — no está disponible en tiempo de init. El prefijo `env:` aísla cada workspace automáticamente; se personaliza con `workspace_key_prefix`.
- Antes de borrar un workspace, destruí sus recursos: `terraform destroy`, después `terraform workspace select default && terraform workspace delete <nombre>`.
- Artículo fuente: https://stackpractices.com/es/recipes/terraform-workspace-environment-isolation/
