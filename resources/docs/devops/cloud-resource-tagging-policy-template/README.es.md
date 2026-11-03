# Política de Etiquetado de Recursos Cloud — Herramientas ejecutables

Companion del doc de StackPractices [Plantilla de Política de Etiquetado de Recursos Cloud](https://stackpractices.com/es/docs/cloud-resource-tagging-policy-template/).

## Archivos

| Archivo | Stack | Propósito |
| --- | --- | --- |
| `src/detect-untagged.py` | Python 3.9+ + `boto3` | Escanea EC2, S3 y RDS en varias regiones buscando etiquetas requeridas faltantes (`team`, `environment`, `product`, `cost-center`, `owner`) e imprime un informe JSON. Maneja el error `NoSuchTagSet` que lanzan los buckets sin etiquetar. |
| `src/tag-policy.tf` | Terraform (provider AWS) | Variable `required_tags` + local `default_tags` que aplica la convención de minúsculas con guiones a recursos EC2, S3 y RDS. |

## Ejecutar

`src/detect-untagged.py` necesita credenciales de AWS (variables de entorno, `~/.aws` o instance profile) — hace llamadas de solo lectura:

```bash
pip install boto3
python src/detect-untagged.py
```

`src/tag-policy.tf` es un fragmento de módulo, no un proyecto standalone — copia el bloque `locals`/`variable` en tu Terraform y referencia `local.default_tags` en los recursos etiquetables. Edita `REGIONS` en el script y el conjunto de etiquetas en el mapa `required_tags` para adaptarlo a tu política.
