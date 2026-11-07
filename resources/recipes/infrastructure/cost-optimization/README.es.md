# Optimización de costos cloud — Archivos complementarios

Artefactos ejecutables de la [receta de optimización de costos cloud](https://stackpractices.com/es/recipes/cost-optimization/)
de StackPractices. Cada archivo funciona tal cual contra una cuenta real de AWS.

## Archivos

| Archivo | Qué hace |
|---------|----------|
| `find-orphaned-resources.sh` | Barrido semanal de volúmenes EBS desasociados, Elastic IPs sin asociar, snapshots de más de 90 días, instancias paradas y ENIs huérfanas. Solo lectura. |
| `budget-alerts.tf` | AWS Budgets: presupuesto mensual total + por servicio (EC2) con alertas por email al 80% real, 100% real y 100% forecast. |
| `dev-schedule.tf` | Acciones programadas de Auto Scaling que corren dev/staging de 9 a 18 h de lunes a viernes — ~73% de ahorro fuera de horario. |
| `infracost-ci.yml` | GitHub Action que comenta el diff de costo de Terraform en los pull requests. |

## Inicio rápido

```bash
# 1. Mira qué está fugando dinero ahora mismo (solo lectura)
chmod +x find-orphaned-resources.sh
./find-orphaned-resources.sh us-east-1

# 2. Activa las alertas de presupuesto
terraform init
terraform apply -var="alert_email=finops@example.com" \
  -target=aws_budgets_budget.monthly_total

# 3. Programa tu ASG de dev fuera de horario
terraform apply -var="asg_name=my-dev-asg" \
  -target=aws_autoscaling_schedule.dev_scale_up \
  -target=aws_autoscaling_schedule.dev_scale_down

# 4. Copia infracost-ci.yml a .github/workflows/infracost.yml
#    y configura el secret INFRACOST_API_KEY en el repo.
```

## Requisitos

- AWS CLI v2 configurado (`aws configure` o `AWS_PROFILE`)
- Terraform >= 1.0 para los `.tf`
- `jq` para el script de barrido
- API key de Infracost para el workflow de CI

## Fuente

- Receta EN: https://stackpractices.com/recipes/cost-optimization/
- Receta ES: https://stackpractices.com/es/recipes/cost-optimization/
