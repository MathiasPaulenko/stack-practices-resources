# Plantilla de Handoff On-Call — Recursos complementarios

Archivos complementarios de [Plantilla de Handoff On-Call](https://stackpractices.com/es/docs/on-call-handoff-template/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `on-call-handoff-template.md` | Reporte de entrega rellenable: incidentes, alertas, salud, cambios, escalamiento, verificación de accesos, notas |
| `example-filled.md` | La plantilla rellenada con un handoff de turno real (incidente P2 de API de pagos, rollback, despliegue pendiente) |

## Cómo usarlo

1. Copia `on-call-handoff-template.md` en la wiki del equipo, drive compartido o herramienta de incidentes.
2. Actualízalo durante el turno, no al final: la memoria comprime mal bajo fatiga.
3. Recorre el documento con el ingeniero entrante en ~20 minutos: incidentes, alertas, salud, cambios, problemas conocidos, preguntas.
4. Ejecuta la sección 7 (verificación de accesos) antes de cerrar: el fallo clásico es un entrante que no puede entrar en nada.
5. Pide confirmación explícita; "lo leí" no es una confirmación.
6. Compara con `example-filled.md` para calibrar el nivel de detalle.

Para handoffs asíncronos entre zonas horarias, el artículo incluye un formato corto listo para Slack.