# Assessment de Madurez de Observabilidad — Recursos Companion

Archivos companion de la [Plantilla de Assessment de Madurez de Observabilidad](https://stackpractices.com/es/docs/observability-maturity-assessment-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `assessment-template.md` | Markdown | Plantilla completa de assessment con 5 dimensiones, scoring, gaps y roadmap |
| `scoring-sheet.csv` | CSV | Datos de scoring listos para hoja de cálculo, 5 dimensiones y 30 criterios |

## Inicio rápido

### 1. Copiar la plantilla de assessment

```bash
cp assessment-template.md mi-equipo-assessment.md
```

Edita `mi-equipo-assessment.md` y reemplaza `<Team / Service>`, `<Name>` y los valores placeholder con los datos de tu equipo.

### 2. Importar hoja de scoring

Abre `scoring-sheet.csv` en Excel, Google Sheets o cualquier editor de CSV para跟踪ar los scores por dimensión.

## Estructura del assessment

1. **Logging** — estructura, niveles, correlation IDs, retención, buscabilidad, datos sensibles
2. **Métricas** — métricas RED/USE, métricas de negocio, cardinalidad, dashboards, SLOs
3. **Tracing** — tracing distribuido, propagación, span attributes, sampling, correlación
4. **Alertas** — ruido, routing, runbooks, alertas basadas en SLO, escalación, contexto
5. **Cultura** — ownership, revisión de incidentes, action items, on-call, training

## Niveles de madurez

| Nivel | Nombre | Descripción |
|-------|--------|-------------|
| 1 | Reactivo | Logs sin estructurar, sin métricas/traces, debugging manual |
| 2 | Básico | Logs estructurados, métricas clave, sin tracing, alertas ruidosas |
| 3 | Proactivo | Logs + dashboards + tracing, SLOs, alertas accionables |
| 4 | Predictivo | Detección de anomalías, alertas SLO, error budgets, runbooks |
| 5 | Autónomo | Remediación automática, profiling continuo, self-healing |

## Referencias

- [Google SRE Workbook](https://sre.google/workbook/)
- [OpenTelemetry](https://opentelemetry.io/)
- [Monitoreo con Prometheus](https://prometheus.io/docs/introduction/overview/)
