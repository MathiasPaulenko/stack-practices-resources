# Deploy Containers to AWS ECS with Fargate — Companion Files

Runnable companion for the [AWS ECS Fargate recipe](https://stackpractices.com/recipes/aws-ecs-fargate/) on StackPractices.

- `main.tf` — VPC (with NAT gateway for private subnets), ECS cluster, task definition, service with deployment circuit breaker, ALB with health checks and `deregistration_delay`.
- `iam.tf` — execution role (image pull, logs, secrets) and task role (app permissions), plus ALB/ECS security groups.
- `autoscaling.tf` — target tracking on CPU (70%) and memory (80%) with sensible cooldowns.
- `secrets.tf` — Secrets Manager secret injected into the task via `secrets` in the container definition.
- `deploy.yml` — GitHub Actions workflow: build → push to ECR → `update-service` with forced new deployment.

Usage:

```bash
terraform init
terraform apply
```

Then set `secrets.AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` in your GitHub repo (or switch to OIDC `role-to-assume`) and place `deploy.yml` under `.github/workflows/`.
