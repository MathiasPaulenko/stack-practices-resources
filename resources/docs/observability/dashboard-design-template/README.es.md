# Plantilla de Diseño de Dashboards — Recursos Companion

Archivos companion para la [Plantilla de Diseño de Dashboards](https://stackpractices.com/es/docs/dashboard-design-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `dashboard-template.md` | Markdown | Documento de diseño completo: layout, specs de paneles, config de SLOs, variables, anotaciones |
| `dashboard.json` | JSON | Dashboard de Grafana importable que implementa el layout de 6 filas con queries PromQL y umbrales |
| `slo-alerts.yml` | YAML | Grupo de reglas de Prometheus con alertas de quema rápida y lenta del SLO |

## Inicio rápido

### 1. Copiar el documento de diseño

```bash
cp dashboard-template.md mi-dashboard-de-servicio.md
```

Reemplazá `<Service Name>` y los placeholders de `payment` con los datos de tu servicio.

### 2. Importar el dashboard en Grafana

En Grafana: **Dashboards → New → Import → Upload JSON** y seleccioná `dashboard.json`. Elegí tu data source de Prometheus y actualizá los matchers `service="payment"` de cada panel con el nombre de tu servicio.

### 3. Cargar las reglas de alerta

Agregá `slo-alerts.yml` a los `rule_files` de tu Prometheus y recargá:

```yaml
rule_files:
  - "slo-alerts.yml"
```

Reemplazá `service="payment"` con el label de tu servicio y apuntá la anotación `runbook` a la URL real de tu runbook.

## Referencia del layout

El dashboard se lee de arriba hacia abajo durante un incidente:

1. **Banner de estado** — ¿está roto?
2. **Métricas RED** — ¿qué tan roto?
3. **Tráfico y códigos de estado** — ¿dónde está roto?
4. **Infraestructura** — ¿le faltan recursos?
5. **Métricas de negocio** — ¿cuánto duele?
6. **Enlaces de contexto** — runbooks, logs, trazas.
