# Política de Monitoreo y Alertas — Recursos complementarios

Archivos complementarios de la [Plantilla de Política de Monitoreo y Alertas](https://stackpractices.com/es/docs/monitoring-alerting-policy-template/) en StackPractices.com.

## Qué incluye

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `prometheus-alert-rules.yaml` | YAML | Reglas de alerta con etiquetas `severity` (P1–P5) y `team` que siguen la política — tasa de error, latencia, disco y caducidad de certificados |
| `alertmanager-routing.yaml` | YAML | Árbol de enrutamiento que mapea severidad a canales (PagerDuty / Slack / correo) con `repeat_interval` pensados para escalación y una regla de inhibición P1→P2 |
| `alert-quality-scorecard.md` | Markdown | Tabla de puntuación imprimible para la revisión trimestral de alertas, con bandas de interpretación y registro de revisiones |

## Inicio rápido

### 1. Adapta las reglas de alerta

Sustituye los umbrales de ejemplo por valores calibrados con las métricas de tus últimos 90 días y apunta cada anotación `runbook` a una URL real. Carga las reglas en Prometheus:

```bash
promtool check rules prometheus-alert-rules.yaml
```

### 2. Adapta la configuración de enrutamiento

Reemplaza `P1_SERVICE_KEY`, `P2_SERVICE_KEY`, `SLACK_WEBHOOK_URL` y el correo de destino por credenciales reales, y valida:

```bash
amtool check-config alertmanager-routing.yaml
```

### 3. Ejecuta la revisión trimestral

Copia `alert-quality-scorecard.md` por alerta o por equipo, puntúa los seis criterios y aplica las bandas de interpretación: por debajo de 12 eliminar, 12–17 plan de mejora, 18 o más sana.

## Placeholders

| Placeholder | Reemplazar con |
|-------------|----------------|
| `P1_SERVICE_KEY` / `P2_SERVICE_KEY` | Claves de integración de PagerDuty |
| `SLACK_WEBHOOK_URL` | URL del webhook entrante |
| `team@example.com` | Lista de correo del equipo |
| `runbooks.example.com` | URL base de tus runbooks |
