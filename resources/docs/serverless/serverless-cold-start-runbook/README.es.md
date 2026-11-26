# Runbook de Cold Start Serverless — Recursos Complementarios

Herramientas ejecutables correspondientes al runbook [Serverless Cold Start Runbook](https://stackpractices.com/es/docs/serverless-cold-start-runbook/).

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `warmer.py` | Warmer de Lambda — invoca funciones async para mantener contenedores calientes (schedule vía EventBridge `rate(5 minutes)`) |
| `cold-start-rate.sh` | Tasa de cold starts de la última hora sobre logs de CloudWatch |
| `cold-start-detection.py` | Patrón de flag `_is_warm` a nivel de módulo para detectar cold starts en handlers Python |

Los warmers cuestan menos que provisioned concurrency pero no cubren picos de concurrencia — cada ruta concurrente necesita su propio contenedor caliente.
