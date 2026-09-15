# Plantilla de Documento SLO — Recursos Companion

Archivos companion de la [Plantilla de Documento SLO](https://stackpractices.com/es/docs/slo-document-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `slo-template.md` | Markdown | Documento SLO listo para copiar con SLIs, SLOs, error budgets, dependencias |
| `slo-alerts.yaml` | YAML | Reglas de alertas de Prometheus para burn rate de SLO y latencia |

## Inicio rápido

### 1. Copiar la plantilla

```bash
cp slo-template.md mi-servicio-slo.md
```

Edita `mi-servicio-slo.md` y reemplaza `[Service Name]`, `[team]` y los valores placeholder.

### 2. Desplegar reglas de alertas

Edita `slo-alerts.yaml` y reemplaza `[service]` con el nombre de tu job de Prometheus:

```bash
# Copiar al directorio de reglas de Prometheus
cp slo-alerts.yaml /etc/prometheus/rules/slo-alerts.yaml

# Recargar Prometheus
curl -X POST http://localhost:9090/-/reload
```

## Estructura de la plantilla

1. **Overview** — nombre del servicio, owner, fecha de revisión
2. **SLIs** — disponibilidad, latencia, medidas de throughput
3. **SLOs** — targets con ventanas de medición
4. **Error Budget** — cálculo de budget y política
5. **Umbrales de alertas** — severidad page vs ticket
6. **Dependencias** — servicios upstream y sus SLOs
7. **Guía de selección de SLIs** — SLIs buenos vs malos por tipo de servicio
8. **Notas de revisión** — checklist de revisión trimestral

## Referencias

- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/)
- [Mejores prácticas de alertas en Prometheus](https://prometheus.io/docs/practices/alerting/)
