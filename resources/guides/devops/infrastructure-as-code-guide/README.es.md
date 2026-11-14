# Infrastructure as Code — Código complementario

Código ejecutable de la [guía de Infrastructure as Code](https://stackpractices.com/es/guides/infrastructure-as-code-guide/) en StackPractices.

## Qué incluye

- `modules/vpc/` — un módulo de VPC parametrizado: subnets privadas + públicas en tres AZs, internet gateway y tabla de rutas pública
- `environments/` — layout de directorio-por-entorno (`dev`, `staging`, `production`), cada uno con su propio backend S3 usando lockfile nativo (`use_lockfile = true`, Terraform ≥ 1.10)
- `.github/workflows/iac.yml` — el pipeline plan-en-PR / apply-en-merge con `fmt`, `validate` y Checkov
- `scripts/check-drift.sh` — comprobación programada de drift con `terraform plan -detailed-exitcode` en todos los entornos

## Uso

```bash
cd environments/dev
terraform init   # requiere que exista el bucket del backend S3
terraform plan
```

Cada entorno solo contiene variables, el backend y llamadas a módulos — toda la lógica de recursos vive en `modules/`.

## Relacionados

- Guía (ES): https://stackpractices.com/es/guides/infrastructure-as-code-guide/
- Guía (EN): https://stackpractices.com/guides/infrastructure-as-code-guide/
