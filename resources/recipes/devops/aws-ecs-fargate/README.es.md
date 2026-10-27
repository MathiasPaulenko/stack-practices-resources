# Desplegar Contenedores en ECS con Fargate — Archivos complementarios

Proyecto ejecutable complementario de la [receta de AWS ECS Fargate](https://stackpractices.com/es/recipes/aws-ecs-fargate/) en StackPractices.

- `main.tf` — VPC (con NAT gateway para las subredes privadas), cluster ECS, definición de tarea, servicio con deployment circuit breaker, ALB con health checks y `deregistration_delay`.
- `iam.tf` — execution role (traer imagen, logs, secretos) y task role (permisos de la app), más los security groups del ALB/ECS.
- `autoscaling.tf` — target tracking por CPU (70%) y memoria (80%) con cooldowns razonables.
- `secrets.tf` — secreto de Secrets Manager inyectado en la tarea vía `secrets` en la definición de contenedor.
- `deploy.yml` — workflow de GitHub Actions: build → push a ECR → `update-service` con despliegue forzado.

Uso:

```bash
terraform init
terraform apply
```

Después configura `secrets.AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` en tu repo de GitHub (o cambia a `role-to-assume` con OIDC) y coloca `deploy.yml` bajo `.github/workflows/`.
