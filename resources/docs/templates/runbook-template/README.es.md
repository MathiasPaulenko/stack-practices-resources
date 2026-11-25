# Plantilla de Runbook

Plantilla de runbook reutilizable en Markdown para procedimientos operativos y respuesta a incidentes, a juego con la guía de StackPractices: <https://stackpractices.com/es/docs/runbook-template/>

## Archivos

- `runbook-template.md` — plantilla en blanco para rellenar: metadatos, prerrequisitos, pasos del procedimiento (resultado esperado + rollback por paso), checklist de verificación, tabla de solución de problemas, acciones post-incidente, bloque de escalamiento.
- `runbook-example.md` — la misma plantilla cumplimentada para un escenario real: una alerta `PaymentServiceHighCPU` en Kubernetes, con diagnóstico ramificado y mitigaciones por condición.

## Uso

1. Copia `runbook-template.md` a tu directorio `docs/runbooks/` (o wiki) y renómbralo con el nombre del procedimiento.
2. Rellena la tabla de metadatos (responsable, severidad, frecuencia, última actualización).
3. Escribe pasos que pueda seguir alguien no familiarizado: un comando por paso, resultado esperado, rollback.
4. Enlaza la URL del runbook desde la alerta que lo dispara.

Para orientación sobre cuándo un procedimiento merece runbook, las dos formas (procedimiento vs. diagnóstico) y cómo desplegar una biblioteca de runbooks, lee la guía completa.
