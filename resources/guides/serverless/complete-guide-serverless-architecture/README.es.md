# Pipeline Serverless de Procesamiento de Imágenes

Código companion de la [Guía Completa de Arquitectura Serverless](https://stackpractices.com/es/guides/complete-guide-serverless-architecture/) — el ejemplo resuelto: un pipeline event-driven `Subida a S3 → Lambda de resize → SQS → Lambda de metadata → DynamoDB` con cola de mensajes muertos.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `resize_handler.py` | Lambda disparada por S3: redimensiona la imagen subida (thumbnail/medium/large) y publica las claves generadas en SQS |
| `metadata_handler.py` | Lambda disparada por SQS: escribe la metadata por versión en DynamoDB; devuelve `batchItemFailures` para que solo reintenten los mensajes fallidos |
| `main.tf` | Terraform para todo el stack: ambas Lambdas (empaquetadas vía `archive_file`), roles IAM de mínimo privilegio, buckets S3 + trigger de notificación, cola SQS + DLQ, event source mapping y tabla DynamoDB |
| `requirements.txt` | Dependencias Python (`boto3`, `Pillow`) |

## Ejecutar en local

Los handlers son funciones simples — invócalos con un evento mockeado:

```bash
pip install -r requirements.txt

python - <<'PY'
import json
import metadata_handler

event = {"Records": [{"messageId": "m1", "body": json.dumps({
    "imageId": "img-1",
    "originalKey": "uploads/originals/photo.jpg",
    "thumbnailKey": "uploads/resized/t.jpg",
    "mediumKey": "uploads/resized/m.jpg",
    "largeKey": "uploads/resized/l.jpg",
})}]}
print(metadata_handler.lambda_handler(event, None))
PY
```

`metadata_handler` corre sin credenciales AWS cuando `TABLE_NAME` está configurada y `boto3` está mockeado o apuntando a LocalStack. `resize_handler` necesita acceso a S3 (real o LocalStack) y Pillow.

## Desplegar

`main.tf` es un stack completo — empaqueta los handlers por su cuenta y conecta el IAM, el trigger de S3 y el event source mapping:

```bash
terraform init
terraform apply \
  -var="originals_bucket_name=my-originals-123" \
  -var="resized_bucket_name=my-resized-123"
```

Los nombres de bucket tienen que ser únicos globalmente. Tras el apply, soltar una imagen en `uploads/originals/` del bucket de originales corre el pipeline entero de punta a punta.
