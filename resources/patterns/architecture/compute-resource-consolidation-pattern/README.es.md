# Consolidación de Recursos de Cómputo — Herramientas

Scripts ejecutables que acompañan al
[Patrón de Consolidación de Recursos de Cómputo](https://stackpractices.com/es/patterns/compute-resource-consolidation-pattern/)
en StackPractices.

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `workload-analyzer.py` | Evalúa qué pares de cargas son seguros de consolidar según uso promedio y solapamiento de horas pico |
| `spot-consolidation.py` | Agrupa trabajos por lotes por ventana de ejecución y planifica una instancia spot por ventana (soporta `--dry-run`) |
| `workloads.example.json` | Dataset de ejemplo usable con ambos scripts |

## Uso

```bash
# ¿Qué cargas pueden compartir un nodo?
python workload-analyzer.py workloads.example.json

# ¿Cómo se agrupan los trabajos por lotes en ventanas spot? (sin llamadas a AWS)
python spot-consolidation.py workloads.example.json --dry-run
```

## Requisitos

- Python 3.10+
- `boto3` solo para peticiones spot reales (no necesario con `--dry-run`)

Ambos scripts devuelven código distinto de cero ante entrada inválida, así que pueden actuar como gate en CI.
