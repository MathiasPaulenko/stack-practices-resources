# Jobs Programados con Funciones Serverless — Recursos complementarios

Archivos ejecutables de la receta [Ejecutar Jobs Programados con Funciones Serverless](https://stackpractices.com/es/recipes/scheduled-jobs/) en StackPractices.

## Archivos

| Archivo | Qué es |
|---------|--------|
| `daily_report_lambda.py` | Handler Lambda en Python que genera el reporte del día anterior y lo sube a S3. Sustituye `generate_sales_report` por tu agregación real. |
| `eventbridge_rule.tf` | Terraform del schedule: regla de EventBridge con `cron(0 2 * * ? *)`, el target Lambda y el `aws_lambda_permission` que permite a EventBridge invocar la función. |
| `cloud_scheduler_job.yaml` | Definición de job de Google Cloud Scheduler que llama a una Cloud Function HTTP con autenticación OIDC, a las `0 2 * * *` UTC. |
| `timer_trigger_function.py` | Timer Trigger de Azure Functions (modelo Python v2) que corre cada día a las 2:00 AM con la expresión NCRONTAB `0 0 2 * * *`. |

## Uso

- **AWS**: comprime `daily_report_lambda.py`, despliégala como `report_generator` y ejecuta `terraform apply` en una carpeta con `eventbridge_rule.tf`. La regla dispara cada día a las 2 AM UTC.
- **GCP**: `gcloud scheduler jobs create http daily-cleanup --schedule="0 2 * * *" --uri=<url-función> --oidc-service-account-email=<sa>` o importa la definición YAML.
- **Azure**: copia `timer_trigger_function.py` en un proyecto de Function App (modelo de programación Python v2) y despliega.

Todos los horarios corren en UTC por defecto. Diseña el handler para que sea idempotente — la plataforma puede reintentar y ejecutarlo dos veces.
