# Terraform en Producción — Recursos Complementarios

Artefactos ejecutables de la guía [Guía Completa de Terraform en Producción](https://stackpractices.com/es/guides/complete-guide-terraform-production/) — la capa operativa: estado remoto con bloqueo nativo, aislamiento de entornos, detección de drift, un pipeline CI/CD que aplica el plan revisado y políticas como código.

Para el módulo de VPC que referencia `environments/production/main.tf`, consulta el companion hermano `resources/guides/devops/complete-guide-terraform-modules/`.

## Contenido

| Ruta | Qué es |
|---|---|
| `bootstrap/main.tf` | Bucket de estado de un solo uso: versionado + bloqueo de acceso público + `prevent_destroy` |
| `environments/production/backend.tf` | Backend S3 con `use_lockfile` (bloqueo nativo, TF ≥ 1.10 — sin DynamoDB) |
| `environments/production/main.tf` | Módulo raíz delgado: `default_tags` del provider + composición de módulos |
| `environments/production/variables.tf` | Variable de región + `db_password` sensible alimentada por `TF_VAR_` en CI |
| `policies/sentinel/require-tags.sentinel` | Política de etiquetas obligatorias (solo HCP Terraform/Enterprise) |
| `policies/checks.tf` | Alternativa con bloque `check` nativo para pipelines OSS |
| `scripts/drift-check.sh` | Detección de drift real con `plan -refresh-only` |
| `.github/workflows/terraform.yml` | Pipeline: validate → artefacto plan → aprobación → `apply plan.tfplan` (OIDC, sin claves AWS) |
| `.github/workflows/drift-detection.yml` | Job programado de drift |

## Notas

- Todos los nombres `sp-*` y el ID de cuenta `123456789012` son placeholders — sustitúyelos por los tuyos.
- El artefacto del plan puede contener valores sensibles; el workflow mantiene `retention-days: 5` y separa los roles de lectura (`GitHubTerraformPlan`) y escritura (`GitHubTerraformApply`).
- `drift-check.sh` sale con 1 cuando hay drift para que el job programado aparezca en rojo — la remediación sigue siendo decisión humana.
