# Plantilla de Línea de Tiempo de Incidentes — Recursos complementarios

Archivos complementarios de [Plantilla de Línea de Tiempo de Incidentes](https://stackpractices.com/es/docs/incident-timeline-template/) en StackPractices.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `incident-timeline-template.md` | Plantilla en blanco rellenable — notación T±, tabla de análisis de retrasos, checklist de calidad |
| `example-filled.md` | La plantilla rellenada con el ejemplo SEV1 del artículo (incidente de rotación de JWT en auth-service) |

## Cómo usarla

1. Copia `incident-timeline-template.md` a tu documento de postmortem o repo.
2. Rellena la cronología durante o justo después del incidente — cada evento con marca de tiempo y fuente.
3. Ejecuta el análisis de retrasos: cada brecha mayor a 10 minutos necesita una anotación y un item de acción.
4. Revisa el checklist de calidad al final antes de publicar la cronología.
5. Compara con `example-filled.md` para calibrar la granularidad.

Todas las marcas de tiempo en UTC. Prefiere fuentes de máquina (métricas, alertas, CI/CD, chat) sobre la memoria.
