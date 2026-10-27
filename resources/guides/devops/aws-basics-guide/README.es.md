# Guía AWS Básico — Recursos descargables

Assets listos para usar de la [guía AWS Básico](https://stackpractices.com/es/guides/aws-basics-guide/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `aws-commands.sh` | Comandos AWS CLI de la guía: lanzar EC2, operaciones S3, volumen EBS, instancia RDS, alarma de facturación |
| `lambda_handler.py` | Handler Lambda mínimo en Python |
| `dynamodb_basics.py` | put/get en DynamoDB con boto3 |
| `iam-policy.json` | Ejemplo de política S3 de mínimo privilegio con condición de región |

## Uso

1. Configura la AWS CLI y las credenciales primero (`aws configure`).
2. Revisa cada comando antes de ejecutarlo — reemplaza los IDs de ejemplo (`ami-*`, `sg-*`, `subnet-*`, account IDs) por los tuyos.
3. El comando de la alarma de facturación va en `us-east-1` — es donde AWS publica las métricas de facturación.
