# Guía de optimización de costos cloud — Archivos complementarios

Artefactos de la [guía del programa de optimización de costos cloud](https://stackpractices.com/es/guides/cost-optimization-cloud-guide/)
de StackPractices.

## Archivos

| Archivo | Qué hace |
|---------|----------|
| `rightsize_report.py` | Detecta instancias subutilizadas desde un CSV de métricas usando p95 de CPU (no el promedio). Imprime recomendaciones DOWNSIZE vs TERMINATE. |
| `cost-inventory.csv` | El inventario del ejemplo trabajado de la guía — un desglose de gasto por servicio que puedes adaptar para tu propia Fase 1 de auditoría. |

## Inicio rápido

```bash
# 1. Exporta 30 días de métricas p95 a un CSV con columnas:
#    instance_id, instance_type, cpu_p95, memory_p95

# 2. Corre el analizador
python rightsize_report.py instance_metrics.csv
python rightsize_report.py instance_metrics.csv --cpu-threshold 30

# 3. Copia cost-inventory.csv y completa tu propio desglose por servicio
```

## Requisitos

- Python 3.9+ (solo stdlib — sin pandas)
- Métricas exportadas de CloudWatch, Azure Monitor o tu stack de observabilidad

## Fuente

- Guía EN: https://stackpractices.com/guides/cost-optimization-cloud-guide/
- Guía ES: https://stackpractices.com/es/guides/cost-optimization-cloud-guide/
