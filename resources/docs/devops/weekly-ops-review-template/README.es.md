# Plantilla de Revisión Semanal de Operaciones — Recursos complementarios

Archivos complementarios de la [Plantilla de Revisión Semanal de Operaciones](https://stackpractices.com/es/docs/weekly-ops-review-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `weekly-ops-review.md` | Markdown | Plantilla independiente: resumen ejecutivo, revisión de incidentes, análisis de costos, rendimiento, acciones, riesgos |
| `summarize-week.py` | Python 3 | Genera la tabla de resumen ejecutivo a partir de un JSON de incidentes y costos; avisa de picos de costo y presupuestos de error bajos |

## Inicio rápido

### 1. Copia la plantilla

```bash
cp weekly-ops-review.md reviews/$(date +%Y-%m-%d)-ops-review.md
```

### 2. Genera la tabla de resumen

```bash
python summarize-week.py week.json
```

El script lee un JSON (`incidents`, `cost_this_week`, `cost_last_week`, `cost_budget`, `error_budget_pct`, `error_budget_last_pct`) e imprime la tabla de la sección 1 con tendencias semana a semana. Aparecen avisos cuando el costo sube >5% o el presupuesto de error baja del 50%.

## Adáptalo antes de producción

1. Conecta el JSON a las APIs de tu tracker de incidentes y herramienta de costos.
2. Ajusta los objetivos de la tabla (`< 3` incidentes, `> 50%` presupuesto de error) a tus SLOs.
3. Mantén la revisión bajo 30 minutos: la plantilla es la agenda, no la reunión.
