# Provisionar una VPC de AWS con Terraform

Configuración Terraform completa para una VPC de AWS lista para producción: subredes públicas y privadas en tres zonas de disponibilidad, NAT gateways, tablas de ruteo, security groups restrictivos, VPC Flow Logs y VPC endpoints.

Código de acompañamiento de la receta de StackPractices:
[Provisionar una VPC de AWS con Terraform](https://stackpractices.com/es/recipes/terraform-aws-vpc/)

## Uso

```bash
terraform init
terraform plan -var="region=us-east-1"
terraform apply
```

Para un entorno dev sensible a costos con un solo NAT gateway:

```bash
terraform apply -var="single_nat_gateway=true"
```

## Archivos

| Archivo | Contenido |
|---|---|
| `versions.tf` | Requisitos del provider y región |
| `variables.tf` | Región, CIDR, AZs, toggle `single_nat_gateway` |
| `vpc.tf` | VPC, subredes públicas y privadas |
| `gateways.tf` | Internet Gateway, EIPs, NAT gateways |
| `routing.tf` | Tablas de ruteo públicas/privadas y asociaciones |
| `security.tf` | Security groups de web y base de datos |
| `flow_logs.tf` | VPC Flow Logs a CloudWatch |
| `endpoints.tf` | Endpoint Gateway de S3, endpoint Interface de Secrets Manager |
| `nacls.tf` | Network ACL para las subredes públicas |
| `outputs.tf` | IDs de VPC, subredes y security groups |

## Notas

- Con `single_nat_gateway=false` (por defecto) corre un NAT gateway por AZ — sin punto único de fallo y sin cargos de transferencia entre zonas.
- Requiere credenciales de AWS configuradas (`aws configure` o variables de entorno) y Terraform >= 1.5.
