# Recursos de la Plantilla de Runbook de Guardia

Recursos complementarios de [Plantilla de Runbook de Guardia](https://stackpractices.com/es/docs/on-call-runbook-template/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `runbook/on-call-runbook-template.md` | Plantilla de runbook indexada por alertas: siete procedimientos de respuesta con síntomas, pasos de diagnóstico, resolución y escalado — incluyendo la lista de anti-patrones |
| `scripts/diagnose.sh` | Colector de diagnóstico ejecutable: reúne estado del servicio, logs, recursos, red, despliegues y un health check en un reporte con timestamp |
| `monitoring/prometheus-alerts.yml` | Reglas de alertas de Prometheus conectadas a las secciones del runbook vía anotaciones `runbook:` y `dashboard:` |
| `monitoring/kubectl-diagnostics.md` | One-liners de diagnóstico en Kubernetes para estado de pods, logs, eventos y depuración de red |
| `checklists/post-incident-update.md` | Checklist post-incidente que mantiene el runbook actualizado después de cada incidente |

## Uso

1. Copia `runbook/on-call-runbook-template.md`, completa el nombre de tu servicio y mapea tus alertas reales a las secciones.
2. Haz ejecutable `scripts/diagnose.sh` (`chmod +x`) y déjalo en la máquina a la que acceden los ingenieros de guardia.
3. Adapta `monitoring/prometheus-alerts.yml` a tus métricas — la anotación `runbook:` es lo que enlaza la página con el procedimiento.
4. Corre `checklists/post-incident-update.md` después de cada incidente para que el runbook absorba lo aprendido.
