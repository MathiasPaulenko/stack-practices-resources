# Plantilla de Asignación de Costos en la Nube — Kit Complementario

Artefactos reutilizables extraídos de la [Plantilla de Asignación de Costos](https://stackpractices.com/es/docs/infrastructure-cost-allocation-template/) de StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `aws-tag-policy.yaml` | Política de etiquetas de AWS Organizations que exige etiquetas de costo al crear recursos |
| `terraform-tag-enforcement.hcl` | Módulo de Terraform que aplica etiquetas base obligatorias + validación en CI |
| `kubecost-allocation.yaml` | Configuración de Kubecost para asignación por namespace/etiquetas y reparto de costos compartidos |
| `detect-untagged-resources.py` | Escaneo semanal: detecta recursos de AWS sin etiquetar y reporta su costo semanal |
| `monthly-cost-report.txt` | Formato de reporte mensual de asignación rellenable para finanzas |
| `cost-allocation-worksheet.csv` | Hoja de trabajo de asignación por recurso (importable a Sheets/Excel) |

## Uso

1. Despliega `aws-tag-policy.yaml` (o el equivalente en Terraform) antes de asignar nada — el etiquetado retroactivo nunca cierra el hueco por completo.
2. Configura Kubecost con `kubecost-allocation.yaml` si Kubernetes supone una parte significativa del gasto.
3. Programa `detect-untagged-resources.py` semanalmente; dirige el gasto sin etiquetar a un centro de costos de cuarentena.
4. Rellena `cost-allocation-worksheet.csv` por recurso y genera el reporte mensual a partir de `monthly-cost-report.txt`.

Consulta el documento para el modelo completo, las reglas de reparto y el playbook de implantación.
