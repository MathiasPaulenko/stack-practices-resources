# Almacenamiento Blob: patrones de S3, GCS y Azure

Código companion de la [Guía de Blob Storage](https://stackpractices.com/es/guides/blob-storage-guide/) en StackPractices.

## Archivos

| Archivo | Qué hace |
|---|---|
| `s3_upload.py` | URLs firmadas PUT/GET más subida multiparte automática vía boto3 TransferConfig |
| `lifecycle.json` | Regla de ciclo de vida S3: Standard → IA (30d) → Glacier (90d) → Deep Archive (1 año), abortos a los 7d |
| `cors.json` | Regla CORS del bucket acotada a tu origen para subidas directas desde el navegador |

## Uso

```bash
# Generar una URL firmada de subida y enviar un archivo
python s3_upload.py --bucket myapp-uploads-prod --key uploads/2025/10/report.pdf \
  --file report.pdf --type application/pdf

# Aplicar la regla de ciclo de vida
aws s3api put-bucket-lifecycle-configuration \
  --bucket myapp-reports-prod \
  --lifecycle-configuration file://lifecycle.json

# Aplicar CORS para subidas desde el navegador
aws s3api put-bucket-cors \
  --bucket myapp-uploads-prod \
  --cors-configuration file://cors.json
```

El equivalente en Azure usa `generate_blob_sas` para tokens SAS y `BlobClient.upload_blob(max_concurrency=N)` para el troceado automático — consulta los pasos 2 y 3 de la guía para el código funcional.
