# Plantilla de Tracking de Costos de LLM — Recursos Complementarios

Archivos complementarios de la [Plantilla de Tracking de Costos de LLM](https://stackpractices.com/es/docs/ai-llm-cost-tracking-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `budget_config.yaml` | YAML | Presupuesto mensual, umbrales de alerta (50/75/90/100%), presupuestos por funcionalidad, límites por nivel de usuario |
| `llm_cost_monitor.py` | Python | Monitor de referencia: agrega el gasto por día/funcionalidad, dispara alertas por umbral, sale con código distinto de cero al estrangular |
| `schema.sql` | SQL | Tablas Postgres para el log por petición y el rollup diario, con los índices que importan |
| `llm-cost-report-template.md` | Markdown | Esqueleto del reporte mensual: resumen, costo por funcionalidad/modelo, top usuarios, acciones, recomendaciones |

## Inicio rápido

### 1. Crea las tablas

```bash
psql -d tu_bd -f schema.sql
```

### 2. Ajusta la configuración de presupuesto

Edita `budget_config.yaml`: tu presupuesto mensual real, los destinatarios y qué funcionalidades se pueden deshabilitar al 100%.

### 3. Ejecuta el monitor

Exporta cada llamada al LLM como una línea JSONL (ver el esquema de log por petición en la plantilla) y ejecuta:

```bash
pip install pyyaml
python llm_cost_monitor.py --config budget_config.yaml --log usage.jsonl
```

Imprime el chequeo de presupuesto (utilización + alertas a disparar) y el reporte diario. El código de salida es `1` cuando se dispara el umbral de estrangulación del 100% — conéctalo a tu scheduler o sistema de alertas. Una cadencia por hora es la adecuada para la mayoría de cargas de trabajo.

### 4. Rellena el reporte mensual

Copia `llm-cost-report-template.md` cada mes y rellena cada `[placeholder]` desde la tabla de rollup.

## Adapta antes de producción

1. Actualiza la tabla de precios de la plantilla antes de fiarte de cualquier número — los precios de los modelos quedan obsoletos rápido.
2. Decide qué funcionalidades son no críticas *ahora*; la lista `disabled_features` no es el momento para improvisar.
3. Lleva las alertas `notify` a un canal que alguien lea de verdad — un umbral sin vigilancia es decoración.
