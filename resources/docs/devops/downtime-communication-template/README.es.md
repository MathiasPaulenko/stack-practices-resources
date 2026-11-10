# Plantilla de Comunicación de Incidentes y Caídas — Recursos complementarios

Archivos complementarios de la [Plantilla de Comunicación de Incidentes y Caídas](https://stackpractices.com/es/docs/downtime-communication-template/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `downtime-communication-template.md` | Plantilla rellenable en blanco — metadatos, matriz de audiencias, seis bloques de mensajes, tabla de tiempos por severidad, checklist de aprobación |
| `status-page-messages.md` | Copy para página de estado del ciclo completo SEV 1 (Investigando → Identificado → Monitorizando → Resuelto) más una variante corta para SEV 3 |
| `service-template-checkout.yaml` | Plantilla de servicio pre-construida — rellena dos o tres campos cuando salta el incidente en lugar de escribir desde cero |
| `example-filled.md` | La plantilla maestra rellenada con un SEV 1 realista (fallos de login en EU, resolución en 27 minutos) |

## Cómo usarlo

1. Copia `downtime-communication-template.md` a la wiki de tu equipo o a tu herramienta de incidentes.
2. Rellena la matriz de audiencias con tus canales y responsables reales antes de necesitarla.
3. Crea un `service-template-*.yaml` por cada servicio principal y guárdalo junto al runbook.
4. Durante un incidente: envía los mensajes en el orden indicado — alerta interna, página de estado, resumen ejecutivo — y luego actualiza según la cadencia de severidad.
5. Compara con `example-filled.md` para calibrar cuánto detalle recibe cada audiencia.
6. Tras la resolución, publica el postmortem y reincorpora las lecciones a las plantillas.
