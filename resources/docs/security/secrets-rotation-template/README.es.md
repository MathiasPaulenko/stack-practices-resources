# Plantilla de Rotación de Secretos — Recursos Complementarios

Archivos descargables del artículo [Plantilla de Rotación de Secretos](https://stackpractices.com/es/docs/secrets-rotation-template/).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `secrets-rotation-schedule.md` | Programa de rotación en blanco con política de cadencias, playbook de emergencia, registro de excepciones y métricas |
| `rotation-runbook-db.sh` | Script de rotación de base de datos sin downtime con patrón dual-read |
| `rotation-validation-checklist.md` | Checklist por rotación: transición, pre-revocación y post-revocación |
| `rotation-log-example.md` | Registro de rotación relleno para una credencial de producción |

## Cómo usarlo

1. Copia `secrets-rotation-schedule.md` y rellena el inventario desde los access logs de tu secret manager.
2. Asigna cadencias y responsables por tipo de secreto; configura alertas de 30/14/7 días.
3. Prueba el procedimiento con `rotation-runbook-db.sh` en un secreto de bajo riesgo.
4. Adjunta un `rotation-validation-checklist.md` completo a cada registro de rotación.

English version: [Secrets Rotation Template](https://stackpractices.com/docs/secrets-rotation-template/)
