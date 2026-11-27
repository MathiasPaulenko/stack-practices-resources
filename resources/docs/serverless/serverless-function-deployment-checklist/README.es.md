# Checklist de Despliegue de Funciones Serverless — Recursos

Assets ejecutables que acompañan al [Checklist de Despliegue de Funciones Serverless](https://stackpractices.com/es/docs/serverless-function-deployment-checklist/).

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `deploy.sh` | Pipeline de despliegue: tests unitarios/de integración, empaquetado, deploy, smoke tests y verificación |
| `serverless.yml` | Configuración de referencia de Serverless Framework: dimensionado, IAM de mínimo privilegio, variables por stage, eventos de API Gateway + SQS, alarmas de CloudWatch y rollout canary vía CodeDeploy |

## Uso

```bash
# desplegar a staging (por defecto) o prod
./deploy.sh staging
./deploy.sh prod

# o desplegar directamente con Serverless Framework
npx serverless deploy --stage prod
```

El `serverless.yml` es una referencia, no un drop-in: sustituye ARNs, nombres de bucket, rutas de parámetros SSM y los recursos `AlertTopic`/`OrderQueue` por los tuyos antes de desplegar. El rollout canary solo te protege si las alarmas referenciadas existen — están definidas en `resources:` dentro del mismo archivo.
