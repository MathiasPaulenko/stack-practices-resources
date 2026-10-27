# Reducir Cold Start en AWS Lambda — Archivos complementarios

Proyecto ejecutable complementario de la [receta de cold start de Lambda](https://stackpractices.com/es/recipes/aws-lambda-cold-start-optimization/) en StackPractices.

- `measure_cold_start.py` — patrón de flag a nivel módulo para detectar cold starts dentro del handler.
- `lazy_init.py` — imports/carga de datos diferida para dependencias pesadas (ejemplo con pandas).
- `reuse_connections.py` — reutilización de clientes boto3 a nivel módulo entre invocaciones warm.
- `powertools_logging.py` — logging estructurado con AWS Lambda Powertools.
- `minimal_handler.py` — handler raw de routing en lugar de un framework pesado.
- `cloudwatch-insights-query.txt` — query de Logs Insights para estadísticas de Init Duration.
- `template.yaml` / `snapstart-template.yaml` / `efs-template.yaml` — configs SAM: provisioned concurrency, SnapStart (Java), montaje EFS.
- `serverless.yml` — config del plugin warm-up de Serverless Framework.
- `package-trim.sh` / `arm64-migration.sh` — limpiar archivos de desarrollo del paquete y reconstruir layers para Graviton.
