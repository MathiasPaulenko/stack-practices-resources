# Guía GCP Básico — Recursos Complementarios

Recursos ejecutables de la [guía GCP Básico](https://stackpractices.com/es/guides/gcp-basics-guide/) en StackPractices.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `gcloud-setup.sh` | Configuración del primer día: `gcloud init`, login ADC, proyecto, activación de APIs, alertas de presupuesto |
| `gcloud-services.sh` | Comandos de servicios de la guía: VM de GCE, clúster GKE, despliegue en Cloud Run, Cloud Storage, Persistent Disk, Cloud SQL |
| `bigquery_names.sql` | Consulta de BigQuery sobre un dataset público (nombres de bebé en EE. UU.) |
| `iam-policy.yaml` | Vinculaciones IAM de mínimo privilegio para una cuenta de servicio de carga de trabajo |
| `firestore_example.js` | Escritura mínima en Firestore con el SDK modular de Firebase |

## Uso

1. Instala la CLI de gcloud y ejecuta primero `gcloud init`; después `gcloud auth application-default login` para el código SDK local.
2. Sustituye los marcadores (`my-project`, `my-app-bucket`, ID de cuenta de facturación) por tus valores antes de ejecutar nada.
3. Las alertas de presupuesto avisan —nunca frenan el gasto. Revisa también Facturación → Presupuestos y alertas en la consola.
