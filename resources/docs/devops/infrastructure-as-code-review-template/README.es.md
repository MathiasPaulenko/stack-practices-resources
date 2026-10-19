# Plantilla de Revisión de Infrastructure as Code — Companion

Versiones ejecutables de los ejemplos de [Plantilla de Revisión de Infrastructure as Code](https://stackpractices.com/es/docs/infrastructure-as-code-review-template/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `terraform-review.yml` | Workflow de GitHub Actions — escaneo SARIF de Checkov + `terraform plan` publicado como comentario en el PR |
| `aws_require_tags.py` | Política personalizada de Checkov que exige tags `CostCenter` y `Environment` en recursos AWS |
| `infrastructure_test.go` | Test de Terratest que aplica un módulo VPC y valida sus outputs |
| `drift_detector.py` | Chequeo programado de drift (`plan -detailed-exitcode`) con alerta por email |

## Uso

```bash
# Política personalizada de Checkov
checkov -d terraform/ --external-checks-dir . --framework terraform

# Terratest (necesita credenciales de AWS)
cd test && go test -v -timeout 30m

# Detector de drift (prográmalo con cron o un trigger de CI)
python drift_detector.py
```

## Requisitos

- Terraform >= 1.7, Checkov, Go >= 1.21 (para Terratest)
- Credenciales de AWS para `terraform plan` / Terratest
