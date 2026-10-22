# Plantilla de Postmortem de Incidentes — Recursos complementarios

Archivos complementarios de [Plantilla de Postmortem de Incidentes](https://stackpractices.com/es/docs/incident-postmortem-template/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `incident-postmortem-template.md` | Plantilla rellenable en blanco — resumen, impacto, cronología, cinco porqués, acciones pendientes, lecciones aprendidas |
| `example-filled.md` | La plantilla rellenada con el ejemplo real de caída de pagos P0 del artículo |

## Cómo usarla

1. Copia `incident-postmortem-template.md` en tu repositorio de documentación de incidentes una vez resuelto el incidente.
2. Rellena primero la cronología, solo con fuentes objetivas (PagerDuty, CI/CD, monitorización, logs de chat) — no de memoria.
3. Trabaja los cinco porqués hasta aterrizar en una causa sistémica que, arreglada, habría evitado el incidente.
4. Asigna a cada acción pendiente un responsable, una prioridad y una fecha límite antes de que termine la reunión.
5. Comparte el borrador con todos los equipos de ingeniería en un plazo de 48 horas y compara con `example-filled.md` para calibrar la profundidad.

Mantén el postmortem sin culpables: causas sistémicas, nunca una persona como causa raíz.
