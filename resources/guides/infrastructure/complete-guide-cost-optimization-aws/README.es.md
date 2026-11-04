# Guía Completa de Optimización de Costos en AWS — Archivos de apoyo

Scripts y configuraciones referenciados por la guía:
[Guía Completa de Optimización de Costos en AWS](https://stackpractices.com/es/guides/complete-guide-cost-optimization-aws/)

## Contenido

| Archivo | Qué hace |
|---------|----------|
| `budget-alert.sh` | Crea un presupuesto mensual de AWS con alerta por email al 80% del gasto real. |
| `s3-lifecycle-policy.json` | Regla de ciclo de vida: STANDARD → IA (30d) → GLACIER (90d) → DEEP_ARCHIVE (365d), más expiración a 7 días para objetos temporales. |
| `ec2-fleet-spot.json` | Petición de EC2 Fleet para capacidad Spot con la estrategia `capacity-optimized` en 3 tipos de instancia. |
| `spot-asg-vpc-endpoints.tf` | Terraform: ASG mixto on-demand/Spot más un gateway endpoint de S3 gratuito y un interface endpoint de DynamoDB. |
| `spot-interruption-check.py` | Consulta IMDSv2 por el aviso de terminación Spot de dos minutos y llama a un hook de apagado elegante. |
| `rds-snapshot-cleanup.py` | Borra snapshots manuales de RDS de más de 30 días, con paginación, saltando los que están en uso. |
| `cost-report-lambda.py` | Handler de Lambda que informa a Slack de los servicios por encima de $100/mes; programarlo con EventBridge. |

## Uso

- Los scripts shell/Python esperan credenciales de AWS CLI v2 con permisos de facturación, EC2, RDS y CloudWatch.
- `ec2-fleet-spot.json` está pensado para `aws ec2 create-fleet --cli-input-json file://ec2-fleet-spot.json` — sustituye el ID de launch template y las subnets por los tuyos.
- `spot-asg-vpc-endpoints.tf` referencia `aws_launch_template.app`, `aws_vpc.main`, `aws_route_table.private` y `aws_subnet.private` — conéctalos a tu módulo de VPC.
- Los precios mencionados en la guía son cifras ilustrativas de us-east-1; consulta AWS Pricing para las tarifas vigentes.
