# Plantilla de Análisis de Brechas de Cumplimiento — Recursos Complementarios

Archivos complementarios de la [Plantilla de Análisis de Brechas de Cumplimiento](https://stackpractices.com/es/docs/compliance-gap-analysis-template/) en StackPractices.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `gap-analysis-template.csv` | Tabla de mapeo de controles en CSV: impórtala en Sheets/Excel/Airtable y completa tus propias filas |
| `remediation-plan.csv` | Tabla del plan de remediación en CSV, con columnas de prioridad, dueño, fecha límite y evidencia requerida |
| `collect-evidence.sh` | Recolecta evidencia de AWS para controles comunes de SOC 2 (MFA de IAM, cifrado S3, CloudTrail, AWS Config) en una carpeta fechada |
| `generate-mapping.py` | Genera una matriz de mapeo multi-marco (SOC 2 / ISO 27001 / PCI-DSS) desde un único inventario de controles |

## Uso

```bash
# Completa los CSV en tu herramienta de hojas de cálculo, o
python -c "import csv; print(list(csv.reader(open('gap-analysis-template.csv')))[:2])"

# Recolecta evidencia de AWS (requiere aws CLI con credenciales de solo lectura)
aws sts get-caller-identity
./collect-evidence.sh

# Genera la matriz multi-marco
python generate-mapping.py
```

Los CSV corresponden a las tablas del documento: mapeo de controles, resumen de brechas, plan de remediación y seguimiento de evidencia. Extiende `FRAMEWORK_MAPPING` en el script de Python con tus propios controles para cubrir más IDs de requisito.
