# FinOps — Optimización de Costos Cloud

Recursos acompañantes de la [guía FinOps](https://stackpractices.com/es/guides/finops-guide/)
en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `cost_anomaly_detection.py` | Check diario con Cost Explorer: compara el gasto de ayer con la media de 30 días y reporta los servicios que más gastaron al superar el umbral |
| `tagging_policy.tf` | Módulo Terraform que fuerza etiquetas obligatorias de asignación de costos (Owner, Environment, Project, CostCenter, ManagedBy) con validación |
| `saas_optimization_example.md` | El ejemplo trabajado de la guía: cómo una factura AWS de $50K/mes se recorta un 30% con right-sizing, reservas, ciclo de vida S3, Spot y RDS |

## Uso

```bash
# Detección de anomalías — requiere credenciales AWS con ce:GetCostAndUsage
pip install boto3
python cost_anomaly_detection.py --threshold 1.20
```

```hcl
# Módulo de etiquetado
module "tags" {
  source      = "./tagging_policy"
  team_email  = "platform@example.com"
  environment = "production"
  project     = "billing"
  cost_center = "CC-1234"
}
```

## Notas

- El código de salida del script es `1` en caso de anomalía — conéctalo a
  Slack/PagerDuty desde el planificador en lugar de leer stdout.
- Ajusta `--threshold` a la baja (p. ej. `1.10`) en cargas estables, al alza
  en cargas con picos.
