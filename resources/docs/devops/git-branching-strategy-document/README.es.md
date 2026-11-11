# Documento de Estrategia de Branching en Git — Recursos

Plantillas de estrategia de branching Git descargables, referenciadas por
[Documento de Estrategia de Branching en Git](https://stackpractices.com/es/docs/git-branching-strategy-document/)
en StackPractices.

## Archivos

| Archivo | Qué es |
| --- | --- |
| `branching-strategy-template.md` | Plantilla en blanco: tipos de ramas, flujos de trabajo, conventional commits, requisitos de merge, tagging, rollback y reglas de protección. |
| `branching-strategy-template-es.md` | La misma plantilla en español. |
| `branching-strategy-example.md` | La plantilla completada para un equipo ficticio de "Payments Service". |

## Cómo usarla

1. Copia `branching-strategy-template.md` (o la versión `-es`) a tu repositorio (`docs/` o el wiki).
2. Completa los campos de versión, fecha y responsable en el encabezado.
3. Ajusta nombres de ramas, número de aprobaciones y estrategias de merge a tu equipo.
4. Si no necesitas `staging` ni `release/` (despliegue continuo), borra esas filas: el documento pasa a describir GitHub Flow.

## Licencia

Contenido de [StackPractices](https://stackpractices.com). Libre para usar y adaptar.
