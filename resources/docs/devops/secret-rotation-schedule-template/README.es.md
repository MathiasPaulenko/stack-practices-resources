# Plantilla de Cronograma de Rotación de Secretos — Archivos Companion

Archivos listos para rellenar de la [Plantilla de Cronograma de Rotación de Secretos](https://stackpractices.com/es/docs/secret-rotation-schedule-template/) en StackPractices.

## Archivos

| Archivo | Para qué sirve |
|---------|----------------|
| `secret-rotation-schedule-template.md` | Versión completa en Markdown del cronograma: inventario, política de cadencia, procedimientos, playbook de emergencia, escalación, checklist de validación, registro de excepciones y tabla de métricas. |
| `secret-inventory.csv` | Versión en hoja de cálculo del inventario — impórtala en una wiki segura o herramienta de governance (nunca en una hoja pública). |
| `rotation-log.csv` | Una fila por evento de rotación: quién la ejecutó, qué se actualizó, cómo se verificó y el plan de rollback. |

## Uso

1. Copia `secret-rotation-schedule-template.md` en tu wiki interna y reemplaza cada `YYYY-MM-DD` y `@owner`.
2. Rellena el inventario desde los logs de acceso de tu gestor de secretos — no de memoria.
3. Usa `rotation-log.csv` como traza de auditoría: añade una fila tras cada rotación completada.
4. Guarda todo detrás de control de acceso por roles; el cronograma mismo revela qué secretos existen y cuándo son vulnerables.
